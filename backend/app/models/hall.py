
from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Hall(Base):
    __tablename__ = "halls"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    location_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("locations.id"),
        unique=True,
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    code: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )
