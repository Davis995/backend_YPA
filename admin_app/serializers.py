from rest_framework import serializers
from django.contrib.auth.models import User
from .models import (
    Category, MenuItem, ContactMessage, Booking, 
    Order, OrderItem, AdminUser
)
from .models import *
from datetime import datetime, date



class OrderMenuSerializer(serializers.ModelSerializer):
    items = serializers.SerializerMethodField()
    table = serializers.CharField(source="table.number")
    class Meta:
        model = OrderMenu
        fields= ("status","total_price","table","items")
    def get_items(self,obj):
        query =obj.ordering.all()
        return OrderMenuItemSerializers(query, many=True).data



class OrderMenuItemSerializers(serializers.ModelSerializer):
    item = serializers.CharField(source ="item.name")
    subtotal = serializers.SerializerMethodField()
    class Meta:
        model =orderMenuItem
        fields = ("item","quantity","price","special_request","subtotal")
    def get_subtotal(self,obj):
        return obj.quantity * obj.price




class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model"""
    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'image', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class MenuItemSerializer(serializers.ModelSerializer):
    """Serializer for MenuItem model"""
    categoryName = serializers.CharField(source="category.name" , read_only=True)
   
    is_available = serializers.BooleanField(default=True)  # Add this line
    
    class Meta:
        model = MenuItem
        fields = [
            'id', 'name', 'description', 'price', 'image', 
            'category', 'is_available', 
            'created_at', 'updated_at','categoryName',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    def create(self, validated_data):
        menu =MenuItem.objects.create(**validated_data)
        return menu
        


class ContactMessageSerializer(serializers.ModelSerializer):
    """Serializer for ContactMessage model"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = ContactMessage
        fields = [
            'id', 'name', 'email', 'phone', 'message', 
            'status', 'status_display', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'name', 'email', 'phone', 'date', 'time', 
            'guests', 'status', 'status_display', 'notes', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for OrderItem model"""
    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'name', 'price', 'quantity']
        read_only_fields = ['id']


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order model"""
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'customer_name', 'customer_email', 'customer_phone',
            'total', 'status', 'status_display', 'notes', 'items',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating orders with items"""
    items = OrderItemSerializer(many=True)
    
    class Meta:
        model = Order
        fields = [
            'customer_name', 'customer_email', 'customer_phone',
            'total', 'notes', 'items'
        ]
    
    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)
        
        return order


class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class AdminUserSerializer(serializers.ModelSerializer):
    """Serializer for AdminUser model"""
    user = UserSerializer(read_only=True)
    role_display = serializers.CharField(source='get_role_display', read_only=True)
    
    class Meta:
        model = AdminUser
        fields = [
            'id', 'user', 'role', 'role_display', 'phone', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']


class AdminUserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating admin users"""
    user = UserSerializer()
    
    class Meta:
        model = AdminUser
        fields = ['user', 'role', 'phone']
    
    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(**user_data)
        admin_user = AdminUser.objects.create(user=user, **validated_data)
        return admin_user


# Dashboard Statistics Serializers
class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for dashboard statistics"""
    total_categories = serializers.IntegerField()
    total_menu_items = serializers.IntegerField()
    active_bookings = serializers.IntegerField()
    pending_orders = serializers.IntegerField()
    new_messages = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=10, decimal_places=2)
    recent_bookings = BookingSerializer(many=True)
    recent_orders = OrderSerializer(many=True)


class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model"""
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    
    class Meta:
        model = Booking
        fields = [
            'id', 'name', 'email', 'phone', 'date', 'time', 
            'guests', 'status', 'status_display', 'notes', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate_name(self, value):
        """Validate name is not empty and has minimum length"""
        if not value or not value.strip():
            raise serializers.ValidationError("Name is required.")
        if len(value.strip()) < 2:
            raise serializers.ValidationError("Name must be at least 2 characters long.")
        return value.strip()

    def validate_email(self, value):
        """Validate email format"""
        if not value:
            raise serializers.ValidationError("Email is required.")
        return value

    def validate_date(self, value):
        """Validate booking date is not in the past"""
        if value < date.today():
            raise serializers.ValidationError("Booking date cannot be in the past.")
        return value

    def validate_guests(self, value):
        """Validate number of guests is within reasonable limits"""
        if value < 1:
            raise serializers.ValidationError("Minimum 1 guest is required.")
        if value > 12:
            raise serializers.ValidationError("Maximum 12 guests allowed.")
        return value

    def validate(self, data):
        """Cross-field validation"""
        # Check if booking time is reasonable (e.g., restaurant hours)
        if 'time' in data:
            booking_time = data['time']
            # Assuming restaurant is open 10:00 - 22:00
            if booking_time.hour < 10 or booking_time.hour >= 22:
                raise serializers.ValidationError({
                    'time': 'Bookings are only available between 10:00 AM and 10:00 PM.'
                })
        
        return data



