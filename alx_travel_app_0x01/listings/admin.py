from django.contrib import admin
from .models import Listing, Booking

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ('title', 'city', 'country', 'price_per_night', 'property_type', 'is_available', 'owner')
    list_filter = ('property_type', 'is_available', 'country', 'city')
    search_fields = ('title', 'description', 'address', 'city', 'country')
    list_editable = ('is_available', 'price_per_night')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'listing', 'guest', 'check_in_date', 'check_out_date', 'status', 'total_price')
    list_filter = ('status', 'check_in_date', 'check_out_date')
    search_fields = ('listing__title', 'guest__username', 'guest__email')
    list_editable = ('status',)
    readonly_fields = ('created_at', 'updated_at')
