# Generated by Django 4.0.1 on 2022-03-11 09:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GeniAnalysis_app', '0020_genimodedetails_selected_strike_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='genimodedetails',
            name='genimode_status',
        ),
        migrations.AddField(
            model_name='genimodedetails',
            name='genimode_stop_loss_on',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='genimodedetails',
            name='genimode_target_on',
            field=models.BooleanField(default=False),
        ),
    ]
