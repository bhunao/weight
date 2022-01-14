from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class WeightBase(BaseModel):
    name: str
    weight: float


class WeightCreate(WeightBase):
    pass


class Weight(WeightBase):
    id: int
    date: datetime

    class Config:
        orm_mode = True
