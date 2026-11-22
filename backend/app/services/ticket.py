
from uuid import uuid4
from app.schemas.ticket import TicketTrackingResponse, TicketStatusUpdate
from sqlalchemy.orm import Session

from app.repositories import ticket as ticket_repository
from app.repositories import user as user_repository
from datetime import datetime, timezone

def create_equipment_fault_ticket(
    db: Session,
    user_id: int,
    qr_token: str,
    ticket_data
):
    # 1. Validate QR code and hall
    hall = ticket_repository.get_active_hall_by_qr_token(
        db, qr_token
    )

    if hall is None:
        raise ValueError("Invalid or inactive hall QR code")

    # 2. Validate equipment
    equipment = ticket_repository.get_active_equipment(
        db, ticket_data.equipment_id
    )

    if equipment is None:
        raise ValueError("Equipment not found or inactive")

    if equipment.hall_id != hall.id:
        raise ValueError(
            "Selected equipment does not belong to this hall"
        )

    # 3. Validate problem option
    problem_option = None

    if ticket_data.problem_option_id is not None:
        problem_option = ticket_repository.get_active_problem_option(
            db,
            ticket_data.problem_option_id,
            equipment.equipment_type_id
        )

        if problem_option is None:
            raise ValueError("Invalid problem option for this equipment")

    # 4. Determine description
    description = ticket_data.problem_description

    if description is None and problem_option is not None:
        description = problem_option.problem_name

    if not description:
        raise ValueError("Problem description is required")

    # 5. Determine priority
    priority_mapping = {
        "Class in progress": "Critical",
        "Can be resolved later": "High"
    }

    priority = priority_mapping[ticket_data.urgency_reason]

    # 6. Prepare automatic assignment details
    fault_category_id = (
        problem_option.fault_category_id
        if problem_option else None
    )

    maintenance_team_id = None
    technician_id = None
    status = "Open"

    classification_status = "Pending"

    if fault_category_id is not None:
        fault_category = ticket_repository.get_active_fault_category(
            db, fault_category_id
        )

        if fault_category is not None:
            maintenance_team = user_repository.get_active_maintenance_team(
                db, fault_category.maintenance_team_id
            )

            if maintenance_team is not None:
                maintenance_team_id = maintenance_team.id
                classification_status = "Classified"

                technician_result = (
                    ticket_repository.get_technician_with_lowest_workload(
                        db, maintenance_team.id
                    )
                )

                if technician_result is not None:
                   technician, workload = technician_result
                   technician_id = technician.id
                   
    # 7. Generate tracking code
    tracking_code = f"CV-EF-{uuid4().hex[:12].upper()}"

    # 8. Prepare ticket
    new_ticket_data = {
        "tracking_code": tracking_code,
        "ticket_type": "EQUIPMENT_FAULT",
        "reported_by_user_id": user_id,
        "equipment_id": equipment.id,
        "hall_id": hall.id,
        "problem_option_id": (
            problem_option.id if problem_option else None
        ),
        "urgency_reason": ticket_data.urgency_reason,
        "problem_description": description,
        "fault_category_id": fault_category_id,
        "maintenance_team_id": maintenance_team_id,
        "technician_id": technician_id,
        "priority": priority,
        "status": status,
        "classification_status": classification_status
    }

    # 9. Create ticket and history in one transaction
    try:
        ticket = ticket_repository.create_ticket(
            db, new_ticket_data
        )

        # Record initial ticket creation
        ticket_repository.create_ticket_history(
            db,
            ticket.id,
            user_id,
            priority
        )

        # Record automatic assignment
        if technician_id is not None:
            ticket_repository.create_ticket_assignment_history(
                db=db,
                ticket_id=ticket.id,
                admin_user_id=None,
                old_technician_id=None,
                new_technician_id=technician_id,
                old_status="Open",
                new_status="Open",
                remarks="Automatically assigned to technician"
            )

        db.commit()
        db.refresh(ticket)

        return ticket

    except Exception:
        db.rollback()
        raise



def get_ticket_tracking_details(db: Session, tracking_code: str):
    ticket = ticket_repository.get_ticket_by_tracking_code(
        db, tracking_code
    )

    if ticket is None:
        raise ValueError("Ticket not found")

    history = ticket_repository.get_ticket_history(
        db, ticket.id
    )

    return {
        "tracking_code": ticket.tracking_code,
        "ticket_type": ticket.ticket_type,
        "problem_description": ticket.problem_description,
        "priority": ticket.priority,
        "status": ticket.status,
        "reported_at": ticket.reported_at,
        "resolved_at": ticket.resolved_at,
        "history": history
    }


def get_technician_assigned_tickets(db: Session, user_id: int):
    # 1. Find the technician using the logged-in user's ID
    technician = ticket_repository.get_technician_by_user_id(
        db, user_id
    )

    if technician is None:
        raise ValueError("Technician profile not found or inactive")

    # 2. Retrieve tickets assigned to this technician
    tickets = ticket_repository.get_tickets_by_technician(
        db, technician.id
    )

    return tickets


def assign_ticket_to_technician(
    db: Session,
    ticket_id: int,
    technician_id: int,
    admin_user_id: int
):
    # 1. Find the ticket
    ticket = ticket_repository.get_ticket_by_id(db, ticket_id)

    if ticket is None:
        raise ValueError("Ticket not found")

    # 2. Find an active technician
    technician = ticket_repository.get_active_technician(
        db, technician_id
    )

    if technician is None:
        raise ValueError("Active technician not found")

    # 3. Verify the technician's maintenance team is active
    maintenance_team = user_repository.get_active_maintenance_team(
        db, technician.maintenance_team_id
    )

    if maintenance_team is None:
        raise ValueError("Technician's maintenance team is inactive")

    # 4. Assign technician
    old_technician_id = ticket.technician_id
    old_status = ticket.status

    ticket.technician_id = technician.id
    ticket.maintenance_team_id = maintenance_team.id

    # Change Open to Assigned, but preserve other statuses
    if ticket.status == "Open":
        ticket.status = "Assigned"

    # 5. Record assignment history
    try:
        ticket_repository.create_ticket_assignment_history(
            db=db,
            ticket_id=ticket.id,
            admin_user_id=admin_user_id,
            old_technician_id=old_technician_id,
            new_technician_id=technician.id,
            old_status=old_status,
            new_status=ticket.status,
            remarks="Ticket assigned to technician"
        )

        db.commit()
        db.refresh(ticket)

        return ticket

    except Exception:
        db.rollback()
        raise

def update_ticket_status(
    db: Session,
    ticket_id: int,
    user_id: int,
    status_data: TicketStatusUpdate
):
    # 1. Find the ticket
    ticket = ticket_repository.get_ticket_by_id(db, ticket_id)

    if ticket is None:
        raise ValueError("Ticket not found")

    # 2. Find the logged-in technician
    technician = ticket_repository.get_technician_by_user_id(
        db, user_id
    )

    if technician is None:
        raise ValueError("Technician profile not found or inactive")

    # 3. Check whether this ticket belongs to the technician
    if ticket.technician_id != technician.id:
        raise ValueError("You are not assigned to this ticket")

    # 4. Validate the status transition
    allowed_transitions = {
        "Open": "Accepted",
        "Accepted": "In Progress",
        "In Progress": "Resolved"
    }

    expected_status = allowed_transitions.get(ticket.status)

    if status_data.status != expected_status:
        raise ValueError(
            f"Invalid status transition from {ticket.status}"
        )

    # 5. Require a resolution note
    remarks = (
        status_data.remarks.strip()
        if status_data.remarks
        else None
    )

    if status_data.status == "Resolved" and not remarks:
        raise ValueError("Resolution note is required")

    # 6. Update ticket and save history
    old_status = ticket.status

    try:
        ticket.status = status_data.status

        if status_data.status == "Resolved":
            ticket.resolved_at = datetime.now(timezone.utc)

        ticket_repository.create_ticket_status_history(
            db=db,
            ticket_id=ticket.id,
            changed_by_user_id=user_id,
            old_status=old_status,
            new_status=status_data.status,
            remarks=remarks
        )

        db.commit()
        db.refresh(ticket)

        return ticket

    except Exception:
        db.rollback()
        raise