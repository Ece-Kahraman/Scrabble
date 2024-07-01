# Generated by Django 4.2.4 on 2023-09-12 13:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('boards', '0013_alter_score_room'),
    ]

    operations = [
        migrations.CreateModel(
            name='Hand',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('letters', picklefield.fields.PickledObjectField(editable=False)),
                ('score', models.IntegerField(default=0)),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='room',
            name='creator',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.PROTECT, related_name='creator', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='room',
            name='other',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='other', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='room',
            name='player_count',
            field=models.IntegerField(default=1),
        ),
        migrations.DeleteModel(
            name='Score',
        ),
        migrations.AddField(
            model_name='hand',
            name='room',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boards.room'),
        ),
    ]
