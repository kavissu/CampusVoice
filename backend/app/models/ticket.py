
from datetime import datetime, timezone

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String
)
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Ticket(Base):
    __tablename__ = "tickets"

    __table_args__ = (
        CheckConstraint(
            "priority IN ('Critical', 'High', 'Medium', 'Low')",
            name="ck_ticket_priority"
        ),
        CheckConstraint(
            "ticket_type IN ('EQUIPMENT_FAULT', 'GENERAL_COMPLAINT')",
            name="ck_ticket_type"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    tracking_code: Mapped[str] = mapped_column(
        String(50),
        unique=True,
        nullable=False,
        index=True
    )

    ticket_type: Mapped[str] = mapped_column(
        String(30),
        nullable=False
    )

    # Reporter information
    reported_by_user_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    # Equipment fault details
    equipment_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("equipment.id"),
        nullable=True
    )

    hall_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("halls.id"),
        nullable=True
    )

    problem_option_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("equipment_problem_options.id"),
        nullable=True
    )

    urgency_reason: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    # General complaint details
    qr_scanned_location_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("locations.id"),
        nullable=True
    )

    location_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("locations.id"),
        nullable=True
    )

    complaint_category_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("complaint_categories.id"),
        nullable=True
    )

    complaint_option_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("complaint_options.id"),
        nullable=True
    )

    # Common ticket details
    problem_description: Mapped[str] = mapped_column(
        String(1000),
        nullable=False
    )

    fault_category_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("fault_categories.id"),
        nullable=True
    )

    maintenance_team_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("maintenance_teams.id"),
        nullable=True
    )

    technician_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("technicians.id"),
        nullable=True
    )

    # Priority: Critical, High, Medium, Low
    priority: Mapped[str] = mapped_column(
        String(20),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="Open"
    )

    classification_status: Mapped[str] = mapped_column(
        String(30),
        nullable=False,
        default="Pending"
    )

    reported_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    resolved_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
