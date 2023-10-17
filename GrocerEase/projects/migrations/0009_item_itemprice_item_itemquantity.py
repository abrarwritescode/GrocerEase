# Generated by Django 4.2.5 on 2023-10-04 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_seller_rename_description_item_itemdescription_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='itemprice',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
        migrations.AddField(
            model_name='item',
            name='itemquantity',
            field=models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
        ),
    ]