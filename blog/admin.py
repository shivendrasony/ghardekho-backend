from django.contrib import admin
from .models import BlogPost, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display   = ['title', 'author', 'category', 'status', 'is_featured', 'views', 'created_at']
    list_filter    = ['status', 'is_featured', 'category']
    search_fields  = ['title', 'excerpt', 'tags']
    prepopulated_fields = {'slug': ('title',)}
    list_editable  = ['status', 'is_featured']
    readonly_fields = ['views', 'created_at', 'updated_at']
    ordering       = ['-created_at']
    actions        = ['publish_posts']

    def publish_posts(self, request, queryset):
        from django.utils import timezone
        queryset.update(status='published', published_at=timezone.now())
    publish_posts.short_description = '📢 Publish selected posts'
