from django.db import models
from django.conf import settings
from cars.models import Car

# Create your models here.

class Booking(models.Model):

    STATUS_CHOICES = (
        ('pending',   'Pending'),
        ('approved',  'Approved'),
        ('rejected',  'Rejected'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )
    customer   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    car        = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='bookings')
    start_date = models.DateField()
    end_date   = models.DateField()
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status     = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    note       = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Booking #{self.id} — {self.customer.username} → {self.car}"

    def calculate_total(self):
        if self.start_date and self.end_date:
            days = (self.end_date - self.start_date).days
            if days > 0:
                self.total_cost = days * self.car.price_per_day
        return self.total_cost


class Review(models.Model):

    booking    = models.OneToOneField(Booking, on_delete=models.CASCADE, related_name='review')
    reviewer   = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews')
    rating     = models.PositiveIntegerField()
    comment    = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for Booking #{self.booking.id} — {self.rating} stars"