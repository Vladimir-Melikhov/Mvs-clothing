# 🛍️ Mvs-Clothing | Modern E-Commerce Platform

[![Live Demo](https://img.shields.io/badge/▶_Live_Demo-mvs--clothing.site-10b981?style=for-the-badge&logoColor=white)](https://mvs-clothing.site)

A sleek, fully-featured e-commerce platform for apparel, built with a robust **Django REST** backend and a dynamic **Vue.js** SPA frontend. Fully containerized with Docker Compose and served behind a single Caddy reverse proxy with automatic HTTPS.

![Django](https://img.shields.io/badge/Django-092E20?style=flat-square&logo=django&logoColor=white)
![DRF](https://img.shields.io/badge/DRF-A30000?style=flat-square&logo=django&logoColor=white)
![Vue.js](https://img.shields.io/badge/Vue.js-4FC08D?style=flat-square&logo=vuedotjs&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![Redis](https://img.shields.io/badge/Redis-DC382D?style=flat-square&logo=redis&logoColor=white)
![Celery](https://img.shields.io/badge/Celery-37814A?style=flat-square&logo=celery&logoColor=white)
![Stripe](https://img.shields.io/badge/Stripe-635BFF?style=flat-square&logo=stripe&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![Caddy](https://img.shields.io/badge/Caddy-1F88C0?style=flat-square&logo=caddy&logoColor=white)

> [!NOTE]
> Demo / portfolio project. Stripe runs in test mode.

---

## 🚀 Key Features

*   **Catalog & Smart Filtering:** Product discovery with filtering by categories, tags, and apparel attributes.
*   **Cart & Order Management:** Full checkout workflow with order tracking and history in the user dashboard.
*   **User Profiles & Authentication:** Custom user model with account confirmation and shipping address management.
*   **Payments:** Stripe integration for checkout (test mode).
*   **Async Tasks:** Celery workers + Redis for background jobs such as confirmation emails.
*   **Modern UI/UX:** Responsive Vue.js single-page application.

---

## 🛠️ Tech Stack

*   **Backend:** Django / Django REST Framework
*   **Frontend:** Vue.js (SPA)
*   **Database:** PostgreSQL
*   **Cache / Broker:** Redis
*   **Async:** Celery (worker + beat)
*   **Payments:** Stripe
*   **Web Server:** Gunicorn (WSGI)
*   **Reverse Proxy:** Caddy (automatic SSL/HTTPS)
*   **Containerization:** Docker & Docker Compose

---

## 🏗️ Architecture

Multi-container setup managed via **Docker Compose**:

*   `web_clothing` — Django REST application (Gunicorn).
*   `db_clothing` — PostgreSQL with a persistent volume.
*   `redis_clothing` — Redis, used as Celery broker / result backend.
*   `celery_clothing` — Celery worker for asynchronous tasks.
*   `celery_beat` — Celery beat scheduler for periodic tasks.
*   `frontend_clothing` — Vue.js SPA build and static asset serving.

A shared **Caddy** container (separate compose project) acts as the single entry point on ports 80/443, routing `/api`, `/admin`, `/static`, `/media` to the backend and everything else to the frontend, while handling SSL certificates automatically.