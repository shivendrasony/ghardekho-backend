from django.db import models
from django.conf import settings


class Property(models.Model):
    LISTING_TYPE = [('sell', 'Sell'), ('rent', 'Rent')]
    PROP_TYPE    = [
        ('Flat', 'Flat'), ('House', 'House'), ('Villa', 'Villa'),
        ('Plot', 'Plot'), ('Commercial', 'Commercial'),
    ]
    BHK_CHOICES  = [
        ('1 BHK', '1 BHK'), ('2 BHK', '2 BHK'), ('3 BHK', '3 BHK'),
        ('4 BHK', '4 BHK'), ('4+ BHK', '4+ BHK'),
    ]
    FURNISH_CHOICES = [
        ('Unfurnished', 'Unfurnished'),
        ('Semi Furnished', 'Semi Furnished'),
        ('Fully Furnished', 'Fully Furnished'),
    ]
    STATUS_CHOICES = [
        ('pending',  'Pending Review'),
        ('active',   'Active'),
        ('rejected', 'Rejected'),
        ('expired',  'Expired'),
    ]
    FACING_CHOICES = [
        ('North','North'), ('South','South'), ('East','East'), ('West','West'),
        ('North-East','North-East'), ('North-West','North-West'),
        ('South-East','South-East'), ('South-West','South-West'),
    ]

    # Owner / Agent
    owner        = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='properties')

    # Basic Info
    title        = models.CharField(max_length=300)
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPE)
    prop_type    = models.CharField(max_length=20, choices=PROP_TYPE)
    description  = models.TextField()
    status       = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    # Location
    city         = models.CharField(max_length=100, db_index=True)
    locality     = models.CharField(max_length=200)
    address      = models.TextField()
    pincode      = models.CharField(max_length=10, blank=True)
    latitude     = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude    = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

    # Property Details
    price        = models.BigIntegerField()
    area         = models.PositiveIntegerField(help_text='Area in sq.ft')
    bhk          = models.CharField(max_length=10, choices=BHK_CHOICES, blank=True)
    floor        = models.CharField(max_length=50, blank=True)
    total_floors = models.PositiveIntegerField(null=True, blank=True)
    age          = models.CharField(max_length=50, blank=True)
    furnishing   = models.CharField(max_length=20, choices=FURNISH_CHOICES, blank=True)
    facing       = models.CharField(max_length=15, choices=FACING_CHOICES, blank=True)

    # Pricing
    negotiable   = models.BooleanField(default=False)
    maintenance  = models.PositiveIntegerField(null=True, blank=True, help_text='Monthly maintenance in ₹')
    rera_number  = models.CharField(max_length=100, blank=True)

    # Flags
    is_featured  = models.BooleanField(default=False)
    is_verified  = models.BooleanField(default=False)

    # Meta
    views        = models.PositiveIntegerField(default=0)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        ordering  = ['-created_at']
        verbose_name_plural = 'Properties'

    def __str__(self):
        return self.title

    @property
    def price_per_sqft(self):
        if self.area and self.listing_type == 'sell':
            return round(self.price / self.area)
        return None


class PropertyImage(models.Model):
    property  = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image     = models.ImageField(upload_to='properties/')
    is_cover  = models.BooleanField(default=False)
    order     = models.PositiveSmallIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']

    def __str__(self):
        return f'Image for {self.property.title}'


class PropertyAmenity(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='amenities')
    name     = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class SavedProperty(models.Model):
    user     = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='saved_properties')
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='saved_by')
    saved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'property']
        ordering = ['-saved_at']

    def __str__(self):
        return f'{self.user.name} saved {self.property.title}'


class PropertyAlert(models.Model):
    user         = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='alerts')
    city         = models.CharField(max_length=100)
    prop_type    = models.CharField(max_length=20, blank=True)
    listing_type = models.CharField(max_length=10, blank=True)
    bhk          = models.CharField(max_length=10, blank=True)
    min_price    = models.BigIntegerField(null=True, blank=True)
    max_price    = models.BigIntegerField(null=True, blank=True)
    is_active    = models.BooleanField(default=True)
    created_at   = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Alert: {self.user.name} — {self.bhk} {self.prop_type} in {self.city}'
