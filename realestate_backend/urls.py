from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework_simplejwt.views import TokenRefreshView
from .stats import admin_stats

urlpatterns = [
    path('admin/',                      admin.site.urls),
    path('api/auth/',                   include('accounts.urls')),
    path('api/properties/',             include('properties.urls')),
    path('api/leads/',                  include('leads.urls')),
    path('api/blog/',                   include('blog.urls')),
    path('api/auth/token/refresh/',     TokenRefreshView.as_view(), name='token_refresh'),
    path('api/stats/',                  admin_stats,                name='admin-stats'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
