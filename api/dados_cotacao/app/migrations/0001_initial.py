# Generated by Django 4.2.6 on 2023-11-01 02:20

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DataSolModel',
            fields=[
                ('DataSolicitada', models.CharField(primary_key=True, serialize=False)),
                ('DolarSolicitado', models.FloatField()),
                ('DolarAtual', models.FloatField()),
            ],
        ),
    ]
