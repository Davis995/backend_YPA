from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('auth/login/', views.LoginView.as_view(), name='login'),
    path('auth/logout/', views.LogoutView.as_view(), name='logout'),
    path('auth/profile/', views.UserProfileView.as_view(), name='user-profile'),
    path('auth/change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    
    # Dashboard
    path('dashboard/', views.DashboardStatsView.as_view(), name='dashboard-stats'),
    
    # Categories
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/<int:pk>/', views.CategoryDetailView.as_view(), name='category-detail'),
    
    # Menu Items
    path('menu/', views.MenuItemListView.as_view(), name='menu-list'),
    path('menu/<int:pk>/', views.MenuItemDetailView.as_view(), name='menu-detail'),
    
    # Contact Messages
    path('contacts/', views.ContactMessageListView.as_view(), name='contact-list'),
    path('contacts/<int:pk>/', views.ContactMessageDetailView.as_view(), name='contact-detail'),
    path('contacts/<int:pk>/status/', views.ContactMessageStatusView.as_view(), name='contact-status'),
    
    # Bookings
    path('bookings/', views.BookingListView.as_view(), name='booking-list'),
    path('bookings/<int:pk>/', views.BookingDetailView.as_view(), name='booking-detail'),
    path('bookings/<int:pk>/status/', views.BookingStatusView.as_view(), name='booking-status'),
    
    # Orders
    path('orders/', views.OrderListView.as_view(), name='order-list'),
    path('orders/<int:pk>/', views.OrderDetailView.as_view(), name='order-detail'),
    path('orders/<int:pk>/status/', views.OrderStatusView.as_view(), name='order-status'),
    
    # Admin Users
    path('admin-users/', views.AdminUserListView.as_view(), name='admin-user-list'),
    path('admin-users/<int:pk>/', views.AdminUserDetailView.as_view(), name='admin-user-detail'),


    #cartManagament
    path('cart', views.CartManagement.as_view(), name='cart'),
    #menuItem
      path('menuOrder', views.MenuOrder.as_view(), name='cart'),
]
