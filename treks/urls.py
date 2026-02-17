from django.urls import path
from . import views

app_name = 'treks'

urlpatterns = [
    path('', views.home, name='home'),
    path('provinces/', views.province_list, name='province_list'),
    path('provinces/<int:pk>/', views.province_detail, name='province_detail'),
    path('routes/', views.route_list, name='route_list'),
    path('routes/<int:pk>/', views.route_detail, name='route_detail'),
    path('routes/<int:pk>/book/', views.book_trek, name='book_trek'),
    path('booking/<int:pk>/success/', views.booking_success, name='booking_success'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('register/', views.register, name='register'),
]
