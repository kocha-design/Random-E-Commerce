markdown
# Soko Letu

Multi-vendor marketplace platform built with Django.

## Features
- Customer and Seller registration
- Product listing with images
- Search, filter by category and price
- Subscription-based seller accounts
- Admin panel for managing sellers and payments
- Contact sellers via phone/WhatsApp

## Tech Stack
- Django 6.1
- SQLite (dev) / PostgreSQL (prod)
- HTML/CSS/JS (no framework)
- Pillow (image uploads)

## Setup

1. Clone this repo:
   ```bash
   git clone https://github.com/USERNAME/soko-letu.git
   cd soko-letu
Create virtual environment:

bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/macOS
Install dependencies:

bash
pip install -r requirements.txt
Copy .env.example to .env and fill in values:

bash
cp .env.example .env
Run migrations:

bash
python manage.py migrate
Create superuser:

bash
python manage.py createsuperuser
Run server:

bash
python manage.py runserver
