# Generated by Django 5.2 on 2025-04-22 21:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_alter_useranswer_selected_answer'),
    ]

    operations = [
        migrations.AddField(
            model_name='useranswer',
            name='short_answer',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='useranswer',
            name='is_correct',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='useranswer',
            name='selected_answer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.answer'),
        ),
    ]
