# Generated by Django 2.0.1 on 2018-03-29 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sis', '0017_usercourseworkmembership_coursework'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercourseworkmembership',
            name='completed',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='usercourseworkmembership',
            name='progress',
            field=models.IntegerField(default=0),
        ),
    ]
