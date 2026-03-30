from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import threading
from datetime import datetime

app = FastAPI()

products = {}
carts = {}
orders = {}
logs = []
failure_mode = False
order_id = 1
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


def log(msg):
    logs.append(f"[{datetime.now()}] {msg}")

@app.post("/add_product")
def add_product(p: Product):
    if p.id in products:
        raise HTTPException(400, "Product exists")

    if p.stock < 0:
        raise HTTPException(400, "Invalid stock")

    products[p.id] = {"name": p.name, "price": p.price, "stock": p.stock}
    log(f"Product {p.id} added")
    return {"msg": "Added"}

@app.get("/products")
def view_products():
    return products


@app.post("/add_to_cart")
def add_to_cart(item: CartItem):
    lock.acquire()
    try:
        if item.product_id not in products:
            raise HTTPException(404, "Not found")

        if products[item.product_id]["stock"] < item.quantity:
            raise HTTPException(400, "Not enough stock")

        products[item.product_id]["stock"] -= item.quantity

        carts.setdefault(item.user, {})
        carts[item.user][item.product_id] = carts[item.user].get(item.product_id, 0) + item.quantity

        log(f"{item.user} added {item.product_id}")
        return {"msg": "Added to cart"}
    finally:
        lock.release()


@app.delete("/remove_from_cart")
def remove_from_cart(user: str, product_id: str):
    if user not in carts or product_id not in carts[user]:
        raise HTTPException(404, "Not in cart")

    qty = carts[user][product_id]
    products[product_id]["stock"] += qty
    del carts[user][product_id]

    return {"msg": "Removed"}


@app.get("/view_cart/{user}")
def view_cart(user: str):
    return carts.get(user, {})


@app.post("/place_order/{user}")
def place_order(user: str, coupon: str = ""):
    global order_id

    if user not in carts or not carts[user]:
        raise HTTPException(400, "Cart empty")

    lock.acquire()
    try:
        cart = carts[user]
        total = 0

        for pid, qty in cart.items():
            total += products[pid]["price"] * qty

        
        if total > 1000:
            total *= 0.9

        for qty in cart.values():
            if qty > 3:
                total *= 0.95

       
        if coupon == "SAVE10":
            total *= 0.9
        elif coupon == "FLAT200":
            total -= 200

        
        if failure_mode or random.choice([True, False]):
            for pid, qty in cart.items():
                products[pid]["stock"] += qty
            raise HTTPException(400, "Payment failed")

        oid = f"O{order_id}"
        order_id += 1

        orders[oid] = {
            "user": user,
            "items": cart.copy(),
            "total": total,
            "status": "PAID"
        }

        carts[user] = {}
        log(f"Order {oid} created")

        return {"order_id": oid, "total": total}

    finally:
        lock.release()


@app.post("/cancel_order/{order_id}")
def cancel_order(order_id: str):
    if order_id not in orders:
        raise HTTPException(404, "Not found")

    if orders[order_id]["status"] == "CANCELLED":
        raise HTTPException(400, "Already cancelled")

    for pid, qty in orders[order_id]["items"].items():
        products[pid]["stock"] += qty

    orders[order_id]["status"] = "CANCELLED"
    return {"msg": "Cancelled"}


@app.get("/orders")
def view_orders():
    return orders


@app.get("/low_stock")
def low_stock():
    return {k: v for k, v in products.items() if v["stock"] <= 5}



@app.post("/return_item")
def return_item(order_id: str, product_id: str, qty: int):
    if order_id not in orders:
        raise HTTPException(404, "Order not found")

    products[product_id]["stock"] += qty
    return {"msg": "Returned"}


@app.get("/simulate_concurrent")
def simulate_concurrent():
    def user1():
        add_to_cart(CartItem(user="A", product_id="1", quantity=1))

    def user2():
        add_to_cart(CartItem(user="B", product_id="1", quantity=1))

    t1 = threading.Thread(target=user1)
    t2 = threading.Thread(target=user2)

    t1.start()
    t2.start()
    t1.join()
    t2.join()

    return {"msg": "Concurrent simulation done"}

@app.get("/logs")
def view_logs():
    return logs

@app.post("/toggle_failure")
def toggle_failure():
    global failure_mode
    failure_mode = not failure_mode
    return {"failure_mode": failure_mode}
