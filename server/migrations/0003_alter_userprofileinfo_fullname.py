# Generated by Django 4.1 on 2022-10-21 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0002_alter_userprofileinfo_gender'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofileinfo',
            name='fullname',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
