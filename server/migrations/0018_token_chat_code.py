# Generated by Django 4.1 on 2023-09-17 03:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0017_alter_userprofileinfo_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='token',
            name='chat_code',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
