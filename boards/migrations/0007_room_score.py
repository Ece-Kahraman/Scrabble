# Generated by Django 4.2.4 on 2023-09-04 13:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0006_alter_board_board'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='score',
            field=models.IntegerField(default=0),
        ),
    ]
