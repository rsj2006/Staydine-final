from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='staydine-home'),
    path('about/', views.about, name='staydine-about'),
    path('contact/', views.contact, name='staydine-contact'),
    path("bookings/",views.bookings,name='staydine-room-bookings'),
    path("restaurant/", views.restaurant, name='staydine-restaurant'),
    path('bed-types/', views.bed_types, name='staydine-bed-types'),
    path('my-orders/', views.my_orders, name='my-orders'),
    path('delete-order/', views.delete_order, name='delete-order'),
    
]
# urlpatterns = [
#     path("events",views.events,name='events'),
# ]