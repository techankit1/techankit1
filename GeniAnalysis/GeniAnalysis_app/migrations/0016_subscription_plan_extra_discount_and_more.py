# Generated by Django 4.0.1 on 2022-03-07 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GeniAnalysis_app', '0015_subscription_plan_transaction_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscription_plan',
            name='extra_discount',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='subscription_plan',
            name='extra_discount_text',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
