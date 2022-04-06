from django.utils import timezone
from django.shortcuts import render, redirect
from .models import Topic,Sel
# Create your views here.
def index(request):
    t= Topic.objects.all()
    context = {
        "tset" : t
    }
    return render(request, "vote/index.html",context)
def detail(request,tpk):
    t=Topic.objects.get(id=tpk)
    s=t.sel_set.all()
    context ={
        "t" : t,
        "sset":s
    }
    return render(request,"vote/detail.html",context)
def vote(request,tpk):
    t=Topic.objects.get(id=tpk)
    if not request.user in t.voter.all():
        t.voter.add(request.user)
        spk=request.POST.get("sel")
        s=Sel.objects.get(id=spk)
        s.choicer.add(request.user)
    return redirect("vote:detail",tpk)

def cancel(request, tpk):
    u=request.user
    t = Topic.objects.get(id=tpk)
    t.voter.remove(request.user)
    #t.sel_set.get(choicer=request.user).choicer.remove(request.user)
    u.sel_set.get(topic=t).choicer.remove(u)
    return redirect("vote:detail", tpk)

def create(reqeust):
    if reqeust.method == "POST":
        t= reqeust.POST.get("top")
        c= reqeust.POST.get("con")
        sn=reqeust.POST.getlist("sname")
        sc=reqeust.POST.getlist("scon")
        sp=reqeust.FILES.getlist("spic")
        t=Topic(subject=t, content=c, maker=reqeust.user, pubdate=timezone.now())
        t.save()
        for name, con , pic in zip(sn,sc,sp):
            Sel(topic=t,sname=name,spic=pic,scon=con).save()
        return redirect("vote:index")
    return render(reqeust,"vote/create.html")

def delete(request,tpk):
    t=Topic.objects.get(id=tpk)
    if t.maker == request.user:
        s=t.sel_set.all()
        for i in s:
            i.spic.delete()
        t.delete()
    else:
        pass
    return redirect("vote:index")
