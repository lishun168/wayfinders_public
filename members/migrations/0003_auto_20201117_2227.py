# Generated by Django 3.1.2 on 2020-11-17 22:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0002_auto_20201102_2139'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='companyindustry',
            options={'verbose_name': 'Company Industry', 'verbose_name_plural': 'Company Industries'},
        ),
        migrations.AlterModelOptions(
            name='membercompany',
            options={'verbose_name': 'Member Companies', 'verbose_name_plural': 'Member Companies'},
        ),
        migrations.AlterModelOptions(
            name='memberskills',
            options={'verbose_name': 'Member Skills', 'verbose_name_plural': 'Member Skills'},
        ),
        migrations.AddField(
            model_name='member',
            name='main_image',
            field=models.ImageField(blank=True, upload_to='profile_pic/'),
        ),
    ]
