
from app.models.ticket import Ticket
from app.models.ticket_history import TicketHistory


def create_test_ticket(db_session):
    ticket = Ticket(
        tracking_code="CV-EF-TEST123456",
        ticket_type="EQUIPMENT_FAULT",
        problem_description="Projector is not working",
        priority="Critical",
        status="Open"
    )

    db_session.add(ticket)
    db_session.commit()
    db_session.refresh(ticket)

    history = TicketHistory(
        ticket_id=ticket.id,
        changed_by_user_id=None,
        new_status="Open",
        new_priority="Critical",
        remarks="Equipment fault ticket created"
    )

    db_session.add(history)
    db_session.commit()

    return ticket


def test_track_ticket_success(client, db_session):
    ticket = create_test_ticket(db_session)

    response = client.get(
        f"/api/v1/tickets/track/{ticket.tracking_code}"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["tracking_code"] == ticket.tracking_code
    assert data["problem_description"] == "Projector is not working"
    assert data["priority"] == "Critical"
    assert data["status"] == "Open"
    assert len(data["history"]) == 1
    assert data["history"][0]["new_status"] == "Open"


def test_track_ticket_not_found(client):
    response = client.get(
        "/api/v1/tickets/track/INVALID123"
    )

    assert response.status_code == 404


def test_track_ticket_without_login(client, db_session):
    ticket = create_test_ticket(db_session)

    # No authentication token is provided
    response = client.get(
        f"/api/v1/tickets/track/{ticket.tracking_code}"
    )

    assert response.status_code == 200
