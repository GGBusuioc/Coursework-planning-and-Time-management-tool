# Generated by Django 2.0.1 on 2018-03-29 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sis', '0021_auto_20180329_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usercourseworkmembership',
            name='percentage',
            field=models.IntegerField(choices=[(0, '0'), (25, '25'), (50, '50'), (75, '75'), (100, '100')], default=0),
        ),
    ]
