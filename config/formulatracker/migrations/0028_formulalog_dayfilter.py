# Generated by Django 4.1.4 on 2023-02-10 22:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formulatracker', '0027_remove_weight_weight_units'),
    ]

    operations = [
        migrations.AddField(
            model_name='formulalog',
            name='dayfilter',
            field=models.DateField(null=True),
        ),
    ]
