# Generated by Django 3.2.8 on 2021-11-09 12:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('senseikuApp', '0018_auto_20211109_1045'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='gopay',
            field=models.CharField(default='', max_length=300),
        ),
    ]