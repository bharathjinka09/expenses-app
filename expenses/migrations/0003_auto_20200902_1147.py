# Generated by Django 3.1 on 2020-09-02 06:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('expenses', '0002_auto_20200902_1144'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='article',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='book',
            name='title',
            field=models.CharField(default='', max_length=255),
        ),
    ]
