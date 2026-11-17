from app.db.database import SessionLocal
from app.models.fault_category import FaultCategory
from app.models.maintenance_team import MaintenanceTeam


def seed_fault_categories():
    db = SessionLocal()

    categories = {
        "IT / Computer": "IT Support",
        "Electrical": "Electrical",
        "Plumbing": "Plumbing",
        "Cleaning": "Cleaning",
        "Infrastructure": "General Maintenance"
    }

    try:
        for category_name, team_name in categories.items():

            team = (
                db.query(MaintenanceTeam)
                .filter(MaintenanceTeam.name == team_name)
                .first()
            )

            if team is None:
                raise ValueError(
                    f"Maintenance team '{team_name}' was not found."
                )

            existing_category = (
                db.query(FaultCategory)
                .filter(FaultCategory.name == category_name)
                .first()
            )

            if existing_category is None:
                new_category = FaultCategory(
                    name=category_name,
                    maintenance_team_id=team.id
                )

                db.add(new_category)

        db.commit()

        print("Fault categories seeded successfully!")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_fault_categories()