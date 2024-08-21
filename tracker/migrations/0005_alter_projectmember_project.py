# Generated by Django 5.0.6 on 2024-08-20 14:09

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0004_project_is_deleted'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectmember',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='tracker.project'),
        ),
    ]
