# Generated by Django 2.1.2 on 2018-11-12 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20181112_1542'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='adjectives',
            field=models.TextField(default='adjective', max_length=400),
        ),
    ]
