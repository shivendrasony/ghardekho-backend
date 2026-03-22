from rest_framework import serializers
from .models import Lead, VisitRequest


class LeadSerializer(serializers.ModelSerializer):
    property_title = serializers.CharField(source='property.title', read_only=True)
    property_city  = serializers.CharField(source='property.city',  read_only=True)

    class Meta:
        model  = Lead
        fields = [
            'id', 'property', 'property_title', 'property_city',
            'name', 'email', 'phone', 'message',
            'visit_date', 'visit_message',
            'status', 'agent_note', 'created_at',
        ]
        read_only_fields = ['id', 'status', 'agent_note', 'created_at']

    def create(self, validated_data):
        # Attach logged-in user if authenticated
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['buyer'] = request.user
            if not validated_data.get('name'):
                validated_data['name'] = request.user.name
            if not validated_data.get('email'):
                validated_data['email'] = request.user.email
        return super().create(validated_data)


class LeadUpdateSerializer(serializers.ModelSerializer):
    """For agents to update lead status and notes"""
    class Meta:
        model  = Lead
        fields = ['status', 'agent_note']


class VisitRequestSerializer(serializers.ModelSerializer):
    property_title = serializers.CharField(source='property.title', read_only=True)
    buyer_name     = serializers.CharField(source='buyer.name',     read_only=True)

    class Meta:
        model  = VisitRequest
        fields = ['id', 'property', 'property_title', 'buyer', 'buyer_name', 'visit_date', 'message', 'status', 'created_at']
        read_only_fields = ['id', 'buyer', 'status', 'created_at']

    def create(self, validated_data):
        validated_data['buyer'] = self.context['request'].user
        return super().create(validated_data)
