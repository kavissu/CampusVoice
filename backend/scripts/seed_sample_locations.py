
import secrets

from app.db.database import SessionLocal
from app.models.location import Location


def seed_sample_locations():
    db = SessionLocal()

    locations = [
        {
            "name": "Lecture Hall 01",
            "code": "LH-001",
            "location_type": "LECTURE_HALL"
        },
        {
            "name": "Lecture Hall 02",
            "code": "LH-002",
            "location_type": "LECTURE_HALL"
        },
        {
            "name": "Main Canteen",
            "code": "CAN-001",
            "location_type": "CANTEEN"
        },
        {
            "name": "Engineering Toilet",
            "code": "TOI-001",
            "location_type": "TOILET"
        },
        {
            "name": "Engineering Laboratory 01",
            "code": "LAB-001",
            "location_type": "LABORATORY"
        },
        {
            "name": "Main Corridor",
            "code": "COR-001",
            "location_type": "CORRIDOR"
        },
        {
            "name": "Outdoor Common Area",
            "code": "OUT-001",
            "location_type": "OUTDOOR"
        }
    ]

    try:
        for location_data in locations:

            existing_location = (
                db.query(Location)
                .filter(Location.code == location_data["code"])
                .first()
            )

            if existing_location is None:

                new_location = Location(
                    name=location_data["name"],
                    code=location_data["code"],
                    location_type=location_data["location_type"],
                    qr_code_token=secrets.token_urlsafe(32)
                )

                db.add(new_location)

        db.commit()

        print("Sample locations seeded successfully!")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_sample_locations()
