# Generated by Django 2.0.1 on 2018-03-13 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sis', '0006_auto_20180313_1410'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursework',
            name='end',
            field=models.CharField(default='unspecified', max_length=255),
        ),
        migrations.AlterField(
            model_name='coursework',
            name='start',
            field=models.CharField(default='unspecified', max_length=255),
        ),
    ]
