# Generated by Django 5.1.1 on 2024-11-20 22:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hello', '0007_usuarioleafpoints'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuarioleafpoints',
            name='misiones_completadas',
        ),
    ]