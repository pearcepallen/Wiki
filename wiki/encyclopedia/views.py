from django.shortcuts import render
from django import forms
from . import util

import markdown2

class SearchForm(forms.Form):
    search = forms.CharField(label="Search Encyclopedia")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": SearchForm()
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

def search(request):
    return render(request, "encyclopedia/search.html")





