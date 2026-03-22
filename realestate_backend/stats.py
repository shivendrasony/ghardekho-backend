from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from accounts.models import User
from properties.models import Property
from leads.models import Lead
from blog.models import BlogPost


@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_stats(request):
    """
    GET /api/stats/
    Returns platform-wide stats for Admin Dashboard.
    """
    return Response({
        'total_properties':  Property.objects.count(),
        'active_properties': Property.objects.filter(status='active').count(),
        'pending_properties':Property.objects.filter(status='pending').count(),
        'total_users':       User.objects.count(),
        'total_agents':      User.objects.filter(role='agent').count(),
        'total_buyers':      User.objects.filter(role='buyer').count(),
        'total_leads':       Lead.objects.count(),
        'new_leads':         Lead.objects.filter(status='new').count(),
        'total_blog_posts':  BlogPost.objects.filter(status='published').count(),
        'featured_properties': Property.objects.filter(is_featured=True).count(),
    })
