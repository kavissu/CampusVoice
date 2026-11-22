
from sqlalchemy.orm import Session

from app.models.equipment import Equipment
from app.models.equipment_problem_option import EquipmentProblemOption
from app.models.ticket import Ticket
from app.models.ticket_history import TicketHistory
from app.models.location import Location
from app.models.hall import Hall
from app.models.technician import Technician
from app.models.maintenance_team import MaintenanceTeam
from app.models.fault_category import FaultCategory
from sqlalchemy import func
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


def get_ticket_by_tracking_code(db: Session, tracking_code: str):
    return db.query(Ticket).filter(
        Ticket.tracking_code == tracking_code
    ).first()


def get_ticket_history(db: Session, ticket_id: int):
    return (
        db.query(TicketHistory)
        .filter(TicketHistory.ticket_id == ticket_id)
        .order_by(TicketHistory.changed_at.asc())
        .all()
    )

def get_technician_by_user_id(db: Session, user_id: int):
    return db.query(Technician).filter(
        Technician.user_id == user_id,
        Technician.is_active.is_(True)
    ).first()


def get_tickets_by_technician(db: Session, technician_id: int):
    return (
        db.query(Ticket)
        .filter(Ticket.technician_id == technician_id)
        .order_by(Ticket.reported_at.desc())
        .all()
    )


def get_active_technician(db: Session, technician_id: int):
    return (
        db.query(Technician)
        .filter(
            Technician.id == technician_id,
            Technician.is_active.is_(True)
        )
        .first()
    )


def assign_ticket_to_technician(
    db: Session,
    ticket_id: int,
    technician_id: int,
    maintenance_team_id: int
):
    ticket = db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()

    if ticket is None:
        return None

    old_technician_id = ticket.technician_id

    ticket.technician_id = technician_id
    ticket.maintenance_team_id = maintenance_team_id

    return ticket, old_technician_id


def create_ticket_assignment_history(
    db: Session,
    ticket_id: int,
    admin_user_id: int | None,
    old_technician_id: int | None,
    new_technician_id: int,
    old_status: str,
    new_status: str,
    remarks: str
):
    history = TicketHistory(
        ticket_id=ticket_id,
        changed_by_user_id=admin_user_id,
        old_technician_id=old_technician_id,
        new_technician_id=new_technician_id,
        old_status=old_status,
        new_status=new_status,
        remarks=remarks
    )

    db.add(history)
    db.flush()

    return history

def get_ticket_by_id(db: Session, ticket_id: int):
    return db.query(Ticket).filter(
        Ticket.id == ticket_id
    ).first()


def get_technician_with_lowest_workload(
    db: Session,
    maintenance_team_id: int
):
    active_statuses = ["Open", "Accepted", "In Progress"]

    return (
        db.query(
            Technician,
            func.count(Ticket.id).label("workload")
        )
        .outerjoin(
            Ticket,
            (Ticket.technician_id == Technician.id)
            & (Ticket.status.in_(active_statuses))
        )
        .filter(
            Technician.maintenance_team_id == maintenance_team_id,
            Technician.is_active.is_(True)
        )
        .group_by(Technician.id)
        .order_by(
            func.count(Ticket.id).asc(),
            Technician.id.asc()
        )
        .first()
    )

def get_active_fault_category(db: Session, fault_category_id: int):
    return (
        db.query(FaultCategory)
        .filter(
            FaultCategory.id == fault_category_id,
            FaultCategory.is_active.is_(True)
        )
        .first()
    )

def get_active_fault_category(db: Session, fault_category_id: int):
    return (
        db.query(FaultCategory)
        .filter(
            FaultCategory.id == fault_category_id,
            FaultCategory.is_active.is_(True)
        )
        .first()
    )


def get_technician_with_lowest_workload(
    db: Session,
    maintenance_team_id: int
):
    active_statuses = ["Open", "Assigned", "In Progress"]

    return (
        db.query(
            Technician,
            func.count(Ticket.id).label("workload")
        )
        .outerjoin(
            Ticket,
            (Ticket.technician_id == Technician.id)
            & (Ticket.status.in_(active_statuses))
        )
        .filter(
            Technician.maintenance_team_id == maintenance_team_id,
            Technician.is_active.is_(True)
        )
        .group_by(Technician.id)
        .order_by(
            func.count(Ticket.id).asc(),
            Technician.id.asc()
        )
        .first()
    )

def create_ticket_status_history(
    db: Session,
    ticket_id: int,
    changed_by_user_id: int,
    old_status: str,
    new_status: str,
    remarks: str | None = None
):
    history = TicketHistory(
        ticket_id=ticket_id,
        changed_by_user_id=changed_by_user_id,
        old_status=old_status,
        new_status=new_status,
        remarks=remarks
    )

    db.add(history)
    db.flush()

    return history