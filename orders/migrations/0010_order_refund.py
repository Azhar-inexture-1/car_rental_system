# Generated by Django 4.0.5 on 2022-07-08 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0009_order_payment_intent_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='refund',
            field=models.BooleanField(default=False),
        ),
    ]
