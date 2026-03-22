from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models


class UserManager(BaseUserManager):
    def create_user(self, email, name, password=None, **extra):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user  = self.model(email=email, name=name, **extra)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra):
        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        extra.setdefault('role', 'admin')
        return self.create_user(email, name, password, **extra)


class User(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('buyer',  'Buyer'),
        ('owner',  'Owner'),
        ('agent',  'Agent'),
        ('admin',  'Admin'),
    ]

    email     = models.EmailField(unique=True)
    name      = models.CharField(max_length=150)
    phone     = models.CharField(max_length=15, blank=True)
    role      = models.CharField(max_length=10, choices=ROLE_CHOICES, default='buyer')
    city      = models.CharField(max_length=100, blank=True)
    avatar    = models.ImageField(upload_to='avatars/', blank=True, null=True)

    # Agent-specific
    agency    = models.CharField(max_length=200, blank=True)
    rera_number = models.CharField(max_length=100, blank=True)
    experience  = models.PositiveIntegerField(default=0)   # years
    is_verified = models.BooleanField(default=False)       # admin verified

    is_active  = models.BooleanField(default=True)
    is_staff   = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    objects  = UserManager()
    USERNAME_FIELD  = 'email'
    REQUIRED_FIELDS = ['name']

    class Meta:
        ordering = ['-date_joined']
        verbose_name = 'User'

    def __str__(self):
        return f'{self.name} ({self.email})'

    @property
    def is_agent(self):
        return self.role == 'agent'

    @property
    def is_admin_user(self):
        return self.role == 'admin'
