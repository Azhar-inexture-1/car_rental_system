# Generated by Django 4.0.5 on 2022-07-07 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0004_discount_percentage_off'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='discount',
            name='user_specific',
        ),
    ]
