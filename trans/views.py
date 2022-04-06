from unicodedata import category
from django.shortcuts import render
import googletrans
from googletrans import Translator


def index(request):
    context={}
    if request.method =="POST":
        bf=request.POST.get("bf")
        fr = request.POST.get("fr")
        to=request.POST.get("to")
        translator = Translator()
        if bf:
            tr = translator.translate(bf, src=fr, dest=to)
            context.update({
                "af" : tr.text,
                "bf" : bf,
                "fr" : fr,
                "to" : to
            })
    return render(request, "trans/index.html", context)
