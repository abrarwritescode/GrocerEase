# Generated by Django 4.2.6 on 2024-01-10 05:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0042_remove_order_category_alter_vouchercode_vouchercode'),
    ]

    operations = [
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(default=0)),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.customer')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.item')),
            ],
            options={
                'unique_together': {('customer', 'item')},
            },
        ),
    ]
