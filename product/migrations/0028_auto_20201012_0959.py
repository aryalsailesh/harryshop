# Generated by Django 3.1.1 on 2020-10-12 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0027_orderitem_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderitem',
            name='payment',
            field=models.CharField(choices=[('Cash on delivery', 'Cash on delivery'), ('esewa', 'esewa')], max_length=50, null=True),
        ),
    ]
