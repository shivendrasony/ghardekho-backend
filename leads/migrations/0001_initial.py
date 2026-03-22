from django.db import migrations, models
import django.db.models.deletion

class Migration(migrations.Migration):
    initial = True
    dependencies = [
        ('accounts', '0001_initial'),
        ('properties', '0001_initial'),
    ]
    operations = [
        migrations.CreateModel(
            name='Lead',
            fields=[
                ('id',            models.BigAutoField(auto_created=True, primary_key=True)),
                ('name',          models.CharField(max_length=150)),
                ('email',         models.EmailField(blank=True)),
                ('phone',         models.CharField(max_length=15)),
                ('message',       models.TextField(blank=True)),
                ('visit_date',    models.DateField(blank=True, null=True)),
                ('visit_message', models.TextField(blank=True)),
                ('status',        models.CharField(choices=[('new','New'),('contacted','Contacted'),('visit_set','Visit Scheduled'),('negotiating','Negotiating'),('closed','Closed'),('lost','Lost')], default='new', max_length=15)),
                ('agent_note',    models.TextField(blank=True)),
                ('created_at',    models.DateTimeField(auto_now_add=True)),
                ('updated_at',    models.DateTimeField(auto_now=True)),
                ('property',      models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='leads', to='properties.property')),
                ('buyer',         models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sent_leads', to='accounts.user')),
            ],
            options={'ordering': ['-created_at']},
        ),
        migrations.CreateModel(
            name='VisitRequest',
            fields=[
                ('id',         models.BigAutoField(auto_created=True, primary_key=True)),
                ('visit_date', models.DateField()),
                ('message',    models.TextField(blank=True)),
                ('status',     models.CharField(choices=[('pending','Pending'),('confirmed','Confirmed'),('cancelled','Cancelled'),('completed','Completed')], default='pending', max_length=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('property',   models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visits', to='properties.property')),
                ('buyer',      models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='visits', to='accounts.user')),
            ],
            options={'ordering': ['-created_at']},
        ),
    ]
