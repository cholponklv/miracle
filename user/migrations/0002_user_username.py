# Generated by Django 4.2.2 on 2023-06-19 14:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='username',
            field=models.CharField(default=datetime.datetime(2023, 6, 19, 14, 8, 49, 219807, tzinfo=datetime.timezone.utc), max_length=234, unique=True),
            preserve_default=False,
        ),
    ]