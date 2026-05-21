from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Column, Integer, String

from app.core.database import Base

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(
        nullable=False,
        index=True
    )
    telegram_url: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )
    username: Mapped[str] = mapped_column(
        String(50), 
        nullable=False
    )
    first_name: Mapped[str] = mapped_column(
        String(50),
        nullable=True
    )

    company = relationship("EmployeesCompany", back_populates="employees")
    created_tasks = relationship("Tasks", back_populates="creator", foreign_keys="Tasks.creator_id")
    assigned_tasks = relationship("Tasks", back_populates="responsible", foreign_keys="Tasks.responsible_id")
