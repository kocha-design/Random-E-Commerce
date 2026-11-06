# Random E-Commerce

A multi-vendor marketplace platform built with Django. Customers can browse and buy products, while sellers can list their products and manage their shops.

## Features

- **Guest Shopping** — Customers can browse products and contact sellers directly without signing up.
- **Seller Registration** — Sellers create accounts and manage their own shops.
- **Product Listings** — Sellers can add, edit, and delete products with images.
- **Search & Filter** — Search products, filter by category, and filter by price range.
- **Direct Contact** — Customers contact sellers via phone or WhatsApp.
- **Subscription Model** — Sellers pay a subscription fee to keep their shop active.
- **Admin Dashboard** — Manage sellers, verify payments, and monitor subscriptions.
- **Responsive Design** — Works on desktop, tablet, and mobile.

## Tech Stack

- **Backend:** Django 6.1
- **Database:** SQLite (development) / PostgreSQL (production)
- **Frontend:** HTML5, CSS3, JavaScript (no framework)
- **Image Handling:** Pillow
- **Environment Variables:** python-dotenv

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/kocha-design/Random-E-Commerce.git
cd Random-E-Commerce

2. Create and Activate a Virtual Environment
Windows:

bash
python -m venv venv
venv\Scripts\activate
Linux / macOS:

bash
python3 -m venv venv
source venv/bin/activate
3. Install Dependencies
bash
pip install -r requirements.txt
4. Configure Environment Variables
Copy .env.example to .env:

Windows:

bash
copy .env.example .env
Linux / macOS:

bash
cp .env.example .env
Generate a new SECRET_KEY:

bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
Open .env and paste the generated key into SECRET_KEY=....

5. Apply Migrations
bash
python manage.py migrate
6. Create a Superuser (Admin)
bash
python manage.py createsuperuser
7. (Optional) Seed Demo Data
bash
python seed_data.py
This creates demo categories, sellers, and products with images.

Demo seller credentials (password: test1234):

obligado → Obligado Shop

mama_asha → Mama Asha Mart

tech_hub → Tech Hub Tanzania

8. Run the Development Server
bash
python manage.py runserver
Open your browser and visit:

Home: http://127.0.0.1:8000/

Products: http://127.0.0.1:8000/products/

Admin: http://127.0.0.1:8000/admin/

Project Structure
text
Random-E-Commerce/
├── accounts/              # User, Seller, Payment models
├── products/              # Category, Product models
├── config/                # Django settings and URLs
├── templates/             # All HTML templates
│   ├── accounts/          # Login, register pages
│   ├── products/          # Product list, detail, dashboard
│   └── admin/             # Custom admin views
├── static/                # CSS, JS, images
│   ├── css/
│   ├── js/
│   └── img/
├── media/                 # User uploads (product images)
├── manage.py
├── seed_data.py           # Demo data script
├── requirements.txt
├── .env.example
└── .gitignore
Subscription Model
Sellers pay a monthly subscription fee to keep their shop active. The admin manually verifies M-Pesa payments through the Django admin panel.

Sellers with an active subscription can list products.

Sellers with an expired subscription or pending status cannot list products.

Admin can extend subscriptions or suspend sellers directly from the admin panel.

License
This project is licensed under the MIT License.

Contact
For questions or support:

Email: solutionrandomtech@gmail.com

WhatsApp: +255 679 918 293