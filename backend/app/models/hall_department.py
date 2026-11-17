from sqlalchemy import Column, ForeignKey, Table

from app.db.base import Base


hall_departments = Table(
    "hall_departments",
    Base.metadata,

    Column(
        "hall_id",
        ForeignKey("halls.id"),
        primary_key=True
    ),

    Column(
        "department_id",
        ForeignKey("departments.id"),
        primary_key=True
    )
)