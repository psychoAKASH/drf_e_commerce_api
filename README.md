# 🛒 E-commerce Backend API task

This is a backend API built with Django REST Framework and PostgreSQL (via Docker) for a simple e-commerce platform. It supports user authentication, product browsing, cart management, and order placement. It also includes performance optimization with Redis caching.

---

## 🚀 Features

- JWT Authentication (Register/Login with Token Refresh)
- Role-based access (Admin & Customer)
- Product Catalog with:
  - Filtering
  - Searching
  - Ordering
- Category Listing
- Cart Management (Add/Remove/View)
- Place Orders
- View Order History
- Update Order Status (Admin)
- Pagination on product/order list
- Redis Caching for product list
- Stock Management after orders
- User Profile API

---

## ⚙️ Technologies Used

- Django 4.x
- Django REST Framework
- PostgreSQL (via Docker)
- Redis (for caching)
- SimpleJWT (for authentication)
- Django Filters
- Docker & Docker Compose

---

## 🧩 Project Structure
```markdown
drf_e_commerce_api/
├── app/
    ├── accounts/ # User registration, login, profile
    ├── shop/ # Categories, Products
    ├── orders/ # Cart & Order logic
    ├── config/ # Project settings
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

## ⚡ Installation (Dockerized)

### 1. Clone the Repository

```bash
git clone https://github.com/psychoAKASH/drf_e_commerce_api.git
cd drf_e_commerce_api
```

### 2. Create .env file
```markdown
    POSTGRES_DB=ecommerce
    POSTGRES_USER=postgres
    POSTGRES_PASSWORD=postgres
    DB_HOST=db
    DB_PORT=5432
    SECRET_KEY=your-secret-key
    DEBUG=True
```
### 3. Build and run containers
```bash
docker-compose up --build
```

### 4. Run Migrations and Create Superuser
```bash
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py createsuperuser
```