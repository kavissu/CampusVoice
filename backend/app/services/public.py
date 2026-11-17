
from sqlalchemy.orm import Session

from app.repositories.public import (
    get_hall_equipment_by_qr_token
)


def get_public_hall_equipment(
    db: Session,
    qr_token: str
):
    result = get_hall_equipment_by_qr_token(
        db,
        qr_token
    )

    if result is None:
        return None

    location, hall, equipment_list = result

    return {
        "location": {
            "id": location.id,
            "name": location.name,
            "code": location.code,
        },
        "hall": {
            "id": hall.id,
            "name": hall.name,
            "code": hall.code,
        },
        "equipment": [
            {
                "id": item.id,
                "name": item.name,
                "asset_code": item.asset_code,
                "description": item.description,
            }
            for item in equipment_list
        ],
        "total_equipment": len(equipment_list),
    }
