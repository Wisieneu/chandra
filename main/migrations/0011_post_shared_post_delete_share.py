# Generated by Django 4.1.6 on 2023-02-19 20:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0010_remove_post_shares_share'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='shared_post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shares', to='main.post'),
        ),
        migrations.DeleteModel(
            name='Share',
        ),
    ]
