
import secrets

from app.db.database import SessionLocal
from app.models.location import Location


def seed_reference_facilities():
    db = SessionLocal()

    facilities = [
        {
            "name": "Lecture Hall L211A",
            "code": "REF-LH-L211A",
            "location_type": "LECTURE_HALL"
        },
        {
            "name": "IT Lab",
            "code": "REF-IT-LAB",
            "location_type": "LABORATORY"
        },
        {
            "name": "IT Centre",
            "code": "REF-IT-CENTRE",
            "location_type": "LABORATORY"
        },
        {
            "name": "Auditorium",
            "code": "REF-AUDITORIUM",
            "location_type": "AUDITORIUM"
        },
        {
            "name": "Dyno System",
            "code": "REF-DYNO",
            "location_type": "SPECIALIZED_FACILITY"
        }
    ]

    try:
        for facility in facilities:

            existing = (
                db.query(Location)
                .filter(Location.code == facility["code"])
                .first()
            )

            if existing is None:
                new_location = Location(
                    name=facility["name"],
                    code=facility["code"],
                    location_type=facility["location_type"],
                    qr_code_token=secrets.token_urlsafe(32)
                )

                db.add(new_location)

        db.commit()

        print("University-referenced facilities seeded successfully!")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_reference_facilities()
