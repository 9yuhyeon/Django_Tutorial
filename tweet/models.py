# tweet/models.py
from django.db import models
from user.models import UserModel # user앱의 models.py에 있는 UserModel을 import


# Create your models here.
class TweetModel(models.Model):
    class Meta:
        db_table = "tweet"

    author = models.ForeignKey(UserModel, on_delete=models.CASCADE) # UserModel을 ForeignKey로 참조
    content = models.CharField(max_length=256)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)