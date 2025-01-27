# Generated by Django 4.2.4 on 2023-09-12 13:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('boards', '0014_hand_room_creator_room_other_alter_room_player_count_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Leaderboard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('overall_score', models.IntegerField(default=0)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='room',
            name='creator_hand',
            field=picklefield.fields.PickledObjectField(default=django.utils.timezone.now, editable=False),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='room',
            name='creator_score',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='room',
            name='other_hand',
            field=picklefield.fields.PickledObjectField(editable=False, null=True),
        ),
        migrations.AddField(
            model_name='room',
            name='other_score',
            field=models.IntegerField(null=True),
        ),
        migrations.DeleteModel(
            name='Hand',
        ),
    ]
