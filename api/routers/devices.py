from fastapi import APIRouter, Depends
from fastapi import Depends

from config import config, logging

from db.models import Device, Backend, User_Pydantic, Device_Pydantic, DeviceIn_Pydantic
from tools.convert import utc2local, local2utc

from datetime import datetime, date, timedelta

from dependencies import get_current_user
from typing import List

router = APIRouter(
    prefix="/device",
    tags=["device"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[Device_Pydantic])
async def read_device(user: User_Pydantic = Depends(get_current_user)):
    return await Device.all()

"""
@router.get("/measurements")
async def read_measurements(user: User_Pydantic = Depends(get_current_user), register_id: int = -1, date_from: date = date.today()-timedelta(days=1), date_to: date = date.today()):

    # retrieve user information
    dbsession = NewSession()

    date_to = date_to + timedelta(days=1)

    # retrieve measurements
    if register_id >= 0:
        measurements = dbsession.query(Measurement).filter(Measurement.received_at >= date_from).filter(Measurement.received_at <= date_to).filter(Measurement.register_id == register_id).order_by(Measurement.received_at.desc()).all()
    else:
        measurements = dbsession.query(Measurement).filter(Measurement.received_at >= date_from).filter(Measurement.received_at <= date_to).order_by(Measurement.received_at.desc(), Measurement.register_id).all()

    return measurements

"""