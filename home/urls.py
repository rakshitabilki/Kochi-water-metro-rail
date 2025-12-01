from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.index_view, name='index'),       # homepage
    path('about/', views.about_view, name='about'), # about page
        path('journey/', views.journey, name='journey'),  # Add this
         path("book-ticket/", views.book_ticket, name="book_ticket"),
    path("my-bookings/", views.my_bookings, name="my_bookings"),
    path("my-bookings/<int:booking_id>/cancel/", views.cancel_booking, name="cancel_booking"),
path('terminal/<str:name>/', views.terminal_detail, name='terminal_detail'),

]
