
from app.db.database import SessionLocal
from app.models.equipment_type import EquipmentType


EQUIPMENT_TYPES = [
    "Computer Equipment",
    "Display Equipment",
    "Interactive Display",
    "Audio Equipment",
    "Network Equipment",
    "Cooling Equipment",
    "Electrical Equipment",
]


def seed_equipment_types():
    db = SessionLocal()

    try:
        for type_name in EQUIPMENT_TYPES:
            existing_type = (
                db.query(EquipmentType)
                .filter(EquipmentType.name == type_name)
                .first()
            )

            if existing_type is None:
                new_type = EquipmentType(name=type_name)
                db.add(new_type)

        db.commit()
        print("Equipment types seeded successfully!")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_equipment_types()
