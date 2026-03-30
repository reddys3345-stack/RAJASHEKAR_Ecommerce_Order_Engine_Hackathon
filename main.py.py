from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import threading
import random

app = FastAPI()

products = {}
carts = {}
lock = threading.Lock()


class Product(BaseModel):
    id: str
    name: str
    price: int
    stock: int


class CartItem(BaseModel):
    user: str
    product_id: str
    quantity: int


class UpdateStock(BaseModel):
    product_id: str
    stock: int

@app.post("/add_product")
def add_product(p: Product):
    if p.id in products:
        raise HTTPException(status_code=400, detail="Product ID already exists")

    if p.stock < 0:
        raise HTTPException(status_code=400, detail="Stock cannot be negative")

    products[p.id] = {
        "name": p.name,
        "price": p.price,
        "stock": p.stock
    }

    return {"msg": "Product added successfully"}


@app.put("/update_stock")
def update_stock(data: UpdateStock):
    if data.product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")

    if data.stock < 0:
        raise HTTPException(status_code=400, detail="Stock cannot be negative")

    products[data.product_id]["stock"] = data.stock
    return {"msg": "Stock updated"}


@app.get("/products")
def view_products():
    return products


@app.post("/add_to_cart")
def add_to_cart(item: CartItem):
    if item.product_id not in products:
        raise HTTPException(status_code=404, detail="Product not found")

    if products[item.product_id]["stock"] < item.quantity:
        raise HTTPException(status_code=400, detail="Not enough stock")

    if item.user not in carts:
        carts[item.user] = {}

    carts[item.user][item.product_id] = carts[item.user].get(item.product_id, 0) + item.quantity

    return {"msg": "Added to cart"}


@app.delete("/remove_from_cart")
def remove_from_cart(user: str, product_id: str):
    if user not in carts or product_id not in carts[user]:
        raise HTTPException(status_code=404, detail="Item not in cart")

    del carts[user][product_id]
    return {"msg": "Removed from cart"}


@app.put("/update_cart")
def update_cart(item: CartItem):
    if item.user not in carts or item.product_id not in carts[item.user]:
        raise HTTPException(status_code=404, detail="Item not in cart")

    carts[item.user][item.product_id] = item.quantity
    return {"msg": "Cart updated"}


@app.get("/view_cart/{user}")
def view_cart(user: str):
    if user not in carts or not carts[user]:
        return {"msg": "Cart is empty"}

    result = []
    for pid, qty in carts[user].items():
        product = products[pid]
        result.append({
            "product": product["name"],
            "quantity": qty,
            "price": product["price"]
        })

    return result


@app.post("/place_order/{user}")
def place_order(user: str):
    if user not in carts or not carts[user]:
        raise HTTPException(status_code=400, detail="Cart is empty")

    lock.acquire()

    try:
        total = 0

        for pid, qty in carts[user].items():
            if products[pid]["stock"] < qty:
                raise HTTPException(status_code=400, detail="Stock conflict")

        
        if random.choice([True, False]):
            raise HTTPException(status_code=400, detail="Payment failed")

        
        for pid, qty in carts[user].items():
            products[pid]["stock"] -= qty
            total += products[pid]["price"] * qty

        carts[user] = {}

        return {"msg": "Order successful", "total": total}

    finally:
        lock.release()