# Generated by Django 4.2.4 on 2023-09-07 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0008_board_is_empty'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='player_count',
            field=models.IntegerField(default=0),
        ),
    ]
