

from datetime import datetime
from typing import Optional

from pydantic import ConfigDict, BaseModel,EmailStr


class PostBase(BaseModel):
    title:str
    content:str          ##Pydantic model:used for validation
    published:bool =False

class CreatePost(PostBase):
    pass

class PostResponse(BaseModel):
    id:int
    title:str
    content:str
    published:bool
    created_at:datetime

    model_config = ConfigDict(from_attributes=True)

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    model_config = ConfigDict(from_attributes=True)

class UserLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[int]=None