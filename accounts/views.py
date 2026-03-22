from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter

from .models import User
from .serializers import (
    RegisterSerializer, LoginSerializer, UserSerializer,
    UserPublicSerializer, TokenSerializer, ChangePasswordSerializer
)


class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(TokenSerializer.get_tokens(user), status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            return Response(TokenSerializer.get_tokens(user))
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            token = RefreshToken(request.data.get('refresh'))
            token.blacklist()
            return Response({'detail': 'Logged out successfully.'})
        except TokenError:
            return Response({'detail': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)


class MeView(generics.RetrieveUpdateAPIView):
    serializer_class   = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            request.user.set_password(serializer.validated_data['new_password'])
            request.user.save()
            return Response({'detail': 'Password changed successfully.'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AgentListView(generics.ListAPIView):
    """Public list of all verified agents"""
    queryset           = User.objects.filter(role='agent', is_active=True)
    serializer_class   = UserPublicSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends    = [SearchFilter]
    search_fields      = ['name', 'city', 'agency']


class AgentDetailView(generics.RetrieveAPIView):
    """Public agent profile page"""
    queryset           = User.objects.filter(role='agent', is_active=True)
    serializer_class   = UserPublicSerializer
    permission_classes = [permissions.AllowAny]


# Admin only
class UserListView(generics.ListAPIView):
    queryset           = User.objects.all()
    serializer_class   = UserSerializer
    permission_classes = [permissions.IsAdminUser]
    filter_backends    = [SearchFilter, DjangoFilterBackend]
    search_fields      = ['name', 'email', 'phone']
    filterset_fields   = ['role', 'is_active', 'is_verified']
