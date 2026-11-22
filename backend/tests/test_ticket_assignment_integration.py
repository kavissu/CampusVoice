
from types import SimpleNamespace

from app.models.department import Department
from app.models.role import Role
from app.models.user import User
from app.models.location import Location
from app.models.hall import Hall
from app.models.maintenance_team import MaintenanceTeam
from app.models.technician import Technician
from app.models.fault_category import FaultCategory
from app.models.ticket import Ticket
from app.models.ticket_history import TicketHistory

from app.schemas.ticket import EquipmentFaultCreate
from app.services.ticket import create_equipment_fault_ticket
from app.repositories import ticket as ticket_repository


def test_automatic_assignment_is_saved_in_database(
    db_session,
    monkeypatch
):
    # 1. Create department, roles and maintenance team
    department = Department(
        name="Engineering",
        code="ENG"
    )

    lecturer_role = Role(name="LECTURER")
    technician_role = Role(name="TECHNICIAN")

    team = MaintenanceTeam(
        name="Electrical Team",
        is_active=True
    )

    db_session.add_all([
        department,
        lecturer_role,
        technician_role,
        team
    ])
    db_session.flush()

    # 2. Create lecturer and technician users
    lecturer = User(
        full_name="Test Lecturer",
        email="lecturer.integration@test.com",
        password_hash="test-hash",
        role_id=lecturer_role.id,
        department_id=department.id,
        is_active=True,
        must_change_password=False
    )

    technician_user = User(
        full_name="Test Technician",
        email="technician.integration@test.com",
        password_hash="test-hash",
        role_id=technician_role.id,
        department_id=department.id,
        is_active=True,
        must_change_password=False
    )

    db_session.add_all([lecturer, technician_user])
    db_session.flush()

    technician = Technician(
        user_id=technician_user.id,
        maintenance_team_id=team.id,
        is_active=True
    )

    db_session.add(technician)

    # 3. Create fault category connected to the team
    category = FaultCategory(
        name="Electrical Fault",
        maintenance_team_id=team.id,
        is_active=True
    )

    db_session.add(category)

    # 4. Create QR location and hall
    location = Location(
        name="Test Location",
        code="TEST-LOC",
        location_type="HALL",
        qr_code_token="TEST-QR-INTEGRATION",
        is_active=True
    )

    db_session.add(location)
    db_session.flush()

    hall = Hall(
        location_id=location.id,
        name="Test Hall",
        code="TEST-HALL",
        is_active=True
    )

    db_session.add(hall)
    db_session.flush()

    # 5. Mock equipment and problem-option lookup
    # Assignment, category, team and database operations remain real.
    monkeypatch.setattr(
        ticket_repository,
        "get_active_equipment",
        lambda db, equipment_id: SimpleNamespace(
            id=200,
            hall_id=hall.id,
            equipment_type_id=30
        )
    )

    monkeypatch.setattr(
        ticket_repository,
        "get_active_problem_option",
        lambda db, option_id, type_id: SimpleNamespace(
            id=300,
            fault_category_id=category.id,
            problem_name="Projector is not displaying"
        )
    )

    # 6. Submit an equipment fault
    ticket_data = EquipmentFaultCreate(
        equipment_id=200,
        problem_option_id=300,
        urgency_reason="Class in progress"
    )

    ticket = create_equipment_fault_ticket(
        db=db_session,
        user_id=lecturer.id,
        qr_token="TEST-QR-INTEGRATION",
        ticket_data=ticket_data
    )

    # 7. Retrieve the saved ticket from the database
    saved_ticket = db_session.query(Ticket).filter(
        Ticket.id == ticket.id
    ).one()

    assert saved_ticket.maintenance_team_id == team.id
    assert saved_ticket.technician_id == technician.id
    assert saved_ticket.status == "Open"
    assert saved_ticket.classification_status == "Classified"

    # 8. Verify assignment history was saved
    history = (
        db_session.query(TicketHistory)
        .filter(TicketHistory.ticket_id == ticket.id)
        .order_by(TicketHistory.id.asc())
        .all()
    )

    assert len(history) == 2
    assert history[0].new_status == "Open"
    assert history[1].new_status == "Open"
    assert history[1].new_technician_id == technician.id
    assert history[1].changed_by_user_id is None


def _prepare_unassigned_ticket_test(
    db_session,
    monkeypatch,
    include_category=True
):
    department = Department(
        name="Engineering",
        code="ENG"
    )
    lecturer_role = Role(name="LECTURER")

    db_session.add_all([department, lecturer_role])
    db_session.flush()

    lecturer = User(
        full_name="Test Lecturer",
        email="unassigned.lecturer@test.com",
        password_hash="test-hash",
        role_id=lecturer_role.id,
        department_id=department.id,
        is_active=True,
        must_change_password=False
    )
    db_session.add(lecturer)

    location = Location(
        name="Test Location",
        code="TEST-LOC",
        location_type="HALL",
        qr_code_token="TEST-QR-UNASSIGNED",
        is_active=True
    )
    db_session.add(location)
    db_session.flush()

    hall = Hall(
        location_id=location.id,
        name="Test Hall",
        code="TEST-HALL",
        is_active=True
    )
    db_session.add(hall)

    team = None
    category = None

    if include_category:
        team = MaintenanceTeam(
            name="Electrical Team",
            is_active=True
        )
        db_session.add(team)
        db_session.flush()

        category = FaultCategory(
            name="Electrical Fault",
            maintenance_team_id=team.id,
            is_active=True
        )
        db_session.add(category)

    db_session.flush()

    monkeypatch.setattr(
        ticket_repository,
        "get_active_equipment",
        lambda db, equipment_id: SimpleNamespace(
            id=200,
            hall_id=hall.id,
            equipment_type_id=30
        )
    )

    def get_problem_option(db, option_id, type_id):
        if option_id is None or category is None:
            return None

        return SimpleNamespace(
            id=300,
            fault_category_id=category.id,
            problem_name="Projector is not displaying"
        )

    monkeypatch.setattr(
        ticket_repository,
        "get_active_problem_option",
        get_problem_option
    )

    return lecturer, team, category


def test_ticket_stays_open_when_no_technician_available(
    db_session,
    monkeypatch
):
    lecturer, team, category = _prepare_unassigned_ticket_test(
        db_session,
        monkeypatch
    )

    # Simulate no available technician
    monkeypatch.setattr(
        ticket_repository,
        "get_technician_with_lowest_workload",
        lambda db, team_id: None
    )

    ticket_data = EquipmentFaultCreate(
        equipment_id=200,
        problem_option_id=300,
        urgency_reason="Class in progress"
    )

    ticket = create_equipment_fault_ticket(
        db=db_session,
        user_id=lecturer.id,
        qr_token="TEST-QR-UNASSIGNED",
        ticket_data=ticket_data
    )

    saved_ticket = db_session.query(Ticket).filter(
        Ticket.id == ticket.id
    ).one()

    assert saved_ticket.status == "Open"
    assert saved_ticket.technician_id is None
    assert saved_ticket.maintenance_team_id == team.id
    assert saved_ticket.classification_status == "Classified"

    history = db_session.query(TicketHistory).filter(
        TicketHistory.ticket_id == ticket.id
    ).all()

    assert len(history) == 1
    assert history[0].new_status == "Open"


def test_free_text_ticket_stays_pending_and_unassigned(
    db_session,
    monkeypatch
):
    lecturer, team, category = _prepare_unassigned_ticket_test(
        db_session,
        monkeypatch,
        include_category=False
    )

    ticket_data = EquipmentFaultCreate(
        equipment_id=200,
        problem_option_id=None,
        problem_description="Projector keeps switching off",
        urgency_reason="Can be resolved later"
    )

    ticket = create_equipment_fault_ticket(
        db=db_session,
        user_id=lecturer.id,
        qr_token="TEST-QR-UNASSIGNED",
        ticket_data=ticket_data
    )

    saved_ticket = db_session.query(Ticket).filter(
        Ticket.id == ticket.id
    ).one()

    assert saved_ticket.status == "Open"
    assert saved_ticket.technician_id is None
    assert saved_ticket.maintenance_team_id is None
    assert saved_ticket.fault_category_id is None
    assert saved_ticket.classification_status == "Pending"
    assert saved_ticket.problem_description == (
        "Projector keeps switching off"
    )
