from django.contrib import admin
from .models import Lead, VisitRequest


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display  = ['name', 'phone', 'property', 'status', 'visit_date', 'created_at']
    list_filter   = ['status', 'created_at']
    search_fields = ['name', 'email', 'phone', 'property__title']
    ordering      = ['-created_at']
    list_editable = ['status']


@admin.register(VisitRequest)
class VisitRequestAdmin(admin.ModelAdmin):
    list_display  = ['buyer', 'property', 'visit_date', 'status', 'created_at']
    list_filter   = ['status']
    list_editable = ['status']
