# Generated by Django 4.0.4 on 2022-05-07 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_room_ects'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='ects',
            field=models.DecimalField(decimal_places=1, max_digits=19),
        ),
    ]
