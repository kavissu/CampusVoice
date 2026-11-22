
from sqlalchemy.orm import Session

from app.models.equipment import Equipment
from app.models.equipment_problem_option import EquipmentProblemOption
from app.models.ticket import Ticket
from app.models.ticket_history import TicketHistory
from app.models.location import Location
from app.models.hall import Hall

def get_active_equipment(db: Session, equipment_id: int):
    return db.query(Equipment).filter(
        Equipment.id == equipment_id,
        Equipment.is_active.is_(True)
    ).first()


def get_active_problem_option(
    db: Session,
    problem_option_id: int,
    equipment_type_id: int
):
    return db.query(EquipmentProblemOption).filter(
        EquipmentProblemOption.id == problem_option_id,
        EquipmentProblemOption.equipment_type_id == equipment_type_id,
        EquipmentProblemOption.is_active.is_(True)
    ).first()


def create_ticket(db: Session, ticket_data: dict):
    ticket = Ticket(**ticket_data)

    db.add(ticket)
    db.flush()
    db.refresh(ticket)

    return ticket


def create_ticket_history(
    db: Session,
    ticket_id: int,
    user_id: int,
    priority: str
):
    history = TicketHistory(
        ticket_id=ticket_id,
        changed_by_user_id=user_id,
        new_status="Open",
        new_priority=priority,
        remarks="Equipment fault ticket created"
    )

    db.add(history)
    db.flush()

    return history


def get_active_hall_by_qr_token(db: Session, qr_token: str):
    return (
        db.query(Hall)
        .join(Location, Hall.location_id == Location.id)
        .filter(
            Location.qr_code_token == qr_token,
            Location.is_active.is_(True),
            Hall.is_active.is_(True)
        )
        .first()
    )
