from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('accounts', '0001_initial'),
    ]
    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id',         models.BigAutoField(auto_created=True, primary_key=True)),
                ('name',       models.CharField(max_length=100, unique=True)),
                ('slug',       models.SlugField(blank=True, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={'ordering': ['name'], 'verbose_name_plural': 'Categories'},
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id',           models.BigAutoField(auto_created=True, primary_key=True)),
                ('title',        models.CharField(max_length=300)),
                ('slug',         models.SlugField(blank=True, max_length=320, unique=True)),
                ('excerpt',      models.TextField(max_length=500)),
                ('content',      models.TextField()),
                ('cover_image',  models.ImageField(blank=True, null=True, upload_to='blog/')),
                ('status',       models.CharField(choices=[('draft','Draft'),('published','Published')], default='draft', max_length=10)),
                ('is_featured',  models.BooleanField(default=False)),
                ('read_time',    models.PositiveSmallIntegerField(default=5)),
                ('views',        models.PositiveIntegerField(default=0)),
                ('tags',         models.CharField(blank=True, max_length=300)),
                ('published_at', models.DateTimeField(blank=True, null=True)),
                ('created_at',   models.DateTimeField(auto_now_add=True)),
                ('updated_at',   models.DateTimeField(auto_now=True)),
                ('author',       models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='blog_posts', to='accounts.user')),
                ('category',     models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='posts', to='blog.category')),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
