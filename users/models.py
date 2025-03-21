from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True,blank=True)
    name = models.CharField(max_length=200,blank=True,null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    email = models.EmailField(max_length=500, blank=True,null=True)
    username = models.CharField(max_length=200,blank=True,null=True)
    location = models.CharField(max_length=200,blank=True,null=True)
    SKILL_LEVELS = (
        ('beginner', 'beginner'),
        ('intermediate', 'intermediate'),
        ('advanced', 'advanced'),
    )
    skill_level = models.CharField(max_length=200, choices=SKILL_LEVELS, blank=True,null=True)
    profile_image = models.ImageField(blank=True,null=True,upload_to='profiles/',default='profiles/user-default.png')
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        full_name = self.name +' '+ self.last_name
        return full_name

class TestResults(models.Model):
    test_id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True,blank=True)
    mode = models.CharField(max_length=200, blank=True, null=True)
    total_result = models.CharField(max_length=200,blank=True,null=True)
    result_by_category = models.JSONField(max_length=500,blank=True,null=True)



