# Commerce

## 📘 Project Description

Commerce is an eBay-like e-commerce auction web application built as part of **CS50’s Web Programming with Python and JavaScript (CS50W)**. The project allows users to create auction listings, place bids, leave comments, manage a personal watchlist, and browse listings by category.

The application focuses on server-side web development using **Django**, emphasizing database modeling, user authentication, form handling, and dynamic page rendering.

---

## 🎯 Project Objectives

The primary goals of this project are to:

- Understand Django models and database relationships
- Implement user authentication and authorization
- Work with Django forms and server-side validation
- Manage relational data using the Django ORM
- Handle complex business logic such as bidding rules
- Build dynamic, user-driven web pages

---

## 🚀 Features

- User registration, login, and logout
- Create new auction listings with optional images and categories
- View all active auction listings on the homepage
- Place bids with validation rules enforced
- Add and remove listings from a personal watchlist
- Comment on auction listings
- Close auctions and determine winning bidders
- Browse listings by category
- Random and dynamic content rendering
- Admin interface for managing listings, bids, and comments

---

## 🛠️ Technologies Used

- Python  
- Django  
- HTML & CSS  
- SQLite  
- Django ORM  

---

## 📂 Project Structure

- `auctions/` – Main application containing models, views, URLs, and templates  
- `commerce/` – Django project configuration  
- `templates/` – HTML templates for rendering pages  
- `models.py` – Database models for listings, bids, comments, and categories  
- `views.py` – Application logic and request handling  
- `urls.py` – URL routing for the auctions app  
- `admin.py` – Admin interface configuration  
- `manage.py` – Django management utility  

---

## 🧠 Learning Outcomes

Through this project, I gained hands-on experience with:

- Designing relational database schemas
- Implementing bidding logic and constraints
- Using Django’s authentication system
- Managing many-to-many relationships (watchlists)
- Handling form submission and validation
- Building scalable and maintainable Django applications

---

## ▶️ Running the Project

1. Install dependencies:
   ```bash
   pip install django
2. Apply migrations:
   ```bash
   python manage.py makemigrations auctions
   python manage.py migrate
3. Run the development server:
   ```bash
   python manage.py runserver
4. Open your browser and visit:
   ```bash
   http://127.0.0.1:8000/


