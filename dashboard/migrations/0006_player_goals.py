# Generated by Django 2.0.6 on 2018-06-10 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0005_auto_20180610_1930'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='goals',
            field=models.IntegerField(default=0),
        ),
    ]
