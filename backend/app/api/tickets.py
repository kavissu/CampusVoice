
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.dependencies.auth import require_roles
from app.models.user import User
from app.schemas.ticket import (
    EquipmentFaultCreate,
    EquipmentFaultResponse,
    TicketTrackingResponse,
    TechnicianTicketResponse,
    TicketStatusUpdate
)

from app.services.ticket import( create_equipment_fault_ticket,get_ticket_tracking_details,get_technician_assigned_tickets, update_ticket_status
)


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


@router.get(
    "/tickets/track/{tracking_code}",
    response_model=TicketTrackingResponse
)
def track_ticket(
    tracking_code: str,
    db: Session = Depends(get_db)
):
    try:
        return get_ticket_tracking_details(
            db=db,
            tracking_code=tracking_code
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )


@router.get(
    "/technician/tickets",
    response_model=list[TechnicianTicketResponse],
    tags=["Technician"]
)
def get_my_assigned_tickets(
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("TECHNICIAN"))
):
    try:
        return get_technician_assigned_tickets(
            db=db,
            user_id=current_user.id
        )

    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(error)
        )
@router.patch("/technician/tickets/{ticket_id}/status")
def change_ticket_status(
    ticket_id: int,
    status_data: TicketStatusUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(require_roles("TECHNICIAN"))
):
    try:
        ticket = update_ticket_status(
            db=db,
            ticket_id=ticket_id,
            user_id=current_user.id,
            status_data=status_data
        )

        return {
            "message": "Ticket status updated successfully",
            "ticket_id": ticket.id,
            "tracking_code": ticket.tracking_code,
            "status": ticket.status,
            "resolved_at": ticket.resolved_at
        }

    except ValueError as error:
        detail = str(error)

        if detail == "Ticket not found":
            error_status = status.HTTP_404_NOT_FOUND
        elif "not assigned" in detail or "Technician profile" in detail:
            error_status = status.HTTP_403_FORBIDDEN
        elif "Invalid status transition" in detail:
            error_status = status.HTTP_409_CONFLICT
        else:
            error_status = status.HTTP_400_BAD_REQUEST

        raise HTTPException(
            status_code=error_status,
            detail=detail
        )