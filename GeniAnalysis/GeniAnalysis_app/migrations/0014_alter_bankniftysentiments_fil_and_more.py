# Generated by Django 4.0.1 on 2022-02-17 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('GeniAnalysis_app', '0013_niftysentiments_bankniftysentiments'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankniftysentiments',
            name='fil',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='bankniftysentiments',
            name='oi',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='bankniftysentiments',
            name='preop',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='bankniftysentiments',
            name='sgx',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='niftysentiments',
            name='fil',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='niftysentiments',
            name='oi',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='niftysentiments',
            name='preop',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='niftysentiments',
            name='sgx',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
