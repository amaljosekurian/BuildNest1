# Generated by Django 5.0.1 on 2024-03-07 05:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BuildNestApp', '0033_remove_worker_site_delete_constructionsite'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConstructionSite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=100, null=True)),
                ('start_date', models.DateField(null=True)),
                ('end_date', models.DateField(null=True)),
                ('upload_permits', models.FileField(upload_to='permits/')),
                ('approximate_budget', models.DecimalField(decimal_places=2, max_digits=10, null=True)),
                ('additional_description', models.TextField(null=True)),
                ('site_location', models.CharField(max_length=255, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]