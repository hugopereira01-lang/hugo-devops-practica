from typing import Literal, Optional
from pydantic import BaseModel, EmailStr


class Usuario:
    def __init__(self, id_usr: int, nombre: str, email: str):
        self.id = id_usr
        self.nombre = nombre
        self.email = email

    @property
    def es_admin(self) -> bool:
        return False


class Cliente(Usuario):
    def __init__(self, id_usr: int, nombre: str, email: str, direccion_postal: str):
        super().__init__(id_usr, nombre, email)
        self.direccion_postal = direccion_postal


class Administrador(Usuario):
    def __init__(self, id_usr: int, nombre: str, email: str):
        super().__init__(id_usr, nombre, email)

    @property
    def es_admin(self) -> bool:
        return True


# ESQUEMAS PYDANTIC

class UsuarioCreate(BaseModel):
    nombre: str
    email: EmailStr
    tipo: Literal["cliente", "administrador"]
    direccion_postal: Optional[str] = None


class UsuarioRead(BaseModel):
    id: int
    nombre: str
    email: str
    es_admin: bool