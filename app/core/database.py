import enum

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Enum
from app.core.settings import settings


engine = create_async_engine(settings.DATABASE_URL, 
                             echo=True)

AsyncSessionLocal = async_sessionmaker(bind=engine,
                                       expire_on_commit=False,
                                       class_=AsyncSession)

class Base(DeclarativeBase):
    pass

class TaskStatus(enum.Enum):
    NEW = "новая"
    ACCEPTED_FOR_WORK = "принята в работу"
    IN_PROGRESS = "в процессе"
    DONE = "выполнена"

