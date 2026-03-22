from rest_framework import generics, status, permissions, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q

from .models import Property, SavedProperty, PropertyAlert
from .serializers import (
    PropertyListSerializer, PropertyDetailSerializer,
    PropertyCreateSerializer, SavedPropertySerializer, PropertyAlertSerializer,
)
from .filters import PropertyFilter


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user or request.user.is_staff


class PropertyListView(generics.ListAPIView):
    """
    GET /api/properties/
    Supports: ?city=Mumbai&listing_type=sell&prop_type=Flat&bhk=2 BHK
              &min_price=1000000&max_price=10000000
              &search=bandra&ordering=-created_at
    """
    serializer_class   = PropertyListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class    = PropertyFilter
    search_fields      = ['title', 'city', 'locality', 'address', 'description']
    ordering_fields    = ['price', 'area', 'created_at', 'views']
    ordering           = ['-created_at']

    def get_queryset(self):
        return Property.objects.filter(status='active').select_related('owner').prefetch_related('images', 'amenities')


class PropertyCreateView(generics.CreateAPIView):
    """POST /api/properties/  — authenticated users only"""
    serializer_class   = PropertyCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class PropertyDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET/PUT/PATCH/DELETE /api/properties/<id>/"""
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return Property.objects.select_related('owner').prefetch_related('images', 'amenities', 'saved_by')

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return PropertyCreateSerializer
        return PropertyDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        # Increment view count
        Property.objects.filter(pk=instance.pk).update(views=instance.views + 1)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class FeaturedPropertiesView(generics.ListAPIView):
    """GET /api/properties/featured/"""
    serializer_class   = PropertyListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Property.objects.filter(status='active', is_featured=True).select_related('owner').prefetch_related('images')[:8]


class MyPropertiesView(generics.ListAPIView):
    """GET /api/properties/my/  — agent/owner sees their own listings"""
    serializer_class   = PropertyListSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Property.objects.filter(owner=self.request.user).select_related('owner').prefetch_related('images')


class SavePropertyView(APIView):
    """POST /api/properties/<id>/save/  — toggle save/unsave"""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        try:
            prop = Property.objects.get(pk=pk, status='active')
        except Property.DoesNotExist:
            return Response({'detail': 'Property not found.'}, status=status.HTTP_404_NOT_FOUND)

        saved, created = SavedProperty.objects.get_or_create(user=request.user, property=prop)
        if not created:
            saved.delete()
            return Response({'saved': False, 'message': 'Property removed from saved list.'})
        return Response({'saved': True, 'message': 'Property saved successfully.'})


class SavedPropertiesView(generics.ListAPIView):
    """GET /api/properties/saved/  — buyer's saved properties"""
    serializer_class   = SavedPropertySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return SavedProperty.objects.filter(user=self.request.user).select_related('property__owner').prefetch_related('property__images')


class PropertyAlertListCreateView(generics.ListCreateAPIView):
    serializer_class   = PropertyAlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PropertyAlert.objects.filter(user=self.request.user)


class PropertyAlertDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class   = PropertyAlertSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return PropertyAlert.objects.filter(user=self.request.user)


# Admin views
class AdminPropertyListView(generics.ListAPIView):
    """Admin: view all properties including pending"""
    serializer_class   = PropertyListSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter]
    filterset_class    = PropertyFilter
    search_fields      = ['title', 'city', 'owner__name']

    def get_queryset(self):
        return Property.objects.select_related('owner').prefetch_related('images')


@api_view(['PATCH'])
@permission_classes([permissions.IsAdminUser])
def admin_verify_property(request, pk):
    """PATCH /api/properties/<id>/verify/  — admin approves/rejects"""
    try:
        prop = Property.objects.get(pk=pk)
    except Property.DoesNotExist:
        return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

    action = request.data.get('action')   # 'approve' or 'reject'
    if action == 'approve':
        prop.status = 'active'
        prop.is_verified = True
    elif action == 'reject':
        prop.status = 'rejected'
    else:
        return Response({'detail': 'action must be approve or reject.'}, status=status.HTTP_400_BAD_REQUEST)

    prop.save()
    return Response({'status': prop.status, 'is_verified': prop.is_verified})
