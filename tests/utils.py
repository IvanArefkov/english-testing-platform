from .models import Question
from django.contrib import messages
import json
from django.db.models import Max
from random import randint, choices

# VALIDATE AND UPLOAD THE FILE TO DB
def validate_upload_questions(request, questions_file):
    if not questions_file.name.endswith('.json'):
        messages.warning(request, 'Please upload a JSON file')
    else:
        file_data = questions_file.read().decode('utf-8')
        try:
            json_data = json.loads(file_data)
            highest_id = Question.objects.aggregate(Max('question_id'))['question_id__max'] or 0
            for item in json_data:
                highest_id = highest_id + 1
                if item['type'] == 'multiple_choice':
                    multiple_choice_question(item, highest_id)
                elif item['type'] == 'fill_in_blank':
                    fill_in_blank(item, highest_id)
                elif item['type'] == 'essay_prompt':
                    essay_prompt_question(item, highest_id)
            messages.success(request, 'The file is uploaded successfully')
        except json.JSONDecodeError:
            messages.error(request, 'Invalid JSON')

def multiple_choice_question(item,highest_id):
    question = Question.objects.create(
        question_id=highest_id,
        category=item['category'],
        question_type=item['type'],
        difficulty=item['difficulty'],
        passage=item['passage'],
        question_text=item['question_text'],
        correct_answer=item['correct_answer'],
        answers=item['answers'],
        explanation=item['explanation'],
    )
    question.save()

def fill_in_blank(item,highest_id):
    question = Question.objects.create(
        question_id=highest_id,
        category=item['category'],
        question_type=item['type'],
        difficulty=item['difficulty'],
        sentence_template=item['sentence_template'],
        correct_answer=item['correct_answer'],
        hint=item['hint'],
        explanation=item['explanation'], )
    question.save()

def essay_prompt_question(item,highest_id):
    question = Question.objects.create(
        question_id=highest_id,
        category=item['category'],
        question_type=item['type'],
        difficulty=item['difficulty'],
        question_text=item['question_text'],
        hint=item['hint'],
        explanation=item['explanation'],
    )
    question.save()

def get_questions(request,mode):
    if mode == 'Exam' or mode == 'Practice':
        question_set = Question.objects.order_by("?")[:50]
    elif mode == 'Reading':
        question_set = Question.objects.filter(category='reading').order_by("?")[:3]
    elif mode == 'Grammar':
        question_set = Question.objects.filter(category='grammar').order_by("?")[:3]
    elif mode == 'Writing':
        question_set = Question.objects.filter(category='writing').order_by("?")[:3]
    elif mode == 'Vocabulary':
        question_set = Question.objects.filter(category='vocabulary').order_by("?")[:3]
    else:
        messages.error(request, 'Invalid mode')
        return None
    return question_set