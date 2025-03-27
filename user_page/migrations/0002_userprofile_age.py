# Generated by Django 2.2.28 on 2025-03-27 14:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_page', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='age',
            field=models.IntegerField(default=16, validators=[django.core.validators.MinValueValidator(16), django.core.validators.MaxValueValidator(100)]),
            preserve_default=False,
        ),
    ]
