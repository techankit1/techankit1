# Generated by Django 4.0.1 on 2022-04-08 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GeniAnalysis_app', '0032_bnfhistorylog_call_ltp_bnfhistorylog_call_oi_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='MarketWeekOfDate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('off_date', models.DateField()),
            ],
        ),
    ]
