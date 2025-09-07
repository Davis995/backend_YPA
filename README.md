# Restaurant Admin Backend

A Django REST API backend for managing a restaurant's admin operations including menu items, bookings, orders, and customer messages.

## Features

- **Dashboard Statistics**: Real-time overview of restaurant operations
- **Menu Management**: CRUD operations for categories and menu items
- **Booking Management**: Handle table reservations and status updates
- **Order Management**: Process food orders with status tracking
- **Contact Management**: Handle customer inquiries and messages
- **Admin User Management**: Manage admin users and roles
- **Django Admin Interface**: Built-in admin panel for data management

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip (Python package installer)

### Installation

1. **Clone the repository and navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create a virtual environment:**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment:**
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run database migrations:**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create a superuser:**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the development server:**
   ```bash
   python manage.py runserver
   ```

The API will be available at `http://localhost:8000/api/`
The Django admin interface will be available at `http://localhost:8000/admin/`

## API Endpoints

### Authentication
All endpoints require authentication. Use Django's session authentication or basic authentication.

### Dashboard
- `GET /api/dashboard/` - Get dashboard statistics

### Categories
- `GET /api/categories/` - List all categories
- `POST /api/categories/` - Create a new category
- `GET /api/categories/{id}/` - Get category details
- `PUT /api/categories/{id}/` - Update category
- `DELETE /api/categories/{id}/` - Delete category

### Menu Items
- `GET /api/menu/` - List all menu items
- `POST /api/menu/` - Create a new menu item
- `GET /api/menu/{id}/` - Get menu item details
- `PUT /api/menu/{id}/` - Update menu item
- `DELETE /api/menu/{id}/` - Delete menu item

### Contact Messages
- `GET /api/contacts/` - List all contact messages
- `GET /api/contacts/{id}/` - Get contact message details
- `PUT /api/contacts/{id}/` - Update contact message
- `DELETE /api/contacts/{id}/` - Delete contact message
- `PATCH /api/contacts/{id}/status/` - Update message status

### Bookings
- `GET /api/bookings/` - List all bookings
- `GET /api/bookings/{id}/` - Get booking details
- `PUT /api/bookings/{id}/` - Update booking
- `DELETE /api/bookings/{id}/` - Delete booking
- `PATCH /api/bookings/{id}/status/` - Update booking status

### Orders
- `GET /api/orders/` - List all orders
- `POST /api/orders/` - Create a new order
- `GET /api/orders/{id}/` - Get order details
- `PUT /api/orders/{id}/` - Update order
- `DELETE /api/orders/{id}/` - Delete order
- `PATCH /api/orders/{id}/status/` - Update order status

### Admin Users
- `GET /api/admin-users/` - List all admin users
- `POST /api/admin-users/` - Create a new admin user
- `GET /api/admin-users/{id}/` - Get admin user details
- `PUT /api/admin-users/{id}/` - Update admin user
- `DELETE /api/admin-users/{id}/` - Delete admin user

## Data Models

### Category
```json
{
  "id": 1,
  "name": "Main Course",
  "description": "Delicious main dishes",
  "image": "/media/categories/main-course.jpg",
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z"
}
```

### MenuItem
```json
{
  "id": 1,
  "name": "Grilled Chicken",
  "description": "Tender grilled chicken with herbs",
  "price": "15.99",
  "image": "/media/menu/grilled-chicken.jpg",
  "category": "Meals",
  "category_display": "Meals",
  "is_available": true,
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z"
}
```

### Booking
```json
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "+1234567890",
  "date": "2024-01-15",
  "time": "19:00:00",
  "guests": 4,
  "status": "confirmed",
  "status_display": "Confirmed",
  "notes": "Window seat preferred",
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z"
}
```

### Order
```json
{
  "id": 1,
  "customer_name": "Jane Smith",
  "customer_email": "jane@example.com",
  "customer_phone": "+1234567890",
  "total": "45.97",
  "status": "preparing",
  "status_display": "Preparing",
  "notes": "Extra spicy please",
  "items": [
    {
      "id": 1,
      "menu_item": 1,
      "name": "Grilled Chicken",
      "price": "15.99",
      "quantity": 2
    }
  ],
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z"
}
```

### ContactMessage
```json
{
  "id": 1,
  "name": "Alice Johnson",
  "email": "alice@example.com",
  "phone": "+1234567890",
  "message": "Do you have vegetarian options?",
  "status": "new",
  "status_display": "New",
  "created_at": "2024-01-01T10:00:00Z",
  "updated_at": "2024-01-01T10:00:00Z"
}
```

### AdminUser
```json
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
```

## Status Values

### Booking Status
- `new` - New booking
- `confirmed` - Confirmed booking
- `cancelled` - Cancelled booking

### Order Status
- `pending` - Order pending
- `confirmed` - Order confirmed
- `preparing` - Order being prepared
- `ready` - Order ready for pickup/delivery
- `delivered` - Order delivered
- `cancelled` - Order cancelled

### Contact Message Status
- `new` - New message
- `handled` - Message handled

### Admin User Roles
- `admin` - Full admin access
- `manager` - Manager access

## File Uploads

The API supports file uploads for:
- Category images: `/media/categories/`
- Menu item images: `/media/menu/`

Use `multipart/form-data` for requests with file uploads.

## Error Handling

The API returns appropriate HTTP status codes:
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `404` - Not Found
- `500` - Internal Server Error

Error responses include a message describing the issue:
```json
{
  "error": "Invalid status value"
}
```

## Development

### Running Tests
```bash
python manage.py test
```

### Creating Migrations
```bash
python manage.py makemigrations
```

### Applying Migrations
```bash
python manage.py migrate
```

### Shell Access
```bash
python manage.py shell
```

## Production Deployment

For production deployment:

1. Set `DEBUG = False` in settings.py
2. Configure a production database (PostgreSQL recommended)
3. Set up static file serving
4. Configure environment variables for sensitive data
5. Set up HTTPS
6. Configure proper CORS settings

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License.





