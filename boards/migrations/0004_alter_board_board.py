# Generated by Django 4.2.4 on 2023-08-31 07:29

from django.db import migrations
import picklefield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0003_alter_board_board'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='board',
            field=picklefield.fields.PickledObjectField(editable=False),
        ),
    ]
