# Generated by Django 5.0 on 2023-12-24 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usertoken2',
            name='password',
            field=models.CharField(max_length=200),
        ),
        migrations.AlterField(
            model_name='usertoken2',
            name='user',
            field=models.CharField(max_length=200),
        ),
    ]
