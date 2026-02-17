from django.contrib import admin
from .models import Province, TrekkingRoute, Booking


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'headquarters']
    search_fields = ['name', 'code']


@admin.register(TrekkingRoute)
class TrekkingRouteAdmin(admin.ModelAdmin):
    list_display = ['name', 'province', 'difficulty', 'duration_days', 'price_per_person', 'is_featured', 'is_active']
    list_filter = ['province', 'difficulty', 'best_season', 'is_featured', 'is_active']
    search_fields = ['name', 'description']
    list_editable = ['is_featured', 'is_active']


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ['booking_reference', 'full_name', 'route', 'trek_start_date', 'num_trekkers', 'total_price', 'status']
    list_filter = ['status', 'route__province', 'require_guide', 'require_porter']
    search_fields = ['booking_reference', 'full_name', 'email']
    list_editable = ['status']
    readonly_fields = ['booking_reference', 'created_at']
