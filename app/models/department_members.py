from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey

from app.core.database import Base

class DepartmentMembers(Base):
    __tablename__ = "department_members"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    departmant_id: Mapped[int] = mapped_column(ForeignKey("departments.id", ondelete="CASCADE"))

    members = relationship("Users", back_populates="department")
    department = relationship("Departments", back_populates="members")