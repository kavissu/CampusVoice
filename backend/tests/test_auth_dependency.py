
from fastapi import HTTPException

from app.dependencies.auth import get_current_user
from app.models.user import User
from app.models.role import Role
from app.models.department import Department
from app.core.security import create_access_token
from fastapi.security import HTTPAuthorizationCredentials

def create_test_user(db, is_active=True):
    department = Department(
        name="Computer Engineering",
        code="TEST-CO"
    )
    db.add(department)
    db.flush()

    role = Role(name="LECTURER")
    db.add(role)
    db.flush()

    user = User(
        full_name="Test Lecturer",
        email="lecturer.test@example.com",
        password_hash="test_hash",
        role_id=role.id,
        department_id=department.id,
        is_active=is_active
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def test_valid_token_returns_user(db_session):
    user = create_test_user(db_session)
    token = create_access_token(user.id)

    result = get_current_user(
    create_credentials(token),
    db_session
)

    assert result.id == user.id
    assert result.email == user.email


def test_inactive_user_is_rejected(db_session):
    user = create_test_user(db_session, is_active=False)
    token = create_access_token(user.id)

    try:
        get_current_user(
    create_credentials(token),
    db_session
)
        assert False, "Inactive user should be rejected"
    except HTTPException as error:
        assert error.status_code == 401


def test_nonexistent_user_is_rejected(db_session):
    token = create_access_token(user_id=99999)

    try:
        get_current_user(
    create_credentials(token),
    db_session
)
        assert False, "Nonexistent user should be rejected"
    except HTTPException as error:
        assert error.status_code == 401


def test_invalid_token_is_rejected(db_session):
    try:
        get_current_user(
    create_credentials("invalid.token.value"),
    db_session
)
        assert False, "Invalid token should be rejected"
    except HTTPException as error:
        assert error.status_code == 401

def create_credentials(token):
    return HTTPAuthorizationCredentials(
        scheme="Bearer",
        credentials=token
    )