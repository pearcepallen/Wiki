from django.shortcuts import render
from django.http import HttpResponse
from . import util

import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):
    try:
        return render(request, "encyclopedia/entry.html", {
            "content": markdown2.markdown(util.get_entry(name)), 
            "name": name
        })
    except TypeError:
        return render(request, "encyclopedia/entry_notfound.html",{
            "name": name
        })


