
from datetime import datetime, timezone

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class TicketHistory(Base):
    __tablename__ = "ticket_history"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    ticket_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("tickets.id"),
        nullable=False
    )

    changed_by_user_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=True
    )

    # Status changes
    old_status: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True
    )

    new_status: Mapped[str | None] = mapped_column(
        String(30),
        nullable=True
    )

    # Priority changes
    old_priority: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    new_priority: Mapped[str | None] = mapped_column(
        String(20),
        nullable=True
    )

    # Technician assignment changes
    old_technician_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("technicians.id"),
        nullable=True
    )

    new_technician_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("technicians.id"),
        nullable=True
    )

    remarks: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    changed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
