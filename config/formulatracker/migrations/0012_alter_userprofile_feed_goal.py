# Generated by Django 4.1.4 on 2023-01-29 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formulatracker', '0011_user_feed_goal_user_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='feed_goal',
            field=models.SmallIntegerField(default=0, null=True),
        ),
    ]
