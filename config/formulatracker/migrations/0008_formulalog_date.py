# Generated by Django 4.1.4 on 2023-01-27 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formulatracker', '0007_formulalog_date_of_feed'),
    ]

    operations = [
        migrations.AddField(
            model_name='formulalog',
            name='date',
            field=models.DateField(null=True),
        ),
    ]
