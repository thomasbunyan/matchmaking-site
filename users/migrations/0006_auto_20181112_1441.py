# Generated by Django 2.1.2 on 2018-11-12 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20181112_1437'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='hobby',
            options={'verbose_name_plural': 'hobbies'},
        ),
        migrations.AlterField(
            model_name='profile',
            name='hobbies',
            field=models.ManyToManyField(blank=True, related_name='categories', to='users.Hobby'),
        ),
    ]
