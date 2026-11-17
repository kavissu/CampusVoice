
from app.db.database import SessionLocal
from app.models.equipment import Equipment
from app.models.equipment_type import EquipmentType
from app.models.department import Department
from app.models.hall import Hall


SAMPLE_EQUIPMENT = [
    {
        "name": "Desktop Computer",
        "asset_code": "DEV-PC-001",
        "description": "Development sample desktop computer",
        "equipment_type": "Computer Equipment",
        "department": "CO",
        "hall_code": "DEV-LH-L211A",
    },
    {
        "name": "Projector",
        "asset_code": "DEV-PROJ-001",
        "description": "Development sample classroom projector",
        "equipment_type": "Display Equipment",
        "department": "CO",
        "hall_code": "DEV-LH-L211A",
    },
    {
        "name": "Smart Board",
        "asset_code": "DEV-SB-001",
        "description": "Development sample interactive display",
        "equipment_type": "Interactive Display",
        "department": "CO",
        "hall_code": "DEV-LH-L211A",
    },
    {
        "name": "Microphone",
        "asset_code": "DEV-MIC-001",
        "description": "Development sample classroom microphone",
        "equipment_type": "Audio Equipment",
        "department": "CO",
        "hall_code": "DEV-LH-L211A",
    },
    {
        "name": "Network Switch",
        "asset_code": "DEV-NS-001",
        "description": "Development sample network switch",
        "equipment_type": "Network Equipment",
        "department": "CO",
        "hall_code": "DEV-LH-L211A",
    },
]


def seed_equipment():
    db = SessionLocal()

    try:
        for item in SAMPLE_EQUIPMENT:

            existing_equipment = (
                db.query(Equipment)
                .filter(Equipment.asset_code == item["asset_code"])
                .first()
            )

            if existing_equipment is not None:
                continue

            equipment_type = (
                db.query(EquipmentType)
                .filter(
                    EquipmentType.name == item["equipment_type"]
                )
                .first()
            )

            department = (
                db.query(Department)
                .filter(Department.code == item["department"])
                .first()
            )

            hall = (
                db.query(Hall)
                .filter(Hall.code == item["hall_code"])
                .first()
            )

            if not equipment_type or not department or not hall:
                raise ValueError(
                    f"Missing related data for {item['asset_code']}"
                )

            new_equipment = Equipment(
                name=item["name"],
                asset_code=item["asset_code"],
                description=item["description"],
                equipment_type_id=equipment_type.id,
                department_id=department.id,
                hall_id=hall.id,
            )

            db.add(new_equipment)

        db.commit()
        print("Sample equipment seeded successfully!")

    except Exception:
        db.rollback()
        raise

    finally:
        db.close()


if __name__ == "__main__":
    seed_equipment()
