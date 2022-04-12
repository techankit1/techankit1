# Generated by Django 4.0.1 on 2022-02-11 09:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GeniAnalysis_app', '0007_remove_userdetails_is_approved_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='is_login',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userdetails',
            name='login_token',
            field=models.CharField(blank=True, default='', max_length=100, null=True),
        ),
    ]