# Generated by Django 3.2.6 on 2022-04-03 01:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0004_dosageform_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='dosageform',
            name='cantProd',
            field=models.IntegerField(default=0),
        ),
    ]
