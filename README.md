# Zoza Services API

A Flask-based REST API for managing inventory, products, and branches.

## Features
- **Authentication**: API Key-based registration and login (no JWT).
- **Product Management**: CRUD operations for products with pagination and filtering.
- **Dashboard**: Real-time statistics for inventory value and stock levels.
- **Multi-branch Support**: Track stock across different locations.
- **Role-Based Access**: Admin, Manager, and Staff roles with custom decorators.

## Setup
1. Create a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the application:
   ```bash
   python run.py
   ```

---

## Authentication (API Key Based)

This API uses **API Keys** instead of JWT tokens for authentication.

### Authentication Flow

#### 1. Register a New User
- **Method**: `POST`
- **URL**: `http://localhost:5000/api/auth/register`
- **Body** (JSON):
```json
{
    "username": "johndoe",
    "first_name": "John",
    "last_name": "Doe",
    "email": "john@example.com",
    "password": "securepassword123"
}
```
- **Response**: Returns `api_key` - **save this key safely**

#### 2. Login to Get API Key
- **Method**: `POST`
- **URL**: `http://localhost:5000/api/auth/login`
- **Body** (JSON):
```json
{
    "email": "john@example.com",
    "password": "securepassword123"
}
```
- **Response**: Returns `api_key`

#### 3. Using the API Key
For all protected endpoints, include the API key in the header:
- **Header Key**: `X-API-Key`
- **Header Value**: Your API key (e.g., `abc123xyz...`)

---

## Testing with Postman

### 1. Environment Setup
- **Base URL**: `http://localhost:5000/api`
- Create a Postman Environment and add variables:
  - `baseUrl`: `http://localhost:5000/api`
  - `api_key`: (Leave empty, will be updated after login/register)

### 2. Authentication

#### Register
- **Method**: `POST`
- **URL**: `{{baseUrl}}/auth/register`
- **Body**:
```json
{
    "username": "admin",
    "first_name": "Admin",
    "last_name": "User",
    "email": "admin@example.com",
    "password": "password123"
}
```
- **Important**: Copy the `api_key` from the response into your Postman environment variable.

#### Login
- **Method**: `POST`
- **URL**: `{{baseUrl}}/auth/login`
- **Body**:
```json
{
    "email": "admin@example.com",
    "password": "password123"
}
```

### 3. Using Protected Endpoints

Add the API key to **Headers** (not Authorization tab):
- **Key**: `X-API-Key`
- **Value**: `{{api_key}}`

#### Create a Product (Admin Only)
- **Method**: `POST`
- **URL**: `{{baseUrl}}/products/`
- **Headers**: `X-API-Key: {{api_key}}`
- **Body**:
```json
{
    "name": "Sample Product",
    "buying_price": 150.0,
    "product_id": "PROD-001",
    "unit": "pcs",
    "threshold": 5
}
```

#### List Products
- **Method**: `GET`
- **URL**: `{{baseUrl}}/products/`
- **Headers**: `X-API-Key: {{api_key}}`
- **Query Params**:
  - `page`: 1
  - `per_page`: 10
  - `search`: Sample (Optional)

---

## Role-Based Access

| Role | Access Level |
|------|---------------|
| **admin** | Full access to all operations (create, read, update, delete) |
| **manager** | Can manage products, inventory, categories, suppliers |
| **staff** | Read-only access to products, categories, suppliers |

### Protected Routes by Role

| Endpoint | Method | Required Role |
|----------|--------|---------------|
| `/api/products/` | GET | Any authenticated |
| `/api/products/` | POST | admin |
| `/api/products/<id>` | PUT | admin |
| `/api/products/<id>` | DELETE | admin |
| `/api/inventory/transaction` | POST | Any authenticated |
| `/api/inventory/levels` | GET | Any authenticated |
| `/api/categories/` | GET/POST | Any authenticated |
| `/api/suppliers/` | GET/POST | Any authenticated |
| `/api/dashboard/stats` | GET | Any authenticated |

---

## API Endpoints Summary

### Authentication (`/api/auth`)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/register` | POST | Register new user (returns api_key) |
| `/login` | POST | Login, returns api_key |
| `/me` | GET | Get current user info |
| `/refresh-key` | POST | Generate new API key |

### Products (`/api/products`)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | List products (paginated, searchable) |
| `/` | POST | Create product (admin only) |
| `/<id>` | PUT | Update product (admin only) |
| `/<id>` | DELETE | Delete product (admin only) |

### Inventory (`/api/inventory`)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/transaction` | POST | Record stock in/out |
| `/levels` | GET | Get stock levels by branch |

### Categories (`/api/categories`)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | List all categories |
| `/` | POST | Create category |

### Suppliers (`/api/suppliers`)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | List all suppliers |
| `/` | POST | Add supplier |

### Dashboard (`/api/dashboard`)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/stats` | GET | Get inventory statistics |

---

## API Documentation
Once the server is running, visit:
`http://localhost:5000/apidocs/` for the interactive Swagger documentation.

---

## Custom Decorators

The project uses custom decorators for authentication and authorization:

```python
# Any authenticated user
@require_auth()

# Specific roles
@require_auth(roles=['admin', 'manager'])

# Admin only shortcut
@admin_required()

# Manager or Admin shortcut
@manager_required()
```

These decorators are defined in `app/utils/decorators.py` and use API keys instead of JWT tokens.

---

## Database Schema

See `ERD.md` for the complete Entity Relationship Diagram showing all tables and relationships.