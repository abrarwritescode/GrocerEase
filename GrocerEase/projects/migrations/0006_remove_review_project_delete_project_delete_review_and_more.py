# Generated by Django 4.2.5 on 2023-10-01 18:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_customer_is_verified_customer_otp'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='project',
        ),
        migrations.DeleteModel(
            name='project',
        ),
        migrations.DeleteModel(
            name='Review',
        ),
        migrations.DeleteModel(
            name='Tag',
        ),
    ]
