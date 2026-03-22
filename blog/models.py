from django.db import models
from django.conf import settings
from django.utils.text import slugify


class Category(models.Model):
    name       = models.CharField(max_length=100, unique=True)
    slug       = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering     = ['name']
        verbose_name_plural = 'Categories'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class BlogPost(models.Model):
    STATUS_CHOICES = [('draft', 'Draft'), ('published', 'Published')]

    title      = models.CharField(max_length=300)
    slug       = models.SlugField(unique=True, max_length=320, blank=True)
    author     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='blog_posts')
    category   = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts')
    excerpt    = models.TextField(max_length=500)
    content    = models.TextField()
    cover_image = models.ImageField(upload_to='blog/', blank=True, null=True)
    status     = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    is_featured = models.BooleanField(default=False)
    read_time  = models.PositiveSmallIntegerField(default=5, help_text='Estimated read time in minutes')
    views      = models.PositiveIntegerField(default=0)
    tags       = models.CharField(max_length=300, blank=True, help_text='Comma-separated tags')
    published_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_tags_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()]
