# Generated by Django 4.1 on 2022-10-22 14:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0003_alter_userprofileinfo_fullname'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofileinfo',
            name='date_of_birth',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='userurl',
            name='timestamp',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
