from django.urls import path
from .views import (
    PropertyListView, PropertyCreateView, PropertyDetailView,
    FeaturedPropertiesView, MyPropertiesView,
    SavePropertyView, SavedPropertiesView,
    PropertyAlertListCreateView, PropertyAlertDetailView,
    AdminPropertyListView, admin_verify_property,
)

urlpatterns = [
    # Public
    path('',                            PropertyListView.as_view(),           name='property-list'),
    path('featured/',                   FeaturedPropertiesView.as_view(),     name='property-featured'),

    # Authenticated
    path('create/',                     PropertyCreateView.as_view(),         name='property-create'),
    path('my/',                         MyPropertiesView.as_view(),           name='my-properties'),
    path('saved/',                      SavedPropertiesView.as_view(),        name='saved-properties'),
    path('<int:pk>/save/',              SavePropertyView.as_view(),           name='property-save'),

    # Property detail (public GET, auth for PUT/DELETE)
    path('<int:pk>/',                   PropertyDetailView.as_view(),         name='property-detail'),

    # Alerts
    path('alerts/',                     PropertyAlertListCreateView.as_view(),name='property-alerts'),
    path('alerts/<int:pk>/',            PropertyAlertDetailView.as_view(),    name='property-alert-detail'),

    # Admin
    path('admin/all/',                  AdminPropertyListView.as_view(),      name='admin-property-list'),
    path('admin/<int:pk>/verify/',      admin_verify_property,                name='admin-verify-property'),
]
