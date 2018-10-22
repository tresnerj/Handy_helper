from django.db import models
from django.core.exceptions import ValidationError
from apps.login_reg.models import *


class JobsManager(models.Manager):    
    def job_validator(self, postData):
        errors = {}
        if len(postData['title']) < 3 or len(postData['title']) > 50:
            errors["title"] = "Title cannot be shorter than 3 characters or longer than 50 characters"
        if len(postData['desc']) < 10 :
            errors["desc"] = "Description cannot be shorter than 10 characters"
        if len(postData['location']) < 10:
            errors["location"] = "Location cannot be shorter than 10 characters"
        return errors

class Jobs(models.Model):
    user = models.ForeignKey(Users, related_name = 'job')
    title = models.CharField(max_length=50)
    assigned = models.CharField(max_length=50)
    desc = models.CharField(max_length=500)
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = JobsManager()

class JobsAssigned(models.Model):
    user = models.ForeignKey(Users, related_name = 'job_assigned')
    title = models.CharField(max_length=50)
    desc = models.CharField(max_length=500)
    location = models.CharField(max_length=255)
    orig_id = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



