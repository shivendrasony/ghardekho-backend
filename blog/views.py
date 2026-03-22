from rest_framework import generics, permissions, filters
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend

from .models import BlogPost, Category
from .serializers import (
    BlogListSerializer, BlogDetailSerializer,
    BlogCreateSerializer, CategorySerializer,
)


class CategoryListView(generics.ListAPIView):
    """GET /api/blog/categories/"""
    queryset           = Category.objects.all()
    serializer_class   = CategorySerializer
    permission_classes = [permissions.AllowAny]


class BlogListView(generics.ListAPIView):
    """
    GET /api/blog/
    ?category=investment&search=patna&is_featured=true&ordering=-views
    """
    serializer_class   = BlogListSerializer
    permission_classes = [permissions.AllowAny]
    filter_backends    = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields   = ['category__slug', 'is_featured', 'author']
    search_fields      = ['title', 'excerpt', 'tags']
    ordering_fields    = ['created_at', 'views']
    ordering           = ['-created_at']

    def get_queryset(self):
        return BlogPost.objects.filter(
            status='published'
        ).select_related('author', 'category')


class BlogDetailView(generics.RetrieveUpdateDestroyAPIView):
    """GET /api/blog/<slug>/"""
    lookup_field       = 'slug'
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return BlogPost.objects.select_related('author', 'category')

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return BlogCreateSerializer
        return BlogDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        BlogPost.objects.filter(pk=instance.pk).update(views=instance.views + 1)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class BlogCreateView(generics.CreateAPIView):
    """POST /api/blog/create/  — admin/staff only"""
    serializer_class   = BlogCreateSerializer
    permission_classes = [permissions.IsAdminUser]


class FeaturedBlogListView(generics.ListAPIView):
    """GET /api/blog/featured/"""
    serializer_class   = BlogListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return BlogPost.objects.filter(status='published', is_featured=True).select_related('author', 'category')[:4]
