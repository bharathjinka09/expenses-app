# Generated by Django 3.1 on 2020-09-02 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('article', models.CharField(default='', max_length=255)),
                ('title', models.CharField(default='', max_length=255)),
                ('author', models.CharField(default='', max_length=255)),
                ('page_no', models.CharField(default='', max_length=255)),
            ],
            options={
                'db_table': 'Book',
            },
        ),
    ]
