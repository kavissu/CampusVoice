
import secrets

from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.repositories.user import (
    get_user_by_email,
    get_role_by_name,
    get_department_by_id,
    get_active_maintenance_team,
    create_user,
    create_technician,
)


def create_user_account(
    db: Session,
    full_name: str,
    email: str,
    role_name: str,
    department_id: int,
    maintenance_team_id: int | None = None,
) -> dict:

    # 1. Normalize input
    email = email.strip().lower()
    role_name = role_name.strip().upper()

    # 2. Allow only Lecturer and Technician
    if role_name not in ["LECTURER", "TECHNICIAN"]:
        raise ValueError("Only Lecturer and Technician accounts can be created")

    # 3. Check duplicate email
    if get_user_by_email(db, email):
        raise ValueError("This email is already registered")

    # 4. Check role
    role = get_role_by_name(db, role_name)
    if role is None:
        raise ValueError("Invalid role")

    # 5. Check department
    department = get_department_by_id(db, department_id)
    if department is None:
        raise ValueError("Department not found")

    # 6. Validate maintenance team
    maintenance_team = None

    if role_name == "TECHNICIAN":
        if maintenance_team_id is None:
            raise ValueError("Technician must have a maintenance team")

        maintenance_team = get_active_maintenance_team(
            db, maintenance_team_id
        )

        if maintenance_team is None:
            raise ValueError("Active maintenance team not found")

    elif maintenance_team_id is not None:
        raise ValueError("Lecturer cannot be assigned to a maintenance team")

    # 7. Generate temporary password
    temporary_password = secrets.token_urlsafe(12)

    # 8. Hash the password
    password_hash = hash_password(temporary_password)

    try:
        # 9. Create user
        user = create_user(
            db=db,
            full_name=full_name,
            email=email,
            password_hash=password_hash,
            role_id=role.id,
            department_id=department.id,
        )

        # 10. Create technician record when needed
        if role_name == "TECHNICIAN":
            create_technician(
                db=db,
                user_id=user.id,
                maintenance_team_id=maintenance_team.id,
            )

        # 11. Save all changes together
        db.commit()
        db.refresh(user)

        return {
            "id": user.id,
            "full_name": user.full_name,
            "email": user.email,
            "role": role_name,
            "temporary_password": temporary_password,
            "must_change_password": user.must_change_password,
        }

    except Exception:
        db.rollback()
        raise
