import uuid

from datetime import datetime, timedelta, timezone

from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base

class CompanyInvite(Base):
    __tablename__ = "company_invites"

    token: Mapped[str] = mapped_column(primary_key=True,
                                       default=lambda: uuid.uuid4().hex[:12])
    company_id: Mapped[int] = mapped_column(ForeignKey("companies.id", ondelete="CASCADE"))

    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc) + timedelta(hours=24))
