# Generated by Django 2.0.6 on 2018-06-30 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0041_round_qualified_revision'),
    ]

    operations = [
        migrations.AlterField(
            model_name='round',
            name='position',
            field=models.CharField(default='', max_length=24, null=True),
        ),
    ]
