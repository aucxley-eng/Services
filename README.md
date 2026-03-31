# Zoza Services API

A Flask-based REST API for managing inventory, products, and branches.

## Features
- **Authentication**: JWT-based registration and login.
- **Product Management**: CRUD operations for products with pagination and filtering.
- **Dashboard**: Real-time statistics for inventory value and stock levels.
- **Multi-branch Support**: Track stock across different locations.

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

## Testing with Postman

### 1. Environment Setup
- **Base URL**: `http://localhost:5000/api`
- Create a Postman Environment and add a variable:
    - `baseUrl`: `http://localhost:5000/api`
    - `token`: (Leave empty, will be updated after login)

### 2. Authentication Flow

#### Register a New User
- **Method**: `POST`
- **URL**: `{{baseUrl}}/auth/register`
- **Body** (JSON):
```json
{
    "name": "John Doe",
    "email": "john@example.com",
    "password": "securepassword123"
}
```

#### Login & Get Token
- **Method**: `POST`
- **URL**: `{{baseUrl}}/auth/login`
- **Body** (JSON):
```json
{
    "email": "john@example.com",
    "password": "securepassword123"
}
```
- **Action**: Copy the `access_token` from the response.

### 3. Testing Protected Endpoints
For any request that requires authentication (Products, Dashboard, etc.):
1. Go to the **Authorization** tab in Postman.
2. Select **Type**: `Bearer Token`.
3. Paste the `access_token` into the **Token** field.

#### Create a Product
- **Method**: `POST`
- **URL**: `{{baseUrl}}/products/`
- **Body** (JSON):
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
- **Query Params**:
    - `page`: 1
    - `per_page`: 10
    - `search`: Sample (Optional)

---

## API Documentation
Once the server is running, visit:
`http://localhost:5000/apidocs/` for the interactive Swagger documentation.
