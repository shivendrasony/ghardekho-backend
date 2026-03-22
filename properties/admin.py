from django.contrib import admin
from .models import Property, PropertyImage, PropertyAmenity, SavedProperty, PropertyAlert


class PropertyImageInline(admin.TabularInline):
    model  = PropertyImage
    extra  = 1
    fields = ['image', 'is_cover', 'order']


class PropertyAmenityInline(admin.TabularInline):
    model  = PropertyAmenity
    extra  = 3
    fields = ['name']


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display   = ['title', 'owner', 'city', 'prop_type', 'listing_type', 'price', 'status', 'is_verified', 'is_featured', 'views', 'created_at']
    list_filter    = ['status', 'listing_type', 'prop_type', 'city', 'is_verified', 'is_featured']
    search_fields  = ['title', 'city', 'locality', 'owner__name', 'owner__email']
    ordering       = ['-created_at']
    readonly_fields = ['views', 'created_at', 'updated_at']
    inlines        = [PropertyImageInline, PropertyAmenityInline]
    list_editable  = ['status', 'is_verified', 'is_featured']

    fieldsets = (
        ('Basic Info',    {'fields': ('owner', 'title', 'listing_type', 'prop_type', 'description', 'status')}),
        ('Location',      {'fields': ('city', 'locality', 'address', 'pincode', 'latitude', 'longitude')}),
        ('Details',       {'fields': ('price', 'area', 'bhk', 'floor', 'total_floors', 'age', 'furnishing', 'facing')}),
        ('Pricing',       {'fields': ('negotiable', 'maintenance', 'rera_number')}),
        ('Flags',         {'fields': ('is_featured', 'is_verified')}),
        ('Meta',          {'fields': ('views', 'created_at', 'updated_at')}),
    )

    actions = ['mark_active', 'mark_rejected', 'mark_featured']

    def mark_active(self, request, queryset):
        queryset.update(status='active', is_verified=True)
    mark_active.short_description = '✅ Approve selected properties'

    def mark_rejected(self, request, queryset):
        queryset.update(status='rejected')
    mark_rejected.short_description = '❌ Reject selected properties'

    def mark_featured(self, request, queryset):
        queryset.update(is_featured=True)
    mark_featured.short_description = '⭐ Mark as featured'


@admin.register(SavedProperty)
class SavedPropertyAdmin(admin.ModelAdmin):
    list_display  = ['user', 'property', 'saved_at']
    search_fields = ['user__name', 'property__title']


@admin.register(PropertyAlert)
class PropertyAlertAdmin(admin.ModelAdmin):
    list_display = ['user', 'city', 'prop_type', 'bhk', 'is_active', 'created_at']
    list_filter  = ['is_active', 'city', 'prop_type']
