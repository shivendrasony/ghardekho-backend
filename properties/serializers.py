from rest_framework import serializers
from accounts.serializers import UserPublicSerializer
from .models import Property, PropertyImage, PropertyAmenity, SavedProperty, PropertyAlert


class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PropertyImage
        fields = ['id', 'image', 'is_cover', 'order']


class PropertyAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model  = PropertyAmenity
        fields = ['id', 'name']


class PropertyListSerializer(serializers.ModelSerializer):
    """Compact serializer for listing cards"""
    cover_image   = serializers.SerializerMethodField()
    owner_name    = serializers.CharField(source='owner.name', read_only=True)
    owner_verified = serializers.BooleanField(source='owner.is_verified', read_only=True)
    price_per_sqft = serializers.IntegerField(read_only=True)

    class Meta:
        model  = Property
        fields = [
            'id', 'title', 'listing_type', 'prop_type', 'price', 'price_per_sqft',
            'area', 'bhk', 'city', 'locality', 'cover_image',
            'is_featured', 'is_verified', 'owner_name', 'owner_verified',
            'views', 'created_at',
        ]

    def get_cover_image(self, obj):
        img = obj.images.filter(is_cover=True).first() or obj.images.first()
        if img:
            request = self.context.get('request')
            return request.build_absolute_uri(img.image.url) if request else img.image.url
        return None


class PropertyDetailSerializer(serializers.ModelSerializer):
    """Full serializer for property detail page"""
    images    = PropertyImageSerializer(many=True, read_only=True)
    amenities = serializers.SerializerMethodField()
    owner     = UserPublicSerializer(read_only=True)
    price_per_sqft = serializers.IntegerField(read_only=True)
    is_saved  = serializers.SerializerMethodField()

    class Meta:
        model  = Property
        fields = [
            'id', 'title', 'listing_type', 'prop_type', 'description', 'status',
            'city', 'locality', 'address', 'pincode', 'latitude', 'longitude',
            'price', 'price_per_sqft', 'area', 'bhk', 'floor', 'total_floors',
            'age', 'furnishing', 'facing', 'negotiable', 'maintenance', 'rera_number',
            'is_featured', 'is_verified', 'views',
            'images', 'amenities', 'owner', 'is_saved', 'created_at', 'updated_at',
        ]

    def get_amenities(self, obj):
        return [a.name for a in obj.amenities.all()]

    def get_is_saved(self, obj):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return obj.saved_by.filter(user=request.user).exists()
        return False


class PropertyCreateSerializer(serializers.ModelSerializer):
    amenities = serializers.ListField(child=serializers.CharField(), write_only=True, required=False)
    images    = serializers.ListField(child=serializers.ImageField(), write_only=True, required=False)

    class Meta:
        model  = Property
        fields = [
            'title', 'listing_type', 'prop_type', 'description',
            'city', 'locality', 'address', 'pincode',
            'price', 'area', 'bhk', 'floor', 'total_floors',
            'age', 'furnishing', 'facing', 'negotiable', 'maintenance', 'rera_number',
            'amenities', 'images',
        ]

    def create(self, validated_data):
        amenities_data = validated_data.pop('amenities', [])
        images_data    = validated_data.pop('images', [])
        validated_data['owner'] = self.context['request'].user

        prop = Property.objects.create(**validated_data)

        # Create amenities
        PropertyAmenity.objects.bulk_create([
            PropertyAmenity(property=prop, name=name) for name in amenities_data
        ])

        # Create images
        for i, img in enumerate(images_data):
            PropertyImage.objects.create(
                property=prop, image=img,
                is_cover=(i == 0), order=i
            )

        return prop


class SavedPropertySerializer(serializers.ModelSerializer):
    property = PropertyListSerializer(read_only=True)

    class Meta:
        model  = SavedProperty
        fields = ['id', 'property', 'saved_at']


class PropertyAlertSerializer(serializers.ModelSerializer):
    class Meta:
        model  = PropertyAlert
        fields = ['id', 'city', 'prop_type', 'listing_type', 'bhk', 'min_price', 'max_price', 'is_active', 'created_at']
        read_only_fields = ['id', 'created_at']

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)
