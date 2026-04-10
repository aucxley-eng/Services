# Entity Relationship Diagram (ERD)

## Zoza Services API - Database Schema

### Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              ZOZA SERVICES ERD                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│     ┌──────────────┐                        ┌──────────────┐                   │
│     │    users     │                        │  categories  │                   │
│     ├──────────────┤                        ├──────────────┤                   │
│     │ id (PK)      │                        │ id (PK)      │                   │
│     │ username     │                        │ name         │                   │
│     │ first_name   │                        └──────┬───────┘                   │
│     │ last_name    │                               │                           │
│     │ email        │                               │ 1:N                       │
│     │ password_hash│                               ▼                           │
│     │ role         │                      ┌──────────────┐                   │
│     │ api_key      │◄──────────           │  products    │                   │
│     │ created_at   │           N:1        ├──────────────┤                   │
│     └──────────────┘                      │ id (PK)      │                   │
│                                            │ product_id   │                   │
│                                            │ name         │                   │
│     ┌──────────────┐                      │ buying_price │                   │
│     │  branches    │                      │ selling_price│                   │
│     ├──────────────┤                      │ unit         │                   │
│     │ id (PK)      │                      │ expiry_date  │                   │
│     │ name         │                      │ threshold    │                   │
│     │ location     │                      │ category_id  │                   │
│     │ phone        │                      │ image_url    │                   │
│     └──────┬───────┘                      └──────┬───────┘                   │
│            │                                     │                           │
│     ┌─────┴─────┐                        ┌───────┴─────────┐                  │
│     ▼           ▼                        ▼                 ▼                  │
│  ┌────────┐ ┌─────────┐             ┌──────────┐   ┌──────────┐             │
│  │ stock  │ │ orders │             │ suppliers│   │ stock    │             │
│  ├────────┤ ├─────────┤             ├──────────┤   ├──────────┤             │
│  │ id(PK) │ │ id (PK) │             │ id (PK)  │   │ id (PK)  │             │
│  │product │ │product_ │             │ name     │   │product_id│             │
│  │_id(FK) │ │ id(FK)  │────────────►│ email    │   │branch_id │             │
│  │branch_ │ │supplier │             │ phone    │   │quantity  │             │
│  │id(FK)  │ │ _id(FK) │             │taking_ret│   └──────────┘             │
│  │quantity│ │branch_id│             └──────────┘        │                    │
│  └────────┘ │ quantity│                                1:1                   │
│       ▲     │ status  │                                │                    │
│       │     │order_date                              N:N                    │
│       │     └─────────┘                                │                    │
│       │             │                                  ▼                    │
│       │             │                          ┌──────────────┐             │
│       └─────────────┴──────────────────────────│  products    │             │
│                                                  └──────────────┘             │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Database Tables Detail

### 1. users
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTOINCREMENT | Unique user ID |
| username | VARCHAR(50) | UNIQUE, NOT NULL | Unique username |
| first_name | VARCHAR(50) | NOT NULL | User's first name |
| last_name | VARCHAR(50) | NOT NULL | User's last name |
| email | VARCHAR(120) | UNIQUE, NOT NULL | User's email |
| password_hash | VARCHAR(255) | NOT NULL | Hashed password |
| role | VARCHAR(20) | DEFAULT='staff' | User role (admin/manager/staff) |
| api_key | VARCHAR(64) | UNIQUE | API key for authentication |
| created_at | DATETIME | DEFAULT=CURRENT_TIMESTAMP | Account creation time |

---

### 2. branches
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTOINCREMENT | Unique branch ID |
| name | VARCHAR(100) | NOT NULL | Branch name |
| location | VARCHAR(200) | NULL | Branch location (e.g., "Singanallur, Coimbatore") |
| phone | VARCHAR(20) | NULL | Branch contact number |

**Relationships:**
- One Branch → Many Stock (1:N)
- One Branch → Many Orders (1:N)

---

### 3. categories
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTOINCREMENT | Unique category ID |
| name | VARCHAR(50) | UNIQUE, NOT NULL | Category name |

**Relationships:**
- One Category → Many Products (1:N)

---

### 4. products
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTOINCREMENT | Unique product ID |
| product_id | VARCHAR(50) | UNIQUE | SKU or barcode |
| name | VARCHAR(100) | NOT NULL | Product name |
| buying_price | FLOAT | NOT NULL | Cost price |
| selling_price | FLOAT | NULL | Retail price (for profit calculation) |
| unit | VARCHAR(20) | NULL | Unit of measurement (e.g., "kg", "pcs") |
| expiry_date | DATE | NULL | Product expiration date |
| threshold | INTEGER | DEFAULT=10 | Low stock alert threshold |
| category_id | INTEGER | FK → categories.id | Category reference |
| image_url | VARCHAR(255) | NULL | URL to product image |

**Relationships:**
- Many Products ← One Category (N:1)
- One Product → Many Stock (1:N)
- One Product → Many Orders (1:N)

---

### 5. suppliers
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTOINCREMENT | Unique supplier ID |
| name | VARCHAR(100) | NOT NULL | Supplier name |
| email | VARCHAR(120) | NULL | Supplier email |
| phone | VARCHAR(20) | NULL | Supplier phone |
| taking_returns | BOOLEAN | DEFAULT=TRUE | Whether supplier accepts returns |

**Relationships:**
- One Supplier → Many Orders (1:N)

---

### 6. stock
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTOINCREMENT | Unique stock ID |
| product_id | INTEGER | FK → products.id, NOT NULL | Product reference |
| branch_id | INTEGER | FK → branches.id, NOT NULL | Branch reference |
| quantity | INTEGER | DEFAULT=0 | Current stock quantity |

**Unique Constraint:** product_id + branch_id (UNIQUE)

**Relationships:**
- Many Stock ← One Product (N:1)
- Many Stock ← One Branch (N:1)

---

### 7. orders
| Column | Type | Constraints | Description |
|--------|------|-------------|-------------|
| id | INTEGER | PK, AUTOINCREMENT | Unique order ID |
| product_id | INTEGER | FK → products.id | Product reference |
| supplier_id | INTEGER | FK → suppliers.id | Supplier reference |
| branch_id | INTEGER | FK → branches.id | Branch reference |
| quantity | INTEGER | NULL | Order quantity |
| status | VARCHAR(20) | DEFAULT='Pending' | Order status (Pending/Confirmed/Delayed/Returned) |
| order_date | DATETIME | DEFAULT=CURRENT_TIMESTAMP | Order creation time |

**Relationships:**
- Many Orders ← One Product (N:1)
- Many Orders ← One Supplier (N:1)
- Many Orders ← One Branch (N:1)

---

## Relationship Summary Table

| From Table | To Table | Relationship | Type |
|------------|----------|--------------|------|
| User | - | Self | - |
| Category | Product | 1 Category has N Products | One-to-Many |
| Product | Stock | 1 Product has N Stock records | One-to-Many |
| Branch | Stock | 1 Branch has N Stock records | One-to-Many |
| Product | Order | 1 Product has N Orders | One-to-Many |
| Supplier | Order | 1 Supplier has N Orders | One-to-Many |
| Branch | Order | 1 Branch has N Orders | One-to-Many |

---

## Business Logic Notes

### Stock Tracking (Multi-Branch)
- Stock is tracked per **product per branch** combination
- This allows different branches to have different quantities of the same product
- Unique constraint ensures one stock record per product-branch pair

### Order Flow
- Orders link products to suppliers and branches
- Status tracks order lifecycle: Pending → Confirmed → Delayed/Returned

### Role-Based Access
- **admin**: Full access to all operations
- **manager**: Can manage products, inventory, orders
- **staff**: Limited access (typically read-only)

### API Authentication
- Users receive an API key upon registration
- API key must be included in `X-API-Key` header for protected routes
- Role-based decorators control access levels

---

## Implementation Notes

- Database: SQLite (default) / PostgreSQL (production)
- ORM: SQLAlchemy
- API Authentication: Custom API Key decorator (no JWT)
- Password Security: Werkzeug hashing (bcrypt-like)