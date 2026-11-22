
from app.models.department import Department
from app.models.role import Role
from app.models.user import User
from app.models.maintenance_team import MaintenanceTeam
from app.models.technician import Technician
from app.models.ticket import Ticket
from app.repositories import ticket as ticket_repository


def test_selects_technician_with_lowest_workload(db_session):
    # 1. Create department, role and maintenance team
    department = Department(
        name="Engineering",
        code="ENG"
    )
    role = Role(name="TECHNICIAN")
    team = MaintenanceTeam(
        name="Electrical Team",
        is_active=True
    )

    db_session.add_all([department, role, team])
    db_session.flush()

    # 2. Create two technician users
    user1 = User(
        full_name="Technician One",
        email="tech1@test.com",
        password_hash="test-hash",
        role_id=role.id,
        department_id=department.id
    )

    user2 = User(
        full_name="Technician Two",
        email="tech2@test.com",
        password_hash="test-hash",
        role_id=role.id,
        department_id=department.id
    )

    db_session.add_all([user1, user2])
    db_session.flush()

    # 3. Create technician profiles
    technician1 = Technician(
        user_id=user1.id,
        maintenance_team_id=team.id,
        is_active=True
    )

    technician2 = Technician(
        user_id=user2.id,
        maintenance_team_id=team.id,
        is_active=True
    )

    db_session.add_all([technician1, technician2])
    db_session.flush()

    # 4. Technician One has two active tickets
    for i in range(2):
        db_session.add(Ticket(
            tracking_code=f"TEST-ONE-{i}",
            ticket_type="EQUIPMENT_FAULT",
            problem_description="Projector fault",
            priority="High",
            status="Assigned",
            technician_id=technician1.id
        ))

    # Technician Two has one active ticket
    db_session.add(Ticket(
        tracking_code="TEST-TWO-1",
        ticket_type="EQUIPMENT_FAULT",
        problem_description="Microphone fault",
        priority="High",
        status="In Progress",
        technician_id=technician2.id
    ))

    # A resolved ticket should not count towards workload
    db_session.add(Ticket(
        tracking_code="TEST-TWO-2",
        ticket_type="EQUIPMENT_FAULT",
        problem_description="Old fault",
        priority="High",
        status="Resolved",
        technician_id=technician2.id
    ))

    db_session.flush()

    # 5. Find the technician with the lowest workload
    result = ticket_repository.get_technician_with_lowest_workload(
        db_session,
        team.id
    )

    selected_technician, workload = result

    assert selected_technician.id == technician2.id
    assert workload == 1
