# Generated by Django 4.2.6 on 2023-10-22 20:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0031_rename_user_favorite_customer'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='favorite_count',
            field=models.IntegerField(default=0),
        ),
    ]
