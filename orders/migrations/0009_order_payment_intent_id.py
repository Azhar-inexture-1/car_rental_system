# Generated by Django 4.0.5 on 2022-07-08 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_order_discount'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_intent_id',
            field=models.CharField(default='invalid', max_length=100, unique=True),
            preserve_default=False,
        ),
    ]
