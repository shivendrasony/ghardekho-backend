from rest_framework import serializers
from accounts.serializers import UserPublicSerializer
from .models import BlogPost, Category


class CategorySerializer(serializers.ModelSerializer):
    post_count = serializers.SerializerMethodField()

    class Meta:
        model  = Category
        fields = ['id', 'name', 'slug', 'post_count']

    def get_post_count(self, obj):
        return obj.posts.filter(status='published').count()


class BlogListSerializer(serializers.ModelSerializer):
    author   = UserPublicSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags_list = serializers.SerializerMethodField()
    cover_image_url = serializers.SerializerMethodField()

    class Meta:
        model  = BlogPost
        fields = [
            'id', 'title', 'slug', 'author', 'category', 'excerpt',
            'cover_image_url', 'is_featured', 'read_time', 'views',
            'tags_list', 'published_at', 'created_at',
        ]

    def get_tags_list(self, obj):
        return obj.get_tags_list()

    def get_cover_image_url(self, obj):
        if obj.cover_image:
            request = self.context.get('request')
            return request.build_absolute_uri(obj.cover_image.url) if request else obj.cover_image.url
        return None


class BlogDetailSerializer(BlogListSerializer):
    class Meta(BlogListSerializer.Meta):
        fields = BlogListSerializer.Meta.fields + ['content', 'status', 'updated_at']


class BlogCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model  = BlogPost
        fields = ['title', 'category', 'excerpt', 'content', 'cover_image', 'status', 'is_featured', 'read_time', 'tags']

    def create(self, validated_data):
        validated_data['author'] = self.context['request'].user
        return super().create(validated_data)
