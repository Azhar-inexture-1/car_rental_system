# Generated by Django 4.0.5 on 2022-07-07 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0002_discount_user_discount_user_specific'),
    ]

    operations = [
        migrations.AlterField(
            model_name='discount',
            name='stripe_discount_id',
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
