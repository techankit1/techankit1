# Generated by Django 4.0.1 on 2022-03-21 05:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GeniAnalysis_app', '0022_userdetails_subscription_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='transaction',
            name='start_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
