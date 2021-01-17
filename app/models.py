from django.db import models
from django.conf import settings
from django.utils import timezone


class Post(models.Model):
  author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  term = models.CharField("用語", max_length=200)
  content = models.TextField("読み方")
  created = models.DateTimeField("作成日", default=timezone.now)

  def __str__(self):
    return self.term