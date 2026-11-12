# hugo-devops-practica
**Autor:** Hugo Pereira López
**Asignatura:** Arquitectura del Software

## Descripción
API REST de una tienda online desarrollada con FastAPI en la Práctica 2.
Permite registrar usuarios (clientes y administradores), gestionar productos
(genéricos, electrónicos y ropa) y realizar pedidos con control de stock.
Los datos se guardan en memoria mientras la aplicación está en marcha.

En la Práctica 3.2 la API se ha contenerizado con Docker y la imagen está
publicada en Docker Hub.

## Estructura del proyecto
```
hugo-devops-practica/
├── src/
│   ├── main.py              # API FastAPI: endpoints
│   ├── models/              # Dominio y esquemas: Usuario, Producto, Pedido
│   └── services/
│       └── Tienda_service.py   # Lógica de negocio de la tienda
├── Dockerfile               # Receta de la imagen Docker
├── .dockerignore            # Lo que no entra en la imagen
├── requirements.txt         # Dependencias con versiones fijadas
├── .gitignore
└── README.md
```

## Requisitos
- Python 3.12 o superior (para ejecutar sin Docker)
- Docker Desktop (para ejecutar con Docker)
- Dependencias de `requirements.txt`: FastAPI, Uvicorn, Pydantic y email-validator

## Cómo ejecutar sin Docker
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python src/main.py
```
Después abre http://127.0.0.1:8000/docs para probar la API desde el navegador.

## Docker

### Imagen publicada
La imagen está en Docker Hub:
https://hub.docker.com/r/hugopereiraa/hugo-devops-practica

Etiquetas disponibles: `1.0.0` y `latest` (para `linux/amd64` y `linux/arm64`).

### 1. Construir la imagen
Desde la raíz del repositorio:
```bash
docker build -t hugo-devops-practica:1.0.0 .
```
Comprueba que aparece en la lista:
```bash
docker images hugo-devops-practica
```

### 2. Ejecutar el contenedor
```bash
docker run -d --name hugo-api -p 8000:8000 hugo-devops-practica:1.0.0
```
- `-d` lo deja en segundo plano.
- `--name hugo-api` le da un nombre fácil de recordar.
- `-p 8000:8000` conecta el puerto 8000 del ordenador con el del contenedor.

Otros ejemplos:
```bash
# Ver los logs del contenedor
docker logs hugo-api

# Usar otro puerto con la variable de entorno PORT
docker run -d --name hugo-api-9000 -e PORT=9000 -p 9000:9000 hugo-devops-practica:1.0.0

# Parar y borrar los contenedores
docker stop hugo-api hugo-api-9000
docker rm hugo-api hugo-api-9000
```

### 3. Descargar la imagen de Docker Hub (pull)
No hace falta clonar el repositorio:
```bash
docker pull hugopereiraa/hugo-devops-practica:1.0.0
docker run -d --name hugo-api -p 8000:8000 hugopereiraa/hugo-devops-practica:1.0.0
```

### 4. Publicar una nueva versión (push)
```bash
docker login
docker buildx build --platform linux/amd64,linux/arm64 \
  -t hugopereiraa/hugo-devops-practica:1.0.0 \
  -t hugopereiraa/hugo-devops-practica:latest \
  --push .
```

### Variables de entorno
| Variable | Valor por defecto | Para qué sirve |
|----------|-------------------|----------------|
| `PORT` | `8000` | Puerto en el que escucha Uvicorn dentro del contenedor |

La aplicación no usa contraseñas ni claves, así que no hay secretos que configurar.

### Salida esperada y pruebas
Al arrancar, `docker logs hugo-api` debe mostrar:
```
INFO:     Started server process [1]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```

Pruebas:
1. Abre http://localhost:8000/docs y verás la documentación Swagger con los
   apartados Usuarios, Productos y Pedidos.
2. O prueba desde la terminal:
```bash
# Crear un cliente -> 201
curl -X POST http://localhost:8000/usuarios \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Ana","email":"ana@example.com","tipo":"cliente","direccion_postal":"Calle Mayor 1"}'

# Crear un producto -> 201
curl -X POST http://localhost:8000/productos \
  -H "Content-Type: application/json" \
  -d '{"tipo":"generico","nombre":"Taza","precio":5.5,"stock":10}'

# Crear un pedido de 2 tazas -> 201, total 11.0
curl -X POST http://localhost:8000/pedidos \
  -H "Content-Type: application/json" \
  -d '{"cliente_id":1,"items":[{"producto_id":1,"cantidad":2}]}'

# Ver los productos: el stock de la taza ha bajado a 8
curl http://localhost:8000/productos
```
3. El contenedor no se ejecuta como root: `docker exec hugo-api whoami`
   devuelve `appuser`.

## Endpoints
| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | `/usuarios` | Registra un cliente o un administrador |
| GET | `/usuarios` | Lista los usuarios |
| GET | `/usuarios/{usuario_id}` | Obtiene un usuario |
| POST | `/productos` | Crea un producto (generico, electronico o ropa) |
| GET | `/productos` | Lista los productos |
| GET | `/productos/{producto_id}` | Obtiene un producto |
| DELETE | `/productos/{producto_id}` | Elimina un producto |
| POST | `/pedidos` | Crea un pedido y descuenta el stock |
| GET | `/usuarios/{cliente_id}/pedidos` | Pedidos de un cliente, por fecha |

## Flujo de trabajo con Git
- `main`: rama estable y protegida. Solo recibe cambios mediante Pull Request.
- `feature/`: una rama corta por cada tarea (`feature/docs`, `feature/docker`).
- Commits pequeños con prefijo: `feat:`, `docs:`, `chore:`, `fix:`.
