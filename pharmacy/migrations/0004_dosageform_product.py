# Generated by Django 3.2.6 on 2022-03-31 23:25

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('pharmacy', '0003_auto_20220331_1632'),
    ]

    operations = [
        migrations.CreateModel(
            name='DosageForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('dci', models.CharField(default=None, max_length=100)),
                ('tradename', models.CharField(default=None, max_length=100)),
                ('dose', models.CharField(default='100 mg', max_length=10)),
                ('description', models.CharField(max_length=400)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('img', models.ImageField(blank=True, null=True, upload_to='images/')),
                ('stock', models.IntegerField(default=0)),
                ('cantVendidos', models.IntegerField(default=0)),
                ('valid_from', models.DateTimeField(blank=True, default=django.utils.timezone.now, null=True)),
                ('valid_to', models.DateTimeField(null=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('dosageForm', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='drugs', to='pharmacy.dosageform')),
            ],
        ),
    ]