
from app.db.database import SessionLocal
from app.models.maintenance_team import MaintenanceTeam


def seed_maintenance_teams():
    db = SessionLocal()

    teams = [
        "IT Support",
        "Electrical",
        "Plumbing",
        "Cleaning",
        "General Maintenance"
    ]

    try:
        for team_name in teams:

            existing_team = (
                db.query(MaintenanceTeam)
                .filter(MaintenanceTeam.name == team_name)
                .first()
            )

            if existing_team is None:
                new_team = MaintenanceTeam(name=team_name)
                db.add(new_team)

        db.commit()

        print("Maintenance teams seeded successfully!")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_maintenance_teams()
