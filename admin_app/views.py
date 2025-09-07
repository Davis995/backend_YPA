from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Q
from django.utils import timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from datetime import timedelta
from rest_framework.parsers import MultiPartParser, FormParser
from .models import (
    Category, MenuItem, ContactMessage, Booking, 
    Order, OrderItem, AdminUser
    
)
from .models import *
from .serializers import *


class MenuOrder(APIView):
    def get(self,request):
        query = OrderMenu.objects.all()
        serializer = OrderMenuSerializer(query, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

class CartManagement(APIView):
    def post(self,request):

        data = request.data
        print(data)
        get_table_query = Table.objects.get(number=data["table_id"])
        if get_table_query:
           order = OrderMenu.objects.create(total_price = data["total_amount"],
                                     table=get_table_query,status=data["status"]                               )
        for  item in data["items"]:
            get_item = MenuItem.objects.get(id=item["menu_item_id"])
            price = float(item["price"])
            orderMenuItem.objects.create(
            ordermenu = order,item=get_item,quantity=item["quantity"],price=price,special_request=item["special_requests"]
            )
        print(get_table_query)

        return Response({"status":True},status=status.HTTP_200_OK)





class LoginView(APIView):
    """API view for user login"""
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        print(username)
        if not username or not password:
            return Response(
                {'error': 'Username and password are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user = authenticate(username=username, password=password)
        
        if user is not None:
            login(request, user)
            try:
                admin_user = AdminUser.objects.get(user=user)
                return Response({
                    'message': 'Login successful',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'role': admin_user.role,
                        'role_display': admin_user.get_role_display()
                    }
                })
            except AdminUser.DoesNotExist:
                return Response({
                    'message': 'Login successful',
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'role': 'admin',
                        'role_display': 'Admin'
                    }
                })
        else:
            return Response(
                {'error': 'Invalid credentials'}, 
                status=status.HTTP_401_UNAUTHORIZED
            )


class LogoutView(APIView):
    """API view for user logout"""
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({'message': 'Logout successful'})


class UserProfileView(APIView):
    """API view for getting and updating current user profile"""
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        try:
            admin_user = AdminUser.objects.get(user=user)
            return Response({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': admin_user.role,
                'role_display': admin_user.get_role_display(),
                'phone': admin_user.phone
            })
        except AdminUser.DoesNotExist:
            return Response({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': 'admin',
                'role_display': 'Admin',
                'phone': ''
            })

    def put(self, request):
        user = request.user
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')
        email = request.data.get('email', '')
        
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save()
        
        try:
            admin_user = AdminUser.objects.get(user=user)
            return Response({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': admin_user.role,
                'role_display': admin_user.get_role_display(),
                'phone': admin_user.phone
            })
        except AdminUser.DoesNotExist:
            return Response({
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'role': 'admin',
                'role_display': 'Admin',
                'phone': ''
            })


class ChangePasswordView(APIView):
    """API view for changing user password"""
    # permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        old_password = request.data.get('old_password')
        new_password = request.data.get('new_password')
        
        if not old_password or not new_password:
            return Response(
                {'error': 'Old password and new password are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if not user.check_password(old_password):
            return Response(
                {'error': 'Current password is incorrect'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(new_password)
        user.save()
        
        return Response({'message': 'Password changed successfully'})


class DashboardStatsView(APIView):
    """API view for dashboard statistics"""
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        # Calculate statistics
        total_categories = Category.objects.count()
        total_menu_items = MenuItem.objects.count()
        
        # Active bookings (new or confirmed)
        active_bookings = Booking.objects.filter(
            status__in=['new', 'confirmed']
        ).count()
        
        # Pending orders (pending or confirmed)
        pending_orders = Order.objects.filter(
            status__in=['pending', 'confirmed']
        ).count()
        
        # New messages
        new_messages = ContactMessage.objects.filter(status='new').count()
        
        # Total revenue
        total_revenue = Order.objects.filter(
            status__in=['delivered', 'ready']
        ).aggregate(total=Sum('total'))['total'] or 0
        
        # Recent bookings (last 5)
        recent_bookings = Booking.objects.all()[:5]
        
        # Recent orders (last 5)
        recent_orders = Order.objects.all()[:5]
        
        data = {
            'total_categories': total_categories,
            'total_menu_items': total_menu_items,
            'active_bookings': active_bookings,
            'pending_orders': pending_orders,
            'new_messages': new_messages,
            'total_revenue': total_revenue,
            'recent_bookings': BookingSerializer(recent_bookings, many=True).data,
            'recent_orders': OrderSerializer(recent_orders, many=True).data,
        }
        
        serializer = DashboardStatsSerializer(data)
        return Response(serializer.data)


# Category Views
class CategoryListView(APIView):
    """API view for listing and creating categories"""
    # permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]  # <--- important

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():

            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryDetailView(APIView):
    """API view for retrieving, updating and deleting categories"""
    # permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, pk):
        return get_object_or_404(Category, pk=pk)

    def get(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data)

    def put(self, request, pk):
        category = self.get_object(pk)
        serializer = CategorySerializer(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Menu Item Views
class MenuItemListView(APIView):
    """API view for listing and creating menu items"""
    # permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        menu_items = MenuItem.objects.all()
        serializer = MenuItemSerializer(menu_items, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = MenuItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MenuItemDetailView(APIView):
    """API view for retrieving, updating and deleting menu items"""
    # permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self, pk):
        return get_object_or_404(MenuItem, pk=pk)

    def get(self, request, pk):
        menu_item = self.get_object(pk)
        serializer = MenuItemSerializer(menu_item)
        return Response(serializer.data)

    def put(self, request, pk):
        menu_item = self.get_object(pk)
        serializer = MenuItemSerializer(menu_item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        menu_item = self.get_object(pk)
        menu_item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# Contact Message Views
class ContactMessageListView(APIView):
    """API view for listing contact messages"""
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        messages = ContactMessage.objects.all()
        serializer = ContactMessageSerializer(messages, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        """Create a new contact message"""
        try:
            serializer = ContactMessageSerializer(data=request.data)
            if serializer.is_valid():
                # Save the contact message
                contact_message = serializer.save()
                
                # Return the created message with success response
                return Response(
                    {
                        'message': 'Contact message sent successfully!',
                        'data': ContactMessageSerializer(contact_message).data
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                # Return validation errors
                return Response(
                    {
                        'error': 'Validation failed',
                        'errors': serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            # Handle unexpected errors
            return Response(
                {
                    'error': 'Failed to create contact message',
                    'detail': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )











class ContactMessageDetailView(APIView):
    """API view for retrieving, updating and deleting contact messages"""
    # permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(ContactMessage, pk=pk)

    def get(self, request, pk):
        message = self.get_object(pk)
        serializer = ContactMessageSerializer(message)
        return Response(serializer.data)

    def put(self, request, pk):
        message = self.get_object(pk)
        serializer = ContactMessageSerializer(message, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        message = self.get_object(pk)
        message.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class ContactMessageStatusView(APIView):
    """API view for updating contact message status"""
    # permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        message = get_object_or_404(ContactMessage, pk=pk)
        status_value = request.data.get('status')
        
        if status_value not in ['new', 'handled']:
            return Response(
                {'error': 'Invalid status'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        message.status = status_value
        message.save()
        serializer = ContactMessageSerializer(message)
        return Response(serializer.data)


# Booking Views
class BookingListView(APIView):
    """API view for listing bookings"""
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        bookings = Booking.objects.all()
        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)
    def post(self, request):
        """Create a new booking"""
        try:
            serializer = BookingSerializer(data=request.data)
            if serializer.is_valid():
                # Save the booking
                booking = serializer.save()
                
                # Return the created booking with success response
                return Response(
                    {
                        'message': 'Booking created successfully!',
                        'data': BookingSerializer(booking).data
                    },
                    status=status.HTTP_201_CREATED
                )
            else:
                # Return validation errors
                return Response(
                    {
                        'error': 'Validation failed',
                        'errors': serializer.errors
                    },
                    status=status.HTTP_400_BAD_REQUEST
                )
        except Exception as e:
            # Handle unexpected errors
            return Response(
                {
                    'error': 'Failed to create booking',
                    'detail': str(e)
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BookingDetailView(APIView):
    """API view for retrieving, updating and deleting bookings"""
    # permission_classes = [IsAuthenticated]
   
        
    
    def get_object(self, pk):
        return get_object_or_404(Booking, pk=pk)

    def get(self, request, pk):
        booking = self.get_object(pk)
        serializer = BookingSerializer(booking)
        return Response(serializer.data)

    def put(self, request, pk):
        booking = self.get_object(pk)
        serializer = BookingSerializer(booking, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        booking = self.get_object(pk)
        booking.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class BookingStatusView(APIView):
    """API view for updating booking status"""
    # permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        booking = get_object_or_404(Booking, pk=pk)
        status_value = request.data.get('status')
        
        if status_value not in ['new', 'confirmed', 'cancelled']:
            return Response(
                {'error': 'Invalid status'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        booking.status = status_value
        booking.save()
        serializer = BookingSerializer(booking)
        return Response(serializer.data)


# Order Views
class OrderListView(APIView):
    """API view for listing and creating orders"""
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = OrderCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetailView(APIView):
    """API view for retrieving, updating and deleting orders"""
    # permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(Order, pk=pk)

    def get(self, request, pk):
        order = self.get_object(pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def put(self, request, pk):
        order = self.get_object(pk)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        order = self.get_object(pk)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderStatusView(APIView):
    """API view for updating order status"""
    # permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        order = get_object_or_404(Order, pk=pk)
        status_value = request.data.get('status')
        
        valid_statuses = ['pending', 'confirmed', 'preparing', 'ready', 'delivered', 'cancelled']
        if status_value not in valid_statuses:
            return Response(
                {'error': 'Invalid status'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        order.status = status_value
        order.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data)


# Admin User Views
class AdminUserListView(APIView):
    """API view for listing and creating admin users"""
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        admin_users = AdminUser.objects.all()
        serializer = AdminUserSerializer(admin_users, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = AdminUserCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminUserDetailView(APIView):
    """API view for retrieving, updating and deleting admin users"""
    # permission_classes = [IsAuthenticated]

    def get_object(self, pk):
        return get_object_or_404(AdminUser, pk=pk)

    def get(self, request, pk):
        admin_user = self.get_object(pk)
        serializer = AdminUserSerializer(admin_user)
        return Response(serializer.data)

    def put(self, request, pk):
        admin_user = self.get_object(pk)
        serializer = AdminUserSerializer(admin_user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        admin_user = self.get_object(pk)
        admin_user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
