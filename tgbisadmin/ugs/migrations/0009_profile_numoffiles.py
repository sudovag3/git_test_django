# Generated by Django 3.1.1 on 2020-09-20 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugs', '0008_auto_20200919_1411'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='numOfFiles',
            field=models.PositiveIntegerField(default=0, verbose_name='Количество файлов'),
        ),
    ]