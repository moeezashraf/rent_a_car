from django.contrib import admin
from .models import Car, CarImage

# Register your models here.

class CarImageInline(admin.TabularInline):
    model = CarImage
    extra = 1

@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model', 'year', 'owner', 'price_per_day', 'is_available', 'is_approved']
    list_filter = ['is_available', 'is_approved', 'car_type']
    list_editable = ['is_available', 'is_approved']
    inlines = [CarImageInline]