# Generated by Django 2.0.1 on 2018-03-15 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sis', '0009_auto_20180314_1933'),
    ]

    operations = [
        migrations.AddField(
            model_name='coursework',
            name='percentage',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]