# Generated by Django 2.0.6 on 2018-06-16 00:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0029_bet_checked'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bet',
            options={'ordering': ['source']},
        ),
        migrations.AlterModelOptions(
            name='gambler',
            options={'ordering': ['name']},
        ),
        migrations.RenameField(
            model_name='gambler',
            old_name='points_winner',
            new_name='points_result',
        ),
    ]