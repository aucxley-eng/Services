# Zoza Services API

A production-ready Flask REST API for managing inventory, products, suppliers, branches, and categories with JWT authentication, role-based access control, and comprehensive testing.

## Features

- **JWT Authentication**: Secure token-based authentication with role claims
- **Product Management**: CRUD operations with pagination, search, and categories
- **Supplier Management**: Full CRUD for suppliers with returns tracking
- **Branch Management**: Multi-branch support with employee assignments
- **Category Management**: Product categorization with relationships
- **Inventory Tracking**: Stock in/out transactions with audit trail
- **Low Stock Alerts**: Automatic alerts when stock falls below threshold
- **Transaction History**: Complete audit trail of all stock movements
- **Role-Based Access**: Admin, Manager, and Staff with distinct permissions
- **Flask-Marshmallow**: Input validation and serialization
- **Flask-Migrate**: Database version control with Alembic
- **Comprehensive Tests**: 62 unit tests covering all endpoints

## Quick Start

```bash
# Clone and setup
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Initialize database
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# Run tests
python -m pytest tests/ -v

# Run server
python run.py
```

## Project Structure

```
app/
├── __init__.py           # Application factory
├── extensions.py          # Flask extensions (Marshmallow, Migrate)
├── api_response.py        # Standardized API responses
├── auth/                  # Authentication module
│   ├── domain/           # User model with role methods
│   ├── repo/            # User repository
│   ├── routes/          # Register, login, me, refresh
│   ├── schema/          # User serialization schema
│   └── service/         # Auth business logic
├── branches/             # Branch management
├── categories/           # Category management
├── inventory/            # Stock transactions & tracking
│   ├── domain/          # Stock & StockTransaction models
│   ├── repo/            # Stock repository
│   ├── routes/          # Transaction, levels, history endpoints
│   └── service/         # Inventory business logic
├── products/             # Product management
│   ├── domain/          # Product model with relationships
│   ├── repo/            # Product repository with search
│   ├── routes/          # CRUD endpoints
│   ├── schema/          # Marshmallow schemas
│   └── service/         # Product business logic
└── suppliers/            # Supplier management
```

## Database Models & Relationships

```
┌─────────────┐       ┌─────────────┐       ┌─────────────────┐
│   Branch    │       │    User     │       │    Category     │
├─────────────┤       ├─────────────┤       ├─────────────────┤
│ id          │◄──────│ branch_id   │       │ id              │
│ name        │       │ id          │       │ name            │
│ location    │       │ username    │       │ description     │
└──────┬──────┘       │ role        │       └────────┬────────┘
       │              └─────────────┘                │
       │                                           │
       ▼              ┌────────────────────────────┘
┌─────────────┐       │
│   Stock     │◄──────┤
├─────────────┤       │              ┌─────────────┐
│ id          │◄──────┤              │   Product   │
│ branch_id   │       │              ├─────────────┤
│ product_id  │       │              │ id          │
│ quantity    │       │              │ name        │
└──────┬──────┘       │              │ buying_price│
       │              │              │ category_id │
       ▼              │              │ threshold   │
┌─────────────────┐   │              └─────────────┘
│StockTransaction │   │
├─────────────────┤   │
│ id              │   │
│ stock_id        │◄──┘
│ user_id         │◄──────┐
│ quantity        │       │
│ type (in/out)   │       │
│ reason          │       │
│ notes           │       │
│ created_at      │       │
└─────────────────┘       │
                          │
                          ▼
                    ┌─────────────┐
                    │    User     │
                    ├─────────────┤
                    │ id          │
                    │ ...         │
                    └─────────────┘
```

## API Endpoints

### Authentication (`/api/auth`)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/register` | Register new user |
| POST | `/login` | Login, returns JWT token |
| GET | `/me` | Get current user info |
| POST | `/refresh-token` | Refresh JWT token |

### Branches (`/api/branches`)
| Method | Endpoint | Access |
|--------|----------|--------|
| GET | `/` | All users |
| POST | `/` | Admin only |
| GET | `/<id>` | All users |
| PUT | `/<id>` | Admin only |
| DELETE | `/<id>` | Admin only |

### Categories (`/api/categories`)
| Method | Endpoint | Access |
|--------|----------|--------|
| GET | `/` | All users |
| POST | `/` | Admin only |
| GET | `/<id>` | All users |
| PUT | `/<id>` | Admin only |
| DELETE | `/<id>` | Admin only |

### Products (`/api/products`)
| Method | Endpoint | Access |
|--------|----------|--------|
| GET | `/?page=1&per_page=10&search=name` | All users |
| POST | `/` | Admin, Manager |
| GET | `/<id>` | All users |
| PUT | `/<id>` | Admin, Manager |
| DELETE | `/` | Admin only |

### Suppliers (`/api/suppliers`)
| Method | Endpoint | Access |
|--------|----------|--------|
| GET | `/` | All users |
| POST | `/` | Admin, Manager |
| GET | `/<id>` | All users |
| PUT | `/<id>` | Admin, Manager |
| DELETE | `/` | Admin only |

### Inventory (`/api/inventory`)
| Method | Endpoint | Access |
|--------|----------|--------|
| POST | `/transaction` | Admin, Manager |
| GET | `/levels?branch_id=1` | All users |
| GET | `/low-stock` | Admin, Manager |
| GET | `/history?product_id=1&branch_id=1` | Admin, Manager |

## Role-Based Access Control

| Feature | Admin | Manager | Staff |
|---------|-------|---------|-------|
| **Branches** | | | |
| Create branch | ✓ | ✗ | ✗ |
| Delete branch | ✓ | ✗ | ✗ |
| View branches | ✓ | ✓ | ✓ |
| **Products** | | | |
| Create product | ✓ | ✓ | ✗ |
| Update product | ✓ | ✓ | ✗ |
| Delete product | ✓ | ✗ | ✗ |
| View products | ✓ | ✓ | ✓ |
| **Categories** | | | |
| Create category | ✓ | ✗ | ✗ |
| Delete category | ✓ | ✗ | ✗ |
| View categories | ✓ | ✓ | ✓ |
| **Suppliers** | | | |
| Create supplier | ✓ | ✓ | ✗ |
| Delete supplier | ✓ | ✗ | ✗ |
| View suppliers | ✓ | ✓ | ✓ |
| **Inventory** | | | |
| Stock transaction | ✓ | ✓ | ✗ |
| View stock levels | ✓ | ✓ | ✓ |
| Low stock alerts | ✓ | ✓ | ✗ |
| Transaction history | ✓ | ✓ | ✗ |

## Example Requests

### Register Admin
```bash
POST /api/auth/register
{
    "username": "admin",
    "first_name": "Admin",
    "last_name": "User",
    "email": "admin@example.com",
    "password": "password123",
    "role": "admin"
}
```

### Create Category
```bash
POST /api/categories/
{
    "name": "Food & Beverages",
    "description": "Food and beverage products"
}
```

### Create Product with Category
```bash
POST /api/products/
{
    "name": "Maggi Noodles",
    "buying_price": 50,
    "selling_price": 80,
    "unit": "packets",
    "threshold": 10,
    "category_id": 1
}
```

### Stock Transaction
```bash
POST /api/inventory/transaction
{
    "product_id": 1,
    "branch_id": 1,
    "quantity": 100,
    "type": "in",
    "reason": "Purchase from supplier"
}
```

### Get Transaction History
```bash
GET /api/inventory/history?product_id=1&branch_id=1&limit=50
```

## Response Format

All responses follow a consistent format:

```json
{
    "data": { ... },
    "message": "Success message"
}
```

Error responses include additional fields:

```json
{
    "error": "Validation Error",
    "message": "Missing required fields",
    "details": "buying_price is required",
    "solution": "Provide buying_price in request body"
}
```

## Database Migrations

```bash
# Initialize (first time only)
flask db init

# Create migration
flask db migrate -m "Add new field"

# Apply migration
flask db upgrade

# Rollback
flask db downgrade

# Show current version
flask db current
```

## Running Tests

```bash
# Run all tests
python -m pytest tests/ -v

# Run specific test file
python -m pytest tests/test_products.py -v

# Run with coverage
python -m pytest tests/ --cov=app --cov-report=html
```

## API Documentation

Interactive Swagger documentation available at:
```
http://localhost:5000/apidocs/
```

## Environment Variables

```bash
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
DATABASE_URL=sqlite:///kanban.db
```

## Tech Stack

- **Flask** - Web framework
- **Flask-JWT-Extended** - JWT authentication
- **Flask-SQLAlchemy** - ORM
- **Flask-Marshmallow** - Serialization & validation
- **Flask-Migrate** - Database migrations
- **Flask-CORS** - Cross-origin support
- **Flasgger** - API documentation
- **Pytest** - Testing framework