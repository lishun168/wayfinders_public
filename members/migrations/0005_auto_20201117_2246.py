# Generated by Django 3.1.2 on 2020-11-17 22:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0004_auto_20201117_2243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='main_image',
            field=models.ImageField(blank=True, upload_to='static/members/profile_pic/'),
        ),
    ]
