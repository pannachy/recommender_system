from pydantic import BaseModel
from typing import List

'''
модели pydentic
'''

class PostGet(BaseModel):
    id: int
    text: str = ""
    topic: str = ""

    class Config:
        orm_mode = True

class Response(BaseModel):
    exp_group: str
    recommendations: List[PostGet]