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
---

## 📬 API Endpoints (Examples)

| Endpoint              | Method          | Description                 |
| --------------------- | --------------- | --------------------------- |
| `/api/register/`      | POST            | Register new user           |
| `/api/token/`         | POST            | Login and get token         |
| `/api/token/refresh/` | POST            | Refresh access token        |
| `/api/products/`      | GET             | List all products           |
| `/api/cart/`          | GET/POST/DELETE | Cart operations             |
| `/api/orders/`        | GET/POST        | Place/view orders           |
| `/api/profile/`       | GET/PUT         | View or update user profile |

---

## ✅ To Do (Future Improvements)
- Real-time notifications via Django Channels

- Payment integration

- Frontend (React/Vue) integration

- Admin dashboard panel

---

## 📌 Samples for API endpoints

### 🔐 Auth Endpoints (JWT)
| Method | Endpoint              | Description                |
| ------ | --------------------- | -------------------------- |
| POST   | `/api/token/`         | Get access & refresh token |
| POST   | `/api/token/refresh/` | Refresh access token       |

```bash
POST /api/token/
{
  "email": "user@example.com",
  "password": "yourpassword"
}
```

### 👤 User Profile
| Method | Endpoint        | Description           |
| ------ | --------------- | --------------------- |
| GET    | `/api/profile/` | Get current user info |
| PUT    | `/api/profile/` | Update profile        |

### 🛍️ Products & Categories
| Method | Endpoint                        | Description         |
| ------ | ------------------------------- | ------------------- |
| GET    | `/api/categories/`              | List all categories |
| GET    | `/api/products/`                | List all products   |
| GET    | `/api/products/?search=shirt`   | Search products     |
| GET    | `/api/products/?ordering=price` | Order products      |
| GET    | `/api/products/?category=1`     | Filter by category  |
| GET    | `/api/products/<id>/`           | Get product details |

### 🛒 Cart API
| Method | Endpoint            | Description           |
| ------ | ------------------- | --------------------- |
| GET    | `/api/cart/`        | View cart             |
| POST   | `/api/cart/add/`    | Add item to cart      |
| POST   | `/api/cart/remove/` | Remove item from cart |

