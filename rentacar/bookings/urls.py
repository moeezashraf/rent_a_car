# bookings/urls.py

from django.urls import path
from .views import *

urlpatterns = [
    path('create/', BookingCreateView.as_view(), name='booking-create'),
    path('my-bookings/', MyBookingsView.as_view(), name='my-bookings'),
    path('<int:pk>/', BookingDetailView.as_view(), name='booking-detail'),
    path('<int:pk>/cancel/', CancelBookingView.as_view(), name='booking-cancel'),

    path('owner/', OwnerBookingsView.as_view(), name='owner-bookings'),
    path('<int:pk>/manage/', BookingStatusUpdateView.as_view(), name='booking-manage'),
    path('<int:pk>/complete/', CompleteBookingView.as_view(), name='booking-complete'),

    path('review/', ReviewCreateView.as_view(), name='review-create'),

    path('admin/all/', AdminBookingListView.as_view(), name='admin-booking-list'),
    path('admin/<int:pk>/action/', AdminBookingActionView.as_view(), name='admin-booking-action'),
]