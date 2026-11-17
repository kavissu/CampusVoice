
from app.models.user import User
from app.models.role import Role
from app.repositories.auth import get_user_by_email


def test_get_user_by_email_returns_user(db_session):

    role = Role(name="LECTURER")
    db_session.add(role)
    db_session.flush()

    user = User(
        full_name="Test Lecturer",
        email="lecturer.test@example.com",
        password_hash="test_hash",
        role_id=role.id,
        is_active=True
    )

    db_session.add(user)
    db_session.commit()

    result = get_user_by_email(
        db_session,
        "lecturer.test@example.com"
    )

    assert result is not None
    assert result.email == "lecturer.test@example.com"


def test_get_user_by_email_returns_none(db_session):

    result = get_user_by_email(
        db_session,
        "unknown@example.com"
    )

    assert result is None
