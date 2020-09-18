from django.db import models
from django.utils import timezone
from django.contrib.auth import get_user_model
from taggit.managers import TaggableManager
import datetime


User = get_user_model()


class Note(models.Model):
    def __str__(self):
        return self.title
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    
    title = models.CharField(max_length=200)
    body = models.TextField()
    pub_date = models.DateTimeField('date published', auto_now_add=True)
    owner = models.ForeignKey(User, related_name='notes', on_delete=models.CASCADE, default='Nobody')
    tags = TaggableManager(blank=True)


class Permalink(models.Model):
    key = models.CharField(primary_key=True, max_length=8)
    refersTo = models.OneToOneField(Note, on_delete=models.CASCADE)
