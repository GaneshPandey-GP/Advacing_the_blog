# Generated by Django 3.1.1 on 2020-10-14 02:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0002_post_read_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='read_time',
            field=models.IntegerField(default=0),
        ),
    ]
