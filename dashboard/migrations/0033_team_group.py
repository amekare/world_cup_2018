# Generated by Django 2.0.6 on 2018-06-23 05:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0032_auto_20180621_0317'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='group',
            field=models.CharField(choices=[('A', 'Grupo A'), ('B', 'Grupo B'), ('C', 'Grupo C'), ('D', 'Grupo D'), ('E', 'Grupo E'), ('F', 'Grupo F'), ('G', 'Grupo G'), ('H', 'Grupo H')], default='A', max_length=1, null=True),
        ),
    ]