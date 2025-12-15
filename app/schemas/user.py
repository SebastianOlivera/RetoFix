from pydantic import BaseModel


class UserCreate(BaseModel):
    nombre: str
    password: str
