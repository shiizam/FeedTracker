# Generated by Django 4.1.4 on 2023-01-29 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formulatracker', '0010_alter_userprofile_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='feed_goal',
            field=models.SmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(blank=True, upload_to='profile_pics'),
        ),
    ]
