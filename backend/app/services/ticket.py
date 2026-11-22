
from uuid import uuid4

from sqlalchemy.orm import Session

from app.repositories import ticket as ticket_repository


def create_equipment_fault_ticket(
    db: Session,
    user_id: int,
    qr_token: str,
    ticket_data
):
    # 1. Validate the QR code and get its active hall
    hall = ticket_repository.get_active_hall_by_qr_token(
        db,
        qr_token
    )

    if hall is None:
        raise ValueError("Invalid or inactive hall QR code")

    # 2. Validate the selected equipment
    equipment = ticket_repository.get_active_equipment(
        db,
        ticket_data.equipment_id
    )

    if equipment is None:
        raise ValueError("Equipment not found or inactive")

    # 3. Check whether the equipment belongs to the scanned hall
    if equipment.hall_id != hall.id:
        raise ValueError(
            "Selected equipment does not belong to this hall"
        )

    # 4. Validate the selected problem option, if provided
    problem_option = None

    if ticket_data.problem_option_id is not None:
        problem_option = (
            ticket_repository.get_active_problem_option(
                db,
                ticket_data.problem_option_id,
                equipment.equipment_type_id
            )
        )

        if problem_option is None:
            raise ValueError(
                "Invalid problem option for this equipment"
            )

    # 5. Determine the problem description
    description = ticket_data.problem_description

    if description is None and problem_option is not None:
        description = problem_option.problem_name

    if not description:
        raise ValueError("Problem description is required")

    # 6. Determine priority from lecturer's urgency selection
    priority_mapping = {
        "Class in progress": "Critical",
        "Can be resolved later": "High"
    }

    priority = priority_mapping[ticket_data.urgency_reason]

    # 7. Generate a unique tracking code
    tracking_code = f"CV-EF-{uuid4().hex[:12].upper()}"

    # 8. Prepare ticket data
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
        "fault_category_id": (
            problem_option.fault_category_id
            if problem_option else None
        ),
        "priority": priority,
        "status": "Open",
        "classification_status": (
            "Pending" if problem_option is None else "Classified"
        )
    }

    # 9. Create ticket and history in one transaction
    try:
        ticket = ticket_repository.create_ticket(
            db,
            new_ticket_data
        )

        ticket_repository.create_ticket_history(
            db,
            ticket.id,
            user_id,
            priority
        )

        db.commit()
        db.refresh(ticket)

        return ticket

    except Exception:
        db.rollback()
        raise
