# Generated by Django 4.0.4 on 2022-07-01 05:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('files', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='slug',
            field=models.SlugField(),
        ),
    ]