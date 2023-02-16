# Generated by Django 4.1.4 on 2023-02-06 19:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formulatracker', '0018_delete_units'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='units',
            field=models.CharField(choices=[('METRIC', 'Metric'), ('IMPERIAL', 'Imperial')], default='Imperial', max_length=8),
        ),
    ]
