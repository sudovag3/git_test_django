# Generated by Django 3.1.1 on 2020-12-12 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugs', '0043_webinarsdjango_webinarvideourl'),
    ]

    operations = [
        migrations.AlterField(
            model_name='registers',
            name='user_who_know_impact',
            field=models.TextField(default='Не определено', verbose_name='Откуда знает'),
        ),
        migrations.AlterField(
            model_name='webinarsdjango',
            name='webinarVideoUrl',
            field=models.TextField(default=0, verbose_name='Ссылка на запись'),
        ),
    ]
