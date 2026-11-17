
import pytest
from fastapi import HTTPException

from app.models.user import User
from app.models.role import Role
from app.dependencies.auth import require_roles


def create_role_user(db, role_name):

    role = Role(name=role_name)
    db.add(role)
    db.flush()

    user = User(
        full_name=f"Test {role_name}",
        email=f"{role_name.lower()}@example.com",
        password_hash="test_hash",
        role_id=role.id,
        is_active=True
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def test_admin_access_allowed(db_session):

    user = create_role_user(db_session, "ADMIN")

    check_admin = require_roles("ADMIN")

    result = check_admin(user, db_session)

    assert result.id == user.id


def test_lecturer_cannot_access_admin_resource(db_session):

    user = create_role_user(db_session, "LECTURER")

    check_admin = require_roles("ADMIN")

    with pytest.raises(HTTPException) as error:
        check_admin(user, db_session)

    assert error.value.status_code == 403


def test_technician_cannot_access_admin_resource(db_session):

    user = create_role_user(db_session, "TECHNICIAN")

    check_admin = require_roles("ADMIN")

    with pytest.raises(HTTPException) as error:
        check_admin(user, db_session)

    assert error.value.status_code == 403
