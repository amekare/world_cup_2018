# Generated by Django 2.0.6 on 2018-06-14 01:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0018_auto_20180613_2250'),
    ]

    operations = [
        migrations.CreateModel(
            name='FirstMatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team1', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='fteam1', to='dashboard.Team')),
                ('team2', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='fteam2', to='dashboard.Team')),
            ],
        ),
        migrations.AlterField(
            model_name='match',
            name='source',
            field=models.CharField(default='Oficial', max_length=48),
        ),
        migrations.AlterField(
            model_name='round',
            name='round',
            field=models.CharField(choices=[('1', 'Primera fase'), ('2', 'Octavos'), ('3', 'Cuarto'), ('4', 'Semifinales'), ('5', 'Tercer lugar'), ('6', 'Finales')], default='1er', max_length=1),
        ),
    ]
