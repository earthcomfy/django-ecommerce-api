# Django Ecommerce API

An E-commerce API built using Django Rest Framework.

## Basic Features
- Registration using either phone number or email https://github.com/earthcomfy/drf-phone-email-auth
- Basic E-commerce features.
- Custom permissions set for necessary endpoints.
- Payment integration using Stripe.
- Documentation using [DRF Spectacular](https://drf-spectacular.readthedocs.io/en/latest/)
- Dockerized for local development and production

## Technologies Used
- Django Rest Framework
- PostgreSQL
- Celery
- Redis
- Nginx
- Docker
- Stripe

## ER Diagram
Here is the Entity-Relationship diagram generated using https://dbdiagram.io/

![ER-Diagram](https://user-images.githubusercontent.com/66206865/192154014-3299110f-9ab7-4bd2-9dc0-aa6790074ed9.png)

## Getting Started

Clone this repository to your local machine and rename the `.env.example` file found in the root directory of the project to `.env` and update the environment variables accordingly.

```
$ docker-compose up
$ docker-compose exec web python manage.py createsuperuser
```

Navigate to http://localhost:8000/admin/
