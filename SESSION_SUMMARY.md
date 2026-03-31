# Zoza Services - Development Session Summary

This document summarizes the key architectural explanations and improvements made during our development session on March 26, 2026.

## 1. Project Architecture & Connectivity
The project follows a professional Flask API structure:
- **`run.py`**: The entry point that initializes the app and creates database tables.
- **`app/__init__.py`**: The "Factory" where Flask, SQLAlchemy, JWT, and Blueprints are connected.
- **`app/api/`**: Contains all functional modules (Auth, Products, Inventory, etc.).
- **`app/models.py`**: Defines the database structure (Tables and Relationships).
- **`app/schemas.py`**: The "Translator" that converts database objects into clean JSON for the frontend.

## 2. User & Security Logic
- **Registration**: Located in `app/api/auth/routes.py`. It now includes strict validation for email format (regex), password strength, and specific uniqueness checks for username and email.
- **Login**: Authenticates users and issues a **JWT (JSON Web Token)**. This token acts as a digital ID card.
- **Roles**:
    - `staff`: Default role assigned at registration.
    - `admin`: Higher permission level, manually assigned in the database or by another admin.
- **Guards**: Found in `app/utils/decorators.py`. Uses `@jwt_required()` and `@admin_required()` to protect sensitive routes.

## 3. Professional Restructuring (Applied)
We upgraded the codebase from a basic structure to a professional API service:
- **Folder Rename**: Moved `app/blueprints` to `app/api`.
- **Enhanced Error Handling**: 
    - Replaced generic errors with specific feedback (e.g., "The username 'x' is already taken").
    - Added global error handlers for 404 (Not Found) and 400 (Bad Request) in `app/__init__.py`.
    - Implemented database existence checks (e.g., verifying if a `category_id` exists before creating a product).

## 4. How to Use Postman
- **Base URL**: `http://127.0.0.1:5000/api/`
- **Auth Routes**: `/api/auth/register` and `/api/auth/login`.
- **Authentication**: For protected routes, use the **Authorization** tab, select **Bearer Token**, and paste the `access_token` received during login.

---
*End of Summary*
