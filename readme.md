# 🛒 Commerce – CS50 Web Project

## 🚀 Overview

**Commerce** is a full-stack e-commerce auction platform built as part of Harvard’s **CS50 Web Programming with Python and JavaScript** course.

The application allows users to create listings, place bids, comment, manage watchlists, and browse items by categories. This project demonstrates my ability to build a **data-driven web application**, design **relational models**, and implement **interactive user flows** using Django and JavaScript.

---

## 🎯 Key Features

* 🏷️ **Create Listings**

  * Users can create auction listings with title, description, price, image, and category

* 💰 **Bidding System**

  * Real-time bid validation (must be higher than current price)
  * Tracks highest bidder and updates listing dynamically

* ⭐ **Watchlist**

  * Users can save and manage listings of interest

* 💬 **Comments System**

  * Add and display comments per listing

* 📂 **Categories**

  * Filter listings by category

* 🔒 **Authentication System**

  * Register, login, logout with Django authentication

* 🧾 **Listing Status**

  * Close auctions and determine winners

---

## 🧠 What This Project Demonstrates

### 1. Backend Engineering (Django)

* Relational database modeling (Users, Listings, Bids, Comments)
* Business logic implementation (bid validation, auction closing)
* Django ORM for efficient data handling
* Form handling and validation

### 2. Full-Stack Integration

* Rendering dynamic content using Django templates
* Handling POST/GET requests
* Synchronizing frontend state with backend logic

### 3. Application Logic & Data Integrity

* Enforcing bid rules (no invalid bids)
* Managing relationships between models
* Ensuring consistent auction state

### 4. User-Centered Design

* Clear workflows (browse → bid → win)
* Organized UI structure
* Feedback messages for user actions

---

## 🛠️ Tech Stack

* **Backend:** Python, Django
* **Frontend:** HTML, CSS
* **Database:** SQLite (default, easily replaceable)
* **Architecture:** MVT (Model-View-Template)

---

## 🧩 Project Structure

```bash
commerce/
│
├── auctions/
│   ├── models.py        # Data models (Listings, Bids, Comments, Users)
│   ├── views.py         # Core application logic
│   ├── forms.py         # Django forms
│   ├── templates/       # HTML templates
│
├── db.sqlite3           # Database (development)
├── manage.py
```

---

## ⚙️ How to Run

1. Clone the repository:

```bash
git clone https://github.com/LeodanyPM/Commerce--CS50--Project.git
cd Commerce--CS50--Project
```

2. Install dependencies:

```bash
pip install django
```

3. Run migrations:

```bash
python manage.py migrate
```

4. Start the server:

```bash
python manage.py runserver
```

5. Open in browser:

```
http://127.0.0.1:8000
```

---



## 💡 Design Decisions

* **Django ORM for Data Integrity**
  Ensures relationships between bids, users, and listings are consistent and secure.

* **Server-Side Rendering**
  Chosen to prioritize simplicity, reliability, and clarity of logic.

* **Separation of Concerns**
  Models handle data, views handle logic, templates handle presentation.

* **Validation at Backend Level**
  Prevents invalid bids regardless of frontend behavior.

---

## 📈 Potential Improvements

* Convert to REST API + React frontend (SPA)
* Add real-time bidding (WebSockets)
* Implement pagination and search
* Improve UI/UX design (modern styling framework)
* Add payment simulation or checkout system

---

## 👤 About Me

I am currently focused on developing strong skills in **full-stack web development** through CS50 and personal projects.

This project reflects my ability to:

* Build complete applications from scratch
* Work with relational data models
* Implement real-world business logic
* Write clean and maintainable code

---

## ⚠️ Disclaimer for CS50 Students

This repository is shared **for educational and portfolio purposes only**.

If you are currently enrolled in **CS50 Web**, you must **not copy or submit this code as your own work**. Doing so would violate the course’s academic honesty policy.

You are encouraged to:

* Use this project only as a reference after completing your own solution
* Learn from the structure and logic
* Build your own independent implementation

---



