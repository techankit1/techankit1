# Generated by Django 4.0.1 on 2022-03-11 06:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GeniAnalysis_app', '0019_genimodedetails_symbol'),
    ]

    operations = [
        migrations.AddField(
            model_name='genimodedetails',
            name='selected_strike_price',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]