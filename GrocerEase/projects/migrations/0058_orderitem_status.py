# Generated by Django 4.2.5 on 2024-01-17 14:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0057_delete_voucherusage'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='status',
            field=models.CharField(choices=[('Pending', 'Pending'), ('Processing', 'Processing'), ('Shipped', 'Shipped'), ('Delivered', 'Delivered'), ('Cancelled', 'Cancelled')], default='Pending', max_length=20),
        ),
    ]
