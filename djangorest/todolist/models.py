from django.db import models
from django.utils import timezone
from pygments.lexers import get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments import highlight
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class Tag(models.Model):
    name = models.CharField(max_length=50, null=True)
    
    def __str__(self):
        return "{}".format(self.name)

class Tasklist(models.Model):
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, null = True, on_delete=models.CASCADE)

    def __str__(self):
        return "{}".format(self.name)
    

class Task(models.Model):
    tasklist = models.ForeignKey(Tasklist, related_name='tasks', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True)
    description = models.TextField(max_length=1000, blank=True)
    completed = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)
    date_modified = models.DateField(auto_now=True)
    tags = models.ManyToManyField(Tag)
    shared = models.CharField(default=True, max_length = 3, null=True)

    def __str__(self):
        return "{}".format(self.name)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email_confirmed = models.BooleanField(default=False)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()
    
    
