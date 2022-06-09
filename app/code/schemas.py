#This is where we will link the data from SQL to Python

from typing import Union
from pydantic import BaseModel


class PlayerBase(BaseModel):
    name: str

class PlayerCreate(PlayerBase):
    gold: int

class Player(PlayerBase):
    id: int
    name: str
    gold: int

    class Config:
        orm_mode = True
