# Generated by Django 3.1.1 on 2020-10-31 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugs', '0032_webinarsdjango_webinarurl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='webinarsdjango',
            name='webinarID',
            field=models.TextField(verbose_name='Идентификатор Вебинара'),
        ),
    ]
