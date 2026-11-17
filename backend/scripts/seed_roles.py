
from app.db.database import SessionLocal
from app.models.role import Role


def seed_roles():
    db = SessionLocal()

    roles = [
        "ADMIN",
        "LECTURER",
        "TECHNICIAN"
    ]

    try:
        for role_name in roles:

            existing_role = (
                db.query(Role)
                .filter(Role.name == role_name)
                .first()
            )

            if existing_role is None:
                new_role = Role(name=role_name)
                db.add(new_role)

        db.commit()

        print("Roles seeded successfully!")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_roles()
