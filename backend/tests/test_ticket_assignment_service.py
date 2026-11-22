
from types import SimpleNamespace

from app.schemas.ticket import EquipmentFaultCreate
from app.services import ticket as ticket_service
from app.repositories import ticket as ticket_repository
from app.repositories import user as user_repository


def test_equipment_fault_is_automatically_assigned(monkeypatch):
    captured = {}

    # Mock the existing database records
    monkeypatch.setattr(
        ticket_repository,
        "get_active_hall_by_qr_token",
        lambda db, token: SimpleNamespace(id=10)
    )

    monkeypatch.setattr(
        ticket_repository,
        "get_active_equipment",
        lambda db, equipment_id: SimpleNamespace(
            id=20,
            hall_id=10,
            equipment_type_id=30
        )
    )

    monkeypatch.setattr(
        ticket_repository,
        "get_active_problem_option",
        lambda db, option_id, type_id: SimpleNamespace(
            id=40,
            fault_category_id=50,
            problem_name="Projector is not displaying"
        )
    )

    monkeypatch.setattr(
        ticket_repository,
        "get_active_fault_category",
        lambda db, category_id: SimpleNamespace(
            id=50,
            maintenance_team_id=60
        )
    )

    monkeypatch.setattr(
        user_repository,
        "get_active_maintenance_team",
        lambda db, team_id: SimpleNamespace(id=60)
    )

    # Technician with the lowest workload
    selected_technician = SimpleNamespace(id=70)

    monkeypatch.setattr(
        ticket_repository,
        "get_technician_with_lowest_workload",
        lambda db, team_id: (selected_technician, 0)
    )

    # Capture the ticket and history data
    def fake_create_ticket(db, ticket_data):
        captured["ticket"] = ticket_data.copy()
        return SimpleNamespace(id=100, **ticket_data)

    def fake_assignment_history(db, **kwargs):
        captured["history"] = kwargs

    monkeypatch.setattr(
        ticket_repository,
        "create_ticket",
        fake_create_ticket
    )

    monkeypatch.setattr(
        ticket_repository,
        "create_ticket_history",
        lambda *args: None
    )

    monkeypatch.setattr(
        ticket_repository,
        "create_ticket_assignment_history",
        fake_assignment_history
    )

    # Simple database substitute
    class DummyDB:
        def commit(self):
            pass

        def refresh(self, ticket):
            pass

        def rollback(self):
            pass

    ticket_data = EquipmentFaultCreate(
        equipment_id=20,
        problem_option_id=40,
        urgency_reason="Class in progress"
    )

    result = ticket_service.create_equipment_fault_ticket(
        db=DummyDB(),
        user_id=5,
        qr_token="TEST-QR",
        ticket_data=ticket_data
    )

    # Verify the saved assignment details
    assert captured["ticket"]["maintenance_team_id"] == 60
    assert captured["ticket"]["technician_id"] == 70
    assert captured["ticket"]["status"] == "Open"
    assert captured["ticket"]["classification_status"] == "Classified"
    assert captured["ticket"]["priority"] == "Critical"

    # Verify assignment history
    assert captured["history"]["new_technician_id"] == 70
    assert captured["history"]["new_status"] == "Open"

    assert result.id == 100
