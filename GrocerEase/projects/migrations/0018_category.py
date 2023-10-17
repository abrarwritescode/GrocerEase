# Generated by Django 4.2.5 on 2023-10-17 13:21

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0017_item_seller_alter_item_itemfeaturedimage'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('categoryname', models.CharField(max_length=200)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
            ],
        ),
    ]