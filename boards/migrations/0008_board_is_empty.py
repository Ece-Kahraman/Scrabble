# Generated by Django 4.2.4 on 2023-09-05 08:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0007_room_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='board',
            name='is_empty',
            field=models.BooleanField(default=True),
        ),
    ]
