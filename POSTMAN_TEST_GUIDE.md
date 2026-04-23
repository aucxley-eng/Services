# Postman Testing Guide - Zoza Services API

A comprehensive testing guide for all Zoza Services API endpoints using Postman.

---

## Table of Contents

1. [Setup](#setup)
2. [Authentication](#authentication)
3. [Branches](#branches)
4. [Categories](#categories)
5. [Products](#products)
6. [Suppliers](#suppliers)
7. [Inventory](#inventory)
8. [Full Test Flow](#full-test-flow)
9. [Expected HTTP Status Codes](#expected-http-status-codes)

---

## Setup

### 1. Import Collection
- Open Postman → Click **Import** → Select `zoza-services-api` or create new collection

### 2. Set Environment
- Click **Environments** → **Add** → Create `Development`
- Add variables:
  | Variable | Initial Value | Current Value |
  |----------|---------------|---------------|
  | `base_url` | `http://localhost:5000` | `http://localhost:5000` |
  | `token` | (empty) | (empty) |
  | `admin_token` | (empty) | (empty) |
  | `manager_token` | (empty) | (empty) |

### 3. Add Authorization Header
- In collection settings → **Authorization**:
  - Type: **Bearer Token**
  - Token: `{{token}}`

---

## Authentication

### Base URL
```
{{base_url}}/api/auth
```

---

### POST /register

Register a new user (Admin).

**Request**
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

**Expected Response (201)**
```json
{
    "data": {
        "id": 1,
        "username": "admin",
        "first_name": "Admin",
        "last_name": "User",
        "email": "admin@example.com",
        "role": "admin"
    },
    "message": "User registered successfully"
}
```

---

### POST /login

Login and get JWT token.

**Request**
```json
{
    "username": "admin",
    "password": "password123"
}
```

**Expected Response (200)**
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "message": "Login successful"
}
```

**Action**: Copy `access_token` to environment variable `admin_token`

---

### POST /register (Manager)

Register a manager user.

**Request**
```json
{
    "username": "manager1",
    "first_name": "John",
    "last_name": "Manager",
    "email": "manager@example.com",
    "password": "password123",
    "role": "manager"
}
```

**Action**: Login and copy token to `manager_token`

---

### POST /register (Staff)

Register a staff user.

**Request**
```json
{
    "username": "staff1",
    "first_name": "Jane",
    "last_name": "Staff",
    "email": "staff@example.com",
    "password": "password123",
    "role": "staff"
}
```

---

### GET /me

Get current user info.

**Headers**
| Key | Value |
|-----|-------|
| Authorization | Bearer `{{admin_token}}` |

**Expected Response (200)**
```json
{
    "data": {
        "id": 1,
        "username": "admin",
        "first_name": "Admin",
        "last_name": "User",
        "email": "admin@example.com",
        "role": "admin"
    },
    "message": "User details retrieved"
}
```

---

### POST /refresh-token

Refresh JWT token.

**Headers**
| Key | Value |
|-----|-------|
| Authorization | Bearer `{{admin_token}}` |

**Expected Response (200)**
```json
{
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "message": "Token refreshed successfully"
}
```

---

## Branches

### Base URL
```
{{base_url}}/api/branches
```

---

### POST / (Create Branch) - Admin Only

**Headers**
| Key | Value |
|-----|-------|
| Authorization | Bearer `{{admin_token}}` |

**Request**
```json
{
    "name": "Singanallur Branch",
    "location": "Singanallur, Coimbatore",
    "phone": "0422-123456"
}
```

**Expected Response (201)**
```json
{
    "data": {
        "id": 1,
        "name": "Singanallur Branch",
        "location": "Singanallur, Coimbatore",
        "phone": "0422-123456"
    },
    "message": "Branch created successfully"
}
```

---

### GET / (List All Branches)

**Headers**
| Key | Value |
|-----|-------|
| Authorization | Bearer `{{admin_token}}` |

**Expected Response (200)**
```json
{
    "data": [
        {
            "id": 1,
            "name": "Singanallur Branch",
            "location": "Singanallur, Coimbatore",
            "phone": "0422-123456"
        }
    ],
    "message": "Branches retrieved successfully"
}
```

---

### GET /{id} (Get Branch by ID)

**URL**: `{{base_url}}/api/branches/1`

**Headers**
| Key | Value |
|-----|-------|
| Authorization | Bearer `{{admin_token}}` |

**Expected Response (200)**
```json
{
    "data": {
        "id": 1,
        "name": "Singanallur Branch",
        "location": "Singanallur, Coimbatore",
        "phone": "0422-123456"
    },
    "message": "Branch retrieved successfully"
}
```

---

### PUT /{id} (Update Branch) - Admin Only

**URL**: `{{base_url}}/api/branches/1`

**Headers**
| Key | Value |
|-----|-------|
| Authorization | Bearer `{{admin_token}}` |

**Request**
```json
{
    "name": "Singanallur Branch Updated",
    "location": "Updated Location, Coimbatore",
    "phone": "0422-999999"
}
```

**Expected Response (200)**
```json
{
    "data": {
        "id": 1,
        "name": "Singanallur Branch Updated",
        "location": "Updated Location, Coimbatore",
        "phone": "0422-999999"
    },
    "message": "Branch updated successfully"
}
```

---

### DELETE /{id} (Delete Branch) - Admin Only

**URL**: `{{base_url}}/api/branches/1`

**Headers**
| Key | Value |
|-----|-------|
| Authorization | Bearer `{{admin_token}}` |

**Expected Response (200)**
```json
{
    "message": "Branch deleted successfully"
}
```

---

## Categories

### Base URL
```
{{base_url}}/api/categories
```

---

### POST / (Create Category) - Admin Only

**Headers**
| Key | Value |
|-----|-------|
| Authorization | Bearer `{{admin_token}}` |

**Request**
```json
{
    "name": "Food & Beverages",
    "description": "Food and beverage products"
}
```

**Expected Response (201)**
```json
{
    "data": {
        "id": 1,
        "name": "Food & Beverages",
        "description": "Food and beverage products"
    },
    "message": "Category created successfully"
}
```

---

### GET / (List All Categories)

**Headers**
| Key | Value |
|-----|-------|
| Authorization | Bearer `{{admin_token}}` |

**Expected Response (200)**
```json
{
    "data": [
        {
            "id": 1,
            "name": "Food & Beverages",
            "description": "Food and beverage products"
        }
    ],
    "message": "Categories retrieved successfully"
}
```

---

### GET /{id} (Get Category by ID)

**URL**: `{{base_url}}/api/categories/1`

**Headers**
| Key | Value |
|-----|-------|
| Authorization | Bearer `{{admin_token}}` |

**Expected Response (200)**
```json
{
    "data": {
        "id": 1,
        "name": "Food & Beverages",
        "description": "Food and beverage products"
    },
    "message": "Category retrieved successfully"
}
```

---

### PUT /{id} (Update Category) - Admin Only

**URL**: `{{base_url}}/api/categories/1`

**Headers**
| Key | Value |
|-----|-------|
| Authorization | Bearer `{{admin_token}}` |

**Request**
```json
{
    "name": "Food & Beverages Updated",
    "description": "Updated description"
}
```

**Expected Response (200)**
```json
{
    "data": {
        "id": 1,
        "name": "Food & Beverages Updated",
        "description": "Updated description"
    },
    "message": "Category updated successfully"
}
```

---

### DELETE /{id} (Delete Category) - Admin Only

**URL**: `{{base_url}}/api/categories/1`

**Headers**
| Key | Value |
|-----|-------|
| Authorization | Bearer `{{admin_token}}` |

**Expected Response (200)**
```json
{
    "message": "Category deleted successfully"
}
```

---

## Products

### Base URL
```
{{base_url}}/api/products
```

---

### POST / (Create Product) - Admin, Manager

**Headers**
| Key | Value |
|-----|-------|
| Authorization | Bearer `{{admin_token}}` |

**Request**
```json
{
    "name": "Maggi Noodles",
    "buying_price": 50,
    "selling_price": 80,
    "unit": "packets",
    "threshold": 10,
    "category_id": 1
}
```

**Expected Response (201)**
```json
{
    "data": {
        "id": 1,
        "name": "Maggi Noodles",
        "buying_price": 50,
        "selling_price": 80,
        "unit": "packets",
        "threshold": 10,
        "category_id": 1
    },
    "message": "Product created successfully"
}
```

---

### GET / (List Products with Pagination & Search)

**URL**: `{{base_url}}/api/products?page=1&per_page=10&search=maggi`

**Headers**
| Key | Value |
|-----|-------|
| Authorization | Bearer `{{admin_token}}` |

**Query Parameters**
| Parameter | Description | Example |
|-----------|-------------|----------|
| page | Page number | 1 |
| per_page | Items per page | 10 |
| search | Search by name | maggi |

**Expected Response (200)**
```json
{
    "data": [
        {
            "id": 1,
            "name": "Maggi Noodles",
            "buying_price": 50,
            "selling_price": 80,
            "unit": "packets",
            "threshold": 10,
            "category_id": 1
        }
    ],
    "message": "Products retrieved successfully"
}
```

---

### GET /{id} (Get Product by ID)

**URL**: `{{base_url}}/api/products/1`

**Headers**
| Key | Value |
|-----|-------|
| Authorization | Bearer `{{admin_token}}` |

**Expected Response (200)**
```json
{
    "data": {
        "id": 1,
        "name": "Maggi Noodles",
        "buying_price": 50,
        "selling_price": 80,
        "unit": "packets",
        "threshold": 10,
        "category_id": 1
    },
    "message": "Product retrieved successfully"
}
```

---

### PUT /{id} (Update Product) - Admin, Manager

**URL**: `{{base_url}}/api/products/1`

**Headers**
| Key | Value |
|-----|-------|
| Authorization | Bearer `{{admin_token}}` |

**Request**
```json
{
    "name": "Maggi Noodles Updated",
    "buying_price": 55,
    "selling_price": 85,
    "unit": "packets",
    "threshold": 15,
    "category_id": 1
}
```

**Expected Response (200)**
```json
{
    "data": {
        "id": 1,
        "name": "Maggi Noodles Updated",
        "buying_price": 55,
        "selling_price": 85,
        "unit": "packets",
        "threshold": 15,
        "category_id": 1
    },
    "message": "Product updated successfully"
}
```

---

### DELETE / (Delete Product) - Admin Only

**URL**: `{{base_url}}/api/products/1`

**Headers**
| Key | Value |
|-----|-------|
| Authorization | Bearer `{{admin_token}}` |

**Expected Response (200)**
```json
{
    "message": "Product deleted successfully"
}
```

---

## Suppliers

### Base URL
```
{{base_url}}/api/suppliers
```

---

### POST / (Create Supplier) - Admin, Manager

**Headers**
| Key | Value |
|-----|-------|
| Authorization | Bearer `{{admin_token}}` |

**Request**
```json
{
    "name": "Nestle India",
    "email": "contact@nestle.com",
    "phone": "1800-123-4567",
    "taking_returns": true
}
```

**Expected Response (201)**
```json
{
    "data": {
        "id": 1,
        "name": "Nestle India",
        "email": "contact@nestle.com",
        "phone": "1800-123-4567",
        "taking_returns": true
    },
    "message": "Supplier created successfully"
}
```

---

### GET / (List All Suppliers)

**Headers**
| Key | Value |
|-----|-------|
| Authorization | Bearer `{{admin_token}}` |

**Expected Response (200)**
```json
{
    "data": [
        {
            "id": 1,
            "name": "Nestle India",
            "email": "contact@nestle.com",
            "phone": "1800-123-4567",
            "taking_returns": true
        }
    ],
    "message": "Suppliers retrieved successfully"
}
```

---

### GET /{id} (Get Supplier by ID)

**URL**: `{{base_url}}/api/suppliers/1`

**Headers**
| Key | Value |
|-----|-------|
| Authorization | Bearer `{{admin_token}}` |

**Expected Response (200)**
```json
{
    "data": {
        "id": 1,
        "name": "Nestle India",
        "email": "contact@nestle.com",
        "phone": "1800-123-4567",
        "taking_returns": true
    },
    "message": "Supplier retrieved successfully"
}
```

---

### PUT /{id} (Update Supplier) - Admin, Manager

**URL**: `{{base_url}}/api/suppliers/1`

**Headers**
| Key | Value |
|-----|-------|
| Authorization | Bearer `{{admin_token}}` |

**Request**
```json
{
    "name": "Nestle India Updated",
    "email": "updated@nestle.com",
    "phone": "1800-999-9999",
    "taking_returns": false
}
```

**Expected Response (200)**
```json
{
    "data": {
        "id": 1,
        "name": "Nestle India Updated",
        "email": "updated@nestle.com",
        "phone": "1800-999-9999",
        "taking_returns": false
    },
    "message": "Supplier updated successfully"
}
```

---

### DELETE / (Delete Supplier) - Admin Only

**URL**: `{{base_url}}/api/suppliers/1`

**Headers**
| Key | Value |
|-----|-------|
| Authorization | Bearer `{{admin_token}}` |

**Expected Response (200)**
```json
{
    "message": "Supplier deleted successfully"
}
```

---

## Inventory

### Base URL
```
{{base_url}}/api/inventory
```

---

### POST /transaction (Stock In) - Admin, Manager

Add stock to inventory.

**Headers**
| Key | Value |
|-----|-------|
| Authorization | Bearer `{{admin_token}}` |

**Request**
```json
{
    "product_id": 1,
    "branch_id": 1,
    "quantity": 100,
    "type": "in",
    "reason": "Purchase from supplier",
    "notes": "Initial stock"
}
```

**Expected Response (201)**
```json
{
    "data": {
        "id": 1,
        "product_id": 1,
        "branch_id": 1,
        "quantity": 100,
        "type": "in"
    },
    "message": "Stock transaction completed successfully"
}
```

---

### POST /transaction (Stock Out) - Admin, Manager

Remove stock from inventory.

**Headers**
| Key | Value |
|-----|-------|
| Authorization | Bearer `{{admin_token}}` |

**Request**
```json
{
    "product_id": 1,
    "branch_id": 1,
    "quantity": 10,
    "type": "out",
    "reason": "Sold to customer",
    "notes": "Daily sales"
}
```

**Expected Response (201)**
```json
{
    "data": {
        "id": 2,
        "product_id": 1,
        "branch_id": 1,
        "quantity": 10,
        "type": "out"
    },
    "message": "Stock transaction completed successfully"
}
```

---

### GET /levels (Get Stock Levels)

Get current stock levels per branch.

**URL**: `{{base_url}}/api/inventory/levels?branch_id=1`

**Headers**
| Key | Value |
|-----|-------|
| Authorization | Bearer `{{admin_token}}` |

**Query Parameters**
| Parameter | Description | Example |
|-----------|-------------|----------|
| branch_id | Filter by branch (optional) | 1 |

**Expected Response (200)**
```json
{
    "data": [
        {
            "id": 1,
            "product_id": 1,
            "product_name": "Maggi Noodles",
            "branch_id": 1,
            "branch_name": "Singanallur Branch",
            "quantity": 90
        }
    ],
    "message": "Stock levels retrieved successfully"
}
```

---

### GET /low-stock (Low Stock Alerts)

Get products below threshold.

**Headers**
| Key | Value |
|-----|-------|
| Authorization | Bearer `{{admin_token}}` |

**Expected Response (200)**
```json
{
    "data": [
        {
            "product_id": 2,
            "product_name": "Low Stock Product",
            "branch_id": 1,
            "branch_name": "Singanallur Branch",
            "quantity": 3,
            "threshold": 10
        }
    ],
    "message": "Low stock products retrieved successfully"
}
```

---

### GET /history (Transaction History)

Get audit trail of all stock movements.

**URL**: `{{base_url}}/api/inventory/history?product_id=1&branch_id=1&limit=50`

**Headers**
| Key | Value |
|-----|-------|
| Authorization | Bearer `{{admin_token}}` |

**Query Parameters**
| Parameter | Description | Example |
|-----------|-------------|----------|
| product_id | Filter by product | 1 |
| branch_id | Filter by branch | 1 |
| limit | Number of records | 50 |

**Expected Response (200)**
```json
{
    "data": [
        {
            "id": 2,
            "stock_id": 1,
            "product_id": 1,
            "branch_id": 1,
            "user_id": 1,
            "quantity": 10,
            "type": "out",
            "reason": "Sold to customer",
            "notes": "Daily sales",
            "created_at": "2024-04-23T10:30:00"
        },
        {
            "id": 1,
            "stock_id": 1,
            "product_id": 1,
            "branch_id": 1,
            "user_id": 1,
            "quantity": 100,
            "type": "in",
            "reason": "Purchase from supplier",
            "notes": "Initial stock",
            "created_at": "2024-04-23T10:00:00"
        }
    ],
    "message": "Transaction history retrieved successfully"
}
```

---

## Full Test Flow

A complete end-to-end test sequence:

### Step 1: Register Users
```
POST /api/auth/register (admin)
POST /api/auth/register (manager)
POST /api/auth/register (staff)
```

### Step 2: Login (Get Tokens)
```
POST /api/auth/login (admin) → Save to admin_token
POST /api/auth/login (manager) → Save to manager_token
```

### Step 3: Create Branch (Admin only)
```
POST /api/branches/
```

### Step 4: Create Category (Admin only)
```
POST /api/categories/
```

### Step 5: Create Product (Admin/Manager)
```
POST /api/products/
```

### Step 6: Create Supplier (Admin/Manager)
```
POST /api/suppliers/
```

### Step 7: Add Stock (Admin/Manager)
```
POST /api/inventory/transaction (type: "in")
```

### Step 8: Remove Stock (Admin/Manager)
```
POST /api/inventory/transaction (type: "out")
```

### Step 9: View Stock Levels
```
GET /api/inventory/levels?branch_id=1
```

### Step 10: View Low Stock
```
GET /api/inventory/low-stock
```

### Step 11: View Transaction History
```
GET /api/inventory/history?product_id=1&branch_id=1
```

---

## Role-Based Access Tests

### Test: Staff Cannot Create Branch

**Setup**:
1. Login as staff → Get `staff_token`
2. Set Authorization to `Bearer {{staff_token}}`

**Request**:
```
POST /api/branches/
{
    "name": "Test Branch",
    "location": "Test Location"
}
```

**Expected Response (403)**
```json
{
    "error": "Access Denied",
    "message": "You do not have permission to perform this action",
    "solution": "Contact administrator for access"
}
```

### Test: Manager Cannot Delete Branch

**Request** (with manager_token):
```
DELETE /api/branches/1
```

**Expected Response (403)**
```json
{
    "error": "Access Denied",
    "message": "You do not have permission to perform this action",
    "solution": "Contact administrator for access"
}
```

---

## Expected HTTP Status Codes

| Code | Meaning | Usage |
|------|---------|-------|
| 200 | OK | GET, PUT successful |
| 201 | Created | POST successful |
| 400 | Bad Request | Validation error |
| 401 | Unauthorized | No token / Invalid token |
| 403 | Forbidden | Insufficient permissions |
| 404 | Not Found | Resource not found |
| 422 | Unprocessable Entity | Invalid data format |

---

## Error Response Format

Validation Error:
```json
{
    "error": "Validation Error",
    "message": "Missing required fields",
    "details": "buying_price is required",
    "solution": "Provide buying_price in request body"
}
```

Authentication Error:
```json
{
    "error": "Authentication Error",
    "message": "Invalid token",
    "solution": "Please login again"
}
```

Authorization Error:
```json
{
    "error": "Access Denied",
    "message": "You do not have permission to perform this action",
    "solution": "Contact administrator for access"
}
```

---

## Quick Reference Card

| Action | Method | Endpoint | Role |
|--------|--------|----------|------|
| Register | POST | `/api/auth/register` | Public |
| Login | POST | `/api/auth/login` | Public |
| Get Profile | GET | `/api/auth/me` | All |
| List Branches | GET | `/api/branches` | All |
| Create Branch | POST | `/api/branches` | Admin |
| Update Branch | PUT | `/api/branches/{id}` | Admin |
| Delete Branch | DELETE | `/api/branches/{id}` | Admin |
| List Products | GET | `/api/products` | All |
| Create Product | POST | `/api/products` | Admin, Manager |
| Update Product | PUT | `/api/products/{id}` | Admin, Manager |
| Delete Product | DELETE | `/api/products/{id}` | Admin |
| Stock In/Out | POST | `/api/inventory/transaction` | Admin, Manager |
| View Stock | GET | `/api/inventory/levels` | All |
| Low Stock | GET | `/api/inventory/low-stock` | Admin, Manager |
| History | GET | `/api/inventory/history` | Admin, Manager |

---

## Tips for Presentation

1. **Start with Login** - Show token generation first
2. **Demo Role Differences** - Show admin vs staff access
3. **Show Inventory Flow** -Stock in → View levels → Stock out → View history
4. **Use Swagger** - Point to `/apidocs/` as alternative
5. **Test Suite** - Run `pytest tests/ -v` to show 62 passing tests

Happy Testing!