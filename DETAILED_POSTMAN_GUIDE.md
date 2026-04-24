# COMPLETE POSTMAN TESTING GUIDE - Every Detail Covered

This is the most comprehensive guide for testing the Zoza Services API. Every single detail is covered - from setting up Postman to testing all endpoints with all three roles.

---

# TABLE OF CONTENTS

1. [Understanding the Token System](#1-understanding-the-token-system)
2. [Postman Setup - Complete](#2-postman-setup---complete)
3. [How to Use Tokens in Postman](#3-how-to-use-tokens-in-postman)
4. [Admin User - Everything](#4-admin-user---everything)
5. [Manager User - Everything](#5-manager-user---everything)
6. [Staff User - Everything](#6-staff-user---everything)
7. [Testing All Endpoints](#7-testing-all-endpoints)
8. [Complete Role Permissions Table](#8-complete-role-permissions-table)
9. [Common Errors and Fixes](#9-common-errors-and-fixes)
10. [Quick Reference](#10-quick-reference)

---

# SECTION 1: UNDERSTANDING THE TOKEN SYSTEM

## What is a JWT Token?

A JWT (JSON Web Token) is a security token that proves you are logged in. Think of it like a digital ID card that expires after 1 hour.

## Why Do We Need Tokens?

Every protected endpoint requires authentication. The token tells the server:
- Who you are (user ID)
- What your role is (admin, manager, or staff)
- When your token expires

## What Happens If You Don't Use a Token?

You will get: `401 Unauthorized` - "No JWT token was provided"

## What Happens If Your Token Expires?

You will get: `401 Unauthorized` - "Token has expired"

## Solution When Token Expires

Simply login again to get a new token - it takes 2 seconds.

---

# SECTION 2: POSTMAN SETUP - COMPLETE

## Step 2.1: Create Workspace (Optional but Recommended)

1. Open Postman
2. Click on "Workspaces" in the top left
3. Click "Create Workspace"
4. Name it "Zoza Services Testing"
5. Click Create
6. Select "My Workspace" or your new workspace

## Step 2.2: Create Collection

### What is a Collection?

A collection is a folder that holds all your API requests. It makes testing organized.

### How to Create

1. Look at the left sidebar in Postman
2. Find the **Collections** tab (it has a folder icon)
3. Click the **+** button next to Collections
4. A new collection appears with a default name like "New Collection"
5. **Double-click** on the name to edit it
6. Type: `Zoza Services API`
7. Press **Enter** on your keyboard

## Step 2.3: Set Up Environment Variables

### What Are Environment Variables?

Environment variables are placeholders that you can reuse. Instead of typing `http://127.0.0.1:5000` every time, you type `{{base_url}}`.

### How to Set Up

1. In the left sidebar, find **Environments** (next to Collections)
2. Click the **+** button
3. The environment name is highlighted - type: `Development`
4. Below, you will see a table with columns: Variable, Initial Value, Current Value
5. Add these variables one by one:

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
| last_token | (leave empty) | (leave empty) |

6. Click the **Save** button (looks like a floppy disk in the top right of the environment panel)

### What Each Variable Means

| Variable | Purpose |
|----------|---------|
| base_url | The server URL (http://127.0.0.1:5000) |
| admin_token | Token for admin user |
| manager_token | Token for manager user |
| staff_token | Token for staff user |
| branch_id | ID of last created branch |
| category_id | ID of last created category |
| product_id | ID of last created product |
| supplier_id | ID of last created supplier |
| last_token | Token for current user (convenience) |

## Step 2.4: Select the Environment

1. Look at the top right of Postman
2. You will see a dropdown that might say "No Environment"
3. Click the dropdown
4. Select **Development**
5. You will know it's selected because it shows "Development" in the dropdown

## Step 2.5: Create Sub-Folders for Organization (Optional)

Inside your collection, create folders for each role:

1. Right-click on "Zoza Services API" collection
2. Click "Add Folder"
3. Name it "Admin Requests"
4. Repeat to create:
   - Admin Requests
   - Manager Requests
   - Staff Requests
   - Branches
   - Categories
   - Products
   - Suppliers
   - Inventory

This keeps everything organized.

---

# SECTION 3: HOW TO USE TOKENS IN POSTMAN

## Understanding the Authorization Header

Every protected request needs an Authorization header in this format:

```
Authorization: Bearer YOUR_ACCESS_TOKEN_HERE
```

**Breakdown:**
- `Authorization` = the header name
- `Bearer` = the type of authentication
- `YOUR_ACCESS_TOKEN_HERE` = the long string you got from login

## Method 1: Adding Token to Every Request (Manual)

### Step by Step

1. Create or open a request
2. Click on the **Headers** tab
3. Under "Key", type: `Authorization`
4. Under "Value", type: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (paste your actual token)
5. Make sure the checkbox is checked

### Important Headers for Every Request

Always add these headers for EVERY request:

| Header Key | Header Value |
|-----------|--------------|
| Content-Type | application/json |
| Authorization | Bearer YOUR_TOKEN_HERE |

## Method 2: Using Environment Variables (Recommended)

### Setting Up

1. After login, copy the `access_token` from the response
2. Go to Environments → Development
3. Click on "Current Value" for the appropriate token field
4. Paste the token
5. Click Save

### Using in Requests

Now in any request:
1. Click Headers tab
2. Under "Key": `Authorization`
3. Under "Value": `Bearer {{admin_token}}`

Postman will automatically substitute `{{admin_token}}` with your actual token.

## Method 3: Collection-Level Authorization (Auto for All Requests)

This automatically adds the token to ALL requests in the collection:

### How to Set Up

1. Right-click on "Zoza Services API" collection
2. Click **Edit**
3. Go to the **Authorization** tab
4. In the "Type" dropdown, select **Bearer Token**
5. In the "Token" field, type: `{{admin_token}}`
6. Click **Save**

Now ALL requests in this collection will have the Authorization header automatically!

### Warning

This uses ONE token for ALL requests. For testing different roles, you'll need to:
- Either create separate collections for each role
- OR use Method 1/2 and change the token manually

## Method 4: Quick Token Saving (Saves Time)

After getting a token from login:

1. Copy the token (everything in quotes after "access_token":)
2. Go to your environment
3. Paste into the appropriate token field
4. Click Save

Now you can use `{{admin_token}}` in any request.

---

## Where DOES the Token Go? (The Answer)

### Token Location Summary

| Location | What Happens |
|----------|-------------|
| Headers tab **Authorization** field | ✅ WORKS |
| Body tab | ❌ DOES NOT WORK |
| URL/Params | ❌ DOES NOT WORK |

### Correct Format

**Headers tab:**
```
Key: Authorization
Value: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJmcmVzaCI6ZmFsc2UsImlhdCI6MTc3...
```

### Wrong Formats (Do NOT Use)

❌ Token in Body:
```json
{
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "name": "Branch"
}
```

❌ Token in URL:
```
http://127.0.0.1:5000/api/branches/?token=eyJhbGciOiJIUzI1NiIs...
```

❌ No Authorization header at all

---

# SECTION 4: ADMIN USER - EVERYTHING

The admin has COMPLETE access to everything in the system.

## Prerequisites: Start Your Server

Before testing, make sure your server is running:

1. Open terminal/command prompt
2. Navigate to your project folder
3. Run: `python3 run.py`
4. Wait for: "Running on http://127.0.0.1:5000"

## Step 4.1: Register Admin (First Ever Step)

### URL
```
POST {{base_url}}/api/auth/register
```

### Headers
| Key | Value |
|-----|-------|
| Content-Type | application/json |

### Body (raw JSON)
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

### Click Send

### Expected Response (201 Created)
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

### What to Do Next
1. Copy the `access_token` from the response
2. Go to Environment → Development
3. Paste into admin_token (Current Value)
4. Click Save

---

## Step 4.2: Login as Admin

### URL
```
POST {{base_url}}/api/auth/login
```

### Headers
| Key | Value |
|-----|-------|
| Content-Type | application/json |

### Body
```json
{
  "email": "admin@example.com",
  "password": "password123"
}
```

### Click Send

### Expected Response (200 OK)
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

### Why Login Again If Already Registered?

- After server restart, old tokens are invalidated
- After 1 hour, token expires
- To get a fresh token

---

## Step 4.3: Get My Profile

### URL
```
GET {{base_url}}/api/auth/me
```

### Headers
| Key | Value |
|-----|-------|
| Content-Type | application/json |
| Authorization | Bearer {{admin_token}} |

### Click Send

### Expected Response (200 OK)
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

## Step 4.4: Refresh Token

### URL
```
POST {{base_url}}/api/auth/refresh-token
```

### Headers
| Key | Value |
|-----|-------|
| Content-Type | application/json |
| Authorization | Bearer {{admin_token}} |

### Body
(Leave empty or `{}`)

### Click Send

### Expected Response (200 OK)
```json
{
  "data": {
    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  },
  "message": "Token refreshed successfully"
}
```

### Update Your Token

1. Copy the new access_token
2. Update admin_token in your environment
3. Click Save

---

## Step 4.5: Create First Branch

### URL
```
POST {{base_url}}/api/branches/
```

### Headers
| Key | Value |
|-----|-------|
| Content-Type | application/json |
| Authorization | Bearer {{admin_token}} |

### Body
```json
{
  "name": "Main Branch",
  "location": "Coimbatore",
  "phone": "0422-123456"
}
```

### Click Send

### Expected Response (201 Created)
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

### Note the branch_id
1. Note the "id": 1
2. Save to branch_id in environment

---

## Step 4.6: Get All Branches

### URL
```
GET {{base_url}}/api/branches/
```

### Headers
| Key | Value |
|-----|-------|
| Content-Type | application/json |
| Authorization | Bearer {{admin_token}} |

### Click Send

### Expected Response (200 OK)
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
      }
    ]
  },
  "message": "Branches retrieved successfully"
}
```

---

## Step 4.7: Get Branch by ID

### URL
```
GET {{base_url}}/api/branches/1
```

### Headers
Same as before

### Click Send

---

## Step 4.8: Update Branch

### URL
```
PUT {{base_url}}/api/branches/1
```

### Headers
Same as before

### Body
```json
{
  "name": "Main Branch Updated",
  "location": "New Coimbatore",
  "phone": "0422-999999"
}
```

### Click Send

---

## Step 4.9: Delete Branch

### URL
```
DELETE {{base_url}}/api/branches/1
```

### Headers
Same as before

### Click Send

---

## Step 4.10: Create Category

### URL
```
POST {{base_url}}/api/categories/
```

### Headers
| Key | Value |
|-----|-------|
| Content-Type | application/json |
| Authorization | Bearer {{admin_token}} |

### Body
```json
{
  "name": "Food & Beverages",
  "description": "Food and drinks"
}
```

### Expected Response (201 Created)
```json
{
  "data": {
    "id": 1,
    "name": "Food & Beverages",
    "description": "Food and drinks"
  },
  "message": "Category created successfully"
}
```

### Note: Save category_id = 1

---

## Step 4.11: Get All Categories

### URL
```
GET {{base_url}}/api/categories/
```

### Headers
Admin token

### Click Send

---

## Step 4.12: Update Category

### URL
```
PUT {{base_url}}/api/categories/1
```

### Body
```json
{
  "name": "Updated Category",
  "description": "New description"
}
```

---

## Step 4.13: Delete Category

### URL
```
DELETE {{base_url}}/api/categories/1
```

---

## Step 4.14: Create Supplier

### URL
```
POST {{base_url}}/api/suppliers/
```

### Headers
Admin token

### Body
```json
{
  "name": "Nestle India",
  "email": "contact@nestle.com",
  "phone": "1800-123-4567",
  "taking_returns": true
}
```

### Note: Save supplier_id = 1

---

## Step 4.15: Get All Suppliers

### URL
```
GET {{base_url}}/api/suppliers/
```

---

## Step 4.16: Update Supplier

### URL
```
PUT {{base_url}}/api/suppliers/1
```

### Body
```json
{
  "name": "Updated Supplier",
  "email": "new@email.com"
}
```

---

## Step 4.17: Delete Supplier

### URL
```
DELETE {{base_url}}/api/suppliers/1
```

---

## Step 4.18: Create Product

### URL
```
POST {{base_url}}/api/products/
```

### Body
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

### Note: Save product_id = 1

---

## Step 4.19: Get All Products

### URL
```
GET {{base_url}}/api/products/?page=1&per_page=10
```

---

## Step 4.20: Search Products

### URL
```
GET {{base_url}}/api/products/?search=maggi
```

---

## Step 4.21: Get Product by ID

### URL
```
GET {{base_url}}/api/products/1
```

---

## Step 4.22: Update Product

### URL
```
PUT {{base_url}}/api/products/1
```

### Body
```json
{
  "name": "Updated Product",
  "buying_price": 55,
  "selling_price": 85
}
```

---

## Step 4.23: Delete Product

### URL
```
DELETE {{base_url}}/api/products/1
```

---

## Step 4.24: Stock In (Add Inventory) - Detailed

### URL
```
POST {{base_url}}/api/inventory/transaction
```

### Headers
| Key | Value |
|-----|-------|
| Content-Type | application/json |
| Authorization | Bearer {{admin_token}} |

### Body Breakdown

The body must contain these REQUIRED fields:
- product_id (which product to add stock to)
- branch_id (which branch's inventory)
- quantity (how many units)
- type (must be "in" for adding)

OPTIONAL fields:
- reason (why are we adding stock)
- notes (any additional information)

### Complete Body
```json
{
  "product_id": 1,
  "branch_id": 1,
  "quantity": 100,
  "type": "in",
  "reason": "Purchase from supplier",
  "notes": "Initial stock for new product"
}
```

### Click Send

### Expected Response (201 Created)
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

### Response Breakdown

| Field | Meaning |
|-------|---------|
| transaction_id | Unique ID for this transaction (1) |
| previous_quantity | Stock before adding (0) |
| current_quantity | Stock after adding (100) |
| change | How much added (+100) |
| low_stock_alert | true if below threshold |
| recorded_by | Who made the change |

---

## Step 4.24B: Stock In - Add More Stock

### Scenario
You already added 100 items, now you want to add 50 more.

### Body
```json
{
  "product_id": 1,
  "branch_id": 1,
  "quantity": 50,
  "type": "in",
  "reason": "Restocking",
  "notes": "Weekly order"
}
```

### Expected Response
```json
{
  "data": {
    "transaction_id": 2,
    "details": {
      "product": "Maggi Noodles",
      "branch": "Main Branch",
      "previous_quantity": 100,
      "current_quantity": 150,
      "change": "+50"
    }
  }
}
```

Notice: previous_quantity is now 100, current_quantity is 150!

---

## Step 4.25: Stock Out (Remove Inventory) - Detailed

### What This Does
Removes stock from inventory when products are sold, damaged, lost, or expired.

### URL
```
POST {{base_url}}/api/inventory/transaction
```

### Headers
| Key | Value |
|-----|-------|
| Content-Type | application/json |
| Authorization | Bearer {{admin_token}} |

### Body - REQUIRED Fields

- product_id - which product
- branch_id - which branch
- quantity - how many to remove (MUST be less than current stock!)
- type - must be "out"

### Body
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

### Click Send

### Expected Response (201 Created)
```json
{
  "data": {
    "transaction_id": 3,
    "message": "Stock removed successfully",
    "details": {
      "product": "Maggi Noodles",
      "branch": "Main Branch",
      "previous_quantity": 150,
      "current_quantity": 140,
      "change": "-10",
      "low_stock_alert": false,
      "reason": "Sold to customer",
      "recorded_by": "Admin User"
    }
  }
}
```

### Important: Stock Out Validation

❌ If you try to remove MORE than available:
```json
{
  "product_id": 1,
  "branch_id": 1,
  "quantity": 200,
  "type": "out"
}
```

You will get:
```json
{
  "error": "Error",
  "message": "Cannot remove 200 units. Only 140 available."
}
```

Status: **400 Bad Request**

---

## Step 4.26: Get Stock Levels - Detailed

### What This Shows
Current stock quantity for ALL products at ALL branches.

### URL
```
GET {{base_url}}/api/inventory/levels
```

### URL with Branch Filter
```
GET {{base_url}}/api/inventory/levels?branch_id=1
```

### Headers
| Key | Value |
|-----|-------|
| Content-Type | application/json |
| Authorization | Bearer {{admin_token}} |

### Click Send

### Expected Response (200 OK)
```json
{
  "data": {
    "stock_levels": [
      {
        "product_id": 1,
        "product_name": "Maggi Noodles",
        "branch_id": 1,
        "branch_name": "Main Branch",
        "quantity": 140
      }
    ]
  },
  "message": "Stock levels retrieved successfully"
}
```

### What Each Field Means

| Field | Value |
|-------|-------|
| product_id | 1 |
| product_name | "Maggi Noodles" |
| branch_id | 1 |
| branch_name | "Main Branch" |
| quantity | 140 (current stock) |

---

## Step 4.27: Get Low Stock Alerts - Detailed

### What This Shows
Products where quantity is at or below the threshold (default threshold is 10).

### URL
```
GET {{base_url}}/api/inventory/low-stock
```

### With Branch Filter
```
GET {{base_url}}/api/inventory/low-stock?branch_id=1
```

### Headers
Admin or Manager token required

### Click Send

### Scenario 1: No Low Stock (Good!)
```json
{
  "data": {
    "low_stock_products": []
  },
  "message": "Low stock products retrieved successfully"
}
```

### Scenario 2: Low Stock Found
```json
{
  "data": {
    "low_stock_products": [
      {
        "product_id": 1,
        "product_name": "Maggi Noodles",
        "branch_id": 1,
        "branch_name": "Main Branch",
        "current_quantity": 5,
        "threshold": 10,
        "severity": "warning"
      }
    ]
  }
}
```

### Severity Levels

| Severity | When |
|----------|------|
| warning | quantity is between 1 and threshold |
| critical | quantity is 0 |

---

## Step 4.28: Get Transaction History - Detailed

### What This Shows
Complete audit trail of all stock movements.

### URL
```
GET {{base_url}}/api/inventory/history
```

### With All Filters
```
GET {{base_url}}/api/inventory/history?product_id=1&branch_id=1&limit=50
```

### Filter Options

| Parameter | Description | Example |
|-----------|-------------|---------|
| product_id | Filter by product | 1 |
| branch_id | Filter by branch | 1 |
| stock_id | Filter by stock record | 1 |
| limit | Number of records (default 50) | 50 |

### Headers
Admin or Manager token required

### Click Send

### Expected Response
```json
{
  "data": {
    "transactions": [
      {
        "id": 3,
        "type": "out",
        "quantity": 10,
        "reason": "Sold to customer",
        "notes": "Daily sales",
        "created_at": "2024-04-23T14:30:00",
        "user": "Admin User"
      },
      {
        "id": 2,
        "type": "in",
        "quantity": 50,
        "reason": "Restocking",
        "notes": "Weekly order",
        "created_at": "2024-04-23T12:00:00",
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
  },
  "message": "Transaction history retrieved successfully"
}
```

### Transaction Fields Explained

| Field | Meaning |
|-------|---------|
| id | Transaction ID |
| type | "in" = added, "out" = removed |
| quantity | Units changed |
| reason | Why it changed |
| notes | Additional info |
| created_at | When it happened |
| user | Who made the change |

---

## Inventory Testing - Complete Scenarios

### Scenario 1: New Product - First Stock Entry

**Goal**: Add a new product and initial stock

**Step 1**: Create product (returns product_id: 2)
```
POST {{base_url}}/api/products/
Body: {"name": "New Product", "buying_price": 100}
```

**Step 2**: Add initial stock
```
POST {{base_url}}/api/inventory/transaction
Body: {
  "product_id": 2,
  "branch_id": 1,
  "quantity": 200,
  "type": "in",
  "reason": "Initial stock"
}
```

**Step 3**: Verify
```
GET {{base_url}}/api/inventory/levels?branch_id=1
```

---

### Scenario 2: Customer Purchase

**Goal**: Record a sale (removes stock)

**Step 1**: Customer buys 5 items
```
POST {{base_url}}/api/inventory/transaction
Body: {
  "product_id": 1,
  "branch_id": 1,
  "quantity": 5,
  "type": "out",
  "reason": "Sale to customer",
  "notes": "Invoice #12345"
}
```

**Step 2**: Check remaining stock
```
GET {{base_url}}/api/inventory/levels?branch_id=1
```

---

### Scenario 3: Damaged Items

**Goal**: Remove damaged stock

**Step 1**: Remove damaged items
```
POST {{base_url}}/api/inventory/transaction
Body: {
  "product_id": 1,
  "branch_id": 1,
  "quantity": 3,
  "type": "out",
  "reason": "Damaged",
  "notes": "Water damage in warehouse"
}
```

---

### Scenario 4: Stock Return from Another Branch

**Goal**: Transfer stock between branches (simulated)

**Step 1**: Remove from Branch A
```
POST {{base_url}}/api/inventory/transaction
Body: {
  "product_id": 1,
  "branch_id": 1,
  "quantity": 20,
  "type": "out",
  "reason": "Transfer to Branch B"
}
```

**Step 2**: Add to Branch B
```
POST {{base_url}}/api/inventory/transaction
Body: {
  "product_id": 1,
  "branch_id": 2,
  "quantity": 20,
  "type": "in",
  "reason": "Transfer from Branch A"
}
```

---

### Scenario 5: Check Low Stock

**Goal**: Find products needing restock

```
GET {{base_url}}/api/inventory/low-stock?branch_id=1
```

If any products show here, they are at or below threshold!

---

### Scenario 6: Audit Trail Check

**Goal**: See all movements for a product

```
GET {{base_url}}/api/inventory/history?product_id=1&branch_id=1&limit=100
```

This shows every stock change for that product at that branch!

---

## Inventory Error Cases

### Error: Product Not Found
```
Body: {"product_id": 999, "branch_id": 1, "quantity": 10, "type": "in"}
```
Response:
```json
{"error": "Error", "message": "Product with ID '999' does not exist."}
```

### Error: Branch Not Found
```
Body: {"product_id": 1, "branch_id": 999, "quantity": 10, "type": "in"}
```
Response:
```json
{"error": "Error", "message": "Branch with ID '999' does not exist."}
```

### Error: Negative Quantity
```
Body: {"product_id": 1, "branch_id": 1, "quantity": -10, "type": "in"}
```
Response:
```json
{"error": "Error", "message": "Quantity must be a positive number."}
```

### Error: Missing Type
```
Body: {"product_id": 1, "branch_id": 1, "quantity": 10}
```
Response:
```json
{"error": "Error", "message": "Missing required data: type"}
```

### Error: Invalid Type
```
Body: {"product_id": 1, "branch_id": 1, "quantity": 10, "type": "move"}
```
Response:
```json
{"error": "Error", "message": "Transaction type must be either 'in' or 'out'."}
```

### Error: Remove More Than Available
```
Body: {"product_id": 1, "branch_id": 1, "quantity": 1000, "type": "out"}
```
Response:
```json
{"error": "Error", "message": "Cannot remove 1000 units. Only 132 available."}
```

### Error: Staff Cannot Do Transaction
```
Headers: Authorization: Bearer {{staff_token}}
POST {{base_url}}/api/inventory/transaction
Body: {"product_id": 1, "branch_id": 1, "quantity": 10, "type": "in"}
```
Response:
```json
{"error": "Forbidden", "message": "Access denied", "details": "Only admins and managers can record stock transactions"}
```

---

## Inventory - Role Permissions Summary

| Action | Admin | Manager | Staff |
|--------|:-----:|:-------:|:------:|
| Stock In (add) | ✓ | ✓ | ✗ |
| Stock Out (remove) | ✓ | ✓ | ✗ |
| View Levels | ✓ | ✓ | ✓ |
| View Low Stock | ✓ | ✓ | ✗ |
| View History | ✓ | ✓ | ✗ |

---

# SECTION 5: MANAGER USER - EVERYTHING

Manager can manage products, suppliers, and inventory, but CANNOT create/delete branches or categories.

## Step 5.1: Register Manager

### URL
```
POST {{base_url}}/api/auth/register
```

### Body
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

### Save the token as manager_token

---

## Step 5.2: Login as Manager

### URL
```
POST {{base_url}}/api/auth/login
```

### Body
```json
{
  "email": "manager@example.com",
  "password": "password123"
}
```

### Save the token as manager_token

---

## Manager Inventory Testing

### Can Do Stock In
```
POST {{base_url}}/api/inventory/transaction
Headers: Manager token
Body: {
  "product_id": 1,
  "branch_id": 1,
  "quantity": 25,
  "type": "in",
  "reason": "Manager adding stock"
}
```
✅ Works - Status 201

### Can Do Stock Out
```
POST {{base_url}}/api/inventory/transaction
Body: {
  "product_id": 1,
  "branch_id": 1,
  "quantity": 5,
  "type": "out",
  "reason": "Manager sale"
}
```
✅ Works - Status 201

### Can View Stock Levels
```
GET {{base_url}}/api/inventory/levels?branch_id=1
```
✅ Works - Status 200

### Can View Low Stock
```
GET {{base_url}}/api/inventory/low-stock?branch_id=1
```
✅ Works - Status 200

### Can View History
```
GET {{base_url}}/api/inventory/history?product_id=1&branch_id=1
```
✅ Works - Status 200

---

## Manager Inventory - Cannot Do

### Cannot View Transaction History
Actually YES, manager CAN view history.

---

# SECTION 6: STAFF USER - EVERYTHING

Staff has the least permissions - mostly read-only access.

Staff has the least permissions - mostly read-only access.

## Step 6.1: Register Staff

### URL
```
POST {{base_url}}/api/auth/register
```

### Body
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

### Save the token as staff_token

---

## Step 6.2: Login as Staff

### URL
```
POST {{base_url}}/api/auth/login
```

### Body
```json
{
  "email": "staff@example.com",
  "password": "password123"
}
```

---

## Step 6.3: What Staff CAN Do

### Can View Stock Levels
```
GET {{base_url}}/api/inventory/levels?branch_id=1
Headers: staff_token
```
✅ Works - Status 200

---

## Step 6.4: What Staff CANNOT Do (Inventory)

### CANNOT Do Stock In (Add Stock)
```
POST {{base_url}}/api/inventory/transaction
Headers: staff_token
Body: {
  "product_id": 1,
  "branch_id": 1,
  "quantity": 10,
  "type": "in"
}
```
❌ 403 Forbidden - "Only admins and managers can record stock transactions"

### CANNOT Do Stock Out (Remove Stock)
```
POST {{base_url}}/api/inventory/transaction
Headers: staff_token
Body: {
  "product_id": 1,
  "branch_id": 1,
  "quantity": 5,
  "type": "out"
}
```
❌ 403 Forbidden

### CANNOT View Low Stock Alerts
```
GET {{base_url}}/api/inventory/low-stock?branch_id=1
Headers: staff_token
```
❌ 403 Forbidden

### CANNOT View Transaction History
```
GET {{base_url}}/api/inventory/history?product_id=1&branch_id=1
Headers: staff_token
```
❌ 403 Forbidden

---

# SECTION 7: TESTING ALL ENDPOINTS

## Complete Endpoint Reference Table

### Authentication Endpoints

| Method | URL | Auth Required? | Body Required | Success Status |
|--------|-----|---------------|--------------|---------------|---------------|
| POST | /api/auth/register | No | username, first_name, last_name, email, password, role | 201 |
| POST | /api/auth/login | No | email, password | 200 |
| GET | /api/auth/me | Yes (JWT) | - | 200 |
| POST | /api/auth/refresh-token | Yes (JWT) | - | 200 |

### Branch Endpoints

| Method | URL | Who Can Use | Body Required | Success Status |
|--------|-----|------------|--------------|---------------|
| GET | /api/branches/ | All users | - | 200 |
| POST | /api/branches/ | Admin only | name (required), location, phone | 201 |
| GET | /api/branches/{id} | All users | - | 200 |
| PUT | /api/branches/{id} | Admin only | name, location, phone | 200 |
| DELETE | /api/branches/{id} | Admin only | - | 200 |

### Category Endpoints

| Method | URL | Who Can Use | Body Required | Success Status |
|--------|-----|------------|--------------|---------------|
| GET | /api/categories/ | All users | - | 200 |
| POST | /api/categories/ | Admin only | name (required), description | 201 |
| GET | /api/categories/{id} | All users | - | 200 |
| PUT | /api/categories/{id} | Admin only | name, description | 200 |
| DELETE | /api/categories/{id} | Admin only | - | 200 |

### Product Endpoints

| Method | URL | Who Can Use | Body Required | Success Status |
|--------|-----|------------|--------------|---------------|
| GET | /api/products/ | All users | Query: page, per_page, search | 200 |
| POST | /api/products/ | Admin, Manager | name, buying_price (required) | 201 |
| GET | /api/products/{id} | All users | - | 200 |
| PUT | /api/products/{id} | Admin, Manager | name, prices, etc. | 200 |
| DELETE | /api/products/{id} | Admin only | - | 200 |

### Supplier Endpoints

| Method | URL | Who Can Use | Body Required | Success Status |
|--------|-----|------------|--------------|---------------|
| GET | /api/suppliers/ | All users | - | 200 |
| POST | /api/suppliers/ | Admin, Manager | name (required), email, phone | 201 |
| GET | /api/suppliers/{id} | All users | - | 200 |
| PUT | /api/suppliers/{id} | Admin, Manager | name, email, phone | 200 |
| DELETE | /api/suppliers/{id} | Admin only | - | 200 |

### Inventory Endpoints

| Method | URL | Who Can Use | Body Required | Success Status |
|--------|-----|------------|--------------|---------------|
| POST | /api/inventory/transaction | Admin, Manager | product_id, branch_id, quantity, type (in/out) | 201 |
| GET | /api/inventory/levels | All users | Query: branch_id (optional) | 200 |
| GET | /api/inventory/low-stock | Admin, Manager | Query: branch_id (optional) | 200 |
| GET | /api/inventory/history | Admin, Manager | Query: product_id, branch_id, limit | 200 |

---

# SECTION 8: COMPLETE ROLE PERMISSIONS TABLE

| Action | Admin | Manager | Staff |
|--------|:-----:|:-------:|:------:|
| **Branches** | | | |
| View branches | ✓ | ✓ | ✓ |
| Create branch | ✓ | ✗ | ✗ |
| Update branch | ✓ | ✗ | ✗ |
| Delete branch | ✓ | ✗ | ✗ |
| **Categories** | | | |
| View categories | ✓ | ✓ | ✓ |
| Create category | ✓ | ✗ | ✗ |
| Update category | ✓ | ✗ | ✗ |
| Delete category | ✓ | ✗ | ✗ |
| **Products** | | | |
| View products | ✓ | ✓ | ✓ |
| Create product | ✓ | ✓ | ✗ |
| Update product | ✓ | ✓ | ✗ |
| Delete product | ✓ | ✗ | ✗ |
| **Suppliers** | | | |
| View suppliers | ✓ | ✓ | ✓ |
| Create supplier | ✓ | ✓ | ✗ |
| Update supplier | ✓ | ✓ | ✗ |
| Delete supplier | ✓ | ✗ | ✗ |
| **Inventory** | | | |
| View stock levels | ✓ | ✓ | ✓ |
| Stock in (add) | ✓ | ✓ | ✗ |
| Stock out (remove) | ✓ | ✓ | ✗ |
| View low stock | ✓ | ✓ | ✗ |
| View history | ✓ | ✓ | ✗ |

---

# SECTION 9: COMMON ERRORS AND FIXES

## Error 1: 422 Unprocessable Entity

### Cause
Request body is empty or not valid JSON.

### Fix Step by Step
1. Click **Body** tab
2. Select **raw** radio button
3. In the dropdown, select **JSON** (not Text)
4. Enter valid JSON in the text area
5. Make sure all JSON syntax is correct (commas, quotes)

---

## Error 2: 401 Unauthorized - "No JWT token was provided"

### Cause
No Authorization header or it's missing.

### Fix Step by Step
1. Click **Headers** tab
2. Check if "Authorization" header exists
3. If not, add it:
   - Key: `Authorization`
   - Value: `Bearer {{admin_token}}`
4. Make sure the checkbox is checked

---

## Error 3: 401 Unauthorized - "Token has expired"

### Cause
Token is older than 1 hour.

### Fix Step by Step
1. POST to `/api/auth/login`
2. Use email and password
3. Copy the new access_token
4. Update your environment variable
5. Click Save

---

## Error 4: 403 Forbidden - "Access denied"

### Cause
Your role doesn't have permission for this action.

### Possible Causes
- You're logged in as staff but trying to create a branch
- You're logged in as manager but trying to delete something

### Fix Step by Step
1. Login with an admin account
2. Copy the admin_token
3. Use that token for the request

---

## Error 5: 404 Not Found - "Route not found"

### Cause
Wrong URL or endpoint doesn't exist.

### Fix Step by Step
1. Check the URL is correct
2. Check spelling
3. Make sure you're using the right HTTP method (GET, POST, PUT, DELETE)

---

## Error 6: 400 Bad Request - "Missing required fields"

### Cause
Required fields not in request body.

### Fix Step by Step
1. Read the error message
2. Add the missing fields to your JSON body
3. Check field names are correct

---

## Error 7: 400 Bad Request - "Validation Error"

### Cause
Invalid data in request body.

### Fix Step by Step
1. Check the details in the response
2. Fix the data format
3. Example: "buying_price is required" - add buying_price to body

---

# SECTION 10: QUICK REFERENCE

## How to Test (Quick Steps)

### 1. Always Start Server
```bash
python3 run.py
```

### 2. Register First User (Admin)
- POST /api/auth/register with role: "admin"

### 3. Login to Get Token
- POST /api/auth/login

### 4. Copy Token
- Go to Environment → Paste to admin_token → Save

### 5. Test Protected Endpoints
- Add Headers: Authorization: Bearer {{admin_token}}

---

## Token Flow Summary

```
Register → Get Token → Save Token → Use Token in Headers → (1 hour later) → Login Again → Get New Token
```

---

## Headers Checklist (Every Request)

Before clicking Send, verify:

- [ ] Content-Type: application/json
- [ ] Authorization: Bearer {{token}}
- [ ] Checkbox is checked for both

---

## Body Checklist (For POST/PUT)

- [ ] Body tab selected
- [ ] raw selected
- [ ] JSON selected in dropdown
- [ ] Valid JSON in text area

---

## Quick Test Order

1. Register admin → get admin_token
2. Login → get fresh token
3. Create branch → save branch_id
4. Create category → save category_id
5. Create supplier → save supplier_id
6. Create product → save product_id
7. Stock in
8. Stock out
9. View levels
10. View history

---

# END OF COMPREHENSIVE GUIDE