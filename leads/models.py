from django.db import models
from django.conf import settings


class Lead(models.Model):
    STATUS_CHOICES = [
        ('new',       'New'),
        ('contacted', 'Contacted'),
        ('visit_set', 'Visit Scheduled'),
        ('negotiating','Negotiating'),
        ('closed',    'Closed'),
        ('lost',      'Lost'),
    ]

    # Relations
    property = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='leads')
    buyer    = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_leads')

    # Buyer contact info (for non-registered users too)
    name    = models.CharField(max_length=150)
    email   = models.EmailField(blank=True)
    phone   = models.CharField(max_length=15)
    message = models.TextField(blank=True)

    # Visit scheduling
    visit_date    = models.DateField(null=True, blank=True)
    visit_message = models.TextField(blank=True)

    # Status tracking
    status     = models.CharField(max_length=15, choices=STATUS_CHOICES, default='new')
    agent_note = models.TextField(blank=True, help_text='Internal note by agent')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} → {self.property.title[:40]}'


class VisitRequest(models.Model):
    STATUS_CHOICES = [
        ('pending',   'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]

    property   = models.ForeignKey('properties.Property', on_delete=models.CASCADE, related_name='visits')
    buyer      = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='visits')
    visit_date = models.DateField()
    message    = models.TextField(blank=True)
    status     = models.CharField(max_length=15, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Visit by {self.buyer.name} on {self.visit_date}'
