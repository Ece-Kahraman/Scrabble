# Generated by Django 4.2.4 on 2023-08-31 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('boards', '0004_alter_board_board'),
    ]

    operations = [
        migrations.AlterField(
            model_name='board',
            name='board',
            field=models.BinaryField(),
        ),
    ]
