import uvicorn
from fastapi import FastAPI, HTTPException, status
from fastapi.responses import RedirectResponse
from typing import List

from models.Usuario import UsuarioCreate, UsuarioRead
from models.Producto import ProductoCreate, ProductoRead
from models.Pedido import PedidoCreate, PedidoRead, PedidoItemRead
from services.Tienda_service import TiendaService

app = FastAPI(
    title="Sistema de Gestión de Tienda",
    description="API para la gestión modular de Usuarios, Productos y Pedidos",
    version="1.0.0"
)


# Instancia global del servicio de la tienda
servicio = TiendaService()


# Redirigir a la documentación 
@app.get("/", include_in_schema=False)
def inicio():
    return RedirectResponse(url="/docs")


# ENDPOINTS DE USUARIOS 
@app.post("/usuarios", response_model=UsuarioRead, status_code=status.HTTP_201_CREATED, tags=["Usuarios"])
def crear_usuario(usuario_in: UsuarioCreate):
    """Crea un nuevo usuario (Cliente o Administrador)."""
    try:
        usuario = servicio.crear_usuario(usuario_in)
        return UsuarioRead(
            id=usuario.id,
            nombre=usuario.nombre,
            email=usuario.email,
            es_admin=usuario.es_admin
        )
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get("/usuarios/{usuario_id}", response_model=UsuarioRead, tags=["Usuarios"])
def obtener_usuario(usuario_id: int):
    """Devuelve la información de un usuario concreto por su ID."""
    usuario = servicio.obtener_usuario(usuario_id)
    if not usuario:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Usuario no encontrado")
    return UsuarioRead(
        id=usuario.id,
        nombre=usuario.nombre,
        email=usuario.email,
        es_admin=usuario.es_admin
    )


@app.get("/usuarios", response_model=List[UsuarioRead], tags=["Usuarios"])
def listar_usuarios():
    """Devuelve la lista completa de usuarios registrados."""
    usuarios = servicio.listar_usuarios()
    return [
        UsuarioRead(
            id=u.id,
            nombre=u.nombre,
            email=u.email,
            es_admin=u.es_admin
        ) for u in usuarios
    ]


# ENDPOINTS DE PRODUCTOS 
def _mapear_producto_a_read(producto) -> ProductoRead:
    return ProductoRead(
        id=producto.id,
        tipo=producto.tipo(),
        nombre=producto.nombre,
        precio=producto.precio,
        stock=producto.stock,
        meses_garantia=getattr(producto, 'meses_garantia', None),
        talla=getattr(producto, 'talla', None),
        color=getattr(producto, 'color', None)
    )


@app.post("/productos", response_model=ProductoRead, status_code=status.HTTP_201_CREATED, tags=["Productos"])
def crear_producto(producto_in: ProductoCreate):
    """Crea un nuevo producto (genérico, electrónico o ropa)."""
    try:
        producto = servicio.crear_producto(producto_in)
        return _mapear_producto_a_read(producto)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get("/productos", response_model=List[ProductoRead], tags=["Productos"])
def listar_productos():
    """Devuelve la lista completa de productos registrados."""
    productos = servicio.listar_productos()
    return [_mapear_producto_a_read(p) for p in productos]


@app.get("/productos/{producto_id}", response_model=ProductoRead, tags=["Productos"])
def obtener_producto(producto_id: int):
    """Devuelve un producto concreto por su ID."""
    producto = servicio.obtener_producto(producto_id)
    if not producto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return _mapear_producto_a_read(producto)


@app.delete("/productos/{producto_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Productos"])
def eliminar_producto(producto_id: int):
    """Elimina un producto del catálogo por su ID."""
    exito = servicio.eliminar_producto(producto_id)
    if not exito:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Producto no encontrado")
    return None


# ENDPOINTS DE PEDIDOS 
def _mapear_pedido_a_read(pedido) -> PedidoRead:
    items_read = [
        PedidoItemRead(
            producto_id=item.producto.id,
            nombre_producto=item.producto.nombre,
            precio_unitario=item.producto.precio,
            cantidad=item.cantidad,
            subtotal=item.subtotal
        ) for item in pedido.items
    ]
    return PedidoRead(
        id=pedido.id,
        fecha=pedido.fecha,
        cliente_id=pedido.cliente_id,
        total=pedido.total,
        items=items_read
    )


@app.post("/pedidos", response_model=PedidoRead, status_code=status.HTTP_201_CREATED, tags=["Pedidos"])
def crear_pedido(pedido_in: PedidoCreate):
    """Crea un nuevo pedido verificando existencia de cliente, producto y stock."""
    try:
        pedido = servicio.crear_pedido(pedido_in)
        return _mapear_pedido_a_read(pedido)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.get("/usuarios/{cliente_id}/pedidos", response_model=List[PedidoRead], tags=["Pedidos"])
def obtener_pedidos_cliente(cliente_id: int):
    """Devuelve el historial de pedidos de un cliente específico."""
    try:
        pedidos = servicio.obtener_pedidos_cliente(cliente_id)
        return [_mapear_pedido_a_read(p) for p in pedidos]
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


# Iniciar la API con el botón VSC 
if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
