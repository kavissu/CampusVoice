
from app.db.database import SessionLocal
from app.models.location import Location
from app.models.hall import Hall


def seed_halls():
    db = SessionLocal()

    try:
        location = (
            db.query(Location)
            .filter(Location.code == "REF-LH-L211A")
            .first()
        )

        if location is None:
            raise ValueError(
                "Lecture Hall L211A location was not found."
            )

        existing_hall = (
            db.query(Hall)
            .filter(Hall.location_id == location.id)
            .first()
        )

        if existing_hall is None:
            new_hall = Hall(
                location_id=location.id,
                name="Lecture Hall L211A",
                code="DEV-LH-L211A"
            )

            db.add(new_hall)

        db.commit()

        print("Hall records seeded successfully!")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_halls()
