# Generated by Django 3.1.1 on 2020-10-14 02:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Posts', '0003_auto_20201014_0754'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='read_time',
            new_name='reading_time',
        ),
    ]
