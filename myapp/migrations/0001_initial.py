# Generated by Django 5.2 on 2025-04-21 10:35

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='About',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('subtitle', models.TextField()),
                ('paragraph_one', models.TextField()),
                ('bullet_1', models.CharField(max_length=255)),
                ('bullet_2', models.CharField(max_length=255)),
                ('bullet_3', models.CharField(max_length=255)),
                ('paragraph_two', models.TextField()),
                ('read_more_link', models.URLField(blank=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='about_images/')),
            ],
        ),
        migrations.CreateModel(
            name='BlogPost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('role', models.CharField(max_length=255)),
                ('text', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='testimonials/')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
