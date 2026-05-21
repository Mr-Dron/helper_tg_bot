from sqlalchemy import String, Text, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, TaskStatus

class Tasks(Base):
    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
        index=True
        )
    description: Mapped[str | None] = mapped_column(
        Text
        )
    status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus),
        default=TaskStatus.NEW
        )

    creator_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
        )
    responsible_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL")
        )
    company_id: Mapped[int] = mapped_column(
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False
        )
    
    creator = relationship("Users", back_populates="created_tasks", foreign_keys=[creator_id])
    responsible = relationship("Users", back_populates="assigned_tasks", foreign_keys=[responsible_id])
    company = relationship("Companies", back_populates="tasks")