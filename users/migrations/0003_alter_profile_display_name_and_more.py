# Generated by Django 4.1.5 on 2023-01-23 18:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='display_name',
            field=models.CharField(default='<django.db.models.fields.related.OneToOneField>', max_length=32),
        ),
        migrations.AlterField(
            model_name='profile',
            name='profile_picture',
            field=models.ImageField(default='assets/default.jpg', upload_to='profile_pictures'),
        ),
    ]