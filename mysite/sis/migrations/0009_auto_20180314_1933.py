# Generated by Django 2.0.1 on 2018-03-14 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sis', '0008_coursework_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursework',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]