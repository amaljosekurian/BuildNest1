# Generated by Django 5.0.1 on 2024-02-05 15:54

import django.contrib.auth.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlotBasicData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('approximate_budget', models.DecimalField(decimal_places=2, max_digits=10)),
                ('plot_address', models.TextField()),
                ('plot_id_document', models.FileField(upload_to='plot_id_documents/')),
                ('plot_location', models.CharField(max_length=255)),
                ('square_feet', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ProjectData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_floors', models.PositiveIntegerField()),
                ('work_area_required', models.BooleanField(default=False)),
                ('store_room_required', models.BooleanField(default=False)),
                ('dining_room_required', models.BooleanField(default=False)),
                ('kitchen_type', models.CharField(choices=[('open', 'Open Kitchen'), ('normal', 'Normal Kitchen')], max_length=10)),
                ('additional_amenities', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Worker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('worker_id', models.CharField(max_length=20)),
                ('worker_name', models.CharField(max_length=100)),
                ('worker_region', models.CharField(max_length=100)),
                ('worker_job_role', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=50)),
                ('salary_frequency', models.CharField(max_length=10)),
                ('salary', models.DecimalField(decimal_places=2, max_digits=10)),
                ('site_id', models.CharField(max_length=20)),
                ('contractor_id', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='PlotData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_is_Done', models.BooleanField(default=False)),
                ('plan_pdf', models.FileField(blank=True, null=True, upload_to='pdfs/')),
                ('plan_fee', models.BigIntegerField(null=True)),
                ('payment_request', models.BooleanField(default=False)),
                ('plotBaseData', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='BuildNestApp.plotbasicdata')),
                ('projectdata', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='BuildNestApp.projectdata')),
            ],
        ),
        migrations.CreateModel(
            name='PlotImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plot_images', models.ImageField(blank=True, null=True, upload_to='plot_images/')),
                ('plot', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='BuildNestApp.plotdata')),
            ],
        ),
        migrations.CreateModel(
            name='FloorDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('floor_number', models.PositiveIntegerField()),
                ('num_rooms', models.PositiveIntegerField()),
                ('num_bathrooms', models.PositiveIntegerField()),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BuildNestApp.projectdata')),
            ],
        ),
        migrations.CreateModel(
            name='Usertable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone', models.CharField(max_length=20)),
                ('is_contractor', models.BooleanField(default=False)),
                ('is_client', models.BooleanField(default=False)),
                ('is_purchase_manager', models.BooleanField(default=False)),
                ('is_admin', models.BooleanField(default=False)),
                ('is_engineer', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AddField(
            model_name='plotdata',
            name='contractor',
            field=models.ForeignKey(limit_choices_to={'is_contractor': True}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contractor', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='plotdata',
            name='engineer',
            field=models.ForeignKey(limit_choices_to={'is_engineer': True}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='engineer', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='plotdata',
            name='plot_user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
