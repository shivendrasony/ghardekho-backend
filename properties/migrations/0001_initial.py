from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('accounts', '0001_initial'),
    ]
    operations = [
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id',           models.BigAutoField(auto_created=True, primary_key=True)),
                ('title',        models.CharField(max_length=300)),
                ('listing_type', models.CharField(choices=[('sell','Sell'),('rent','Rent')], max_length=10)),
                ('prop_type',    models.CharField(choices=[('Flat','Flat'),('House','House'),('Villa','Villa'),('Plot','Plot'),('Commercial','Commercial')], max_length=20)),
                ('description',  models.TextField()),
                ('status',       models.CharField(choices=[('pending','Pending'),('active','Active'),('rejected','Rejected'),('expired','Expired')], default='pending', max_length=10)),
                ('city',         models.CharField(db_index=True, max_length=100)),
                ('locality',     models.CharField(max_length=200)),
                ('address',      models.TextField()),
                ('pincode',      models.CharField(blank=True, max_length=10)),
                ('latitude',     models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('longitude',    models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True)),
                ('price',        models.BigIntegerField()),
                ('area',         models.PositiveIntegerField()),
                ('bhk',          models.CharField(blank=True, max_length=10)),
                ('floor',        models.CharField(blank=True, max_length=50)),
                ('total_floors', models.PositiveIntegerField(blank=True, null=True)),
                ('age',          models.CharField(blank=True, max_length=50)),
                ('furnishing',   models.CharField(blank=True, max_length=20)),
                ('facing',       models.CharField(blank=True, max_length=15)),
                ('negotiable',   models.BooleanField(default=False)),
                ('maintenance',  models.PositiveIntegerField(blank=True, null=True)),
                ('rera_number',  models.CharField(blank=True, max_length=100)),
                ('is_featured',  models.BooleanField(default=False)),
                ('is_verified',  models.BooleanField(default=False)),
                ('views',        models.PositiveIntegerField(default=0)),
                ('created_at',   models.DateTimeField(auto_now_add=True)),
                ('updated_at',   models.DateTimeField(auto_now=True)),
                ('owner',        models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='properties', to='accounts.user')),
            ],
            options={'ordering': ['-created_at'], 'verbose_name_plural': 'Properties'},
        ),
        migrations.CreateModel(
            name='PropertyImage',
            fields=[
                ('id',         models.BigAutoField(auto_created=True, primary_key=True)),
                ('image',      models.ImageField(upload_to='properties/')),
                ('is_cover',   models.BooleanField(default=False)),
                ('order',      models.PositiveSmallIntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('property',   models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='properties.property')),
            ],
            options={'ordering': ['order', 'created_at']},
        ),
        migrations.CreateModel(
            name='PropertyAmenity',
            fields=[
                ('id',       models.BigAutoField(auto_created=True, primary_key=True)),
                ('name',     models.CharField(max_length=100)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='amenities', to='properties.property')),
            ],
        ),
        migrations.CreateModel(
            name='SavedProperty',
            fields=[
                ('id',       models.BigAutoField(auto_created=True, primary_key=True)),
                ('saved_at', models.DateTimeField(auto_now_add=True)),
                ('property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_by', to='properties.property')),
                ('user',     models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='saved_properties', to='accounts.user')),
            ],
            options={'unique_together': {('user', 'property')}, 'ordering': ['-saved_at']},
        ),
        migrations.CreateModel(
            name='PropertyAlert',
            fields=[
                ('id',           models.BigAutoField(auto_created=True, primary_key=True)),
                ('city',         models.CharField(max_length=100)),
                ('prop_type',    models.CharField(blank=True, max_length=20)),
                ('listing_type', models.CharField(blank=True, max_length=10)),
                ('bhk',          models.CharField(blank=True, max_length=10)),
                ('min_price',    models.BigIntegerField(blank=True, null=True)),
                ('max_price',    models.BigIntegerField(blank=True, null=True)),
                ('is_active',    models.BooleanField(default=True)),
                ('created_at',   models.DateTimeField(auto_now_add=True)),
                ('user',         models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='alerts', to='accounts.user')),
            ],
        ),
    ]
