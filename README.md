# Zoza Services API

A Flask-based REST API for managing inventory, products, suppliers, and branches.

## Features
- **JWT Authentication**: Secure token-based authentication
- **Product Management**: CRUD operations with pagination and filtering
- **Supplier Management**: Full CRUD for suppliers
- **Branch Management**: Multi-branch support
- **Role-Based Access**: Admin, Manager, and Staff roles

## Setup
1. Create virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate
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

## Authentication (JWT Based)

### Register
- **Method**: `POST`
- **URL**: `http://localhost:5000/api/auth/register`
- **Body**:
```json
{
    "username": "admin",
    "first_name": "Admin",
    "last_name": "User",
    "email": "admin@example.com",
    "password": "password123",
    "role": "admin"
}
```
- **Roles**: `admin`, `manager`, `staff` (default: admin)
- **Response**: Returns `access_token`

### Login
- **Method**: `POST`
- **URL**: `http://localhost:5000/api/auth/login`
- **Body**:
```json
{
    "email": "admin@example.com",
    "password": "password123"
}
```
- **Response**: Returns `access_token`

### Using the Token
Add to all protected endpoints:
- **Header Key**: `Authorization`
- **Header Value**: `Bearer YOUR_ACCESS_TOKEN`

---

## Role-Based Access

### Admin
- Full system access
- Manage branches (create, update, delete)
- Manage employees (hire, fire, assign roles)
- Manage products, suppliers, inventory
- Delete operations

### Manager
- Assigned to a specific branch
- Manage products and inventory for their branch
- Manage suppliers (create, update)
- **Cannot** delete employees (requires admin approval)
- **Cannot** delete products/suppliers/branches (requires admin approval)
- Cannot create or manage branches

### Staff
- Read-only access to all resources
- Process transactions (future)

---

| Feature | Admin | Manager | Staff |
|---------|-------|---------|-------|
| **Branches** | | | |
| Create branch | ✓ | ✗ | ✗ |
| Update branch | ✓ | ✗ | ✗ |
| Delete branch | ✓ | ✗ | ✗ |
| View branches | ✓ | ✓ | ✓ |
| **Products** | | | |
| Create product | ✓ | ✓ | ✗ |
| Update product | ✓ | ✓ | ✗ |
| Delete product | ✓ | ✗ (needs admin) | ✗ |
| View products | ✓ | ✓ | ✓ |
| **Suppliers** | | | |
| Create supplier | ✓ | ✓ | ✗ |
| Update supplier | ✓ | ✓ | ✗ |
| Delete supplier | ✓ | ✗ (needs admin) | ✗ |
| View suppliers | ✓ | ✓ | ✓ |
| **Employees** | | | |
| Create employee | ✓ | ✓ | ✗ |
| Update employee | ✓ | ✓ | ✗ |
| Delete employee | ✓ | ✗ (needs admin) | ✗ |
| View employees | ✓ | ✓ | ✓ |

---

## API Endpoints Summary

### Base URL
```
http://localhost:5000/api
```

### Authentication (`/api/auth`)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/register` | POST | Register new user |
| `/login` | POST | Login, returns token |
| `/me` | GET | Get current user |
| `/refresh-token` | POST | Refresh token |

### Branches (`/api/branches`)
| Endpoint | Method | Description | Access |
|----------|--------|-------------|--------|
| `/` | GET | List branches | all |
| `/` | POST | Create branch | admin, manager |
| `/<id>` | GET | Get branch | all |
| `/<id>` | PUT | Update branch | admin, manager |
| `/<id>` | DELETE | Delete branch | admin, manager |

### Products (`/api/products`)
| Endpoint | Method | Description | Access |
|----------|--------|-------------|--------|
| `/` | GET | List products | all |
| `/` | POST | Create product | admin, manager |
| `/<id>` | GET | Get product | all |
| `/<id>` | PUT | Update product | admin, manager |
| `/<id>` | DELETE | Delete product | admin, manager |

### Suppliers (`/api/suppliers`)
| Endpoint | Method | Description | Access |
|----------|--------|-------------|--------|
| `/` | GET | List suppliers | all |
| `/` | POST | Create supplier | admin, manager |
| `/<id>` | GET | Get supplier | all |
| `/<id>` | PUT | Update supplier | admin, manager |
| `/<id>` | DELETE | Delete supplier | admin, manager |

---

## Postman Examples

### Register Admin
```json
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

### Login
```json
POST /api/auth/login
{
    "email": "admin@example.com",
    "password": "password123"
}
```

### Create Branch
```json
POST /api/branches/
Header: Authorization: Bearer <token>
{
    "name": "Singapore Branch",
    "location": "Singapore",
    "phone": "+65432100",
    "email": "singapore@branch.com"
}
```

### Create Product
```json
POST /api/products/
Header: Authorization: Bearer <token>
{
    "name": "Maggi Noodles",
    "buying_price": 50,
    "selling_price": 80,
    "unit": "packets",
    "threshold": 10
}
```

### Create Supplier
```json
POST /api/suppliers/
Header: Authorization: Bearer <token>
{
    "name": "Acme Suppliers",
    "email": "acme@supplier.com",
    "phone": "+254700000000",
    "taking_returns": true
}
```

---

## Error Responses

All errors include detailed information:

```json
{
    "error": "Validation Error",
    "message": "Missing required fields: name",
    "details": "Missing required fields: name",
    "solution": "Provide name and buying_price"
}
```

### Common Status Codes
- `200` - Success
- `201` - Created
- `400` - Validation Error
- `401` - Unauthorized
- `403` - Forbidden (role not allowed)
- `404` - Not Found
- `409` - Conflict (duplicate)

---

## API Documentation

Visit: `http://localhost:5000/apidocs/` for Swagger UI.

---

## Project Structure

```
app/
├── auth/           # Authentication
│   ├── domain/    # User model
│   ├── repo/     # User repository
│   ├── routes/    # Auth endpoints
│   ├── schema/    # User schema
│   └── service/   # Auth service
├── branches/       # Branch management
├── products/      # Product management
├── suppliers/     # Supplier management
├── inventory/    # Inventory (future)
├── categories/   # Categories (future)
└── dashboard/   # Dashboard (future)
```

---

## Database

SQLite database is stored in `instance/kanban.db`