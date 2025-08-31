# Tramos API

Tramos API is a robust and scalable RESTful system developed with Django and Django REST Framework. It provides a comprehensive solution for managing courses, academic offerings, enrollments, clients, and payments, targeted at educational institutions.

## ✨ Main Features

- **User and Role Management:** JWT-based authentication system with multiple roles (admin, manager, commercial, cashier, observer) for granular access control.
- **Complete Academic Management:** Administration of Services, Courses, Schools, Classrooms, and Course Offers.
- **Booking System:** Handling of individual client bookings and multiple bookings for companies.
- **Client and Company Management:** Registration and tracking of client information and agreements with companies.
- **Payment Integration:** Payment gateway implemented with Transfermóvil to process booking payments.
- **Report Generation:** Dedicated endpoints to generate dynamic reports such as attendance lists, registration sheets, and appearance reports.
- **Automated API Documentation:** Interactive and detailed API documentation available through Swagger UI and Redoc.
- **Action Traceability:** Middleware to log important actions that occur in the system.

## 🛠️ Technologies Used

- **Backend:** Python, Django
- **API:** Django REST Framework
- **Database:** PostgreSQL (via `psycopg2`)
- **Authentication:** JSON Web Tokens (JWT) with `djangorestframework-simplejwt`
- **API Documentation:** `drf-spectacular` to generate OpenAPI schemas (Swagger/Redoc).
- **Environment Variables:** `django-environ`
- **Production Server:** Gunicorn
- **Others:** `requests` for communication with external services.

## 📂 Project Structure

```
tramos-api/
├── api/                    # Main directory for the API application
│   ├── migrations/         # Database migrations
│   ├── models/             # Django models (DB schema)
│   ├── middleware/         # Custom middlewares
│   ├── v1/                 # API Version 1
│   │   ├── filters/        # Filter classes for viewsets
│   │   ├── permissions/    # Custom permissions
│   │   ├── serializers/    # Serializers for models
│   │   ├── viewsets/       # Endpoint logic (Views)
│   │   └── urls.py         # API v1 routes
│   └── ...
├── tramos_api/             # Django project configuration
│   ├── settings.py         # Main configuration
│   └── urls.py             # Main project routes
├── .env                    # File for environment variables (not versioned)
├── manage.py               # Django command-line utility
└── requirements.txt        # Python dependencies
```

## 🚀 Installation and Setup

Follow these steps to set up the local development environment.

**1. Clone the Repository**
```bash
git clone <REPOSITORY_URL>
cd tramos-api
```

**2. Create and Activate a Virtual Environment**
```bash
# On Windows
python -m venv .venv
.venv\Scripts\activate

# On macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

**3. Install Dependencies**
```bash
pip install -r requirements.txt
```

**4. Configure Environment Variables**
Create a file named `.env` in the project root and add the following variables. Replace the values with your configuration.

```ini
# Tramos API .env file
# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY='your_secret_key_here'

# DEBUG: True for development, False for production
DEBUG=True

# Database Configuration (example for PostgreSQL)
DATABASE_URL='psql://user:password@localhost:5432/db_name'

# Transfermóvil Configuration
TM_USERNAME='your_tm_username'
TM_SEED='your_tm_seed'
TM_SOURCE='your_tm_source'
TM_CURRENCY='CUP'
TM_URL_RESPONSE_TRANSFERMOVIL='https://your-domain.com/api/v1/payment/notification/'
TM_CONNECTION='https://api-transfermovil.com/api' # Transfermóvil API URL
```

**5. Run Migrations**
Apply the migrations to create the database schema.
```bash
python manage.py migrate
```

**6. Create a Superuser**
This will allow you to access the Django administration panel.
```bash
python manage.py createsuperuser
```

**7. Run the Development Server**
```bash
python manage.py runserver
```
The API will be available at `http://127.0.0.1:8000/`.

## 📚 API Endpoints

The API is versioned, and all main endpoints are under the `/api/v1/` prefix.

### Authentication
- `POST /api/token/`: Obtains a token pair (access and refresh) from user credentials.
- `POST /api/token/refresh/`: Refreshes an expired access token.

### Main Management
- `/user/`: User management (CRUD).
- `/province/`, `/municipality/`: Province and municipality management.
- `/school/`, `/classroom/`: School and classroom management.
- `/service/`, `/course/`: Service and course management.
- `/offer/`: Course offer management.
- `/client/`: Client management.
- `/company/`: Company management.
- `/booking/`: Individual booking management.
- `/multipleBooking/`: Company booking management.
- `/payment-code/`: Payment code management.

### Payments and Reports
- `POST /api/v1/payment/register/`: Initiates a payment process with Transfermóvil.
- `POST /api/v1/payment/notification/`: Endpoint to receive payment notifications from Transfermóvil.
- `GET /api/v1/reports/offer/current`: Lists current offers.
- `GET /api/v1/reports/course-evaluation/`: Generates detailed course reports.

## 🧪 Running Tests

To run the test suite and verify the code's integrity, use the following command:
```bash
python manage.py test api
```

## 📄 Interactive Documentation

This project uses `drf-spectacular` to generate interactive API documentation. Once the server is running, you can access:

- **Swagger UI:** `http://127.0.0.1:8000/api/v1/swagger/`
- **Redoc:** `http://127.0.0.1:8000/api/v1/redoc/`

These interfaces will allow you to explore all endpoints, see the parameters they accept, and test them in real-time.
