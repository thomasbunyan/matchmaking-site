# Generated by Django 2.1.2 on 2018-11-12 10:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='gender',
            field=models.CharField(default='notspecified', max_length=100),
        ),
    ]
