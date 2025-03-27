# Generated by Django 2.2.28 on 2025-03-27 23:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_page', '0005_auto_20250327_2235'),
    ]

    operations = [
        migrations.CreateModel(
            name='AgeRange',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Budget',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('level', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Cuisine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DietaryNeed',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='DiningVibe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='age_range',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='budget',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='cuisines',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='max_age_difference',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='dietary_needs',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='dining_vibes',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='age_ranges',
            field=models.ManyToManyField(to='user_page.AgeRange'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='budgets',
            field=models.ManyToManyField(to='user_page.Budget'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='regional_cuisines',
            field=models.ManyToManyField(to='user_page.Cuisine'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='dietary_needs',
            field=models.ManyToManyField(to='user_page.DietaryNeed'),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='dining_vibes',
            field=models.ManyToManyField(to='user_page.DiningVibe'),
        ),
    ]
