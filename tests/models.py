from django.db import models
from users.models import Profile

# Create your models here.
class Question(models.Model):
    DIFFICULTY = (
        ('beginner', 'beginner'),
        ('intermediate', 'intermediate'),
        ('advanced', 'advanced'),
    )
    question_id = models.IntegerField(unique=True, primary_key=True, editable=False)
    category = models.CharField(max_length=200, blank=True, null=True)
    question_type = models.CharField(max_length=200, blank=True, null=True)
    difficulty = models.CharField(choices=DIFFICULTY,max_length=200, blank=True, null=True)

    question_prompt = models.TextField(blank=True, null=True)
    question_text = models.TextField(blank=True,null=True)

    correct_answer = models.JSONField(blank=True,null=True)
    answers = models.JSONField(blank=True, null=True)
    hint = models.TextField(blank=True,null=True)
    explanation = models.TextField(blank=True,null=True)

    def __str__(self):
        if self.question_id:
            return "#" + str(self.question_id) + ' ' + self.question_text
        else: return "question formating error"

    class Meta:
        ordering = ['question_id']

class TestResult(models.Model):
    result_id = models.IntegerField(unique=True, primary_key=True, editable=False)
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE)
    test_category = models.CharField(max_length=200, blank=True, null=True)
    score = models.FloatField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "#" + str(self.result_id)
    class Meta:
        ordering = ['result_id']

