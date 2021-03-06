# Generated by Django 4.0.5 on 2022-06-08 12:24

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_user_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone_number',
            field=models.CharField(max_length=10, validators=[django.core.validators.RegexValidator(message='Invalid phone number.', regex='^d{10}$')]),
        ),
    ]
