from enum import Enum
from pydantic import BaseModel, root_validator
from typing import Optional, Any, Dict
from datetime import datetime


class SoundProcessingPlugins(str, Enum):
    bass_enhancer = "calf-sourceforge-net-plugins-BassEnhancer"
    para_eq = "lsp-plug-in-plugins-lv2-para-equalizer-x16-stereo"
    mb_comp_ms = "lsp-plug-in-plugins-lv2-mb-compressor-ms"
    graph_eq = "lsp-plug-in-plugins-lv2-graph-equalizer-x16-stereo"
    limiter = "lsp-plug-in-plugins-lv2-limiter-stereo"

    @staticmethod
    def get_dict():
        return {i.name: i.value for i in SoundProcessingPlugins}


class SoundProcessingFilters(str, Enum):
    bass_enhancer = "00"
    para_eq = "01"
    mb_comp_ms = "02"
    graph_eq = "03"
    limiter = "04"


class BaseConfig(BaseModel):
    bass_enhancer: Dict[str, Any] # {str: Union[bool. int, float]}, 
    para_eq: Dict[str, Any]       # Any allow pydentic serialize from str correctly
    mb_comp_ms: Dict[str, Any]
    graph_eq: Dict[str, Any]
    limiter: Dict[str, Any]
            

class BaseConfigGain(BaseModel):
    config: Optional[BaseConfig] = {}
    gain_out: Optional[float] = None


class BaseTemplate(BaseModel):
    config: Optional[BaseConfig] = {}
    name: str
    en: bool


class BaseTemplateReturn(BaseTemplate):
    id: int
    ctime: Optional[datetime] = None
    atime: Optional[datetime] = None
    dtime: Optional[datetime] = None
