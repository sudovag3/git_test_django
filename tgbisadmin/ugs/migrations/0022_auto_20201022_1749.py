# Generated by Django 3.1.1 on 2020-10-22 14:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugs', '0021_auto_20201022_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registers',
            name='userID',
            field=models.PositiveIntegerField(unique=True, verbose_name='ID'),
        ),
    ]
