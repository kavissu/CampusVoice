
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import require_roles
from app.models.user import User
from app.schemas.ticket import (
    EquipmentFaultCreate,
    EquipmentFaultResponse
)
from app.services.ticket import create_equipment_fault_ticket


router = APIRouter(
    prefix="/api/v1",
    tags=["Tickets"]
)


@router.post(
    "/locations/{qr_token}/equipment-faults",
    response_model=EquipmentFaultResponse,
    status_code=status.HTTP_201_CREATED
)
def submit_equipment_fault(
    qr_token: str,
    ticket_data: EquipmentFaultCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("LECTURER"))
):
    try:
        ticket = create_equipment_fault_ticket(
            db=db,
            user_id=current_user.id,
            qr_token=qr_token,
            ticket_data=ticket_data
        )

        return ticket

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )
