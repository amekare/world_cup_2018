# Generated by Django 2.0.6 on 2018-06-14 05:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0021_auto_20180614_0444'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gambler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.CharField(max_length=48)),
                ('points_winner', models.IntegerField()),
                ('points_score', models.IntegerField()),
                ('points_8vo', models.IntegerField()),
                ('points_4vo', models.IntegerField()),
                ('points_semi', models.IntegerField()),
                ('points_3er', models.IntegerField()),
                ('points_final', models.IntegerField()),
            ],
        ),
    ]
