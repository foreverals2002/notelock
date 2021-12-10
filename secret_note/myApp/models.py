from django.db import models
from django.contrib.auth.models import User
from django.core.files.base import ContentFile



# Create your models here.
class Folder(models.Model):
    folder_name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    date_last_used = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.folder_name

class Note(models.Model):
    note_name = models.CharField(max_length=100)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    folder_name = models.ForeignKey(Folder, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/', null=True)
    date_last_used = models.DateTimeField(auto_now=True)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.note_name
