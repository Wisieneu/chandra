# Generated by Django 4.1.5 on 2023-01-24 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_profile_display_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='display_name',
            field=models.CharField(max_length=32),
        ),
    ]
