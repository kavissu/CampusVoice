
from getpass import getpass

from app.db.database import SessionLocal
from app.models.user import User
from app.models.role import Role
from app.models.department import Department
from app.core.security import hash_password


TEST_LECTURER_EMAIL = "lecturer.test@campusvoice.local"


def seed_test_lecturer():
    db = SessionLocal()

    try:
        # Find the LECTURER role
        role = db.query(Role).filter(
            Role.name == "LECTURER"
        ).first()

        if role is None:
            raise ValueError("LECTURER role not found. Seed roles first.")

        # Check whether the test lecturer already exists
        existing_user = db.query(User).filter(
            User.email == TEST_LECTURER_EMAIL
        ).first()

        if existing_user:
            print("Test lecturer already exists.")
            return

        # Get department
        department_code = input(
            "Enter department code (e.g. CE): "
        ).strip().upper()

        department = db.query(Department).filter(
            Department.code == department_code
        ).first()

        if department is None:
            raise ValueError("Department not found.")

        # Get password securely
        password = getpass("Enter test lecturer password: ")
        confirm_password = getpass("Confirm password: ")

        if password != confirm_password:
            raise ValueError("Passwords do not match.")

        if len(password) < 8:
            raise ValueError("Password must contain at least 8 characters.")

        # Create test lecturer
        user = User(
            full_name="Test Lecturer",
            email=TEST_LECTURER_EMAIL,
            password_hash=hash_password(password),
            role_id=role.id,
            department_id=department.id,
            is_active=True,
            must_change_password=True
        )

        db.add(user)
        db.commit()

        print("Test lecturer created successfully!")
        print("Email:", TEST_LECTURER_EMAIL)
        print("Department:", department.name)
        print("The lecturer must change the password at first login.")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_test_lecturer()
