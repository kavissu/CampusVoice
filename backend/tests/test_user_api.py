
from app.models.user import User
from app.models.role import Role
from app.models.department import Department
from app.models.maintenance_team import MaintenanceTeam
from app.core.security import hash_password


def create_test_admin(db):
    role = Role(name="ADMIN")
    lecturer_role = Role(name="LECTURER")
    technician_role = Role(name="TECHNICIAN")

    db.add_all([role, lecturer_role, technician_role])
    db.flush()

    department = Department(
        name="Computer Engineering",
        code="CE"
    )

    team = MaintenanceTeam(
        name="IT Support",
        is_active=True
    )

    db.add_all([department, team])
    db.flush()

    admin = User(
        full_name="Test Admin",
        email="admin.test@example.com",
        password_hash=hash_password("Admin@123"),
        role_id=role.id,
        is_active=True,
        must_change_password=False
    )

    db.add(admin)
    db.commit()

    return admin, department, team


def get_admin_token(client, db):
    create_test_admin(db)

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": "admin.test@example.com",
            "password": "Admin@123"
        }
    )

    assert response.status_code == 200

    return response.json()["access_token"]


def test_admin_can_create_lecturer(client, db_session):
    token = get_admin_token(client, db_session)

    response = client.post(
        "/api/v1/users/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "full_name": "New Lecturer",
            "email": "newlecturer@example.com",
            "role": "LECTURER",
            "department_id": 1,
            "maintenance_team_id": None
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["full_name"] == "New Lecturer"
    assert data["role"] == "LECTURER"
    assert data["must_change_password"] is True
    assert data["temporary_password"]


def test_admin_can_create_technician(client, db_session):
    token = get_admin_token(client, db_session)

    response = client.post(
        "/api/v1/users/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "full_name": "New Technician",
            "email": "newtechnician@example.com",
            "role": "TECHNICIAN",
            "department_id": 1,
            "maintenance_team_id": 1
        }
    )

    assert response.status_code == 201

    data = response.json()

    assert data["role"] == "TECHNICIAN"
    assert data["must_change_password"] is True
    assert data["temporary_password"]


def test_lecturer_cannot_create_user(client, db_session):
    role = Role(name="LECTURER")
    admin_role = Role(name="ADMIN")

    db_session.add_all([role, admin_role])
    db_session.flush()

    lecturer = User(
        full_name="Test Lecturer",
        email="lecturer@example.com",
        password_hash=hash_password("Lecturer@123"),
        role_id=role.id,
        is_active=True,
        must_change_password=False
    )

    db_session.add(lecturer)
    db_session.commit()

    login = client.post(
        "/api/v1/auth/login",
        json={
            "email": "lecturer@example.com",
            "password": "Lecturer@123"
        }
    )

    token = login.json()["access_token"]

    response = client.post(
        "/api/v1/users/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "full_name": "Another Lecturer",
            "email": "another@example.com",
            "role": "LECTURER",
            "department_id": 1,
            "maintenance_team_id": None
        }
    )

    assert response.status_code == 403


def test_create_user_without_token(client):
    response = client.post(
        "/api/v1/users/",
        json={
            "full_name": "New Lecturer",
            "email": "new@example.com",
            "role": "LECTURER",
            "department_id": 1,
            "maintenance_team_id": None
        }
    )

    assert response.status_code == 401


def test_duplicate_email_rejected(client, db_session):
    token = get_admin_token(client, db_session)

    request_data = {
        "full_name": "New Lecturer",
        "email": "duplicate@example.com",
        "role": "LECTURER",
        "department_id": 1,
        "maintenance_team_id": None
    }

    first_response = client.post(
        "/api/v1/users/",
        headers={"Authorization": f"Bearer {token}"},
        json=request_data
    )

    assert first_response.status_code == 201

    second_response = client.post(
        "/api/v1/users/",
        headers={"Authorization": f"Bearer {token}"},
        json=request_data
    )

    assert second_response.status_code == 400


def test_invalid_department_rejected(client, db_session):
    token = get_admin_token(client, db_session)

    response = client.post(
        "/api/v1/users/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "full_name": "New Lecturer",
            "email": "invalid.department@example.com",
            "role": "LECTURER",
            "department_id": 999,
            "maintenance_team_id": None
        }
    )

    assert response.status_code == 400


def test_technician_without_team_rejected(client, db_session):
    token = get_admin_token(client, db_session)

    response = client.post(
        "/api/v1/users/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "full_name": "New Technician",
            "email": "missing.team@example.com",
            "role": "TECHNICIAN",
            "department_id": 1,
            "maintenance_team_id": None
        }
    )

    assert response.status_code == 400
