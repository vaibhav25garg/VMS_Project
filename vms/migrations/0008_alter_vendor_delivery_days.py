# Generated by Django 4.1.10 on 2024-05-06 06:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vms', '0007_alter_vendor_average_response_time_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vendor',
            name='delivery_days',
            field=models.IntegerField(null=True, verbose_name='Total Day Deliver'),
        ),
    ]
