# Generated by Django 2.0.1 on 2018-04-23 23:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sis', '0031_auto_20180423_2301'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='coursework',
            unique_together={('module', 'title')},
        ),
        migrations.AlterIndexTogether(
            name='coursework',
            index_together={('module', 'title')},
        ),
    ]