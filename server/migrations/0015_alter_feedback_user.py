# Generated by Django 4.1 on 2023-06-13 03:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0014_token'),
    ]

    operations = [
        migrations.AlterField(
            model_name='feedback',
            name='user',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
