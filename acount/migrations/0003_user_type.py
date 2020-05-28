# Generated by Django 3.0.6 on 2020-05-23 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('acount', '0002_auto_20200523_0122'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='type',
            field=models.CharField(choices=[('SLS', 'sales'), ('CLS', 'closer'), ('ADM', 'admin')], default='SLS', max_length=25),
        ),
    ]
