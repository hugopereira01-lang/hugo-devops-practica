from typing import List, Optional, Dict
from models.Producto import Producto, ProductoElectronico, ProductoRopa, ProductoCreate
from models.Usuario import Usuario, Cliente, Administrador, UsuarioCreate
from models.Pedido import Pedido, LineaPedido, PedidoCreate
 
class TiendaService:
    def __init__(self):
        self.usuarios: dict[int, Usuario] = {}
        self.productos: dict[int, Producto] = {}
        self.pedidos: dict[int, Pedido] = {}
        
        self._next_usuario_id = 1
        self._next_producto_id = 1
        self._next_pedido_id = 1
 
    
    # GESTIÓN DE USUARIOS
    def crear_usuario(self, datos: UsuarioCreate) -> Usuario:
        if any(u.email == datos.email for u in self.usuarios.values()):
            raise ValueError("Ya existe un usuario registrado con este correo electrónico.")
 
        usr_id = self._next_usuario_id
        if datos.tipo == "administrador":
            usuario = Administrador(id_usr=usr_id, nombre=datos.nombre, email=datos.email)
        else:
            if not datos.direccion_postal:
                raise ValueError("La dirección postal es obligatoria para los clientes.")
            usuario = Cliente(id_usr=usr_id, nombre=datos.nombre, email=datos.email, direccion_postal=datos.direccion_postal)
 
        self.usuarios[usr_id] = usuario
        self._next_usuario_id += 1
        return usuario
 
    def obtener_usuario(self, usuario_id: int) -> Optional[Usuario]:
        return self.usuarios.get(usuario_id)
 
    def listar_usuarios(self) -> List[Usuario]:
        return list(self.usuarios.values())
 
    
    # GESTIÓN DE PRODUCTOS
    def crear_producto(self, datos: ProductoCreate) -> Producto:
        prod_id = self._next_producto_id
        
        if datos.tipo == "electronico":
            if datos.meses_garantia is None:
                raise ValueError("Se requiere 'meses_garantia' para productos electrónicos.")
            producto = ProductoElectronico(
                id_prod=prod_id,
                nombre=datos.nombre,
                precio=datos.precio,
                stock=datos.stock,
                meses_garantia=datos.meses_garantia
            )
        elif datos.tipo == "ropa":
            if not datos.talla or not datos.color:
                raise ValueError("Se requieren 'talla' y 'color' para productos de ropa.")
            producto = ProductoRopa(
                id_prod=prod_id,
                nombre=datos.nombre,
                precio=datos.precio,
                stock=datos.stock,
                talla=datos.talla,
                color=datos.color
            )
        else:
            producto = Producto(
                id_prod=prod_id,
                nombre=datos.nombre,
                precio=datos.precio,
                stock=datos.stock
            )
 
        self.productos[prod_id] = producto
        self._next_producto_id += 1
        return producto
 
    def obtener_producto(self, producto_id: int) -> Optional[Producto]:
        return self.productos.get(producto_id)
 
    def listar_productos(self) -> List[Producto]:
        return list(self.productos.values())
 
    def eliminar_producto(self, producto_id: int) -> bool:
        if producto_id in self.productos:
            del self.productos[producto_id]
            return True
        return False
 
   
    # GESTIÓN DE PEDIDOS
    def crear_pedido(self, datos: PedidoCreate) -> Pedido:
        # 1. Verificar cliente
        cliente = self.obtener_usuario(datos.cliente_id)
        if not cliente:
            raise ValueError(f"El cliente con ID {datos.cliente_id} no existe.")
        if cliente.es_admin:
            raise ValueError("Los administradores no pueden realizar pedidos.")
 
        if not datos.items:
            raise ValueError("El pedido debe contener al menos un producto.")
 
        # Agrupar cantidades por producto (un mismo producto puede repetirse en varias líneas)
        cantidades: Dict[int, int] = {}
        for item_in in datos.items:
            cantidades[item_in.producto_id] = cantidades.get(item_in.producto_id, 0) + item_in.cantidad
 
        # Verificar existencia y stock de productos con la cantidad total solicitada
        items_pedido = []
        for producto_id, cantidad in cantidades.items():
            producto = self.obtener_producto(producto_id)
            if not producto:
                raise ValueError(f"El producto con ID {producto_id} no existe.")
            if producto.stock < cantidad:
                raise ValueError(f"Stock insuficiente para '{producto.nombre}'. Disponible: {producto.stock}, Solicitado: {cantidad}")
 
            items_pedido.append((producto, cantidad))
 
        #Descontar stock y crear pedido
        lineas_pedido = []
        for producto, cantidad in items_pedido:
            producto.stock -= cantidad
            lineas_pedido.append(LineaPedido(producto=producto, cantidad=cantidad))
 
        pedido_id = self._next_pedido_id
        pedido = Pedido(id_pedido=pedido_id, cliente_id=datos.cliente_id, items=lineas_pedido)
        
        self.pedidos[pedido_id] = pedido
        self._next_pedido_id += 1
        return pedido
 
    def obtener_pedidos_cliente(self, cliente_id: int) -> List[Pedido]:
        cliente = self.obtener_usuario(cliente_id)
        if not cliente:
            raise ValueError(f"El cliente con ID {cliente_id} no existe.")
        
        return [p for p in self.pedidos.values() if p.cliente_id == cliente_id]
 