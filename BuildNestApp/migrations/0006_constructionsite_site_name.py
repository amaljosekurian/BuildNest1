# Generated by Django 5.0.1 on 2024-02-19 09:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BuildNestApp', '0005_remove_constructionsite_site_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='constructionsite',
            name='site_name',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
