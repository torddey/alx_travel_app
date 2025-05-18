from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Listing, Booking

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']

class ListingSerializer(serializers.ModelSerializer):
    """Serializer for Listing model"""
    owner = UserSerializer(read_only=True)
    owner_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='owner',
        write_only=True
    )
    
    class Meta:
        model = Listing
        fields = [
            'id', 'title', 'description', 'address', 'city', 'state', 
            'country', 'zip_code', 'price_per_night', 'property_type',
            'max_guests', 'bedrooms', 'bathrooms', 'amenities', 'images',
            'is_available', 'owner', 'owner_id', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class BookingSerializer(serializers.ModelSerializer):
    """Serializer for Booking model"""
    listing = ListingSerializer(read_only=True)
    listing_id = serializers.PrimaryKeyRelatedField(
        queryset=Listing.objects.all(),
        source='listing',
        write_only=True
    )
    guest = UserSerializer(read_only=True)
    guest_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='guest',
        write_only=True
    )
    
    class Meta:
        model = Booking
        fields = [
            'id', 'listing', 'listing_id', 'guest', 'guest_id',
            'check_in_date', 'check_out_date', 'number_of_guests',
            'total_price', 'status', 'special_requests',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, data):
        """Validate booking dates and guest count"""
        check_in = data.get('check_in_date')
        check_out = data.get('check_out_date')
        number_of_guests = data.get('number_of_guests')
        listing = data.get('listing')
        
        if check_in and check_out:
            if check_in >= check_out:
                raise serializers.ValidationError(
                    "Check-out date must be after check-in date"
                )
        
        if listing and number_of_guests:
            if number_of_guests > listing.max_guests:
                raise serializers.ValidationError(
                    f"Number of guests cannot exceed {listing.max_guests}"
                )
        
        return data 