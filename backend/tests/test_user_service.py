
import pytest

from app.models.user import User
from app.models.role import Role
from app.models.department import Department
from app.models.maintenance_team import MaintenanceTeam
from app.models.technician import Technician

from app.core.security import verify_password
from app.services.user import create_user_account


def setup_test_data(db):
    roles = [
        Role(name="ADMIN"),
        Role(name="LECTURER"),
        Role(name="TECHNICIAN")
    ]

    department = Department(
        name="Computer Engineering",
        code="CE"
    )

    team = MaintenanceTeam(
        name="IT Support",
        is_active=True
    )

    db.add_all(roles + [department, team])
    db.flush()

    return department, team


def test_create_lecturer_success(db_session):
    department, team = setup_test_data(db_session)

    result = create_user_account(
        db=db_session,
        full_name="Test Lecturer",
        email="lecturer@example.com",
        role_name="LECTURER",
        department_id=department.id
    )

    user = db_session.query(User).filter(
        User.email == "lecturer@example.com"
    ).first()

    assert user is not None
    assert result["role"] == "LECTURER"
    assert result["must_change_password"] is True
    assert result["temporary_password"]

    assert verify_password(
        result["temporary_password"],
        user.password_hash
    )


def test_create_technician_success(db_session):
    department, team = setup_test_data(db_session)

    result = create_user_account(
        db=db_session,
        full_name="Test Technician",
        email="technician@example.com",
        role_name="TECHNICIAN",
        department_id=department.id,
        maintenance_team_id=team.id
    )

    user = db_session.query(User).filter(
        User.email == "technician@example.com"
    ).first()

    technician = db_session.query(Technician).filter(
        Technician.user_id == user.id
    ).first()

    assert result["role"] == "TECHNICIAN"
    assert technician is not None
    assert technician.maintenance_team_id == team.id


def test_duplicate_email_rejected(db_session):
    department, team = setup_test_data(db_session)

    create_user_account(
        db=db_session,
        full_name="First Lecturer",
        email="duplicate@example.com",
        role_name="LECTURER",
        department_id=department.id
    )

    with pytest.raises(ValueError, match="already registered"):
        create_user_account(
            db=db_session,
            full_name="Second Lecturer",
            email="duplicate@example.com",
            role_name="LECTURER",
            department_id=department.id
        )


def test_invalid_role_rejected(db_session):
    department, team = setup_test_data(db_session)

    with pytest.raises(ValueError, match="Only Lecturer and Technician"):
        create_user_account(
            db=db_session,
            full_name="Invalid User",
            email="invalid@example.com",
            role_name="ADMIN",
            department_id=department.id
        )


def test_invalid_department_rejected(db_session):
    department, team = setup_test_data(db_session)

    with pytest.raises(ValueError, match="Department not found"):
        create_user_account(
            db=db_session,
            full_name="Test Lecturer",
            email="invalid.department@example.com",
            role_name="LECTURER",
            department_id=999
        )


def test_technician_without_team_rejected(db_session):
    department, team = setup_test_data(db_session)

    with pytest.raises(ValueError, match="must have a maintenance team"):
        create_user_account(
            db=db_session,
            full_name="Test Technician",
            email="missing.team@example.com",
            role_name="TECHNICIAN",
            department_id=department.id
        )


def test_inactive_maintenance_team_rejected(db_session):
    department, team = setup_test_data(db_session)

    team.is_active = False
    db_session.commit()

    with pytest.raises(ValueError, match="Active maintenance team not found"):
        create_user_account(
            db=db_session,
            full_name="Test Technician",
            email="inactive.team@example.com",
            role_name="TECHNICIAN",
            department_id=department.id,
            maintenance_team_id=team.id
        )


def test_lecturer_cannot_have_maintenance_team(db_session):
    department, team = setup_test_data(db_session)

    with pytest.raises(ValueError, match="Lecturer cannot be assigned"):
        create_user_account(
            db=db_session,
            full_name="Test Lecturer",
            email="lecturer.team@example.com",
            role_name="LECTURER",
            department_id=department.id,
            maintenance_team_id=team.id
        )
