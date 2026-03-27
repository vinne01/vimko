# 🚀 Vimko Inventory & Order Management System

---

## 📌 About the Project

**Vimko App** is a Django-based Inventory & Order Management System designed to handle real-world business operations like:

* Product management
* Inventory tracking
* Dealer management
* Order creation & processing

The system ensures **data consistency**, **stock validation**, and **smooth order lifecycle management**.

---

## 🎯 Objective

The goal of this project is to:

* Manage inventory efficiently
* Prevent invalid orders (negative / excess quantity)
* Handle complete order flow from **Draft → Confirmed → Delivered**
* Provide a simple UI using **Django Templates**

---

## 🖥️ Frontend

Frontend is built using:

* Django Templates
* Bootstrap
* HTML, CSS

👉 No React — fully server-rendered UI (beginner friendly + interview ready)

---

## 🛠️ How to Use This App

### 1️⃣ Add Dealer

* Go to Dealer section
* Create new dealer

### 2️⃣ Add Product

* Add product with price
* Inventory is managed separately

### 3️⃣ Manage Inventory

* Admin updates stock
* Stock cannot go negative

### 4️⃣ Create Order

* Select dealer
* Add multiple products
* Enter quantity

### 5️⃣ System Validations

* Prevents invalid quantity
* Prevents ordering more than stock

---

## 🖼️ Application Screenshots

### 🏠 Home Page

![Home](https://ik.imagekit.io/vinaymry/firstapppage.png)

### 📦 Product Page

![Product](https://ik.imagekit.io/vinaymry/oderpage.png)

### 👥 Dealer List

![Dealer]()

### ➕ Dealer Form

![Dealer Form](https://ik.imagekit.io/vinaymry/dealerpage.png)

### 📊 Inventory Page

![Inventory with admin login](https://ik.imagekit.io/vinaymry/inventorypagewithoutadmin.png)

### 🔐 Inventory (Admin Access)

![Inventory with Admin Login ](https://ik.imagekit.io/vinaymry/vinayycvw.png)

### 📑 Order List

![Order](https://ik.imagekit.io/vinaymry/orderpage.png)

### ➕ Order Form

![Order Form](https://ik.imagekit.io/vinaymry/orderedge1.png)

### 📄 Order Detail

![Order Detail](https://ik.imagekit.io/vinaymry/orderdetails.png)

---

## ⚠️ Edge Cases Handling

### ❌ 1. Zero Quantity

* Quantity = 0 not allowed
* Shows error message

![Zero Quantity](https://ik.imagekit.io/vinaymry/orderedge1.png)

---

### ❌ 2. Negative Quantity

* Negative values not allowed
* Validation error shown

![Negative Quantity](https://ik.imagekit.io/vinaymry/orderedge1.png)

---

### ❌ 3. Insufficient Stock

* If ordered quantity > available stock
* Error shown with available stock

![Insufficient Stock](https://ik.imagekit.io/vinaymry/orderedge2.png)

---

### ✅ 4. Successful Order Creation

* Order created successfully
* Inventory auto-updated

![Success](https://ik.imagekit.io/vinaymry/orderedge2.png)

---

## 🔄 Order Flow

```text
Draft → Confirmed → Delivered
```

* Draft: Initial state
* Confirmed: Stock validated
* Delivered: Final state

---

## 🔒 Validations Implemented

* Quantity must be greater than 0
* Cannot order more than available stock
* Inventory never goes negative
* Order items validated before saving

---

## 💡 Key Features

* Atomic transactions (safe DB operations)
* Real-time stock validation
* Clean UI with Bootstrap
* Fully functional CRUD system
* Handles all edge cases

---

## 📁 Project Structure

```
vimko_project/
│
├── core/
│   ├── models.py
│   ├── views.py
│   ├── templates/
│   ├── static/
│
├── manage.py
├── db.sqlite3
```

---

## 🛠️ Setup Instructions

```bash
git clone <your-repo-link>
cd vimko_project

pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate

python manage.py runserver
```

---

## 🚀 Future Improvements

* Add authentication (JWT/Login system)
* Add analytics dashboard
* Convert frontend to React
* Add role-based access

---

## 👨‍💻 Author

**Vinay Maurya**
