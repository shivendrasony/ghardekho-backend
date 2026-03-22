from django.urls import path
from .views import (
    BlogListView, BlogDetailView, BlogCreateView,
    FeaturedBlogListView, CategoryListView,
)

urlpatterns = [
    path('',               BlogListView.as_view(),     name='blog-list'),
    path('featured/',      FeaturedBlogListView.as_view(), name='blog-featured'),
    path('categories/',    CategoryListView.as_view(), name='blog-categories'),
    path('create/',        BlogCreateView.as_view(),   name='blog-create'),
    path('<slug:slug>/',   BlogDetailView.as_view(),   name='blog-detail'),
]
