# Generated by Django 5.2 on 2025-04-22 20:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_question_correct_text_answer_question_question_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useranswer',
            name='selected_answer',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='myapp.answer'),
        ),
    ]
