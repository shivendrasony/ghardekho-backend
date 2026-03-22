from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q

from .models import Lead, VisitRequest
from .serializers import LeadSerializer, LeadUpdateSerializer, VisitRequestSerializer


class IsAgentOfProperty(permissions.BasePermission):
    """Allow only the property owner/agent to view leads for their listing"""
    def has_object_permission(self, request, view, obj):
        return obj.property.owner == request.user or request.user.is_staff


class LeadCreateView(generics.CreateAPIView):
    """
    POST /api/leads/
    Anyone (even unauthenticated) can submit a lead/inquiry.
    """
    serializer_class   = LeadSerializer
    permission_classes = [permissions.AllowAny]


class MyLeadsView(generics.ListAPIView):
    """
    GET /api/leads/mine/
    Buyer sees leads they have submitted.
    """
    serializer_class   = LeadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Lead.objects.filter(buyer=self.request.user).select_related('property')


class AgentLeadsView(generics.ListAPIView):
    """
    GET /api/leads/agent/
    Agent sees all leads for their properties.
    """
    serializer_class   = LeadSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Lead.objects.filter(
            property__owner=self.request.user
        ).select_related('property', 'buyer')


class LeadDetailView(generics.RetrieveUpdateAPIView):
    """
    GET/PATCH /api/leads/<id>/
    Agent can update status and notes.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Lead.objects.filter(
            Q(property__owner=self.request.user) | Q(buyer=self.request.user)
        )

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return LeadUpdateSerializer
        return LeadSerializer


class VisitRequestCreateView(generics.CreateAPIView):
    """POST /api/leads/visits/  — schedule a site visit"""
    serializer_class   = VisitRequestSerializer
    permission_classes = [permissions.IsAuthenticated]


class MyVisitsView(generics.ListAPIView):
    """GET /api/leads/visits/mine/"""
    serializer_class   = VisitRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return VisitRequest.objects.filter(buyer=self.request.user).select_related('property')


class AgentVisitsView(generics.ListAPIView):
    """GET /api/leads/visits/agent/  — all visits for agent's properties"""
    serializer_class   = VisitRequestSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return VisitRequest.objects.filter(
            property__owner=self.request.user
        ).select_related('property', 'buyer')


class VisitStatusUpdateView(APIView):
    """PATCH /api/leads/visits/<id>/status/  — agent confirms or cancels visit"""
    permission_classes = [permissions.IsAuthenticated]

    def patch(self, request, pk):
        try:
            visit = VisitRequest.objects.get(pk=pk, property__owner=request.user)
        except VisitRequest.DoesNotExist:
            return Response({'detail': 'Not found.'}, status=status.HTTP_404_NOT_FOUND)

        new_status = request.data.get('status')
        if new_status not in ['confirmed', 'cancelled', 'completed']:
            return Response({'detail': 'Invalid status.'}, status=status.HTTP_400_BAD_REQUEST)

        visit.status = new_status
        visit.save()
        return Response(VisitRequestSerializer(visit).data)
