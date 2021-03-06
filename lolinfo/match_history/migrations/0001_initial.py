# Generated by Django 3.1 on 2020-09-11 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Summoner',
            fields=[
                ('name', models.TextField(max_length=100, primary_key=True, serialize=False)),
                ('region', models.CharField(choices=[(0, 'EUW'), (1, 'NA'), (2, 'EUNE')], default=0, max_length=9)),
                ('icon_id', models.IntegerField(default=0)),
                ('level', models.IntegerField(default=0)),
                ('lp', models.IntegerField(null=True)),
                ('rank', models.TextField(max_length=50, null=True)),
                ('tier', models.CharField(max_length=50, null=True)),
                ('winrate', models.FloatField(null=True)),
                ('wins', models.IntegerField(null=True)),
                ('losses', models.IntegerField(null=True)),
                ('matches_ref', models.JSONField(null=True)),
                ('matches_history', models.JSONField(null=True)),
            ],
            options={
                'unique_together': {('name', 'region')},
            },
        ),
    ]
