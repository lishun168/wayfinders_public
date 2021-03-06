# Generated by Django 3.1.2 on 2020-11-02 21:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('members', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name': 'Company', 'verbose_name_plural': 'Companies'},
        ),
        migrations.AlterModelOptions(
            name='gallery',
            options={'verbose_name': 'Gallery', 'verbose_name_plural': 'Galleries'},
        ),
        migrations.AlterModelOptions(
            name='industry',
            options={'verbose_name': 'Industry', 'verbose_name_plural': 'Industries'},
        ),
        migrations.AlterModelOptions(
            name='permissions',
            options={'verbose_name': 'Permission', 'verbose_name_plural': 'Permissions'},
        ),
        migrations.RemoveField(
            model_name='member',
            name='company_name',
        ),
    ]
