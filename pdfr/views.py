from django.shortcuts import render, redirect
import pdfplumber

def index(request):
    context={}
    if request.method == "POST":
        pdf=request.FILES.get("pdfr")
        if pdf:
            pdfr=pdfplumber.open(pdf)
            num=len(pdfr.pages)
            context={}
            if pdfr:
                su=""
                for i in range(num):
                    pdfrr=pdfr.pages[i].extract_text()
                    su+=pdfrr
                context.update({
                    "su":su
                })

    
    return render(request,"pdfr/index.html",context)
