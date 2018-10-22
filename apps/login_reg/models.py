from django.db import models
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
import bcrypt, re

nameRegex = re.compile(r'^[a-zA-Z ]+$')
passRegex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).+$')

class UserManager(models.Manager):
    def validateEmail(self, email ):
        try:
            validate_email( email )
            return True
        except ValidationError:
            return False
    
    def registration_validator(self, postData):
        errors = {}
        if not nameRegex.match(postData['name']):
            errors['name'] = "Name must be letters only"
        if len(postData['name']) < 2 or len(postData['name']) > 50:
            errors["name"] = "Name cannot be shorter than 2 characters or longer than 50 characters"
        if not nameRegex.match(postData['alias']):
            errors['alias'] = "Alias must be letters only"
        if len(postData['alias']) < 2  or len(postData['alias']) > 50:
            errors["alias"] = "Alias cannot be shorter than 2 characters or longer than 50 characters"
        if self.validateEmail(postData['email']) != True:
            errors['email'] = 'Email is not valid please try again'
        if len(postData['pw']) < 8:
            errors["pw"] = "Password must be at least 8 chracters"
        if not passRegex.match(postData['pw']):
            errors['pw'] = "Password must contain an uppercase letter, lowercase letter, and a number "
        if postData['pw'] != postData['pw_confirm']:
            errors["pw_confirm"] = "Password confirm field must match password"
        return errors
    
    def login_validator(self, postData):
        user = Users.objects.filter(email = postData['email'])
        errors = {}
        if len(user)==0:
            errors['msg'] = 'Email or password does not match'
        if user and not bcrypt.checkpw(postData['pw'].encode(), user[0].password.encode()):
            errors['msg'] = 'Email or password does not match'
        return errors


class Users(models.Model):
    name = models.CharField(max_length=50)
    alias = models.CharField(max_length=50)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=100)
    objects = UserManager()