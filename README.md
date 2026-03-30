**E-Commerce Order Engine (FastAPI)**

**Project Overview**
This project is a simple backend system that simulates an e-commerce order engine.
It allows users to add products, manage carts, and place orders.
The main idea behind this project is to understand how real-world systems handle:
Multiple users
Inventory management
Order processing
Basic failure handling

**Features**
Add and update products
View available products
Add items to cart (user-wise)
Update and remove cart items
Place orders
Handles stock validation
Simulates payment failures
Prevents inconsistent data using locking

**Tech Stack**
Python
FastAPI
Uvicorn
Pydantic


**How to Run**
Install dependencies:
pip install fastapi uvicorn
Run the server:
uvicorn Supermarket:app --reload
Open browser:
http://127.0.0.1:8000/docs


**API Endpoints**
**Product APIs**
POST /add_product → Add new product
PUT /update_stock → Update product stock
GET /products → View all products
**Cart APIs**
POST /add_to_cart → Add item to cart
PUT /update_cart → Update quantity
DELETE /remove_from_cart → Remove item
GET /view_cart/{user} → View user cart
**Order API**
POST /place_order/{user} → Place order

**Sample Flow**
Add products
Add items to cart
View cart
Place order
Sometimes order may fail due to simulated payment failure.

**Design Notes**
Data is stored using in-memory dictionaries
Each user has a separate cart
Lock is used to avoid stock conflicts during order placement
Random module is used to simulate real-world failures

**Limitations**
No database (data will reset on restart)
No authentication system
Basic validation only

**Future Improvements**
Add database (MySQL / PostgreSQL)
User authentication (JWT)
Order history
Frontend integration
