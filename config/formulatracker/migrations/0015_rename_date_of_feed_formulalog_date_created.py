# Generated by Django 4.1.4 on 2023-02-05 03:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('formulatracker', '0014_alter_user_feed_goal'),
    ]

    operations = [
        migrations.RenameField(
            model_name='formulalog',
            old_name='date_of_feed',
            new_name='date_created',
        ),
    ]
