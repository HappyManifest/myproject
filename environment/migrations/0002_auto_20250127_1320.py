# Generated by Django 3.2.12 on 2025-01-27 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('environment', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('short_description', models.TextField()),
                ('content', models.TextField()),
                ('image', models.ImageField(upload_to='articles/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('short_description', models.TextField()),
                ('content', models.TextField()),
                ('published_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='EnvironmentData',
        ),
    ]
