# Generated by Django 4.2.6 on 2024-05-04 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vms', '0005_alter_vendor_delivery_days'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchaseorder',
            name='_delivery_date_set',
            field=models.BooleanField(default=False, editable=False),
        ),
    ]
