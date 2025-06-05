
<p align="center">
  <img src="https://img.icons8.com/color/96/000000/dumbbell.png" alt="Fitness Booking API" />
</p>

<h1 align="center"> Fitness Booking API</h1>

<p align="center">
  A RESTful API built with Django for managing fitness class registrations and bookings.
</p>

<p align="center">
  <a href="#"><img src="https://img.shields.io/badge/Python-3.10-blue?style=flat-square&logo=python"></a>
  <a href="#"><img src="https://img.shields.io/badge/Django-REST_Framework-green?style=flat-square&logo=django"></a>
  <a href="#"><img src="https://img.shields.io/badge/License-MIT-lightgrey?style=flat-square"></a>
</p>

---

## Table of Contents

- [Abstract](#-abstract)
- [Proposed System](#-proposed-system)
- [Advantages](#-advantages)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Installation](#-installation)
- [API Endpoints](#-api-endpoints)
- [Database Models](#-database-models)
- [Future Improvements](#-future-improvements)

---

##  Abstract

This project is a Django REST Framework-based API for managing fitness class bookings. It allows users to register, log in using JWT authentication, view available fitness classes, and book slots securely. The system handles user validation, slot availability, and stores booking details efficiently. Designed for seamless integration with frontend applications, it provides essential endpoints to support user-friendly fitness management solutions.

---

##  Proposed System

The proposed system offers a centralized API for managing user registrations, class scheduling, and slot bookings in fitness centers. It ensures real-time availability tracking and secure user authentication using JWT.

---

##  Advantages

-  Efficient slot management with automatic availability updates
-  Secure user authentication with hashed passwords and JWT tokens
-  Easy integration with frontend or mobile applications
-  Supports user-specific booking history retrieval
-  Scalable and maintainable RESTful architecture

---

##  Features

- [x] View all available fitness classes
- [x] Book slots in classes (automatically handles availability)
- [x] Fetch booking history by user email
- [x] Admin management via Django Admin Panel
- [x] User registration with email/phone validation
- [x] JWT-based authentication and login

---

##  Tech Stack

| Tool / Library           | Description                                  |
|--------------------------|----------------------------------------------|
|  Python                  | Programming Language                         |
|  Django                  | Backend Web Framework                        |
|  Django REST Framework   | API Development                              |
|  JWT (SimpleJWT)         | Authentication Mechanism                     |
|  SQLite3                 | Default Database (can upgrade to PostgreSQL) |
|  django-cors-headers     | Cross-Origin Resource Sharing (CORS)         |

---

##  Installation

### 1. Clone the Repository
```bash
git clone https://github.com/mithun-k04/Fitness-Application-Omnify.git
cd Fitness-Application-Omnify

 - 2. Create & Activate Virtual Environment
```bash
Copy
Edit
python -m venv env
source env/bin/activate  

- 3. Install Dependencies
```bash
Copy
Edit
pip install -r requirements.txt

- 4. Apply Migrations
```bash
Copy
Edit
python manage.py makemigrations
python manage.py migrate

- 5. Run the Server
```bash
Copy
Edit
python manage.py runserver

---

## API Endpoints
Method	Endpoint	Description
- GET	/api/availableclasses/	Fetch classes with available slots
- POST	/api/slotbooking/	Book a slot in a class
- GET	/api/bookings/<user_email>/	Get all bookings for a user
- POST	/api/userregistration/	Register a new user
- POST	/api/userlogin/	Login and receive JWT token
- CRUD	/api/users/	Manage users (admin/dev use)
- CRUD	/api/classes/	Manage fitness classes (admin/dev use)

---

## Database Models
## User
- Field	Type	Description
- username	Char	User's name
- email	Email	Must be unique
- phone	Char	Must be unique
- password	Char	Hashed password

## FitnessClass
- Field	Type	Description
- name	Char	Class name
- date_time	DateTime	Scheduled date & time
- instructor	Char	Instructor's name
- description	Text	Class details
- total_slots	Integer	Total capacity
- available_slots	Integer	Slots left to book

## Booking
- Field	Type	Description
- fitness_class	FK	Linked to FitnessClass
- client_name	Char	Name of the booking user
- client_email	Email	Used to fetch user bookings
- client_phone	Char	Contact info
- slot	Integer	Slot number assigned
- booked_at	DateTime	Timestamp of the booking

---

## Future Improvements
- Filtering and search options for class listings
- Email notifications on successful bookings
- User dashboard for managing bookings
- Class cancellation and rescheduling support
- Password reset and update functionality

---