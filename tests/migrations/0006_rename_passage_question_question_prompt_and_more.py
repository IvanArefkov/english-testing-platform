# Generated by Django 5.1.7 on 2025-03-24 15:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tests', '0005_rename_incorrect_answer_question_answers'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='passage',
            new_name='question_prompt',
        ),
        migrations.RemoveField(
            model_name='question',
            name='sentence_template',
        ),
    ]
