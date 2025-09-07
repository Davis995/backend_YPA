# Restaurant Admin API Documentation

This document provides detailed information about the Restaurant Admin API endpoints, including request/response examples and authentication methods.

## Base URL
```
http://localhost:8000/api/
```

## Authentication

The API uses Django's session authentication. All endpoints (except login) require authentication.

### Login
**POST** `/api/auth/login/`

Request:
```json
{
  "username": "admin",
  "password": "admin123"
}
```

Response:
```json
{
  "message": "Login successful",
  "user": {
    "id": 1,
    "username": "admin",
    "email": "admin@restaurant.com",
    "first_name": "Admin",
    "last_name": "User",
    "role": "admin",
    "role_display": "Admin"
  }
}
```

### Logout
**POST** `/api/auth/logout/`

Response:
```json
{
  "message": "Logout successful"
}
```

### Get User Profile
**GET** `/api/auth/profile/`

Response:
```json
{
  "id": 1,
  "username": "admin",
  "email": "admin@restaurant.com",
  "first_name": "Admin",
  "last_name": "User",
  "role": "admin",
  "role_display": "Admin",
  "phone": "+1234567890"
}
```

## Dashboard

### Get Dashboard Statistics
**GET** `/api/dashboard/`

Response:
```json
{
  "total_categories": 5,
  "total_menu_items": 8,
  "active_bookings": 2,
  "pending_orders": 1,
  "new_messages": 2,
  "total_revenue": "78.95",
  "recent_bookings": [
    {
      "id": 1,
      "name": "Alice Brown",
      "email": "alice@example.com",
      "phone": "+1234567893",
      "date": "2024-01-15",
      "time": "19:00:00",
      "guests": 4,
      "status": "confirmed",
      "status_display": "Confirmed",
      "notes": "Window seat preferred",
      "created_at": "2024-01-01T10:00:00Z",
      "updated_at": "2024-01-01T10:00:00Z"
    }
  ],
  "recent_orders": [
    {
      "id": 1,
      "customer_name": "David Miller",
      "customer_email": "david@example.com",
      "customer_phone": "+1234567896",
      "total": "45.97",
      "status": "delivered",
      "status_display": "Delivered",
      "notes": "Extra spicy please",
      "items": [
        {
          "id": 1,
          "menu_item": 1,
          "name": "Goat Meat Fried",
          "price": "18.99",
          "quantity": 2
        }
      ],
      "created_at": "2024-01-01T10:00:00Z",
      "updated_at": "2024-01-01T10:00:00Z"
    }
  ]
}
```

## Categories

### List Categories
**GET** `/api/categories/`

Response:
```json
[
  {
    "id": 1,
    "name": "Goat",
    "description": "Delicious goat meat dishes prepared with traditional spices",
    "image": null,
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T10:00:00Z"
  }
]
```

### Create Category
**POST** `/api/categories/`

Request:
```json
{
  "name": "Appetizers",
  "description": "Light starters and appetizers"
}
```

Response:
```json
{
  "id": 6,
  "name": "Appetizers",
  "description": "Light starters and appetizers",
  "image": null,
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z"
}
```

### Get Category
**GET** `/api/categories/{id}/`

Response:
```json
{
  "id": 1,
  "name": "Goat",
  "description": "Delicious goat meat dishes prepared with traditional spices",
  "image": null,
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z"
}
```

### Update Category
**PUT** `/api/categories/{id}/`

Request:
```json
{
  "name": "Goat Dishes",
  "description": "Updated description for goat dishes"
}
```

### Delete Category
**DELETE** `/api/categories/{id}/`

Response: `204 No Content`

## Menu Items

### List Menu Items
**GET** `/api/menu/`

Response:
```json
[
  {
    "id": 1,
    "name": "Goat Meat Fried",
    "description": "Crispy fried goat meat with aromatic spices",
    "price": "18.99",
    "image": null,
    "category": "Goat",
    "category_display": "Goat",
    "is_available": true,
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T10:00:00Z"
  }
]
```

### Create Menu Item
**POST** `/api/menu/`

Request:
```json
{
  "name": "Chicken Wings",
  "description": "Crispy chicken wings with hot sauce",
  "price": "12.99",
  "category": "Meals",
  "is_available": true
}
```

### Update Menu Item
**PUT** `/api/menu/{id}/`

Request:
```json
{
  "name": "Spicy Goat Meat Fried",
  "price": "20.99",
  "is_available": false
}
```

### Delete Menu Item
**DELETE** `/api/menu/{id}/`

Response: `204 No Content`

## Contact Messages

### List Contact Messages
**GET** `/api/contacts/`

Response:
```json
[
  {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "+1234567890",
    "message": "Do you have vegetarian options available?",
    "status": "new",
    "status_display": "New",
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T10:00:00Z"
  }
]
```

### Update Contact Message Status
**PATCH** `/api/contacts/{id}/status/`

Request:
```json
{
  "status": "handled"
}
```

Response:
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "message": "Do you have vegetarian options available?",
  "status": "handled",
  "status_display": "Handled",
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z"
}
```

## Bookings

### List Bookings
**GET** `/api/bookings/`

Response:
```json
[
  {
    "id": 1,
    "name": "Alice Brown",
    "email": "alice@example.com",
    "phone": "+1234567893",
    "date": "2024-01-15",
    "time": "19:00:00",
    "guests": 4,
    "status": "confirmed",
    "status_display": "Confirmed",
    "notes": "Window seat preferred",
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T10:00:00Z"
  }
]
```

### Update Booking Status
**PATCH** `/api/bookings/{id}/status/`

Request:
```json
{
  "status": "cancelled"
}
```

## Orders

### List Orders
**GET** `/api/orders/`

Response:
```json
[
  {
    "id": 1,
    "customer_name": "David Miller",
    "customer_email": "david@example.com",
    "customer_phone": "+1234567896",
    "total": "45.97",
    "status": "delivered",
    "status_display": "Delivered",
    "notes": "Extra spicy please",
    "items": [
      {
        "id": 1,
        "menu_item": 1,
        "name": "Goat Meat Fried",
        "price": "18.99",
        "quantity": 2
      },
      {
        "id": 2,
        "menu_item": 3,
        "name": "Chicken Rolex",
        "price": "8.99",
        "quantity": 1
      }
    ],
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T10:00:00Z"
  }
]
```

### Create Order
**POST** `/api/orders/`

Request:
```json
{
  "customer_name": "New Customer",
  "customer_email": "new@example.com",
  "customer_phone": "+1234567899",
  "total": "25.98",
  "notes": "Delivery to office",
  "items": [
    {
      "menu_item": 1,
      "name": "Goat Meat Fried",
      "price": "18.99",
      "quantity": 1
    },
    {
      "menu_item": 4,
      "name": "Fresh Juice",
      "price": "4.99",
      "quantity": 1
    }
  ]
}
```

### Update Order Status
**PATCH** `/api/orders/{id}/status/`

Request:
```json
{
  "status": "preparing"
}
```

## Admin Users

### List Admin Users
**GET** `/api/admin-users/`

Response:
```json
[
  {
    "id": 1,
    "user": {
      "id": 1,
      "username": "admin",
      "email": "admin@restaurant.com",
      "first_name": "Admin",
      "last_name": "User"
    },
    "role": "admin",
    "role_display": "Admin",
    "phone": "+1234567890",
    "created_at": "2024-01-01T10:00:00Z",
    "updated_at": "2024-01-01T10:00:00Z"
  }
]
```

### Create Admin User
**POST** `/api/admin-users/`

Request:
```json
{
  "user": {
    "username": "manager",
    "email": "manager@restaurant.com",
    "first_name": "Manager",
    "last_name": "User"
  },
  "role": "manager",
  "phone": "+1234567891"
}
```

## File Uploads

For endpoints that support file uploads (categories and menu items), use `multipart/form-data`:

```bash
curl -X POST \
  -H "Content-Type: multipart/form-data" \
  -F "name=New Category" \
  -F "description=Category description" \
  -F "image=@/path/to/image.jpg" \
  http://localhost:8000/api/categories/
```

## Error Responses

### Validation Error (400)
```json
{
  "name": ["This field is required."],
  "price": ["A valid number is required."]
}
```

### Authentication Error (401)
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### Not Found Error (404)
```json
{
  "detail": "Not found."
}
```

### Server Error (500)
```json
{
  "error": "Internal server error"
}
```

## Status Codes

- `200` - Success
- `201` - Created
- `204` - No Content (for DELETE operations)
- `400` - Bad Request
- `401` - Unauthorized
- `404` - Not Found
- `500` - Internal Server Error

## Testing the API

You can test the API using tools like:
- **cURL**: Command-line HTTP client
- **Postman**: GUI-based API testing tool
- **Insomnia**: Modern API client
- **Django REST Framework Browsable API**: Built-in browser interface

### Example cURL Commands

```bash
# Login
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}' \
  http://localhost:8000/api/auth/login/

# Get dashboard stats
curl -X GET \
  -H "Cookie: sessionid=your_session_id" \
  http://localhost:8000/api/dashboard/

# Create a category
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Cookie: sessionid=your_session_id" \
  -d '{"name":"Desserts","description":"Sweet treats"}' \
  http://localhost:8000/api/categories/
```

## Rate Limiting

Currently, no rate limiting is implemented. For production, consider implementing rate limiting using Django REST Framework's throttling classes.

## CORS Configuration

The API is configured to allow requests from:
- `http://localhost:3000`
- `http://127.0.0.1:3000`
- `http://localhost:5173`
- `http://127.0.0.1:5173`

For production, update the CORS settings in `settings.py`.





