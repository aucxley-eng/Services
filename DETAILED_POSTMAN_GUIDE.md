# DETAILED POSTMAN TESTING GUIDE - Step by Step Everything

This guide walks through EVERY single operation in the Zoza Services API. Each action is explained in full detail with screenshots described, exact steps, and expected responses.

---

# TABLE OF CONTENTS

1. [How to Set Up Postman](#1-how-to-set-up-postman)
2. [Admin User - Complete Walkthrough](#2-admin-user---complete-walkthrough)
3. [Manager User - Complete Walkthrough](#3-manager-user---complete-walkthrough)
4. [Staff User - Complete Walkthrough](#4-staff-user---complete-walkthrough)
5. [Testing Branches](#5-testing-branches)
6. [Testing Categories](#6-testing-categories)
7. [Testing Products](#7-testing-products)
8. [Testing Suppliers](#8-testing-suppliers)
9. [Testing Inventory](#9-testing-inventory)
10. [Common Errors and How to Fix Them](#10-common-errors-and-how-to-fix-them)

---

# STEP 1: HOW TO SET UP POSTMAN

## Step 1.1: Create a New Collection

1. Open Postman application
2. Click on **Collections** tab in the left sidebar
3. Click the **+** button or **New Collection** button
4. A new collection will be created with a default name
5. Right-click on the collection → Rename to "Zoza Services API"
6. Press Enter to save

## Step 1.2: Set Up Environment Variables

1. Click on the **Environments** tab (next to Collections)
2. Click the **+** button or **New Environment** button
3. Rename the environment to "Development"
4. You will see two columns: "Variable" and "Initial Value" / "Current Value"
5. Add the following variables:

| Variable | Initial Value | Current Value |
|----------|--------------|---------------|
| base_url | http://127.0.0.1:5000 | http://127.0.0.1:5000 |
| admin_token | (leave empty) | (leave empty) |
| manager_token | (leave empty) | (leave empty) |
| staff_token | (leave empty) | (leave empty) |
| branch_id | (leave empty) | (leave empty) |
| category_id | (leave empty) | (leave empty) |
| product_id | (leave empty) | (leave empty) |
| supplier_id | (leave empty) | (leave empty) |

6. Click the **Save** button (floppy icon) to save the environment

## Step 1.3: Select the Environment

1. In the top-right corner of Postman, you will see a dropdown that says "No Environment" or something else
2. Click on that dropdown
3. Select "Development" from the list
4. The environment is now active - you can use {{base_url}} in your requests

## Step 1.4: Set Up Authorization Header (Optional - Alternative Method)

Instead of adding the token to every request manually, you can set up default authorization:

1. Click on the "Zoza Services API" collection
2. Click the **...** (three dots) or right-click on the collection
3. Select **Edit**
4. Go to the **Authorization** tab
5. In the Type dropdown, select **Bearer Token**
6. In the Token field, type: {{admin_token}}
7. This will automatically add the Authorization header to all requests in this collection
8. Click **Save**

Note: You will need separate collections for each role, or you can manually add headers as shown in the instructions below.

---

# STEP 2: ADMIN USER - COMPLETE WALKTHROUGH

The admin user has FULL access to everything in the system. Here is every single thing an admin can do, explained step by step.

## Step 2.1: Register Admin User

### What This Does
Creates a new admin user account in the system. This is the FIRST step you must do before anything else. Without registering, you cannot login or access any protected endpoints.

### How to Do It in Postman

1. Click on the **+** button next to Collections to create a new request
2. Click on the request name and rename it to "Register Admin"
3. Next to the URL bar, make sure **POST** is selected
4. In the URL field, type: `{{base_url}}/api/auth/register`
   - It should look like: http://127.0.0.1:5000/api/auth/register
5. Click on the **Params** tab - make sure it is empty (we don't need params here)
6. Click on the **Headers** tab:
   - Under "Key", type: Content-Type
   - Under "Value", type: application/json
   - Make sure the checkbox on the left is checked
7. Click on the **Body** tab:
   - Select **raw** (click on the radio button)
   - In the dropdown that appears (which probably says "Text"), select **JSON**
8. In the large text area below, type exactly:

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

9. Click the **Send** button

### What You Should See

Look at the response area below. You should see:

```json
{
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 1,
      "username": "admin",
      "first_name": "Admin",
      "last_name": "User",
      "email": "admin@example.com",
      "role": "admin"
    }
  },
  "message": "User registered successfully"
}
```

And the status should be: **201 Created**

### Important: Copy the Token

1. In the response, find the "access_token" field
2. Copy everything inside the quotes (it starts with "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...")
3. Go to your Environment ("Development")
4. In the "Current Value" field for "admin_token", paste the token
5. Click Save

You will need this token for ALL admin requests!

---

## Step 2.2: Login as Admin

### What This Does
Login with the admin account to get a fresh JWT token. You need to login every time you want to use the API.

### How to Do It in Postman

1. Create a new request → Rename to "Login Admin"
2. Make sure **POST** is selected
3. URL: `{{base_url}}/api/auth/login`
4. Headers tab: Content-Type → application/json
5. Body tab → raw → JSON:

```json
{
  "email": "admin@example.com",
  "password": "password123"
}
```

6. Click **Send**

### What You Should See

```json
{
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    "user": {
      "id": 1,
      "username": "admin",
      "first_name": "Admin",
      "last_name": "User",
      "email": "admin@example.com",
      "role": "admin"
    }
  },
  "message": "Login successful"
}
```

Status: **200 OK**

---

## Step 2.3: Get Current Admin Profile

### What This Does
Shows the profile of the currently logged in admin user. This is useful to verify that the token is working and to see your account details.

### How to Do It in Postman

1. Create a new request → Rename to "Get My Profile"
2. Make sure **GET** is selected
3. URL: `{{base_url}}/api/auth/me`
4. Headers tab:
   - Content-Type → application/json
   - Authorization → Bearer {{admin_token}}
5. Click **Send**

### What You Should See

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

## Step 2.4: Refresh Admin Token

### What This Does
Gets a new JWT token without needing to login again. Useful if your token is about to expire.

### How to Do It in Postman

1. Create a new request → Rename to "Refresh Token"
2. Make sure **POST** is selected
3. URL: `{{base_url}}/api/auth/refresh-token`
4. Headers tab:
   - Content-Type → application/json
   - Authorization → Bearer {{admin_token}}
5. Body tab: (leave empty or just {})
6. Click **Send**

### What You Should See

```json
{
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  },
  "message": "Token refreshed successfully"
}
```

Update the admin_token in your environment with the new token!

---

## Step 2.5: Create First Branch (As Admin)

### What This Does
Creates a new branch/location. This is REQUIRED before you can add products or manage inventory. Every product must be assigned to a branch.

### How to Do It in Postman

1. Create a new request → Rename to "Create Branch - Admin"
2. Make sure **POST** is selected
3. URL: `{{base_url}}/api/branches/`
4. Headers tab:
   - Content-Type → application/json
   - Authorization → Bearer {{admin_token}}
5. Body tab → raw → JSON:

```json
{
  "name": "Main Branch",
  "location": "Coimbatore",
  "phone": "0422-123456"
}
```

6. Click **Send**

### What You Should See

```json
{
  "data": {
    "id": 1,
    "name": "Main Branch",
    "location": "Coimbatore",
    "phone": "0422-123456",
    "email": null,
    "is_active": true
  },
  "message": "Branch created successfully"
}
```

Status: **201 Created**

### Important: Save the Branch ID

1. Note the "id" value (should be 1)
2. Go to your Environment
3. Save 1 as branch_id

---

## Step 2.6: Create Second Branch (As Admin)

### What This Does
You can create multiple branches for different locations.

### How to Do It in Postman

1. Create a new request → Rename to "Create Branch 2"
2. POST to `{{base_url}}/api/branches/`
3. Headers: same as before
4. Body:

```json
{
  "name": "Second Branch",
  "location": "Chennai",
  "phone": "044-12345678"
}
```

5. Click **Send**

### What You Should See

```json
{
  "data": {
    "id": 2,
    "name": "Second Branch",
    "location": "Chennai",
    "phone": "044-12345678",
    "email": null,
    "is_active": true
  },
  "message": "Branch created successfully"
}
```

---

## Step 2.7: Get All Branches (As Admin)

### What This Does
Lists all branches in the system.

### How to Do It in Postman

1. Create a new request → Rename to "Get All Branches"
2. Make sure **GET** is selected
3. URL: `{{base_url}}/api/branches/`
4. Headers tab:
   - Content-Type → application/json
   - Authorization → Bearer {{admin_token}}
5. Click **Send**

### What You Should See

```json
{
  "data": {
    "branches": [
      {
        "id": 1,
        "name": "Main Branch",
        "location": "Coimbatore",
        "phone": "0422-123456",
        "email": null,
        "is_active": true
      },
      {
        "id": 2,
        "name": "Second Branch",
        "location": "Chennai",
        "phone": "044-12345678",
        "email": null,
        "is_active": true
      }
    ]
  },
  "message": "Branches retrieved successfully"
}
```

---

## Step 2.8: Get Single Branch by ID (As Admin)

### What This Does
Gets details of a specific branch by its ID.

### How to Do It in Postman

1. Create a new request → Rename to "Get Branch by ID"
2. GET to `{{base_url}}/api/branches/1`
3. Headers: same as before
4. Click **Send**

### What You Should See

```json
{
  "data": {
    "id": 1,
    "name": "Main Branch",
    "location": "Coimbatore",
    "phone": "0422-123456",
    "email": null,
    "is_active": true
  },
  "message": "Branch retrieved successfully"
}
```

---

## Step 2.9: Update Branch (As Admin)

### What This Does
Updates the details of an existing branch.

### How to Do It in Postman

1. Create a new request → Rename to "Update Branch"
2. Make sure **PUT** is selected
3. URL: `{{base_url}}/api/branches/1`
4. Headers: same as before
5. Body:

```json
{
  "name": "Main Branch Updated",
  "location": "Updated Coimbatore",
  "phone": "0422-999999"
}
```

6. Click **Send**

### What You Should See

```json
{
  "data": {
    "id": 1,
    "name": "Main Branch Updated",
    "location": "Updated Coimbatore",
    "phone": "0422-999999",
    "email": null,
    "is_active": true
  },
  "message": "Branch updated successfully"
}
```

---

## Step 2.10: Delete Branch (As Admin)

### What This Does
Deletes a branch permanently. Only admins can do this.

### How to Do It in Postman

1. Create a new request → Rename to "Delete Branch"
2. Make sure **DELETE** is selected
3. URL: `{{base_url}}/api/branches/2`
4. Headers: same as before
5. Click **Send**

### What You Should See

```json
{
  "message": "Branch deleted successfully"
}
```

---

## Step 2.11: Create Category (As Admin)

### What This Does
Creates a category to organize products. Products belong to categories.

### How to Do It in Postman

1. Create a new request → Rename to "Create Category - Admin"
2. Make sure **POST** is selected
3. URL: `{{base_url}}/api/categories/`
4. Headers tab:
   - Content-Type → application/json
   - Authorization → Bearer {{admin_token}}
5. Body tab → raw → JSON:

```json
{
  "name": "Food & Beverages",
  "description": "Food and beverage products"
}
```

6. Click **Send**

### What You Should See

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

Status: **201 Created**

### Important: Save the Category ID

1. Note the "id" value (should be 1)
2. Save 1 as category_id

---

## Step 2.12: Create Second Category (As Admin)

### How to Do It

1. POST to `{{base_url}}/api/categories/`
2. Body:

```json
{
  "name": "Household Items",
  "description": "Items for household use"
}
```

3. Click **Send**

---

## Step 2.13: Get All Categories (As Admin)

### How to Do It

1. GET `{{base_url}}/api/categories/`
2. Headers: admin token
3. Click **Send**

### What You Should See

```json
{
  "data": {
    "categories": [
      {
        "id": 1,
        "name": "Food & Beverages",
        "description": "Food and beverage products"
      },
      {
        "id": 2,
        "name": "Household Items",
        "description": "Items for household use"
      }
    ]
  },
  "message": "Categories retrieved successfully"
}
```

---

## Step 2.14: Get Category by ID (As Admin)

### How to Do It

1. GET `{{base_url}}/api/categories/1`
2. Click **Send**

---

## Step 2.15: Update Category (As Admin)

### How to Do It

1. PUT `{{base_url}}/api/categories/1`
2. Body:

```json
{
  "name": "Food & Beverages Updated",
  "description": "Updated description"
}
```

3. Click **Send**

---

## Step 2.16: Delete Category (As Admin)

### How to Do It

1. DELETE `{{base_url}}/api/categories/2`
2. Click **Send**

### Response

```json
{
  "message": "Category deleted successfully"
}
```

---

## Step 2.17: Create Supplier (As Admin)

### What This Does
Creates a new supplier/vendor who provides products.

### How to Do It in Postman

1. Create a new request → Rename to "Create Supplier - Admin"
2. Make sure **POST** is selected
3. URL: `{{base_url}}/api/suppliers/`
4. Headers tab:
   - Content-Type → application/json
   - Authorization → Bearer {{admin_token}}
5. Body tab → raw → JSON:

```json
{
  "name": "Nestle India",
  "email": "contact@nestle.com",
  "phone": "1800-123-4567",
  "taking_returns": true
}
```

6. Click **Send**

### What You Should See

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

### Important: Save the Supplier ID

1. Note the "id" value (should be 1)
2. Save 1 as supplier_id

---

## Step 2.18: Get All Suppliers (As Admin)

### How to Do It

1. GET `{{base_url}}/api/suppliers/`
2. Click **Send**

---

## Step 2.19: Get Supplier by ID (As Admin)

### How to Do It

1. GET `{{base_url}}/api/suppliers/1`
2. Click **Send**

---

## Step 2.20: Update Supplier (As Admin)

### How to Do It

1. PUT `{{base_url}}/api/suppliers/1`
2. Body:

```json
{
  "name": "Nestle India Updated",
  "email": "updated@nestle.com",
  "phone": "1800-999-9999",
  "taking_returns": false
}
```

3. Click **Send**

---

## Step 2.21: Delete Supplier (As Admin)

### How to Do It

1. DELETE `{{base_url}}/api/suppliers/1`
2. Click **Send**

---

## Step 2.22: Create Product (As Admin)

### What This Does
Creates a new product in the inventory system. The product needs a name, buying price, and should be linked to a category.

### How to Do It in Postman

1. Create a new request → Rename to "Create Product - Admin"
2. Make sure **POST** is selected
3. URL: `{{base_url}}/api/products/`
4. Headers tab:
   - Content-Type → application/json
   - Authorization → Bearer {{admin_token}}
5. Body tab → raw → JSON:

```json
{
  "name": "Maggi Noodles",
  "buying_price": 50,
  "selling_price": 80,
  "unit": "packets",
  "threshold": 10,
  "category_id": 1,
  "supplier_id": 1
}
```

6. Click **Send**

### What You Should See

```json
{
  "data": {
    "id": 1,
    "name": "Maggi Noodles",
    "buying_price": 50,
    "selling_price": 80,
    "unit": "packets",
    "threshold": 10,
    "category_id": 1,
    "supplier_id": 1
  },
  "message": "Product created successfully"
}
```

### Important: Save the Product ID

1. Note the "id" value (should be 1)
2. Save 1 as product_id

---

## Step 2.23: Get All Products (As Admin)

### How to Do It

1. Create a new request → Rename to "Get All Products"
2. GET `{{base_url}}/api/products/?page=1&per_page=10`
3. Headers: admin token
4. Click **Send**

### What You Should See

```json
{
  "data": {
    "products": [
      {
        "id": 1,
        "name": "Maggi Noodles",
        "buying_price": 50,
        "selling_price": 80,
        "unit": "packets",
        "threshold": 10,
        "category_id": 1,
        "supplier_id": 1
      }
    ]
  },
  "message": "Products retrieved successfully"
}
```

---

## Step 2.24: Search Products (As Admin)

### How to Do It

1. GET `{{base_url}}/api/products/?search=maggi`
2. Click **Send**

### What You Should See

Products with "maggi" in the name.

---

## Step 2.25: Get Product by ID (As Admin)

### How to Do It

1. GET `{{base_url}}/api/products/1`
2. Click **Send**

---

## Step 2.26: Update Product (As Admin)

### How to Do It

1. PUT `{{base_url}}/api/products/1`
2. Body:

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

3. Click **Send**

---

## Step 2.27: Delete Product (As Admin)

### How to Do It

1. DELETE `{{base_url}}/api/products/1`
2. Click **Send**

---

## Step 2.28: Stock In - Add Inventory (As Admin)

### What This Does
Adds stock/inventory to a product at a specific branch. This is how you record new stock received from suppliers.

### How to Do It in Postman

1. Create a new request → Rename to "Stock In - Admin"
2. Make sure **POST** is selected
3. URL: `{{base_url}}/api/inventory/transaction`
4. Headers tab:
   - Content-Type → application/json
   - Authorization → Bearer {{admin_token}}
5. Body tab → raw → JSON:

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

6. Click **Send**

### What You Should See

```json
{
  "data": {
    "transaction_id": 1,
    "message": "Stock added successfully",
    "details": {
      "product": "Maggi Noodles",
      "branch": "Main Branch",
      "previous_quantity": 0,
      "current_quantity": 100,
      "change": "+100",
      "low_stock_alert": false,
      "reason": "Purchase from supplier",
      "recorded_by": "Admin User"
    }
  },
  "message": "Stock transaction recorded"
}
```

---

## Step 2.29: Stock Out - Remove Inventory (As Admin)

### What This Does
Removes stock from inventory (e.g., when items are sold or damaged).

### How to Do It in Postman

1. Create a new request → Rename to "Stock Out - Admin"
2. POST to `{{base_url}}/api/inventory/transaction`
3. Body:

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

4. Click **Send**

### What You Should See

```json
{
  "data": {
    "transaction_id": 2,
    "message": "Stock removed successfully",
    "details": {
      "product": "Maggi Noodles",
      "branch": "Main Branch",
      "previous_quantity": 100,
      "current_quantity": 90,
      "change": "-10",
      "low_stock_alert": false,
      "reason": "Sold to customer",
      "recorded_by": "Admin User"
    }
  }
}
```

---

## Step 2.30: Get Stock Levels (As Admin)

### What This Does
Shows the current stock quantity for all products at each branch.

### How to Do It in Postman

1. Create a new request → Rename to "Get Stock Levels"
2. GET `{{base_url}}/api/inventory/levels?branch_id=1`
3. Headers: admin token
4. Click **Send**

### What You Should See

```json
{
  "data": {
    "stock_levels": [
      {
        "product_id": 1,
        "product_name": "Maggi Noodles",
        "branch_id": 1,
        "branch_name": "Main Branch",
        "quantity": 90
      }
    ]
  }
}
```

---

## Step 2.31: Get Low Stock Alerts (As Admin)

### What This Does
Shows products that are below the threshold and need restocking.

### How to Do It in Postman

1. GET `{{base_url}}/api/inventory/low-stock?branch_id=1`
2. Click **Send**

### What You Should See (if any products are low)

```json
{
  "data": {
    "low_stock_products": [
      {
        "product_id": 1,
        "product_name": "Maggi Noodles",
        "branch_id": 1,
        "branch_name": "Main Branch",
        "current_quantity": 3,
        "threshold": 10,
        "severity": "warning"
      }
    ]
  }
}
```

---

## Step 2.32: Get Transaction History (As Admin)

### What This Does
Shows the complete audit trail of all stock movements (who added/removed stock, when, how much).

### How to Do It in Postman

1. GET `{{base_url}}/api/inventory/history?product_id=1&branch_id=1&limit=50`
2. Click **Send**

### What You Should See

```json
{
  "data": {
    "transactions": [
      {
        "id": 2,
        "type": "out",
        "quantity": 10,
        "reason": "Sold to customer",
        "notes": "Daily sales",
        "created_at": "2024-04-23T10:30:00",
        "user": "Admin User"
      },
      {
        "id": 1,
        "type": "in",
        "quantity": 100,
        "reason": "Purchase from supplier",
        "notes": "Initial stock",
        "created_at": "2024-04-23T10:00:00",
        "user": "Admin User"
      }
    ]
  }
}
```

---

# STEP 3: MANAGER USER - COMPLETE WALKTHROUGH

The manager can manage products and inventory but CANNOT create or delete branches or categories.

## Step 3.1: Register Manager User

### How to Do It

1. POST to `{{base_url}}/api/auth/register`
2. Body:

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

3. Click **Send**
4. Copy the access_token and save it as manager_token in your environment

---

## Step 3.2: Login as Manager

### How to Do It

1. POST to `{{base_url}}/api/auth/login`
2. Body:

```json
{
  "email": "manager@example.com",
  "password": "password123"
}
```

3. Click **Send**

---

## Step 3.3: Manager CANNOT Create Branch

### Test This

1. Try to POST to `{{base_url}}/api/branches/`
2. Use manager_token in Authorization header
3. Body:

```json
{
  "name": "Manager Branch",
  "location": "Test"
}
```

### What You Should See

```json
{
  "error": "Forbidden",
  "message": "Access denied",
  "details": "Only admins can create branches",
  "solution": "Contact the administrator to create a new branch"
}
```

Status: **403 Forbidden**

---

## Step 3.4: Manager CANNOT Delete Branch

### Test This

1. Try to DELETE `{{base_url}}/api/branches/1` with manager token
2. You will get 403 Forbidden

---

## Step 3.5: Manager CANNOT Create Category

### Test This

1. Try to POST to `{{base_url}}/api/categories/`
2. You will get 403 Forbidden

---

## Step 3.6: Manager CANNOT Delete Category

### Test This

1. Try to DELETE `{{base_url}}/api/categories/1` with manager token
2. You will get 403 Forbidden

---

## Step 3.7: Manager CAN Create Product

### How to Do It

1. POST to `{{base_url}}/api/products/`
2. Use manager_token
3. Body:

```json
{
  "name": "Manager Product",
  "buying_price": 100,
  "selling_price": 150,
  "unit": "pcs",
  "threshold": 5
}
```

### What You Should See

```json
{
  "data": {
    "id": 2,
    "name": "Manager Product",
    "buying_price": 100,
    "selling_price": 150,
    ...
  },
  "message": "Product created successfully"
}
```

Status: **201 Created**

---

## Step 3.8: Manager CAN Update Product

### How to Do It

1. PUT to `{{base_url}}/api/products/2`
2. Body:

```json
{
  "name": "Manager Product Updated",
  "buying_price": 110
}
```

3. Click **Send**

---

## Step 3.9: Manager CANNOT Delete Product

### Test This

1. Try to DELETE `{{base_url}}/api/products/2` with manager token
2. You will get 403 Forbidden

---

## Step 3.10: Manager CAN Create Supplier

### How to Do It

1. POST to `{{base_url}}/api/suppliers/`
2. Body:

```json
{
  "name": "Manager Supplier",
  "email": "supplier@manager.com",
  "phone": "1234567890"
}
```

3. Click **Send**

---

## Step 3.11: Manager CAN Update Supplier

### How to Do It

1. PUT `{{base_url}}/api/suppliers/2`
2. Click **Send**

---

## Step 3.12: Manager CANNOT Delete Supplier

### Test This

1. Try DELETE `{{base_url}}/api/suppliers/2` with manager token
2. You will get 403 Forbidden

---

## Step 3.13: Manager CAN Do Stock Transactions

### How to Do It

1. POST to `{{base_url}}/api/inventory/transaction`
2. Body:

```json
{
  "product_id": 1,
  "branch_id": 1,
  "quantity": 50,
  "type": "in",
  "reason": "Manager adding stock"
}
```

3. Click **Send**

---

## Step 3.14: Manager CAN View Stock Levels

### How to Do It

1. GET `{{base_url}}/api/inventory/levels`
2. Click **Send**

---

## Step 3.15: Manager CAN View Low Stock

### How to Do It

1. GET `{{base_url}}/api/inventory/low-stock`
2. Click **Send**

---

## Step 3.16: Manager CAN View Transaction History

### How to Do It

1. GET `{{base_url}}/api/inventory/history`
2. Click **Send**

---

# STEP 4: STAFF USER - COMPLETE WALKTHROUGH

The staff user has the LEAST permissions - mostly read-only access.

## Step 4.1: Register Staff User

### How to Do It

1. POST to `{{base_url}}/api/auth/register`
2. Body:

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

3. Click **Send**
4. Copy the access_token and save it as staff_token

---

## Step 4.2: Login as Staff

### How to Do It

1. POST to `{{base_url}}/api/auth/login`
2. Body:

```json
{
  "email": "staff@example.com",
  "password": "password123"
}
```

3. Click **Send**

---

## Step 4.3: Staff CAN View Branches

### How to Do It

1. GET `{{base_url}}/api/branches/` with staff_token
2. Click **Send**

---

## Step 4.4: Staff CANNOT Create Branch

### Test This

1. Try POST to `{{base_url}}/api/branches/` with staff_token
2. You will get 403 Forbidden

---

## Step 4.5: Staff CAN View Products

### How to Do It

1. GET `{{base_url}}/api/products/` with staff_token
2. Click **Send**

---

## Step 4.6: Staff CANNOT Create Product

### Test This

1. Try POST to `{{base_url}}/api/products/` with staff_token
2. You will get 403 Forbidden

---

## Step 4.7: Staff CANNOT Do Stock Transactions

### Test This

1. Try POST to `{{base_url}}/api/inventory/transaction` with staff_token
2. You will get 403 Forbidden

---

## Step 4.8: Staff CAN View Stock Levels

### How to Do It

1. GET `{{base_url}}/api/inventory/levels` with staff_token
2. Click **Send**

---

## Step 4.9: Staff CANNOT View Low Stock

### Test This

1. Try GET `{{base_url}}/api/inventory/low-stock` with staff_token
2. You will get 403 Forbidden

---

## Step 4.10: Staff CANNOT View Transaction History

### Test This

1. Try GET `{{base_url}}/api/inventory/history` with staff_token
2. You will get 403 Forbidden

---

# STEP 5: TESTING BRANCHES

## Complete Branch Test Table for Admin

| Action | Method | URL | Token | Body | Success Status |
|--------|--------|-----|-------|-------|------|-------------|
| Create branch | POST | /api/branches/ | admin | {"name":"Branch","location":"City"} | 201 |
| Get all branches | GET | /api/branches/ | admin | - | 200 |
| Get branch by ID | GET | /api/branches/1 | admin | - | 200 |
| Update branch | PUT | /api/branches/1 | admin | {"name":"New"} | 200 |
| Delete branch | DELETE | /api/branches/1 | admin | - | 200 |

---

# STEP 6: TESTING CATEGORIES

## Complete Category Test Table

| Action | Method | URL | Token | Body | Success Status |
|--------|--------|-----|-------|-------|-------------|
| Create category | POST | /api/categories/ | admin | {"name":"Cat","desc":"Desc"} | 201 |
| Get all categories | GET | /api/categories/ | admin | - | 200 |
| Get category by ID | GET | /api/categories/1 | admin | - | 200 |
| Update category | PUT | /api/categories/1 | admin | {"name":"New"} | 200 |
| Delete category | DELETE | /api/categories/1 | admin | - | 200 |

---

# STEP 7: TESTING PRODUCTS

## Complete Product Test Table

| Action | Method | URL | Token | Body | Success Status |
|--------|--------|-----|-------|-------|-------------|
| Create product | POST | /api/products/ | admin/manager | {"name":"Prod","price":50} | 201 |
| Get all products | GET | /api/products/ | any | - | 200 |
| Search products | GET | /api/products/?search=name | any | - | 200 |
| Get product by ID | GET | /api/products/1 | any | - | 200 |
| Update product | PUT | /api/products/1 | admin/manager | {"name":"New"} | 200 |
| Delete product | DELETE | /api/products/1 | admin | - | 200 |

---

# STEP 8: TESTING SUPPLIERS

## Complete Supplier Test Table

| Action | Method | URL | Token | Body | Success Status |
|--------|--------|-----|-------|-------|-------------|
| Create supplier | POST | /api/suppliers/ | admin/manager | {"name":"Sup","email":"a@b"} | 201 |
| Get all suppliers | GET | /api/suppliers/ | any | - | 200 |
| Get supplier by ID | GET | /api/suppliers/1 | any | - | 200 |
| Update supplier | PUT | /api/suppliers/1 | admin/manager | {"name":"New"} | 200 |
| Delete supplier | DELETE | /api/suppliers/1 | admin | - | 200 |

---

# STEP 9: TESTING INVENTORY

## Complete Inventory Test Table

| Action | Method | URL | Token | Body | Success Status |
|--------|--------|-----|-------|-------|-------------|
| Add stock (in) | POST | /api/inventory/transaction | admin/manager | {"pid":1,"bid":1,"qty":100,"type":"in"} | 201 |
| Remove stock (out) | POST | /api/inventory/transaction | admin/manager | {"pid":1,"bid":1,"qty":10,"type":"out"} | 201 |
| Get stock levels | GET | /api/inventory/levels?branch_id=1 | any | - | 200 |
| Get low stock | GET | /api/inventory/low-stock?branch_id=1 | admin/manager | - | 200 |
| Get history | GET | /api/inventory/history?pid=1&bid=1 | admin/manager | - | 200 |

---

# STEP 10: COMMON ERRORS AND HOW TO FIX THEM

## Error 1: 422 Unprocessable Entity

### Cause
The request body is empty or not valid JSON.

### Fix
1. Go to Body tab
2. Select **raw**
3. Make sure **JSON** is selected in the dropdown (not Text)
4. Enter valid JSON in the text area

---

## Error 2: 401 Unauthorized

### Cause
No token provided or token expired.

### Fix
1. Go to Headers tab
2. Make sure Authorization header exists
3. Make sure token is correct (not expired)
4. Re-login to get a fresh token

---

## Error 3: 403 Forbidden

### Cause
User role doesn't have permission.

### Fix
1. You are trying an action your role cannot do
2. Use an admin account for that action
3. Or accept that your role cannot do that action

---

## Error 4: 404 Not Found

### Cause
Wrong URL or resource doesn't exist.

### Fix
1. Check the URL is correct
2. Check the resource ID exists

---

## Error 5: 400 Bad Request

### Cause
Missing required fields.

### Fix
1. Read the error message
2. Add the required fields to the body
3. Check field names are correct

---

# QUICK REFERENCE: ROLE PERMISSIONS

| Action | Admin | Manager | Staff |
|--------|:-----:|:-------:|:------:|
| Create Branch | ✓ | ✗ | ✗ |
| Delete Branch | ✓ | ✗ | ✗ |
| View Branch | ✓ | ✓ | ✓ |
| Create Category | ✓ | ✗ | ✗ |
| Delete Category | ✓ | ✗ | ✗ |
| View Category | ✓ | ✓ | ✓ |
| Create Product | ✓ | ✓ | ✗ |
| Update Product | ✓ | ✓ | ✗ |
| Delete Product | ✓ | ✗ | ✗ |
| View Product | ✓ | ✓ | ✓ |
| Create Supplier | ✓ | ✓ | ✗ |
| Delete Supplier | ✓ | ✗ | ✗ |
| View Supplier | ✓ | ✓ | ✓ |
| Stock In/Out | ✓ | ✓ | ✗ |
| View Stock Levels | ✓ | ✓ | ✓ |
| View Low Stock | ✓ | ✓ | ✗ |
| View History | ✓ | ✓ | ✗ |

---

# END OF DETAILED POSTMAN GUIDE