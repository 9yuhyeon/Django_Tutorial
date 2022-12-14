from hashlib import new
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import UserModel
from django.contrib.auth import get_user_model
from django.contrib import auth
from django.contrib.auth.decorators import login_required

# Create your views here.
def sign_up_view(request):
    if request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signup.html')
    elif request.method == 'POST':
        username = request.POST.get('username','')
        password = request.POST.get('password','')
        password2 = request.POST.get('password2','')
        bio = request.POST.get('bio','')

        if password != password2:
            return render(request, 'user/signup.html', {'error':'패스워드가 일치하지 않습니다!'})
        else:
            if username == '' or password == '':
                return render(request, 'user/signup.html',{'error':'이름과 패스워드는 필수 값 입니다.'})
            
            exist_user = get_user_model().objects.filter(username=username)
            if exist_user:
                return render(request, 'user/signup.html',{'error':'사용자가 이미 존재합니다!'})
            else:
                UserModel.objects.create_user(username=username, password=password, bio=bio)
                return redirect('/sign-in')


def sign_in_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        me = auth.authenticate(request, username=username, password=password)
        if me is not None:
            auth.login(request, me)
            return redirect('/')
        else:
            return render(request, 'user/signin.html', {'error':'아이디와 패스워드를 확인 해 주세요!'})
    
    elif request.method == 'GET':
        user = request.user.is_authenticated
        if user:
            return redirect('/')
        else:
            return render(request, 'user/signin.html')

@login_required
def logout(request):
    auth.logout(request)
    return redirect('/')


@login_required
def user_view(request):
    user_list = UserModel.objects.all().exclude(username=request.user.username)
    return render(request, 'user/user_list.html', {'user_list':user_list})


@login_required
def user_follow(request, id):
    me = request.user # 요청한 사람
    click_user = UserModel.objects.get(id=id) # id값으로 선택한 사람의 UserModel을 불러옴
    if me in click_user.followee.all():
        click_user.followee.remove(request.user)
    else:
        click_user.followee.add(request.user)
    return redirect('/user')

