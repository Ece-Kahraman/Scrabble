# Generated by Django 4.2.4 on 2023-09-07 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0011_rename_player_id_score_player'),
    ]

    operations = [
        migrations.RenameField(
            model_name='score',
            old_name='room_id',
            new_name='room',
        ),
    ]
