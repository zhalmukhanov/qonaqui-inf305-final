# Generated by Django 4.0.4 on 2022-05-08 16:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_payment_registration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='registration',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='main.registeration'),
        ),
    ]
