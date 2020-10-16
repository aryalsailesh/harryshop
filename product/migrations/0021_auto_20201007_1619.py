# Generated by Django 3.1.1 on 2020-10-07 10:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0020_auto_20201006_2027'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-updated']},
        ),
        migrations.RemoveField(
            model_name='order',
            name='order',
        ),
        migrations.AddField(
            model_name='order',
            name='order',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, to='product.orderitem'),
            preserve_default=False,
        ),
    ]
