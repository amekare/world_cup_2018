# Generated by Django 2.0.6 on 2018-06-21 03:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0031_auto_20180618_0159'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='gambler',
            options={},
        ),
        migrations.AlterUniqueTogether(
            name='bet',
            unique_together={('source', 'match')},
        ),
    ]
