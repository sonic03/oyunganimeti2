# Generated by Django 3.2 on 2021-04-27 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0007_pincode'),
        ('carts', '0002_cart_subtotal'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='pincode',
            field=models.ManyToManyField(blank=True, to='products.PinCode'),
        ),
    ]
