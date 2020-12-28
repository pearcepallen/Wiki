from django.shortcuts import render
from . import util

import markdown2

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, name):
    return render(request, "encyclopedia/entry.html", {
        "content": markdown2.markdown(util.get_entry(name)), 
        "name": name
    })
