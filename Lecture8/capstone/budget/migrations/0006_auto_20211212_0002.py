# Generated by Django 3.2 on 2021-12-12 00:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0005_auto_20211211_1906'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='created',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='food',
            name='created',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='fun',
            name='created',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='transport',
            name='created',
            field=models.DateField(),
        ),
    ]
