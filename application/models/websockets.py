from enum import Enum
from typing import List

from pydantic import BaseModel, root_validator


class MsgEnum(tuple, Enum):
    op = ('sub', 'unsub')
    type = ('events', 'rds')


class InputMessage(BaseModel):
    """- Входящие сообщения"""
    op: str
    type: str
    radio_id: List[int]

    @root_validator
    def check_message(cls, values):
        op = values.get('op')
        ty = values.get('type')
        ids = values.get('radio_id')

        if op in MsgEnum.op and ty in MsgEnum.type and isinstance(ids, List):
            return values

        raise ValueError(values)
