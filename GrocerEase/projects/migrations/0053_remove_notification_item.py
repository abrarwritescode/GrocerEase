# Generated by Django 4.2.6 on 2024-01-14 18:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0052_alter_orderitem_managers_remove_orderitem_is_deleted'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='notification',
            name='item',
        ),
    ]