from django.shortcuts import render
from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Listing, Booking
from .serializers import ListingSerializer, BookingSerializer

# Create your views here.

class ListingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing travel listings/accommodations.
    
    Provides CRUD operations for listings with filtering and search capabilities.
    """
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['city', 'state', 'country', 'property_type', 'is_available', 'owner']
    search_fields = ['title', 'description', 'address', 'city', 'state', 'country']
    ordering_fields = ['price_per_night', 'created_at', 'updated_at']
    ordering = ['-created_at']

    @swagger_auto_schema(
        operation_description="List all available travel listings",
        manual_parameters=[
            openapi.Parameter('city', openapi.IN_QUERY, description="Filter by city", type=openapi.TYPE_STRING),
            openapi.Parameter('country', openapi.IN_QUERY, description="Filter by country", type=openapi.TYPE_STRING),
            openapi.Parameter('property_type', openapi.IN_QUERY, description="Filter by property type", type=openapi.TYPE_STRING),
            openapi.Parameter('min_price', openapi.IN_QUERY, description="Minimum price per night", type=openapi.TYPE_NUMBER),
            openapi.Parameter('max_price', openapi.IN_QUERY, description="Maximum price per night", type=openapi.TYPE_NUMBER),
            openapi.Parameter('search', openapi.IN_QUERY, description="Search in title, description, address", type=openapi.TYPE_STRING),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new travel listing",
        request_body=ListingSerializer,
        responses={201: ListingSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve a specific listing by ID",
        responses={200: ListingSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a listing (partial update supported)",
        request_body=ListingSerializer,
        responses={200: ListingSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a listing",
        responses={204: "No content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Set the owner to the current user when creating a listing"""
        serializer.save(owner=self.request.user)

class BookingViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing booking reservations.
    
    Provides CRUD operations for bookings with filtering and validation.
    """
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'listing', 'guest', 'check_in_date', 'check_out_date']
    ordering_fields = ['created_at', 'check_in_date', 'check_out_date', 'total_price']
    ordering = ['-created_at']

    def get_queryset(self):
        """Filter bookings to show only user's bookings or all if user is staff"""
        if self.request.user.is_staff:
            return Booking.objects.all()
        return Booking.objects.filter(guest=self.request.user)

    @swagger_auto_schema(
        operation_description="List all bookings (filtered by user permissions)",
        manual_parameters=[
            openapi.Parameter('status', openapi.IN_QUERY, description="Filter by booking status", type=openapi.TYPE_STRING),
            openapi.Parameter('listing', openapi.IN_QUERY, description="Filter by listing ID", type=openapi.TYPE_INTEGER),
            openapi.Parameter('check_in_date', openapi.IN_QUERY, description="Filter by check-in date", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
            openapi.Parameter('check_out_date', openapi.IN_QUERY, description="Filter by check-out date", type=openapi.TYPE_STRING, format=openapi.FORMAT_DATE),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Create a new booking reservation",
        request_body=BookingSerializer,
        responses={201: BookingSerializer}
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Retrieve a specific booking by ID",
        responses={200: BookingSerializer}
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update a booking (partial update supported)",
        request_body=BookingSerializer,
        responses={200: BookingSerializer}
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete a booking",
        responses={204: "No content"}
    )
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    def perform_create(self, serializer):
        """Set the guest to the current user when creating a booking"""
        serializer.save(guest=self.request.user)
