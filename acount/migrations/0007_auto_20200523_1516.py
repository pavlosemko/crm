# Generated by Django 3.0.6 on 2020-05-23 12:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('acount', '0006_leads'),
    ]

    operations = [
        migrations.AddField(
            model_name='leads',
            name='about_client',
            field=models.TextField(blank=True, max_length=250),
        ),
        migrations.AddField(
            model_name='leads',
            name='role',
            field=models.CharField(choices=[('new', 'New'), ('account_fixing', 'Account_fixing'), ('not_interested', 'Not interested'), ('deposit', 'Deposit'), ('registered', 'Registered'), ('waiting', 'Waiting'), ('sales_work', 'Sales work')], default='new', max_length=25),
        ),
        migrations.AddField(
            model_name='leads',
            name='source',
            field=models.TextField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='leads',
            name='manager',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL),
        ),
    ]
