# Generated by Django 2.1 on 2018-12-11 11:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0018_profile_prevheat'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='newMatches',
            field=models.IntegerField(default=0),
        ),
    ]
