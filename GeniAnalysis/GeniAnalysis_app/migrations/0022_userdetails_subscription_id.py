# Generated by Django 4.0.1 on 2022-03-12 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GeniAnalysis_app', '0021_remove_genimodedetails_genimode_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdetails',
            name='subscription_id',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]