
from sqlalchemy.orm import Session

from app.models.user import User
from app.models.role import Role
from app.models.department import Department
from app.models.maintenance_team import MaintenanceTeam
from app.models.technician import Technician


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def get_role_by_name(db: Session, role_name: str) -> Role | None:
    return db.query(Role).filter(Role.name == role_name).first()


def get_department_by_id(db: Session, department_id: int) -> Department | None:
    return db.query(Department).filter(Department.id == department_id).first()


def get_active_maintenance_team(
    db: Session,
    team_id: int
) -> MaintenanceTeam | None:
    return (
        db.query(MaintenanceTeam)
        .filter(
            MaintenanceTeam.id == team_id,
            MaintenanceTeam.is_active == True
        )
        .first()
    )


def create_user(
    db: Session,
    full_name: str,
    email: str,
    password_hash: str,
    role_id: int,
    department_id: int
) -> User:
    user = User(
        full_name=full_name,
        email=email,
        password_hash=password_hash,
        role_id=role_id,
        department_id=department_id,
        is_active=True,
        must_change_password=True
    )

    db.add(user)
    db.flush()

    return user


def create_technician(
    db: Session,
    user_id: int,
    maintenance_team_id: int
) -> Technician:
    technician = Technician(
        user_id=user_id,
        maintenance_team_id=maintenance_team_id,
        is_active=True
    )

    db.add(technician)
    db.flush()

    return technician
