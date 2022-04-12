# Generated by Django 4.0.1 on 2022-04-06 04:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('GeniAnalysis_app', '0029_intradayfutureanalysis'),
    ]

    operations = [
        migrations.CreateModel(
            name='IntradayFutureAnalysisInterval',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interval', models.IntegerField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GeniAnalysis_app.userdetails')),
            ],
        ),
    ]
