# Generated by Django 4.1.4 on 2023-01-27 19:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formulatracker', '0006_alter_formulalog_feed_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='formulalog',
            name='date_of_feed',
            field=models.DateField(auto_now_add=True, null=True),
        ),
    ]