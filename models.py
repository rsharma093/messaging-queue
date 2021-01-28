import datetime
import enum
from datetime import datetime

from fastapi.encoders import jsonable_encoder
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, VARCHAR, TIMESTAMP, Text, JSON, Numeric
from sqlalchemy import text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Session
from sqlalchemy.orm import relationship
from sqlalchemy.types import DateTime, Enum

from db import Base
from schemas.process_schema import ProcessCreateModel, StatusEnum
from utils import test


class Process(Base):
    __tablename__ = 'process'

    id = Column(Integer, primary_key=True, index=True)
    func_name = Column(VARCHAR(255))
    func_params = Column(VARCHAR(255), nullable=True)
    status = Column(VARCHAR(255))
    priority = Column(VARCHAR(255))
    output = Column(VARCHAR(255), nullable=True)
    created_at = Column(TIMESTAMP)
    updated_at = Column(TIMESTAMP)

    @classmethod
    def get_queryset(cls, db: Session):
        return db.query(cls)

    @classmethod
    def list(cls, db: Session):
        return cls.get_queryset(db).all()

    @classmethod
    def create(cls, db: Session, process_component: ProcessCreateModel):
        instance = cls(**process_component.dict())
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance

    @classmethod
    def queued_processes_list(cls, db: Session):
        return cls.get_queryset(db).filter(Process.status == StatusEnum.QUEUED.value).all()

    @classmethod
    def process_status_detail(cls, db:Session, id: int):
        return cls.get_queryset(db).filter(Process.id == id).first()

