from django.contrib import admin
from .models import UserModel # 현재 위치의 models.py에 있는 UserModel 클래스를 import

# Register your models here.
admin.site.register(UserModel) # UserModel을 admin 사이트에 등록