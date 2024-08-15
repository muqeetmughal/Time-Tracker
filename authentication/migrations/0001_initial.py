# Generated by Django 5.0.6 on 2024-08-15 08:07

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(error_messages={'max_length': 'This Email is %(show_value)s characters long. The maximum allowed length is %(limit_value)s.', 'required': 'This Field is required!', 'unique': 'This Email is already registered. Please choose a different one.'}, max_length=254, unique=True, verbose_name='Email address')),
                ('role', models.CharField(choices=[('admin', 'Admin'), ('project_manager', 'Project Manager'), ('employee', 'Employee'), ('freelancer', 'Freelancer')], default='employee', max_length=20)),
                ('full_name', models.CharField(blank=True, max_length=50, null=True)),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('time_zone', models.CharField(choices=[('UTC-12', '(-12:00) Etc/GMT-12'), ('UTC-11', '(-11:00) Pacific/Midway'), ('UTC-10', '(-10:00) Pacific/Honolulu'), ('UTC-9', '(-09:00) America/Anchorage'), ('UTC-8', '(-08:00) America/Los_Angeles'), ('UTC-7', '(-07:00) America/Denver'), ('UTC-6', '(-06:00) America/Chicago'), ('UTC-5', '(-05:00) America/New_York'), ('UTC-4', '(-04:00) America/Santiago'), ('UTC-3', '(-03:00) America/Sao_Paulo'), ('UTC-2', '(-02:00) Etc/GMT-2'), ('UTC-1', '(-01:00) Atlantic/Azores'), ('UTC+0', '(+00:00) Europe/London'), ('UTC+1', '(+01:00) Europe/Paris'), ('UTC+2', '(+02:00) Europe/Athens'), ('UTC+3', '(+03:00) Europe/Moscow'), ('UTC+4', '(+04:00) Asia/Dubai'), ('UTC+5', '(+05:00) Asia/Karachi'), ('UTC+6', '(+06:00) Asia/Dhaka'), ('UTC+7', '(+07:00) Asia/Bangkok'), ('UTC+8', '(+08:00) Asia/Singapore'), ('UTC+9', '(+09:00) Asia/Tokyo'), ('UTC+10', '(+10:00) Australia/Sydney'), ('UTC+11', '(+11:00) Pacific/Noumea'), ('UTC+12', '(+12:00) Pacific/Auckland'), ('UTC+13', '(+13:00) Pacific/Fakaofo'), ('UTC+14', '(+14:00) Pacific/Kiritimati')], max_length=6)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=True)),
                ('is_verified', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]