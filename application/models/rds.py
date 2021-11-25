import enum
from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import (
    BaseModel,
    Field
)
from .base import (
    SuccessResponse
)


class PtyType(str, enum.Enum):
    UNDEFINED = "undefined"
    NEWS = "news"
    AFFAIRS = "affairs"
    INFO = "info"
    SPORT = "sport"
    EDUCATION = "education"
    DRAMA = "drama"
    CULTURE = "culture"
    SCIENCE = "science"
    VARIED = "varied"
    POP = "pop"
    ROCK = "rock"
    EASY = "easy"
    LCLASSIC = "lclassic"
    SCLASSIC = "sclassic"
    OTHER = "other"
    WEATHER = "weather"
    FINANCE = "finance"
    CHILD = "child"
    SOCIAL = "social"
    RELIGION = "religion"
    PHONEIN = "phonein"
    TRAVEL = "travel"
    HOBBY = "hobby"
    JAZZ = "jazz"
    COUNTRY = "country"
    NATIONAL = "national"
    OLDIES = "oldies"
    FOLK = "folk"
    DOCUMENTARY = "documentary"
    ALARM_TEST = "alarm_test"
    ALARM = "alarm"


class RdsType(str, enum.Enum):
    ANIMATE_PS = "animate_ps"
    SIMPLE = "simple"


class AnimationType(str, enum.Enum):
    LEFT_RIGHT = "left-right"
    LINE = "line"
    BY_WORD = "by_word"


class AnimationConf(BaseModel):
    type: AnimationType
    interval: int
    anim_construct: List[str]


class Rds(BaseModel):
    city: str = 'Moscow'
    pi: str = '0'
    pty: PtyType = PtyType.POP
    bf: float = 87.5
    af: List[float] = []
    ps: str = 'CRAFTRAD'
    rt: str = 'Craftradio here'
    ptyn: str = 'Testing'
    type: RdsType = RdsType.SIMPLE
    animate_ps: Optional[dict] = {}


class RdsSuccessResponse(SuccessResponse):
    data: Rds

