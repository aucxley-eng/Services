# Detailed Project File Explanation - Zoza Services API

This document provides a comprehensive explanation of every file in the project, its purpose, and how it fits into the overall architecture.

---

## Table of Contents

1. [Root Configuration Files](#root-configuration-files)
2. [Database Layer](#database-layer)
3. [Application Factory](#application-factory)
4. [Extensions](#extensions)
5. [Authentication Module](#authentication-module)
6. [Branches Module](#branches-module)
7. [Categories Module](#categories-module)
8. [Products Module](#products-module)
9. [Suppliers Module](#suppliers-module)
10. [Inventory Module](#inventory-module)
11. [Orders Module](#orders-module)
12. [API Response Utility](#api-response-utility)
13. [Tests](#tests)

---

## Root Configuration Files

### run.py
**Purpose**: Entry point to start the Flask application server.

**What it does**:
- Imports `create_app` from `app` module to initialize Flask app
- Creates the app instance
- Creates all database tables if they don't exist (`db.create_all()`)
- Runs the development server on port 5000 with debug mode enabled

**Why it exists**: Provides the simplest way to start the API server with `python run.py`

```python
from app import create_app, db

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5000)
```

---

### config.py
**Purpose**: Configuration settings for the Flask application.

**What it does**:
- Defines the base `Config` class with settings:
  - `SECRET_KEY`: Used for session security and CSRF protection
  - `SQLALCHEMY_DATABASE_URI`: Database connection string (default: SQLite)
  - `JWT_SECRET_KEY`: Used to sign JWT tokens
  - `JWT_ACCESS_TOKEN_EXPIRES`: Token expiration time (1 hour)

**Configuration Pattern**: Uses environment variables with fallback defaults for development

---

### requirements.txt
**Purpose**: Lists all Python dependencies required by the project.

**Dependencies**:
| Package | Version | Purpose |
|---------|---------|---------|
| Flask | 3.0.3 | Web framework |
| Flask-SQLAlchemy | 3.1.1 | ORM |
| Flask-Migrate | 4.0.5 | Database migrations |
| Flask-JWT-Extended | 4.6.0 | JWT authentication |
| Flask-CORS | 4.0.1 | Cross-origin support |
| Flasgger | 0.9.7.1 | Swagger documentation |
| marshmallow | 3.21.1 | Serialization/validation |
| Flask-Migrate | 4.0.5 | Database migrations |
| Werkzeug | 3.0.3 | Password hashing |
| flask-login | 0.6.3 | Session management |

---

## Database Layer

### database.py
**Purpose**: Central database configuration and initialization.

**What it does**:
- Creates the SQLAlchemy database instance (`db = SQLAlchemy()`)
- Provides helper function `generate_api_key()` for generating secure random API keys

**Why it exists**: SQLAlchemy needs to be initialized once and imported by all models to avoid circular imports

```python
from flask_sqlalchemy import SQLAlchemy
import secrets

db = SQLAlchemy()

def generate_api_key():
    """Generate a secure random API key"""
    return secrets.token_urlsafe(32)
```

---

### .env
**Purpose**: Environment variables (should be in .gitignore).

**Contains**: Secret keys, database URLs, and other sensitive configuration.

---

## Application Factory

### app/__init__.py
**Purpose**: Flask application factory that creates and configures the app.

**What it does**:

1. **Creates Flask app** with the Config class
2. **Initializes extensions**:
   - SQLAlchemy (`db`)
   - Marshmallow (`ma`)
   - Migrate (`migrate`)
   - JWT Manager
   - CORS
   - Flasgger (Swagger)

3. **Registers blueprints** (routes):
   - `auth_bp` → `/api/auth`
   - `branches_bp` → `/api/branches`
   - `categories_bp` → `/api/categories`
   - `products_bp` → `/api/products`
   - `suppliers_bp` → `/api/suppliers`
   - `inventory_bp` → `/api/inventory`
   - `orders_bp` → `/api/orders`

4. **Error handlers**: Defines custom error responses for:
   - 400 (Bad Request)
   - 404 (Not Found)
   - 405 (Method Not Allowed)
   - 401 (No Authorization)
   - 500 (Internal Server Error)

**Why it exists**: Provides a centralized app configuration following Flask best practices.

---

## Extensions

### app/extensions.py
**Purpose**: Initializes Flask extensions that need app context.

**What it does**:
- Creates Marshmallow instance for serialization:
  ```python
  ma = Marshmallow()
  migrate = Migrate()
  ```

**Used by**: `app/__init__.py` to initialize extensions with the app.

---

## Authentication Module

### app/auth/domain/user.py - User Model
**Purpose**: Defines the User database table and business logic.

**Database Table**: `users`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTOINCREMENT | Unique user ID |
| username | VARCHAR(50) | UNIQUE, NOT NULL | Unique username |
| first_name | VARCHAR(50) | NOT NULL | User's first name |
| last_name | VARCHAR(50) | NOT NULL | User's last name |
| email | VARCHAR(120) | UNIQUE, NOT NULL | User's email |
| password_hash | VARCHAR(255) | NOT NULL | Hashed password |
| role | VARCHAR(20) | DEFAULT='staff' | Role: admin/manager/staff |
| branch_id | INTEGER | FK → branches.id | Assigned branch |
| is_active | BOOLEAN | DEFAULT=True | Account status |
| created_at | DATETIME | DEFAULT=CURRENT_TIMESTAMP | Registration time |

**Business Logic Methods**:
- `is_admin()`: Check if user is admin
- `is_manager()`: Check if user is manager
- `is_staff()`: Check if user is staff
- `can_delete_branch()`: Only admins can delete
- `can_manage_branch()`: Admin or manager of that branch
- `set_password()`: Hashes password using Werkzeug
- `check_password()`: Verifies password hash

---

### app/auth/routes/routes.py - Auth Endpoints
**Purpose**: API endpoints for authentication.

**Endpoints**:

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register` | Register new user |
| POST | `/api/auth/login` | Login and get JWT token |
| GET | `/api/auth/me` | Get current user profile |
| POST | `/api/auth/refresh-token` | Refresh JWT token |

**Process Flow**:
1. User registers → Validation → Create User → Generate JWT → Return token
2. User logs in → Verify credentials → Generate JWT → Return token
3. Protected endpoints require `Authorization: Bearer <token>` header

---

### app/auth/service/__init__.py - AuthService
**Purpose**: Business logic for authentication operations.

**Methods**:

1. **validate_registration_data()**
   - Checks required fields (username, first_name, last_name, email, password)
   - Validates email format using regex
   - Ensures password is at least 6 characters

2. **register()**
   - Validates input data
   - Checks duplicate username and email
   - Creates user with hashed password
   - Generates JWT token with role claims

3. **login()**
   - Verifies email exists
   - Checks password against hash
   - Generates JWT token with role claims

4. **get_user_by_id()**
   - Retrieves user from database

---

### app/auth/repo/user_repository.py - UserRepository
**Purpose**: Database operations for User model.

**Methods**:
- `find_by_id(user_id)`: Get user by ID
- `find_by_email(email)`: Get user by email
- `find_by_username(username)`: Get user by username
- `find_by_api_key(api_key)`: Get user by API key (legacy)
- `create(**kwargs)`: Create new user
- `generate_new_api_key(user)`: Generate new API key

**Inheritance**: Extends `BaseRepository`

---

### app/auth/repo/base_repository.py - BaseRepository
**Purpose**: Common database operations for all models.

**Methods**:
- `get_all()`: Get all records
- `get_by_id(id)`: Get single record by ID
- `create(**kwargs)`: Create new record
- `update(instance, **kwargs)`: Update existing record
- `delete(instance)`: Delete record
- `save(instance)`: Save/update record

---

### app/auth/schema/user_schema.py - UserSchema
**Purpose**: Marshmallow schema for serialization/validation.

**Used for**: Converting User objects to JSON and validating input.

---

### app/auth/middleware/auth_middleware.py
**Purpose**: Request authentication and authorization.

**Functions**:
- Validates JWT token in requests
- Extracts user identity from token
- Checks role-based permissions

---

## Branches Module

### app/branches/domain/branch.py - Branch Model
**Purpose**: Defines the Branch database table.

**Database Table**: `branches`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTOINCREMENT | Unique branch ID |
| name | VARCHAR(100) | NOT NULL | Branch name |
| location | VARCHAR(200) | NULL | Branch location |
| phone | VARCHAR(20) | NULL | Contact number |
| email | VARCHAR(120) | NULL | Email address |
| is_active | BOOLEAN | DEFAULT=True | Branch status |
| created_at | DATETIME | DEFAULT=CURRENT_TIMESTAMP | Creation time |

**Relationships**:
- One Branch → Many Stock (1:N)
- One Branch → Many Users/Employees (1:N)

---

### app/branches/routes/routes.py - Branches Endpoints
**Purpose**: API endpoints for branch management.

**Endpoints**:

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| GET | `/api/branches` | All | List all branches |
| POST | `/api/branches` | Admin | Create branch |
| GET | `/api/branches/{id}` | All | Get branch by ID |
| PUT | `/api/branches/{id}` | Admin | Update branch |
| DELETE | `/api/branches/{id}` | Admin | Delete branch |

---

### app/branches/service/branch_service.py - BranchService
**Purpose**: Business logic for branch operations.

**Methods**:
- `get_all_branches()`: List all branches
- `get_branch(branch_id)`: Get single branch
- `create_branch(data, current_user)`: Create new branch (admin only)
- `update_branch(branch_id, data, current_user)`: Update branch (admin only)
- `delete_branch(branch_id, current_user)`: Delete branch (admin only)

---

### app/branches/repo/branch_repository.py - BranchRepository
**Purpose**: Database operations for Branch model.

**Methods**: Standard CRUD operations inherited from BaseRepository

---

## Categories Module

### app/categories/domain/category.py - Category Model
**Purpose**: Defines the Category database table.

**Database Table**: `categories`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTOINCREMENT | Unique category ID |
| name | VARCHAR(100) | UNIQUE, NOT NULL | Category name |
| description | VARCHAR(255) | NULL | Description |
| is_active | BOOLEAN | DEFAULT=True | Status |
| created_at | DATETIME | DEFAULT=CURRENT_TIMESTAMP | Creation time |

**Relationships**:
- One Category → Many Products (1:N)

---

### app/categories/routes/routes.py - Categories Endpoints
**Purpose**: API endpoints for category management.

**Endpoints**:

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| GET | `/api/categories` | All | List categories |
| POST | `/api/categories` | Admin | Create category |
| GET | `/api/categories/{id}` | All | Get category |
| PUT | `/api/categories/{id}` | Admin | Update category |
| DELETE | `/api/categories/{id}` | Admin | Delete category |

---

### app/categories/service/category_service.py - CategoryService
**Purpose**: Business logic for category operations.

---

### app/categories/repo/category_repository.py - CategoryRepository
**Purpose**: Database operations for Category model.

---

### app/categories/schema/category_schema.py - CategorySchema
**Purpose**: Marshmallow schema for Category serialization.

---

## Products Module

### app/products/domain/product.py - Product Model
**Purpose**: Defines the Product database table.

**Database Table**: `products`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTOINCREMENT | Unique product ID |
| product_id | VARCHAR(50) | UNIQUE | SKU/Barcode |
| name | VARCHAR(100) | NOT NULL | Product name |
| buying_price | FLOAT | NOT NULL | Cost price |
| selling_price | FLOAT | NULL | Retail price |
| unit | VARCHAR(20) | NULL | Unit (kg, pcs, etc.) |
| expiry_date | DATE | NULL | Expiration date |
| threshold | INTEGER | DEFAULT=10 | Low stock threshold |
| category_id | INTEGER | FK → categories.id | Category |
| supplier_id | INTEGER | FK → suppliers.id | Supplier |
| image_url | VARCHAR(255) | NULL | Image URL |

**Relationships**:
- Many Products ← One Category (N:1)
- One Product → Many Stock (1:N)
- One Product → Many Orders (1:N)

---

### app/products/routes/routes.py - Products Endpoints
**Purpose**: API endpoints for product management.

**Endpoints**:

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| GET | `/api/products` | All | List with pagination & search |
| POST | `/api/products` | Admin, Manager | Create product |
| GET | `/api/products/{id}` | All | Get product |
| PUT | `/api/products/{id}` | Admin, Manager | Update product |
| DELETE | `/api/products/{id}` | Admin | Delete product |

**Query Parameters**:
- `page`: Page number (default: 1)
- `per_page`: Items per page (default: 10)
- `search`: Search by product name

---

### app/products/service/product_service.py - ProductService
**Purpose**: Business logic for product operations.

**Methods**:
- `get_all_products(page, per_page, search)`: Paginated product list
- `get_product(product_id)`: Get single product
- `create_product(data, current_user)`: Create new product
- `update_product(product_id, data, current_user)`: Update product
- `delete_product(product_id, current_user)`: Delete product

**Validations**:
- Required: name, buying_price
- Validates category_id and supplier_id exist
- Checks for duplicate product names

---

### app/products/repo/product_repository.py - ProductRepository
**Purpose**: Database operations for Product model.

**Special Methods**:
- `find_by_name(name)`: Find product by name
- `get_all_paginated(page, per_page, search)`: Paginated results with search

---

### app/products/schema/product_schema.py - ProductSchema
**Purpose**: Marshmallow schema for Product serialization.

---

## Suppliers Module

### app/suppliers/domain/supplier.py - Supplier Model
**Purpose**: Defines the Supplier database table.

**Database Table**: `suppliers`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTOINCREMENT | Unique supplier ID |
| name | VARCHAR(100) | NOT NULL | Supplier name |
| email | VARCHAR(120) | NULL | Email address |
| phone | VARCHAR(20) | NULL | Contact number |
| address | VARCHAR(255) | NULL | Address |
| taking_returns | BOOLEAN | DEFAULT=True | Accepts returns |

**Relationships**:
- One Supplier → Many Products (1:N)
- One Supplier → Many Orders (1:N)

---

### app/suppliers/routes/routes.py - Suppliers Endpoints
**Purpose**: API endpoints for supplier management.

**Endpoints**:

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| GET | `/api/suppliers` | All | List suppliers |
| POST | `/api/suppliers` | Admin, Manager | Create supplier |
| GET | `/api/suppliers/{id}` | All | Get supplier |
| PUT | `/api/suppliers/{id}` | Admin, Manager | Update supplier |
| DELETE | `/api/suppliers/{id}` | Admin | Delete supplier |

---

### app/suppliers/service/supplier_service.py - SupplierService
**Purpose**: Business logic for supplier operations.

---

### app/suppliers/repo/supplier_repository.py - SupplierRepository
**Purpose**: Database operations for Supplier model.

---

## Inventory Module

### app/inventory/domain/stock.py - Stock Model
**Purpose**: Tracks current stock levels per product per branch.

**Database Table**: `stock`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTOINCREMENT | Unique record ID |
| product_id | INTEGER | FK → products.id, NOT NULL | Product |
| branch_id | INTEGER | FK → branches.id, NOT NULL | Branch |
| quantity | INTEGER | DEFAULT=0 | Current quantity |

**Unique Constraint**: `product_id + branch_id` (one record per product-branch combination)

**Relationships**:
- Many Stock ← One Product (N:1)
- Many Stock ← One Branch (N:1)

---

### app/inventory/domain/stock_transaction.py - StockTransaction Model
**Purpose**: Audit trail for all stock movements.

**Database Table**: `stock_transactions`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTOINCREMENT | Unique transaction ID |
| stock_id | INTEGER | FK → stock.id, NOT NULL | Stock record |
| user_id | INTEGER | FK → users.id, NOT NULL | User who made change |
| quantity | INTEGER | NOT NULL, >0 | Amount changed |
| type | VARCHAR(10) | NOT NULL | 'in' or 'out' |
| reason | VARCHAR(100) | NULL | Reason for change |
| notes | TEXT | NULL | Additional notes |
| created_at | DATETIME | DEFAULT=CURRENT_TIMESTAMP | When it happened |

**Relationships**:
- One Stock → Many Transactions (1:N)

---

### app/inventory/routes/routes.py - Inventory Endpoints
**Purpose**: API endpoints for inventory management.

**Endpoints**:

| Method | Endpoint | Access | Description |
|--------|----------|--------|-------------|
| POST | `/api/inventory/transaction` | Admin, Manager | Stock in/out |
| GET | `/api/inventory/levels` | All | Stock levels |
| GET | `/api/inventory/low-stock` | Admin, Manager | Low stock alerts |
| GET | `/api/inventory/history` | Admin, Manager | Transaction audit |

**Transaction Request**:
```json
{
    "product_id": 1,
    "branch_id": 1,
    "quantity": 100,
    "type": "in",          // "in" or "out"
    "reason": "Purchase",
    "notes": "Initial stock"
}
```

---

### app/inventory/service/inventory_service.py - InventoryService
**Purpose**: Business logic for all inventory operations.

**Methods**:

1. **stock_transaction(data, current_user)**
   - Validates required fields
   - Verifies product and branch exist
   - Creates stock record if needed
   - Adds/removes quantity based on type
   - Creates audit transaction
   - Returns alert if below threshold

2. **get_stock_levels(branch_id)**
   - Returns all stock records
   - Optionally filtered by branch
   - Includes product and branch names

3. **get_low_stock(branch_id)**
   - Finds all products where quantity <= threshold
   - Includes severity level (critical/warning)

4. **get_transaction_history(stock_id, product_id, branch_id, limit)**
   - Returns paginated audit trail
   - Filters by stock, product, or branch
   - Ordered by most recent first

---

### app/inventory/repo/stock_repository.py - StockRepository
**Purpose**: Database operations for Stock model.

**Special Methods**:
- `find_by_product_and_branch(product_id, branch_id)`: Get stock record
- `get_by_branch(branch_id)`: Get all stock for branch

---

## Orders Module

### app/orders/domain/order.py - Order Model
**Purpose**: Tracks orders from branches to suppliers.

**Database Table**: `orders`

| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTOINCREMENT | Unique order ID |
| product_id | INTEGER | FK → products.id | Product ordered |
| supplier_id | INTEGER | FK → suppliers.id | Supplier |
| branch_id | INTEGER | FK → branches.id | Branch making order |
| quantity | INTEGER | NULL | Order quantity |
| status | VARCHAR(20) | DEFAULT='Pending' | Status |
| order_date | DATETIME | DEFAULT=CURRENT_TIMESTAMP | Order date |

**Statuses**: Pending, Confirmed, Delayed, Returned

---

### app/orders/routes/routes.py - Orders Endpoints
**Purpose**: API endpoints for order management.

**Endpoints**: Standard CRUD operations

---

### app/orders/service/order_service.py - OrderService
**Purpose**: Business logic for order operations.

---

## API Response Utility

### app/api_response.py - APIResponse
**Purpose**: Standardized API response formatting.

**Methods**:

| Method | Status Code | Usage |
|--------|-------------|-------|
| `success()` | 200 | Successful operations |
| `error()` | 400 | Validation/general errors |
| `validation_error()` | 400 | Missing required fields |
| `unauthorized()` | 401 | Authentication failed |
| `forbidden()` | 403 | Permission denied |
| `not_found()` | 404 | Resource not found |
| `conflict()` | 409 | Resource already exists |
| `server_error()` | 500 | Unexpected errors |
| `handle_exception()` | 500 | Catch-all for exceptions |

**Response Format**:
```json
{
    "data": { ... },
    "message": "Success message"
}
```

**Error Format**:
```json
{
    "error": "Error Type",
    "message": "Human readable message",
    "details": "Technical details",
    "solution": "How to fix"
}
```

---

## Tests

### tests/conftest.py
**Purpose**: Pytest configuration and fixtures.

**Fixtures**:
- `app`: Flask test client
- `client`: HTTP test client
- `db`: Test database session

---

### tests/test_auth.py
**Purpose**: Tests for authentication endpoints.

**Coverage**:
- User registration
- Login
- Token refresh

---

### tests/test_products.py
**Purpose**: Tests for product endpoints.

---

### tests/test_inventory.py
**Purpose**: Tests for inventory endpoints.

---

### tests/test_branches.py
**Purpose**: Tests for branch endpoints.

---

### tests/test_categories_suppliers.py
**Purpose**: Tests for category and supplier endpoints.

---

---

## Architecture Summary Flow

```
Request Flow:
┌──────────────┐
│   Request   │
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│   Authentication    │
│  (JWT Token)       │
└──────┬───────────┘
       │
       ▼
┌──────────────────┐
│   Routes Layer   │
│  (endpoints)    │
└──────┬─────────┘
       │
       ▼
┌──────────────────┐
│   Service Layer │
│ (business logic)│
└──────┬─────────┘
       │
       ▼
┌──────────────────┐
│ Repository     │
│ (database)    │
└──────────────┘
```

**Layer Responsibilities**:

1. **Routes**: Handle HTTP requests/responses, authorization checks
2. **Service**: Business logic, validation, orchestrates operations
3. **Repository**: Database operations (CRUD)
4. **Domain/Model**: Database table definitions

---

## Role-Based Access Control (RBAC)

| Feature | Admin | Manager | Staff |
|---------|-------|---------|-------|
| Create Branch | ✓ | ✗ | ✗ |
| Delete Branch | ✓ | ✗ | ✗ |
| View Branch | ✓ | ✓ | ✓ |
| Create Product | ✓ | ✓ | ✗ |
| Update Product | ✓ | ✓ | ✗ |
| Delete Product | ✓ | ✗ | ✗ |
| View Product | ✓ | ✓ | ✓ |
| Create Category | ✓ | ✗ | ✗ |
| Delete Category | ✓ | ✗ | ✗ |
| View Category | ✓ | ✓ | ✓ |
| Stock Transaction | ✓ | ✓ | ✗ |
| View Stock Levels | ✓ | ✓ | ✓ |
| Low Stock Alerts | ✓ | ✓ | ✗ |
| Transaction History | ✓ | ✓ | ✗ |

---

## Presentation Talking Points

1. **Project Structure**: "We follow a layered architecture - Routes → Services → Repositories → Models"
2. **Authentication**: "JWT tokens with role-based access control"
3. **Inventory**: "Per-branch stock tracking with full audit trail"
4. **Testing**: "62 comprehensive tests to ensure reliability"
5. **API Docs**: "Swagger UI available at /apidocs/"
6. **Error Handling**: "Consistent error response format across all endpoints"

---

End of Detailed File Explanation