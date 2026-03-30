**E-Commerce Order Engine (FastAPI)**
**Overview**

This project is a simplified backend system for an e-commerce platform.
It simulates how real systems handle products, carts, and orders with multiple users.

The goal of this project was to understand core backend concepts like:

Inventory management
Order processing
Failure handling
Concurrency (multiple users accessing same data)

**Features Implemented**
Product management (add, view)
Multi-user cart system
Stock reservation while adding to cart
Order placement with payment simulation
Automatic rollback on failure
Order cancellation
Return/refund handling
Discount and coupon support
Low stock alerts
Logging system
Failure mode simulation
Concurrent user simulation

**Tech Stack**
Python
FastAPI
Uvicorn
Pydantic

**How to Run**
Install dependencies:
pip install -r requirements.txt
Run the server:
uvicorn main:app --reload

Open in browser:
http://127.0.0.1:8000/docs

**API Endpoints**
**Product**
POST /add_product
GET /products
GET /low_stock
**Cart**
POST /add_to_cart
DELETE /remove_from_cart
GET /view_cart/{user}
**Orders**
POST /place_order/{user}
POST /cancel_order/{order_id}
GET /orders
POST /return_item
**Others**
GET /logs
GET /simulate_concurrent
POST /toggle_failure

**Sample Flow**
Add products
Add items to cart
View cart
Place order (with or without coupon)
View orders
Cancel or return items

Note: Payment may fail randomly to simulate real-world scenarios.

**Design Approach**
Used in-memory dictionaries as database
Implemented locking for basic concurrency handling
Added failure simulation to test rollback
Designed APIs similar to real backend systems

**Assumptions**
Data is not persisted (resets on restart)
No authentication system
Single server simulation
