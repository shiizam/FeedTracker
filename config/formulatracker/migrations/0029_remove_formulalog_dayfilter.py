# Generated by Django 4.1.4 on 2023-02-10 23:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('formulatracker', '0028_formulalog_dayfilter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='formulalog',
            name='dayfilter',
        ),
    ]
