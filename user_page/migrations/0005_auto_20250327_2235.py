# Generated by Django 2.2.28 on 2025-03-27 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_page', '0004_remove_userprofile_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='age_range',
            field=models.CharField(default='19-21', max_length=10),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='budget',
            field=models.CharField(default='$', max_length=5),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='cuisines',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='dietary_needs',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='dining_vibes',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
