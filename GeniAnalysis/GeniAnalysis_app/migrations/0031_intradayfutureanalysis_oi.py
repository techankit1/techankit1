# Generated by Django 4.0.1 on 2022-04-06 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GeniAnalysis_app', '0030_intradayfutureanalysisinterval'),
    ]

    operations = [
        migrations.AddField(
            model_name='intradayfutureanalysis',
            name='oi',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
