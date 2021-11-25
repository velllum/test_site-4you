from models.devices import (
    DeviceSuccessResponse,
    Device,
    NewDevice,
    DeviceConfig
)
from re import match
from misc import db
from fastapi import APIRouter, Request, Depends
from misc.db import Connection
from db import devices as db_devices
from misc.fastapi.depends.db import get as get_db
from misc.fastapi.depends.session import get as get_session
from misc.handlers import (
    error_400_with_detail,
    error_404,
    UnauthenticatedException
)
from misc.session import Session

router = APIRouter(
    tags=['devices']
)


@router.post("/{radio_id}/devices", response_model=DeviceSuccessResponse)
async def create(
    radio_id: int,
    device: NewDevice,
    conn: db.Connection = Depends(get_db),
    session: Session = Depends(get_session),
):
    if not is_device_id_valid(device.device_id):
        return await error_400_with_detail("Device_id is incorrect")
    if not is_device_config_valid(device.config):
        return await error_400_with_detail("Config is incorrect")
    result = await db_devices.create(conn, radio_id, session.user.id, device)
    return DeviceSuccessResponse(data=result)


@router.get("/{radio_id}/devices/{pk}", response_model=DeviceSuccessResponse)
async def get(
    radio_id: int,
    pk: int,
    conn: Connection = Depends(get_db)
):
    result = await db_devices.select(conn, pk)
    if not result:
        return await error_404("Device doesn't exist or was deleted")
    return DeviceSuccessResponse(data=result)


@router.post("/{radio_id}/devices/{pk}", response_model=DeviceSuccessResponse)
async def update(
    radio_id: int,
    pk: int,
    device: NewDevice,
    session: Session = Depends(get_session),
    conn: Connection = Depends(get_db)
):

    device_response = await db_devices.select(conn, pk)
    if not device_response:
        return await error_400_with_detail("Device doesn't exist or was deleted")
    if device_response.user_id not in [session.user.id, session.user.parent_id]:
        raise UnauthenticatedException()

    if not is_device_id_valid(device.device_id):
        return await error_400_with_detail("Device_id is incorrect")
    if not is_device_config_valid(device.config):
        return await error_400_with_detail("Config is incorrect")

    result = await db_devices.update(conn, pk, device)
    return DeviceSuccessResponse(data=result)


@router.delete("/{radio_id}/devices/{pk}", response_model=DeviceSuccessResponse)
async def delete(
        radio_id: int,
        pk: int,
        session: Session = Depends(get_session),
        conn: Connection = Depends(get_db)
):
    device_response = await db_devices.select(conn, pk)
    if not device_response:
        return await error_400_with_detail("Device doesn't exist or was deleted")

    if device_response.user_id not in [session.user.id, session.user.parent_id]:
        raise UnauthenticatedException()

    result = await db_devices.delete(conn, pk)
    return DeviceSuccessResponse(data=result)


@router.post("/{radio_id}/devices/{pk}/upgrade")
async def upgrade(
        radio_id: int,
        pk: int,
        session: Session = Depends(get_session),
        conn: Connection = Depends(get_db)
):
    pass


def is_device_id_valid(device_id: str) -> bool:
    if match(r"([0-9A-F]{2}:){7}[0-9A-F]{2}", device_id) and len(device_id) == 23:
        return True
    return False


def is_device_config_valid(config: DeviceConfig) -> bool:
    if config == DeviceConfig():
        return True

    config_limits= {
        "output_css": (0, 255),
        "output_audio": (0, 255),
        "output_audio_l": (0, 255),
        "output_audio_r": (0, 255),
        "output_rds": (0, 255),
        "output_audio_l_r": (0, 255),
        "output_pilot": (0, 255),
        "switch_type":  (0, 2),
        "switch_interval": (1, 65535),
        "switch_count": (1, 255),
        "switch_return": (1, 65535)
    }
    config = config.dict()
    for param in config.keys():
        if not config_limits[param][0] <= config[param] <= config_limits[param][1]:
            return False
    return True
