from typing import List

from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

import deps
from models import Process
from schemas.process_schema import ProcessListModel, ProcessCreateModel

router = APIRouter()


@router.post("/add", response_model=ProcessListModel)
def add_process(process_component: ProcessCreateModel, db: Session = Depends(deps.get_db)):
    """
    Create Process
    """
    return jsonable_encoder(Process.create(db=db, process_component=process_component))


@router.get("/status", response_model=List[ProcessListModel])
def queued_processes_list(db: Session = Depends(deps.get_db)):
    """
    List queued processes
    """
    return jsonable_encoder(Process.queued_processes_list(db=db))


@router.get("/status/{id}", response_model=ProcessListModel)
def process_status_detail(id: int, db: Session = Depends(deps.get_db)):
    """
    Get process status detail
    """
    return jsonable_encoder(Process.process_status_detail(db=db, id=id))


@router.get("/output/{id}", response_model=ProcessListModel)
def process_output_list(id: int, db: Session = Depends(deps.get_db)):
    """
    Get process output detail
    """
    return jsonable_encoder(Process.process_status_detail(db=db, id=id))
