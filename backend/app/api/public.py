
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.services.public import get_public_hall_equipment
from app.schemas.public import PublicHallEquipmentResponse

router = APIRouter(
    prefix="/public",
    tags=["Public"]
)


@router.get("/locations/{qr_token}/equipment", 
            response_model=PublicHallEquipmentResponse)
def get_equipment_by_qr(
    qr_token: str,
    db: Session = Depends(get_db)
):
    result = get_public_hall_equipment(
        db,
        qr_token
    )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Location or active hall not found"
        )

    return result
