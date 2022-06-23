# Generated by Django 4.0.5 on 2022-06-17 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0005_alter_car_transmission_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='transmission_type',
            field=models.CharField(choices=[('manual', 'manual'), ('automatic', 'automatic')], default='manual', max_length=10),
        ),
    ]