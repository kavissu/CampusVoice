
from app.db.database import SessionLocal
from app.models.location import Location

db = SessionLocal()

try:
    location = (
        db.query(Location)
        .filter(Location.code == "REF-LH-L211A")
        .first()
    )

    if location:
        print("Location:", location.name)
        print("QR Token:", location.qr_code_token)
    else:
        print("Location not found.")

finally:
    db.close()
