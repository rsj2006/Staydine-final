from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='blog-home'),
    path('about/', views.about, name='blog-about'),
    path('bookings/', views.bookings, name='blog-bookings'),
    path('menu/', views.menu, name='blog-menu'),
    path('events/', views.events, name='blog-events'),
    path('tables/', views.tables, name='blog-tables'),
]
