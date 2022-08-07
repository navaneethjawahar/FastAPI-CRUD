from typing import List, Optional

from pydantic import BaseModel

class StudentBase(BaseModel):
    class Config:
        orm_mode = True
    First_Name: str
    Last_Name: str
    Amount_Due : float
    DOB: Optional[str] = None
    id: int


class StudentCreate(BaseModel):
    class Config:
        orm_mode = True
    First_Name: str
    Last_Name: str
    Amount_Due : float
    DOB: Optional[str] = None


class Item(StudentBase):
    id: int