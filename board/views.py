from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Board, Reply
from django.utils import timezone
from django.contrib import messages

def index(request):
    pg=request.GET.get("page",1)
    cate=request.GET.get("cate","")
    kw=request.GET.get("kw","")

    if kw:
        if cate == "sub":
            t=Board.objects.filter(subject__startswith=kw)
        elif cate =="wri":
            from acc.models import User
            try:
                u=User.objects.get(username=kw)
                t=Board.objects.filter(writer=u)
            except:
                t=Board.objects.none()
        elif cate == "con":
            t=Board.objects.filter(content__contains=kw)
        else:
            t=Board.objects.none()
    else:
        t=Board.objects.all()
    t=t.order_by('pubdate')
    pag=Paginator(t,3)
    obj=pag.get_page(pg)
    context={
        'tset' : obj,
        'cate' : cate,
        'kw':kw
    }
    return render(request, "board/index.html",context)
def detail(request, bpk):
    t= Board.objects.get(id=bpk)
    r= t.reply_set.all()
    context={
        "t" : t,
        "rset" : r
    }
    return render(request, "board/detail.html", context)
def delete(request,bpk):
    t=Board.objects.get(id=bpk)
    if t.writer == request.user:
        t.delete()
    else:
        messages.warning(request,"해킹 노노요")
    return redirect("board:index")

def create(request):
    if request.method == "POST": # 게시글 생성 버튼 누를경우
        s = request.POST.get("sub")
        c = request.POST.get("con")
        Board(subject=s, content=c, writer=request.user, pubdate=timezone.now()).save()
        return redirect("board:index")
        
    return render(request, "board/create.html")

def update(request, bpk):
    b = Board.objects.get(id=bpk)
    if b.writer ==request.user:
        if request.method == "POST":
            s = request.POST.get("sub")
            c = request.POST.get("con")
            b.subject, b.content = s, c
            b.save()
            return redirect("board:detail", bpk)
        context = {
            "b" : b
        }
    else:
        messages.warning(request,"해킹 노노요")
        return redirect("board:index")
    return render(request, "board/update.html", context)

def creply(request,bpk):
    b=Board.objects.get(id=bpk)
    c=request.POST.get("com")
    Reply(board=b, replyer=request.user, comment=c).save()
    return redirect("board:detail",bpk)

def dreply(request,bpk,rpk):
    r=Reply.objects.get(id=rpk)
    if r.replyer == request.user:
        r.delete()
    else:
        messages.warning(request,"해킹 노노요")
        return redirect("board:detail")
    return redirect("board:detail",bpk)

def likey(request,bpk):
    t=Board.objects.get(id=bpk)
    t.likey.add(request.user)
    return redirect("board:detail",bpk)
def unlikey(request,bpk):
    t=Board.objects.get(id=bpk)
    t.likey.remove(request.user)
    return redirect("board:detail",bpk)