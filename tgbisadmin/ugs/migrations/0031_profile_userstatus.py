# Generated by Django 3.1.1 on 2020-10-30 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugs', '0030_auto_20201029_1214'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='userStatus',
            field=models.TextField(default='Посетитель', verbose_name='Статус пользователя'),
        ),
    ]
