# Assignment Task Management System

A full-stack Task Management System built using [Flask](https://flask.palletsprojects.com/?utm_source=chatgpt.com), [PostgreSQL](https://www.postgresql.org/?utm_source=chatgpt.com), WebSockets, Pandas, and NumPy.
This application allows users to register, log in securely, create and manage tasks, track completion status, and view analytics dashboards in real time.

Repository: [Assignment-Task-Management-System](https://github.com/iparigoel/Assignment-Task-Management-System?utm_source=chatgpt.com)

---

# Features

* User Authentication (Register/Login/Logout)
* Secure password hashing using Flask-Bcrypt
* Create, Edit, Delete Tasks
* Mark Tasks as Completed/Pending
* Task Priority Management
* Due Date Support
* Task Analytics Dashboard using Pandas & NumPy
* Real-Time Notifications using WebSockets (Flask-SocketIO)
* PostgreSQL Database Integration
* Session-based Authentication
* Flash Messages & Form Validation

---

# Tech Stack

## Backend

* Python
* Flask
* Flask-SQLAlchemy
* Flask-WTF
* Flask-Bcrypt
* Flask-SocketIO

## Database

* PostgreSQL

## Frontend

* HTML
* CSS
* Jinja2 Templates

## Data Analytics

* Pandas
* NumPy

---

# Project Structure

```bash
Assignment-Task-Management-System/
│
├── app.py
├── models.py
├── forms.py
├── requirements.txt
│
├── templates/
│   ├── layout.html
│   ├── home.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── task.html
│   ├── task_form.html
│   └── analytics.html
│
├── static/
│
└── README.md
```

---

# Installation

## 1. Clone Repository

```bash
git clone https://github.com/iparigoel/Assignment-Task-Management-System.git

cd Assignment-Task-Management-System
```


---

# 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 3. Configure PostgreSQL

Create a PostgreSQL database:

```sql
CREATE DATABASE flask_auth_db;
```

Update database URI inside `app.py`:

```python
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:YOUR_PASSWORD@localhost:5432/flask_auth_db'
```

---

# 4. Run Application

```bash
python app.py
```

Application will run on:

```bash
http://127.0.0.1:5000
```

---

# Real-Time WebSockets

This project uses [Flask-SocketIO](https://flask-socketio.readthedocs.io/en/latest/?utm_source=chatgpt.com) for real-time communication.

Implemented Features:

* Live task updates
* Real-time notifications
* Automatic UI refresh on task actions

Example events:

* Task Created
* Task Deleted
* Task Status Updated

---

# Analytics Dashboard

Using [Pandas](https://pandas.pydata.org/?utm_source=chatgpt.com) and [NumPy](https://numpy.org/?utm_source=chatgpt.com), the application displays:

* Total Tasks
* Completed Tasks
* Pending Tasks
* Completion Percentage

---

# Future Improvements

* Task Categories
* Email Notifications
* JWT Authentication
* REST API Support
* Drag & Drop Kanban Board
* Charts using Matplotlib/Chart.js
* Docker Deployment
* Role-Based Access Control

---

# Learning Outcomes

This project demonstrates:

* Full-stack Flask development
* Authentication & Authorization
* Database CRUD operations
* Real-time systems using WebSockets
* Data analysis with Pandas & NumPy
* PostgreSQL integration
* Template rendering with Jinja2

---

# Author

GitHub: [iparigoel](https://github.com/iparigoel?utm_source=chatgpt.com)

---

# License

This project is licensed under the MIT License.
