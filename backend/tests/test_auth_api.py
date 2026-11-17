
from app.models.user import User
from app.models.role import Role
from app.core.security import hash_password


def create_api_test_user(db):

    role = Role(name="LECTURER")
    db.add(role)
    db.flush()

    user = User(
        full_name="Test Lecturer",
        email="lecturer.test@example.com",
        password_hash=hash_password("Campus@123"),
        role_id=role.id,
        is_active=True,
        must_change_password=True
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def get_login_token(client):

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "lecturer.test@example.com",
            "password": "Campus@123"
        }
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def test_login_api_success(client, db_session):

    create_api_test_user(db_session)

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "lecturer.test@example.com",
            "password": "Campus@123"
        }
    )

    assert response.status_code == 200
    assert response.json()["token_type"] == "bearer"


def test_password_change_api_success(client, db_session):

    create_api_test_user(db_session)
    token = get_login_token(client)

    response = client.post(
        "/api/v1/auth/change-password",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "current_password": "Campus@123",
            "new_password": "NewCampus@456"
        }
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Password changed successfully"


def test_password_change_wrong_current_password(client, db_session):

    create_api_test_user(db_session)
    token = get_login_token(client)

    response = client.post(
        "/api/v1/auth/change-password",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "current_password": "Wrong@123",
            "new_password": "NewCampus@456"
        }
    )

    assert response.status_code == 400


def test_password_change_without_token(client, db_session):

    create_api_test_user(db_session)

    response = client.post(
        "/api/v1/auth/change-password",
        json={
            "current_password": "Campus@123",
            "new_password": "NewCampus@456"
        }
    )

    assert response.status_code == 401


def test_password_change_short_new_password(client, db_session):

    create_api_test_user(db_session)
    token = get_login_token(client)

    response = client.post(
        "/api/v1/auth/change-password",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "current_password": "Campus@123",
            "new_password": "short"
        }
    )

    assert response.status_code == 422
