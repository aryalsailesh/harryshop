# Generated by Django 3.1.1 on 2020-10-09 08:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0023_auto_20201007_1629'),
    ]

    operations = [
        migrations.AlterField(
            model_name='checkout',
            name='appartment_no',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
