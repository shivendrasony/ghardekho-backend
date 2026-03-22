from django.db import migrations, models

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]
    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id',           models.BigAutoField(auto_created=True, primary_key=True)),
                ('password',     models.CharField(max_length=128)),
                ('last_login',   models.DateTimeField(blank=True, null=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('email',        models.EmailField(max_length=254, unique=True)),
                ('name',         models.CharField(max_length=150)),
                ('phone',        models.CharField(blank=True, max_length=15)),
                ('role',         models.CharField(choices=[('buyer','Buyer'),('owner','Owner'),('agent','Agent'),('admin','Admin')], default='buyer', max_length=10)),
                ('city',         models.CharField(blank=True, max_length=100)),
                ('avatar',       models.ImageField(blank=True, null=True, upload_to='avatars/')),
                ('agency',       models.CharField(blank=True, max_length=200)),
                ('rera_number',  models.CharField(blank=True, max_length=100)),
                ('experience',   models.PositiveIntegerField(default=0)),
                ('is_verified',  models.BooleanField(default=False)),
                ('is_active',    models.BooleanField(default=True)),
                ('is_staff',     models.BooleanField(default=False)),
                ('date_joined',  models.DateTimeField(auto_now_add=True)),
                ('updated_at',   models.DateTimeField(auto_now=True)),
                ('groups',       models.ManyToManyField(blank=True, related_name='accounts_user_groups', to='auth.group')),
                ('user_permissions', models.ManyToManyField(blank=True, related_name='accounts_user_perms', to='auth.permission')),
            ],
            options={'ordering': ['-date_joined'], 'verbose_name': 'User'},
        ),
    ]
