#!/usr/bin/env python
"""
Script to populate the database with sample data for the restaurant admin system.
Run this after creating migrations and applying them.
"""

import os
import django
from datetime import date, time
from decimal import Decimal

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'restaurant_admin.settings')
django.setup()

from django.contrib.auth.models import User
from admin_app.models import (
    Category, MenuItem, ContactMessage, Booking, 
    Order, OrderItem, AdminUser
)


def create_sample_data():
    """Create sample data for the restaurant admin system"""
    
    print("Creating sample data...")
    
    # Create admin user
    admin_user, created = User.objects.get_or_create(
        username='admin',
        defaults={
            'email': 'admin@restaurant.com',
            'first_name': 'Admin',
            'last_name': 'User',
            'is_staff': True,
            'is_superuser': True
        }
    )
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print(f"Created admin user: {admin_user.username}")
    
    # Create admin user profile
    admin_profile, created = AdminUser.objects.get_or_create(
        user=admin_user,
        defaults={
            'role': 'admin',
            'phone': '+1234567890'
        }
    )
    if created:
        print(f"Created admin profile for: {admin_user.username}")
    
    # Create categories
    categories_data = [
        {'name': 'Goat', 'description': 'Delicious goat meat dishes prepared with traditional spices'},
        {'name': 'Meals', 'description': 'Hearty main course meals for lunch and dinner'},
        {'name': 'Drinks', 'description': 'Refreshing beverages and soft drinks'},
        {'name': 'Desserts', 'description': 'Sweet treats and desserts to end your meal'},
        {'name': 'Tea', 'description': 'Hot and cold tea varieties'}
    ]
    
    categories = []
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data['name'],
            defaults=cat_data
        )
        categories.append(category)
        if created:
            print(f"Created category: {category.name}")
    
    # Map category IDs for menu items
    category_map = {1: categories[0], 2: categories[1], 3: categories[2], 4: categories[3], 5: categories[4]}
    
    # Create menu items
    menu_items_data = [
        {'name': 'Goat Meat Fried', 'description': 'Crispy fried goat meat with aromatic spices', 'price': Decimal('18.99'), 'category': category_map[1]},
        {'name': 'Goat Meat Boiled', 'description': 'Tender boiled goat meat with herbs', 'price': Decimal('16.99'), 'category': category_map[1]},
        {'name': 'Chicken Rolex', 'description': 'Delicious chicken wrapped in chapati with vegetables', 'price': Decimal('8.99'), 'category': category_map[2]},
        {'name': 'Beef Steak', 'description': 'Grilled beef steak with mashed potatoes', 'price': Decimal('22.99'), 'category': category_map[2]},
        {'name': 'Fresh Juice', 'description': 'Freshly squeezed fruit juice', 'price': Decimal('4.99'), 'category': category_map[3]},
        {'name': 'Coffee', 'description': 'Hot brewed coffee', 'price': Decimal('3.99'), 'category': category_map[3]},
        {'name': 'Chocolate Cake', 'description': 'Rich chocolate cake with cream', 'price': Decimal('6.99'), 'category': category_map[4]},
        {'name': 'Green Tea', 'description': 'Refreshing green tea', 'price': Decimal('2.99'), 'category': category_map[5]},
    ]
    
    menu_items = []
    for item_data in menu_items_data:
        menu_item, created = MenuItem.objects.get_or_create(
            name=item_data['name'],
            defaults=item_data
        )
        menu_items.append(menu_item)
        if created:
            print(f"Created menu item: {menu_item.name}")
    
    # Create contact messages
    contact_messages_data = [
        {'name': 'John Doe', 'email': 'john@example.com', 'phone': '+1234567890', 'message': 'Do you have vegetarian options available?', 'status': 'new'},
        {'name': 'Jane Smith', 'email': 'jane@example.com', 'phone': '+1234567891', 'message': 'What are your opening hours?', 'status': 'handled'},
        {'name': 'Mike Johnson', 'email': 'mike@example.com', 'phone': '+1234567892', 'message': 'Do you offer delivery services?', 'status': 'new'}
    ]
    
    for msg_data in contact_messages_data:
        message, created = ContactMessage.objects.get_or_create(
            email=msg_data['email'],
            defaults=msg_data
        )
        if created:
            print(f"Created contact message from: {message.name}")
    
    # Create bookings
    bookings_data = [
        {'name': 'Alice Brown', 'email': 'alice@example.com', 'phone': '+1234567893', 'date': date(2024, 1, 15), 'time': time(19, 0), 'guests': 4, 'status': 'confirmed', 'notes': 'Window seat preferred'},
        {'name': 'Bob Wilson', 'email': 'bob@example.com', 'phone': '+1234567894', 'date': date(2024, 1, 16), 'time': time(20, 0), 'guests': 2, 'status': 'new', 'notes': 'Anniversary celebration'},
        {'name': 'Carol Davis', 'email': 'carol@example.com', 'phone': '+1234567895', 'date': date(2024, 1, 14), 'time': time(18, 30), 'guests': 6, 'status': 'cancelled', 'notes': 'Large group booking'}
    ]
    
    for booking_data in bookings_data:
        booking, created = Booking.objects.get_or_create(
            email=booking_data['email'],
            date=booking_data['date'],
            time=booking_data['time'],
            defaults=booking_data
        )
        if created:
            print(f"Created booking for: {booking.name}")
    
    # Create orders
    orders_data = [
        {'customer_name': 'David Miller', 'customer_email': 'david@example.com', 'customer_phone': '+1234567896', 'total': Decimal('45.97'), 'status': 'delivered', 'notes': 'Extra spicy please'},
        {'customer_name': 'Emma Taylor', 'customer_email': 'emma@example.com', 'customer_phone': '+1234567897', 'total': Decimal('32.98'), 'status': 'preparing', 'notes': 'No onions'},
        {'customer_name': 'Frank Anderson', 'customer_email': 'frank@example.com', 'customer_phone': '+1234567898', 'total': Decimal('28.97'), 'status': 'pending', 'notes': 'Quick delivery needed'}
    ]
    
    for order_data in orders_data:
        order, created = Order.objects.get_or_create(
            customer_email=order_data['customer_email'],
            defaults=order_data
        )
        if created:
            print(f"Created order for: {order.customer_name}")
            
            # Add order items
            if order.customer_name == 'David Miller':
                OrderItem.objects.create(order=order, menu_item=menu_items[0], name=menu_items[0].name, price=menu_items[0].price, quantity=2)
                OrderItem.objects.create(order=order, menu_item=menu_items[2], name=menu_items[2].name, price=menu_items[2].price, quantity=1)
            elif order.customer_name == 'Emma Taylor':
                OrderItem.objects.create(order=order, menu_item=menu_items[1], name=menu_items[1].name, price=menu_items[1].price, quantity=1)
                OrderItem.objects.create(order=order, menu_item=menu_items[4], name=menu_items[4].name, price=menu_items[4].price, quantity=2)
            elif order.customer_name == 'Frank Anderson':
                OrderItem.objects.create(order=order, menu_item=menu_items[3], name=menu_items[3].name, price=menu_items[3].price, quantity=1)
                OrderItem.objects.create(order=order, menu_item=menu_items[5], name=menu_items[5].name, price=menu_items[5].price, quantity=1)
    
    print("\nSample data creation completed!")
    print(f"Created {Category.objects.count()} categories")
    print(f"Created {MenuItem.objects.count()} menu items")
    print(f"Created {ContactMessage.objects.count()} contact messages")
    print(f"Created {Booking.objects.count()} bookings")
    print(f"Created {Order.objects.count()} orders")
    print(f"Created {AdminUser.objects.count()} admin users")
    print("\nAdmin login credentials:")
    print("Username: admin")
    print("Password: admin123")


if __name__ == '__main__':
    create_sample_data()
