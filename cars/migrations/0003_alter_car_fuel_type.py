# Generated by Django 4.0.5 on 2022-06-16 07:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0002_alter_brand_name_alter_type_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='fuel_type',
            field=models.IntegerField(choices=[('petrol', 'petrol'), ('diesel', 'diesel'), ('gas', 'gas'), ('electric', 'electric')], default=1),
        ),
    ]
