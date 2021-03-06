# Generated by Django 4.0.5 on 2022-07-07 11:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0003_alter_discount_stripe_discount_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='percentage_off',
            field=models.FloatField(default=10, validators=[django.core.validators.MinValueValidator(5.0), django.core.validators.MaxValueValidator(100.0)]),
        ),
    ]
