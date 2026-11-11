from typing import Literal, Optional
from pydantic import BaseModel, Field


class Producto:
    def __init__(self, id_prod: int, nombre: str, precio: float, stock: int):
        self.id = id_prod
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    def tipo(self) -> str:
        return "generico"


class ProductoElectronico(Producto):
    def __init__(self, id_prod: int, nombre: str, precio: float, stock: int, meses_garantia: int):
        super().__init__(id_prod, nombre, precio, stock)
        self.meses_garantia = meses_garantia

    def tipo(self) -> str:
        return "electronico"


class ProductoRopa(Producto):
    def __init__(self, id_prod: int, nombre: str, precio: float, stock: int, talla: str, color: str):
        super().__init__(id_prod, nombre, precio, stock)
        self.talla = talla
        self.color = color

    def tipo(self) -> str:
        return "ropa"



# ESQUEMAS PYDANTIC
class ProductoCreate(BaseModel):
    tipo: Literal["generico", "electronico", "ropa"]
    nombre: str
    precio: float = Field(gt=0, description="El precio debe ser mayor a 0")
    stock: int = Field(ge=0, description="El stock no puede ser negativo")
    meses_garantia: Optional[int] = Field(default=None, ge=0)
    talla: Optional[str] = None
    color: Optional[str] = None


class ProductoRead(BaseModel):
    id: int
    tipo: str
    nombre: str
    precio: float
    stock: int
    meses_garantia: Optional[int] = None
    talla: Optional[str] = None
    color: Optional[str] = None
