# Generated by Django 5.0.6 on 2024-07-16 10:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0003_alter_profile_archived_at'),
        ('tracker', '0002_alter_activity_archived_at_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='membership',
            unique_together={('project', 'user')},
        ),
    ]
