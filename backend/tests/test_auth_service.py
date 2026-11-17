
from app.models.user import User
from app.models.role import Role

from app.core.security import (
    hash_password,
    verify_password,
    verify_access_token
)
from app.services.auth import (
    authenticate_user,
    change_user_password
)



def create_auth_test_user(
    db,
    is_active=True,
    must_change_password=False
):

    role = Role(name="LECTURER")
    db.add(role)
    db.flush()

    user = User(
        full_name="Test Lecturer",
        email="lecturer.test@example.com",
        password_hash=hash_password("Campus@123"),
        role_id=role.id,
        is_active=is_active,
        must_change_password=must_change_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user



def test_successful_login(db_session):

    user = create_auth_test_user(db_session)

    result = authenticate_user(
        db_session,
        "lecturer.test@example.com",
        "Campus@123"
    )

    assert result is not None
    assert result["token_type"] == "bearer"

    payload = verify_access_token(result["access_token"])

    assert payload["sub"] == str(user.id)


def test_login_with_wrong_password(db_session):

    create_auth_test_user(db_session)

    result = authenticate_user(
        db_session,
        "lecturer.test@example.com",
        "Wrong@123"
    )

    assert result is None


def test_login_with_unknown_email(db_session):

    result = authenticate_user(
        db_session,
        "unknown@example.com",
        "Campus@123"
    )

    assert result is None


def test_inactive_user_cannot_login(db_session):

    create_auth_test_user(db_session, is_active=False)

    result = authenticate_user(
        db_session,
        "lecturer.test@example.com",
        "Campus@123"
    )

    assert result is None


def test_successful_password_change(db_session):

    user = create_auth_test_user(
        db_session,
        must_change_password=True
    )

    result = change_user_password(
        db=db_session,
        user=user,
        current_password="Campus@123",
        new_password="NewCampus@456"
    )

    assert result is not None
    assert result["message"] == "Password changed successfully"

    db_session.refresh(user)

    assert verify_password(
        "NewCampus@456",
        user.password_hash
    )

    assert user.must_change_password is False

    payload = verify_access_token(result["access_token"])

    assert payload["sub"] == str(user.id)
    assert payload["must_change_password"] is False


def test_password_change_with_wrong_current_password(db_session):

    user = create_auth_test_user(
        db_session,
        must_change_password=True
    )

    result = change_user_password(
        db=db_session,
        user=user,
        current_password="Wrong@123",
        new_password="NewCampus@456"
    )

    assert result is None

    db_session.refresh(user)

    assert verify_password("Campus@123", user.password_hash)
    assert user.must_change_password is True


def test_password_change_rejects_same_password(db_session):

    user = create_auth_test_user(
        db_session,
        must_change_password=True
    )

    result = change_user_password(
        db=db_session,
        user=user,
        current_password="Campus@123",
        new_password="Campus@123"
    )

    assert result is None
    assert user.must_change_password is True
