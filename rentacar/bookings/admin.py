from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display  = ['id', 'customer', 'car', 'start_date', 'end_date', 'total_cost', 'status', 'created_at']
    list_filter   = ['status']
    search_fields = ['customer__username', 'car__brand', 'car__model']
    list_editable = ['status']
    readonly_fields = ['total_cost', 'created_at', 'updated_at']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display  = ['booking', 'reviewer', 'rating', 'created_at']
    list_filter   = ['rating']
    search_fields = ['reviewer__username']