# Generated by Django 3.1.1 on 2020-10-16 20:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugs', '0018_auto_20201016_2331'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='webinarIDRegister',
            field=models.PositiveIntegerField(verbose_name='Id выбранного вебинара'),
        ),
    ]