
from app.models.location import Location
from app.models.hall import Hall
from app.models.department import Department
from app.models.equipment_type import EquipmentType
from app.models.equipment import Equipment


def create_api_test_data(db):
    department = Department(
        name="Computer Engineering",
        code="CO"
    )

    equipment_type = EquipmentType(
        name="Computer Equipment"
    )

    location = Location(
        name="API Test Hall",
        code="API-TEST-001",
        location_type="LECTURE_HALL",
        qr_code_token="api-test-token",
        is_active=True
    )

    db.add_all([department, equipment_type, location])
    db.flush()

    hall = Hall(
        name="API Test Hall",
        code="API-HALL-001",
        location_id=location.id,
        is_active=True
    )

    db.add(hall)
    db.flush()

    equipment = Equipment(
        name="API Test Computer",
        asset_code="API-PC-001",
        equipment_type_id=equipment_type.id,
        department_id=department.id,
        hall_id=hall.id,
        is_active=True
    )

    db.add(equipment)
    db.commit()


def test_public_equipment_api_success(client, db_session):
    create_api_test_data(db_session)

    response = client.get(
        "/api/v1/public/locations/api-test-token/equipment"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["location"]["name"] == "API Test Hall"
    assert data["hall"]["name"] == "API Test Hall"
    assert data["total_equipment"] == 1
    assert data["equipment"][0]["name"] == "API Test Computer"


def test_public_equipment_api_invalid_token(client):
    response = client.get(
        "/api/v1/public/locations/invalid-token/equipment"
    )

    assert response.status_code == 404

    assert response.json()["detail"] == (
        "Location or active hall not found"
    )
