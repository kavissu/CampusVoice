
from sqlalchemy.orm import Session

from app.models.location import Location
from app.models.hall import Hall
from app.models.equipment import Equipment


def get_hall_equipment_by_qr_token(
    db: Session,
    qr_token: str
):
    # 1. Find the active location using the QR token
    location = (
        db.query(Location)
        .filter(
            Location.qr_code_token == qr_token,
            Location.is_active == True
        )
        .first()
    )

    if location is None:
        return None

    # 2. Find the active hall connected to this location
    hall = (
        db.query(Hall)
        .filter(
            Hall.location_id == location.id,
            Hall.is_active == True
        )
        .first()
    )

    if hall is None:
        return None

    # 3. Retrieve all active equipment in this hall
    equipment_list = (
        db.query(Equipment)
        .filter(
            Equipment.hall_id == hall.id,
            Equipment.is_active == True
        )
        .order_by(Equipment.name)
        .all()
    )

    return location, hall, equipment_list
