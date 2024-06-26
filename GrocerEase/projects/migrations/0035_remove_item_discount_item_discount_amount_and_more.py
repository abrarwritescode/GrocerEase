# Generated by Django 4.2.5 on 2023-12-16 10:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0034_discount_item_discount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='discount',
        ),
        migrations.AddField(
            model_name='item',
            name='discount_amount',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='item',
            name='discount_name',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AddField(
            model_name='item',
            name='discount_percentage',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=5),
        ),
        migrations.AddField(
            model_name='item',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Discount',
        ),
    ]
