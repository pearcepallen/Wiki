from django.shortcuts import render
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from . import util
import random
import markdown2

class NewPageForm(forms.Form):
    page_title = forms.CharField(label=False, widget=forms.TextInput(attrs={'placeholder':'Enter entry title'}))
    page_markdown = forms.CharField(label=False, widget=forms.Textarea(attrs={'placeholder':'Enter content markdown', 'style': 'height: 10%;'}))

class EditPageForm(forms.Form):
    edit_markdown = forms.CharField(label=False, widget=forms.Textarea(attrs={'style': 'height: 10%;'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
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
    if request.method == "GET":
        query = request.GET.get('q')

        #If query is an exact match of term in encyclopedia
        if util.get_entry(query):
            return HttpResponseRedirect(reverse("entry", args=[query]))

        #If query is substring
        substring_match = []
        entries = util.list_entries()
        for entry in entries:
            if query.lower() in entry.lower():
                substring_match.append(entry)
        
        if not substring_match:
            return render(request, "encyclopedia/entry_notfound.html",{
                "name": query
            })

        return render(request, "encyclopedia/search.html",{
            "search": query.upper(),
            "results": substring_match
        })

def create(request):
    if request.method == "POST":
        #Take data submitted and save as form
        form = NewPageForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["page_title"]
            content = form.cleaned_data["page_markdown"]

            #Check if entry already exists 
            if util.get_entry(title):
                return render(request, "encyclopedia/entry_exists.html",{
                    "title": title  
                })
            #Saves form information to disk
            util.save_entry(title, content)
            
            return HttpResponseRedirect(reverse("entry", args=[title]))

    return render(request, "encyclopedia/create.html", {
        "form": NewPageForm()
    })

def edit(request, name):
    if request.method == "POST":
        #Take data submitted and save as form
        form = EditPageForm(request.POST)

        if form.is_valid():
            content = form.cleaned_data["edit_markdown"]
            util.save_entry(name, content)
            return HttpResponseRedirect(reverse("entry", args=[name]))

    initial_dict={"edit_markdown": util.get_entry(name)}
    return render(request, "encyclopedia/edit.html", {
        "form": EditPageForm(initial = initial_dict),
        "name": name
    })

def random_page(request): #do not name random to avoid overriding/overloading
    entries = util.list_entries()
    rand_entry = random.choice(entries)
    
    return HttpResponseRedirect(reverse("entry", args=[rand_entry]))



    
    





