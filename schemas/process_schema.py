from enum import Enum
from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class StatusEnum(str, Enum):
    QUEUED = 'queued'
    IN_PROGRESS = 'in_progress'
    COMPLETED = 'completed'


class PriorityEnum(str, Enum):
    HIGH = 'high'
    LOW = 'low'


class ProcessListModel(BaseModel):
    id: int
    func_name: str
    func_params: Optional[str] = None
    status: str
    priority: str
    output: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_model = True


class ProcessCreateModel(BaseModel):
    func_name: str
    func_params: Optional[str] = None
    priority: PriorityEnum
    status: StatusEnum = StatusEnum.QUEUED
    created_at: datetime = datetime.now()
    updated_at: datetime = datetime.now()

    class Config:
        orm_model = True
