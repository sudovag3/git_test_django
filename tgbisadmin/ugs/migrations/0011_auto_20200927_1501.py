# Generated by Django 3.1.1 on 2020-09-27 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugs', '0010_auto_20200920_1953'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='typeOfAnswer',
        ),
        migrations.AlterField(
            model_name='profile',
            name='numquestion',
            field=models.PositiveIntegerField(default=0, verbose_name='Номер вопроса'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='typeOfQuestion',
            field=models.TextField(default='Не выбрал', verbose_name='Тип задаваемых вопросов'),
        ),
    ]
