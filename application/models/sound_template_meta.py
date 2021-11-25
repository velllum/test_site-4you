
import math
from enum import Enum
from logging import root
from typing import Optional, List, Union

from pydantic import BaseModel, Field, validator
from pydantic.class_validators import root_validator

from misc.sound_templates.conversions import (
    gain_to_db,
    db_to_gain
)

class DataTypes(str, Enum):
    SET = "set"
    FLOAT = "float"
    BOOl = "bool"
    TIME_MS = "time_ms"
    DECIBELS = "dB"
    BOX = "box"
    PERCENT = "percent"


class Set(BaseModel):
    Uniform: int
    RMS: int
    Peak: int
    Low_Pass: int = Field(..., alias='Low-Pass')


class MetaItem(BaseModel):
    value: Optional[Union[bool, float, int]] = None
    type: DataTypes
    to_value: Optional[float] = None
    title: str
    step: Optional[float] = None
    name: str
    label: Optional[str] = None
    from_value: Optional[float] = None
    default: Optional[Union[bool, float, int]] = None
    set: Optional[Set] = None

    #define type cast and validation directly
    @root_validator()
    def validate_values(cls, values):
        return cast_values_types(values)


class MetaParam(BaseModel):
    value: Optional[Union[bool, float, int]] = None
    default: Optional[Union[bool, float, int]] = None
    type: DataTypes
    title: str
    name: Optional[str] = None
    to_value: Optional[float] = None
    step: Optional[float] = None
    label: Optional[str] = None
    from_value: Optional[float] = None
    mode: Optional[str] = None
    items: Optional[List[MetaItem]] = None
    group: Optional[str] = None
    space_after: Optional[bool] = None

    #define type cast and validation directly
    @root_validator()
    def validate_values(cls, values):
        return cast_values_types(values)


class MetaConfig(BaseModel):
    title: str
    plugin: str
    params: List[MetaParam]
    name: str
    enabled: bool
    defaults: str
    tabs: Optional[bool] = None


class MetaTemplate(BaseModel):
    preset: str
    gain_out: float
    config: List[MetaConfig]


def cast_values_types(values: dict) -> dict:
    if values["type"] == DataTypes.BOOl.value:
        values["value"] = bool(values["value"])
        values["default"] = bool(values["default"])
    elif values["type"] == DataTypes.FLOAT.value:
        values["value"] = float(values["value"])
        values["default"] = float(values["default"])
    elif values["type"] == DataTypes.DECIBELS.value:
        if values["value"] == values["default"]:
            values["value"] = float(values["value"])
            values["default"] = float(values["default"])
        else:
            values["value"] = gain_to_db(values["value"])
            values["default"] = float(values["default"])
    elif values["type"] == DataTypes.TIME_MS.value:
        ### Any convertions can be possible here
        values["value"] = float(values["value"])
        values["default"] = float(values["default"])
    elif values["type"] == DataTypes.SET.value:
        values["value"] = int(values["value"])
        values["default"] = int(values["default"])
    elif values["type"] == DataTypes.PERCENT.value:
        ### Any convertions can be possible here
        values["value"] = float(values["value"])
        values["default"] = float(values["default"])
    elif values["type"] == DataTypes.BOX.value:
        values["value"] = None
        values["default"] = None
    return values
