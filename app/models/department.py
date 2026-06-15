from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey

from app.core.database import Base

class Departments(Base):
    __tablename__ = "departments"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    responsible_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"), nullable=False)

    members = relationship("DepartmentMembers", back_populates="department")
    creator = relationship("Users", back_populates="created_departments", foreign_keys=[creator_id])
    responsible = relationship("Users", back_populates="assigned_departments", foreign_keys=[responsible_id])
    tasks = relationship("Tasks", back_populates="department")
    company = relationship("Companies", back_populates="departments")