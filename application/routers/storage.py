from typing import Optional
import logging
import os
from fastapi.responses import JSONResponse
from fastapi import (
    Request, 
    Depends, 
    UploadFile, 
    File,
    Form,
    APIRouter
)
from misc.fastapi.depends.session import get as get_session
from misc.fastapi.depends.db import get as get_db
from misc.fastapi.depends.conf import get as get_conf
from misc.fastapi.depends.mqtt import get as get_mqtt
from misc.db import Connection as DbConnection
from misc.mqtt import Connection as MQTTConnection
from misc.session import Session
from misc.handlers import (
    error_400,
    error_401,
    error_404,
    error_400_with_detail,
    error_500,
    ok_204
)
from models.users import Anonymous
from models.storage import (
    Storage,
    StorageList,
    ItemUpdateExternal, 
    BaseItem,
    FolderAdd,
    StorageType,
    StorageStateType,
    FileProcessingType,
    StorageSuccessResponse,
    StorageListData,
    StorageListSuccessResponse
)
from db import (
    storage as db_storage,
    user_radios as db_user_radios
)
from misc.handlers import (
    UnauthenticatedException,
)
from misc.storage import add_secure_url


logger = logging.getLogger()


router = APIRouter(
    prefix='/storage',
    tags=['storage']
)


async def get_storage_item(
    item_id: int,
    conn: DbConnection = Depends(get_db), 
    session: Session = Depends(get_session),
    conf: dict = Depends(get_conf)
):

    if type(session.user) == Anonymous or not session.user.is_authenticated:
        raise UnauthenticatedException

    if item_id == 0:
        return None

    item = await db_storage.get_item(conn, item_id)
    if not item:
        return None
    
    item_owner_id = item.user_id

    if item_owner_id not in [session.user.id, session.user.parent_id]:
        raise UnauthenticatedException()

    return item


@router.get(
    "/items/{item_id}", 
    name="item",
    response_model=StorageSuccessResponse)
async def get_item(
    request: Request,
    item: Storage = Depends(get_storage_item),
    conf: dict = Depends(get_conf)
):
    """
    returns storage file data by item id if exists 
    else 404 not found exception
    """
    if not item:
        return await error_404()
        
    return StorageSuccessResponse(data=add_storage_secure_url(request, conf, item))


@router.get(
    "/items/{item_id}/list", 
    name="items",
    response_model=StorageListSuccessResponse)
async def get_items(
    request: Request,
    item_id: int,
    item: Storage = Depends(get_storage_item),
    conn: DbConnection = Depends(get_db), 
    session: Session = Depends(get_session),
    conf: dict = Depends(get_conf)
):
    """
    returns storage files data list by parent id
    """
    items = await db_storage.get_items(
        conn, 
        session.user.parent_id or session.user.id, 
        item.id if item else 0
    )

    return StorageListSuccessResponse(data=StorageListData(
            total=len(items),
            page=1,
            limit=len(items),
            items=[add_storage_secure_url(request, conf, item) for item in items]
        )
    )


@router.delete("/items/{item_id}", name="item_delete", response_model=StorageSuccessResponse)
async def delete_item(
    request: Request,
    item: Storage = Depends(get_storage_item),
    conn: DbConnection = Depends(get_db), 
    conf: dict = Depends(get_conf)
):
    """
    disable storage file data (en=False) by item_id
    """
    if not item:
        return await error_404()

    result = await db_storage.disable_item(conn, item.id)
    return StorageSuccessResponse(data=add_storage_secure_url(request, conf, result))


@router.post(
    "/items/{item_id}/folder", 
    name="add_folder",
    response_model=StorageSuccessResponse)
async def add_folder(
    request: Request,
    folder: FolderAdd,
    item_id: int,
    item: Storage = Depends(get_storage_item),
    conn: DbConnection = Depends(get_db), 
    session: Session = Depends(get_session),
    conf: dict = Depends(get_conf)
):
    """
    add folder to storage by parent id
    """
    if item and item.type == StorageType.FILE:
        return await error_400_with_detail("can not create folder, parent is file")

    name = folder.name

    folder_unique = await db_storage.is_unique(
        conn, 
        item.id if item else 0, 
        name,
        StorageType.FOLDER
    )

    if not folder_unique:
        logger.error(
            f"""folder name is not unique, parent_id {item.id if item else 0}, name: {name}"""
        )
        return await error_400_with_detail("folder is not unique")

    item = await db_storage.add_folder(
        conn, 
        name, 
        item.id if item else 0, 
        item.radio_id if item else None, 
        session.user.parent_id or session.user.id
    )
    return StorageSuccessResponse(data=add_storage_secure_url(request, conf, item))


@router.post(
    "/items/{item_id}/upload", 
    name="add_file",
    response_model=StorageSuccessResponse)
async def add_file(
    request: Request,
    item_id: int,
    audio_file: UploadFile = File(...),
    item: Storage = Depends(get_storage_item),
    conn: DbConnection = Depends(get_db), 
    session: Session = Depends(get_session),
    mqtt: MQTTConnection = Depends(get_mqtt),
    conf: dict = Depends(get_conf)
):
    """
    add file to storage by parent_id

    You can specify processing type by processing_type field \n
    Options: \n
        default - Aply timbre_mill and gstreamer processing and convert to mp3. Save origin. \n
        only_convert - Convert to mp3. \n
    
    Peculiarities:
        You can not create folder in root(0) pid, \n
        you need to use internal function or 
        create a new radio for that.

        You can not specify file parent_id, only folder parent_id is allowed. \n
    """
    if not item:
        return await error_400_with_detail("parent not found")
    
    if item.type == StorageType.FILE:
        return await error_400_with_detail("can not create file, parent is file")

    filename, ext = os.path.splitext(audio_file.filename)
    
    result = await db_storage.add_file(conn, filename, item.id, item.radio_id, session.user.id)
    
    temp_file_dir = db_storage.get_temp_dir(conf['storage'])
    target_file_dir = db_storage.get_target_dir(result.id, result.version, conf['storage'])
    status = await db_storage.handle_file(
        mqtt,
        ext,
        audio_file.file,
        result.id,
        temp_file_dir,
        target_file_dir,
        FileProcessingType.DEFAULT
    )
    if status != 0:
        return error_500("unable to handle file, try later")
    return StorageSuccessResponse(data=add_storage_secure_url(request, conf, result))


@router.post(
    "/items/{item_id}", 
    name="item_update",
    response_model=StorageSuccessResponse)
async def update_item(
    request: Request,
    body: ItemUpdateExternal,
    item: Storage = Depends(get_storage_item),
    conn: DbConnection = Depends(get_db),
    session: Session = Depends(get_session),
    conf: dict = Depends(get_conf)
):
    """
    update file data by id

    its possible to update either pid(change parent directory) or name

    WARNING:
        You can not change current pid to file pid.

    """
    if body.pid != item.pid:
        new_parent = await get_storage_item(body.pid, conn, session, conf)
        if new_parent.type == StorageType.FILE:
            return await error_400_with_detail("can not create file, parent is file")

    result = await db_storage.update(conn, item.id, body)
    return StorageSuccessResponse(data=add_storage_secure_url(request, conf, result))


def add_storage_secure_url(request: Request, conf: dict, item: Storage) -> Storage:
    return add_secure_url(request, conf, item)