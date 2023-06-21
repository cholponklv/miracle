# Generated by Django 4.2.2 on 2023-06-20 20:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('game', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='heroteam',
            name='hero',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hero_team', to='game.hero'),
        ),
        migrations.AlterField(
            model_name='heroteam',
            name='team',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='hero_team', to='game.team'),
        ),
        migrations.AlterField(
            model_name='team',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team', to=settings.AUTH_USER_MODEL),
        ),
    ]
