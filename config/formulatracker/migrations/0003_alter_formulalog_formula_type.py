# Generated by Django 4.1.4 on 2023-01-24 17:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('formulatracker', '0002_rename_formula_consumed_formulalog_feed_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formulalog',
            name='formula_type',
            field=models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='formulatracker.formula'),
        ),
    ]
