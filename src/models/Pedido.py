from datetime import datetime
from typing import List
from pydantic import BaseModel, ConfigDict, Field
from models.Producto import Producto


class LineaPedido:
    def __init__(self, producto: Producto, cantidad: int):
        self.producto = producto
        self.cantidad = cantidad

    @property
    def subtotal(self) -> float:
        return self.producto.precio * self.cantidad


class Pedido:
    def __init__(self, id_pedido: int, cliente_id: int, items: List[LineaPedido]):
        self.id = id_pedido
        self.cliente_id = cliente_id
        self.items = items
        self.fecha = datetime.now()

    @property
    def total(self) -> float:
        return sum(item.subtotal for item in self.items)



# ESQUEMAS PYDANTIC

class PedidoItemCreate(BaseModel):
    producto_id: int
    cantidad: int = Field(gt=0, description="La cantidad debe ser mayor a 0")


class PedidoCreate(BaseModel):
    cliente_id: int
    items: List[PedidoItemCreate]


class PedidoItemRead(BaseModel):
    producto_id: int
    nombre_producto: str
    precio_unitario: float
    cantidad: int
    subtotal: float


class PedidoRead(BaseModel):
    id: int
    fecha: datetime
    cliente_id: int
    total: float
    items: List[PedidoItemRead]

    model_config = ConfigDict(from_attributes=True)
