from fastapi import APIRouter, Request, Depends
from misc.db import Connection
from misc.session import Session
from misc import db
from misc.session import Session


router = APIRouter(
    prefix='/users',
    tags=['users']
)


@router.get('/')
async def index(
    conn: Connection = Depends(), 
    session: Session = Depends()
) -> dict:
    result = await db.select_from_table(conn, "pg_stats")
    return result
