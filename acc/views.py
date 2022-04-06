from django.shortcuts import render, redirect
from .models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import check_password
from django.contrib import messages
# Create your views here.

def delete(request):
        u = request.user
        ck= request.POST.get("pwck")
        if check_password(ck, u.password):
            u.pic.delete()
            u.delete()
            return redirect("acc:index")
        else:
            pass
            return redirect("acc:profile")

def index(request):
    return render(request, "acc/index.html")
def login_user(request):
    if request.method =="POST":
        un = request.POST.get("uname")
        up = request.POST.get("upass")
        u = authenticate(username=un, password=up)

        if u:
            login(request,u)
            messages.success(request,f"WELCOME {u}!")
            return redirect("acc:index")
        else:
            messages.error(request,"계정 정보가 일치하지 않습니다")
    return render(request, "acc/login.html")
def logout_user(request):
    logout(request)
    return redirect("acc:index")
def signup(request):
    if request.method == "POST":
        un = request.POST.get ("uname")
        up = request.POST.get ("upass")
        uc = request.POST.get ("ucomment")
        pi = request.FILES.get ("upic")
        try:
            User.objects.create_user(username=un, password=up, comment=uc, pic=pi)
        except:
            messages.error(request,"이미 존재하는 아이디 입니다")
        return redirect("acc:login")    

    return render(request, "acc/sign.html")

def profile(request):
    return render(request,"acc/profile.html")


def update(request):
    if request.method =="POST":
        u=request.user
        up = request.POST.get ("upass")
        uc = request.POST.get ("ucomment")
        pi = request.FILES.get ("upic")
        if up:
            u.set_password(up)
        u.comment=uc
        if pi:
            u.pic.delete()
            u.pic = pi
        u.save()
        login(request,u)
        return redirect("acc:profile")
    return render(request, "acc/update.html")