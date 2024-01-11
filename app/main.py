"""
Este módulo contiene las rutas y funciones para el manejo de items en la aplicación FastAPI.
"""

import os
from typing import List, Union, Annotated
from fastapi import Depends, FastAPI, HTTPException, status, Body, Cookie, Form, File, UploadFile
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.security import APIKeyHeader
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

API_KEY_NAME= "X-API-KEY"
API_KEY = "tu_apy_key_secreta"

app = FastAPI()
app.mount("/static", StaticFiles(directory="./app/static"), name="static")
api_key_header = APIKeyHeader(name=API_KEY_NAME,auto_error=False)

def get_api_key(api_key: str = Depends(api_key_header)):
    if api_key == API_KEY:  # Usar '==' en lugar de '=' para comparar
        return api_key
    else:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acceso no autorizado"
        )

# Modelos
class Product(BaseModel):
    id: int
    name: str
    price: float
    in_stock: bool

class User(BaseModel):
    id: int
    name: str
    email: str

class Order(BaseModel):
    id: int
    user_id: int
    products: List[Product]
    total_price: float
    
class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None


# Datos de ejemplo
products = [
    Product(id=1, name="Laptop", price=1000.0, in_stock=True),
    Product(id=2, name="Smartphone", price=500.0, in_stock=True),
]

users = [
    User(id=1, name="John Doe", email="john@example.com"),
]

orders = []
# templates = Jinja2Templates(directory="templates")

def get_next_order_id():
    return max([order.id for order in orders], default=0) + 1

@app.get("/")
async def read_root():
    return {"Hello": "World And Aliens"}

@app.get('/favicon.ico')
async def favicon():
    file_name = "favicon.ico"
    file_path = os.path.join(app.root_path, "app/static", file_name)
    return FileResponse(path=file_path, headers={"Content-Disposition": "attachment; filename=" + file_name})

@app.get("/items/{item_id}")
async def read_item(item_id: int, q: Union[str, None] = None,):
    return {"item_id": item_id, "q": q}


# Rutas
@app.get("/products", dependencies=[Depends(get_api_key)])
def get_products():
    return products

@app.post("/products", dependencies=[Depends(get_api_key)])
def add_product(product: Product):
    # Verificar si el producto ya existe por ID
    for p in products:
        if p.id == product.id:
            raise HTTPException(status_code=400, detail="El producto ya existe")

    products.append(product)
    return product

@app.put("/products/{product_id}", dependencies=[Depends(get_api_key)])
def update_product(product_id: int, product: Product):
    for idx, p in enumerate(products):
        if p.id == product_id:
            products[idx] = product
            return product
    return {"error": "Producto no encontrado"}

@app.delete("/products/{product_id}", dependencies=[Depends(get_api_key)])
def delete_product(product_id: int):
    for idx, p in enumerate(products):
        if p.id == product_id:
            del products[idx]
            return {"message": "Producto eliminado"}
    return {"error": "Producto no encontrado"}

@app.post("/users")
def create_user(user: User):
    users.append(user)
    return user

@app.put("/users/{user_id}")
def update_user(user_id: int, user: User):
    for idx, u in enumerate(users):
        if u.id == user_id:
            users[idx] = user
            return user
    return {"error": "Usuario no encontrado"}

@app.delete("/users/{user_id}")
def delete_user(user_id: int):
    for idx, u in enumerate(users):
        if u.id == user_id:
            del users[idx]
            return {"message": "Usuario eliminado"}
    return {"error": "Usuario no encontrado"}


# TAREA

@app.get("/ordenes/", response_model=List[Order])  # Cambio de Producto a Order
async def get_ordenes():
    return orders  # Cambio de productos a orders

@app.post("/ordenes/", response_model=Order)  # Cambio de Producto a Order
async def create_orden(order: Order):  # Cambio de producto a order
    orders.append(order)  # Cambio de productos a orders
    return order

@app.put("/ordenes/{orden_id}/", response_model=Order)  # Cambio de Producto a Order
async def update_orden(orden_id: int, order: Order):  # Cambio de producto a order
    for o in orders:  # Cambio de productos a orders
        if o.id == orden_id:
            o.user_id = order.user_id
            o.products = order.products
            o.total_price = order.total_price
            return o
    raise HTTPException(status_code=404, detail="Orden no encontrada")  # Cambio de Producto a Order

@app.delete("/ordenes/{orden_id}/", response_model=Order)  # Cambio de Producto a Order
async def delete_orden(orden_id: int):  # Cambio de producto a order
    for index, o in enumerate(orders):  # Cambio de productos a orders
        if o.id == orden_id:
            del orders[index]  # Cambio de productos a orders
            return o
    raise HTTPException(status_code=404, detail="Orden no encontrada")

@app.put("/items/{item_id}")
async def update_item(
    *,
    item_id: int,
    item: Annotated[
        Item,
        Body(
            openapi_examples={
                "normal": {
                    "summary": "A normal example",
                    "description": "A **normal** item works correctly.",
                    "value": {
                        "name": "Foo",
                        "description": "A very nice Item",
                        "price": 35.4,
                        "tax": 3.2,
                    },
                },
                "converted": {
                    "summary": "An example with converted data",
                    "description": "FastAPI can convert price `strings` to actual `numbers` automatically",
                    "value": {
                        "name": "Bar",
                        "price": "35.4",
                    },
                },
                "invalid": {
                    "summary": "Invalid data is rejected with an error",
                    "value": {
                        "name": "Baz",
                        "price": "thirty five point four",
                    },
                },
            },
        ),
    ],
):
    results = {"item_id": item_id, "item": item}
    return results

@app.get("/itemscookies/")
async def read_items(ads_id: Annotated[str | None, Cookie()] = None):
    return {"ads_id": ads_id}

@app.post("/login/")
async def login(username: Annotated[str, Form()], password: Annotated[str, Form()]):
    return {"username": username}

@app.post("/files/")
async def create_file(file: Annotated[bytes | None, File()] = None):
    if not file:
        return {"message": "No file sent"}
    else:
        return {"file_size": len(file)}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile | None = None):
    if not file:
        return {"message": "No upload file sent"}
    else:
        return {"filename": file.filename}