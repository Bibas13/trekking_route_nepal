from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Province(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='provinces/', blank=True, null=True)
    headquarters = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('treks:province_detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['name']


class TrekkingRoute(models.Model):
    DIFFICULTY_CHOICES = [
        ('easy', 'Easy'),
        ('moderate', 'Moderate'),
        ('hard', 'Hard'),
        ('extreme', 'Extreme'),
    ]
    SEASON_CHOICES = [
        ('spring', 'Spring (Mar-May)'),
        ('summer', 'Summer (Jun-Aug)'),
        ('autumn', 'Autumn (Sep-Nov)'),
        ('winter', 'Winter (Dec-Feb)'),
        ('all', 'All Seasons'),
    ]

    name = models.CharField(max_length=200)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='routes')
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES, default='moderate')
    duration_days = models.PositiveIntegerField(help_text='Number of days')
    distance_km = models.DecimalField(max_digits=6, decimal_places=1, help_text='Distance in kilometers')
    max_altitude = models.PositiveIntegerField(help_text='Maximum altitude in meters', default=0)
    best_season = models.CharField(max_length=10, choices=SEASON_CHOICES, default='autumn')
    start_point = models.CharField(max_length=100)
    end_point = models.CharField(max_length=100)
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2, help_text='Price in USD')
    image = models.ImageField(upload_to='routes/', blank=True, null=True)
    highlights = models.TextField(blank=True, help_text='Key highlights, one per line')
    includes = models.TextField(blank=True, help_text='What is included, one per line')
    excludes = models.TextField(blank=True, help_text='What is excluded, one per line')
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('treks:route_detail', kwargs={'pk': self.pk})

    def get_highlights_list(self):
        return [h.strip() for h in self.highlights.split('\n') if h.strip()]

    def get_includes_list(self):
        return [i.strip() for i in self.includes.split('\n') if i.strip()]

    def get_excludes_list(self):
        return [e.strip() for e in self.excludes.split('\n') if e.strip()]

    class Meta:
        ordering = ['name']


class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='bookings')
    route = models.ForeignKey(TrekkingRoute, on_delete=models.CASCADE, related_name='bookings')
    # Personal Info
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    nationality = models.CharField(max_length=100)
    # Trek Details
    trek_start_date = models.DateField()
    trek_end_date = models.DateField()
    num_trekkers = models.PositiveIntegerField(default=1)
    require_guide = models.BooleanField(default=False)
    require_porter = models.BooleanField(default=False)
    num_porters = models.PositiveIntegerField(default=0)
    # Additional
    special_requests = models.TextField(blank=True)
    emergency_contact_name = models.CharField(max_length=200)
    emergency_contact_phone = models.CharField(max_length=20)
    # Pricing
    total_price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    # Status
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    booking_reference = models.CharField(max_length=20, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.booking_reference} - {self.full_name} - {self.route.name}"

    def save(self, *args, **kwargs):
        if not self.booking_reference:
            import random, string
            self.booking_reference = 'NTR-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        if not self.total_price:
            self.total_price = self.route.price_per_person * self.num_trekkers
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
