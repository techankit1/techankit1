# Generated by Django 4.0.1 on 2022-02-08 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GeniAnalysis_app', '0005_saveopenmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]