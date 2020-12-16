# Generated by Django 3.1.1 on 2020-09-18 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ugs', '0005_question'),
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('respondentId', models.PositiveIntegerField(unique=True, verbose_name='Id ответчика')),
                ('numAnswer', models.PositiveIntegerField(verbose_name='Номер ответа')),
                ('textAnswer', models.TextField(verbose_name='Содержимое ответа')),
                ('typeOfAnswer', models.TextField(verbose_name='Тип ответа')),
            ],
            options={
                'verbose_name': 'Ответ',
                'verbose_name_plural': 'Ответы',
            },
        ),
    ]