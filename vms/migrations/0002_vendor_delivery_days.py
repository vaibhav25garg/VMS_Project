# Generated by Django 4.2.6 on 2024-05-03 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vms', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='delivery_days',
            field=models.CharField(max_length=20, null=True, verbose_name='Total Day Deliver'),
        ),
    ]
