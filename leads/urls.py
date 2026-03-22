from django.urls import path
from .views import (
    LeadCreateView, MyLeadsView, AgentLeadsView, LeadDetailView,
    VisitRequestCreateView, MyVisitsView, AgentVisitsView, VisitStatusUpdateView,
)

urlpatterns = [
    # Leads / Inquiries
    path('',             LeadCreateView.as_view(),      name='lead-create'),
    path('mine/',        MyLeadsView.as_view(),          name='my-leads'),
    path('agent/',       AgentLeadsView.as_view(),       name='agent-leads'),
    path('<int:pk>/',    LeadDetailView.as_view(),       name='lead-detail'),

    # Site Visits
    path('visits/',                    VisitRequestCreateView.as_view(), name='visit-create'),
    path('visits/mine/',               MyVisitsView.as_view(),           name='my-visits'),
    path('visits/agent/',              AgentVisitsView.as_view(),        name='agent-visits'),
    path('visits/<int:pk>/status/',    VisitStatusUpdateView.as_view(),  name='visit-status'),
]
