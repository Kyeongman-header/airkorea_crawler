# Generated by Django 3.2.9 on 2021-11-22 09:22

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='airkorea',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name='airkorea date published'),
        ),
        migrations.AlterField(
            model_name='gps',
            name='pub_date',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
