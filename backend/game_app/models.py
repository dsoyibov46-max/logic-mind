from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Result(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)



class Game(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    thumbnail = models.ImageField(upload_to='games/', blank=True, null=True)
    url_name = models.SlugField(max_length=100, unique=True)  
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title