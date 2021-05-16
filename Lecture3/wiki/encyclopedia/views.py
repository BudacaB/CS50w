from django.shortcuts import render

from . import util
from markdown2 import Markdown
from django import forms
from django.http import HttpResponseRedirect
import random
from django.shortcuts import redirect

class NewSearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

class NewPageForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Enter title'}))
    markdown = forms.CharField(widget=forms.Textarea(attrs={'rows':2, 'cols':15, 'placeholder': 'Enter Markdown here...'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm(),
        "header": "All Pages"
    })

def title(request, title):
    markdowner = Markdown()
    # check get_entry output
    if util.get_entry(title) is None:
        return render(request, "encyclopedia/search_error.html", {
            "search": title,
            "form": NewSearchForm()
        })
    else:
        content = markdowner.convert(util.get_entry(title))
        return render(request, "encyclopedia/wiki.html", {
            "title": title,
            "content": content,
            "form": NewSearchForm()
        })

def search(request):
    if request.method == 'POST':
        form = NewSearchForm(request.POST)
        if form.is_valid():
            search = form.cleaned_data["search"]
            if util.get_entry(search) is None:
                entries = util.list_entries()
                filtered_entries = [k for k in entries if search in k]
                return render(request, "encyclopedia/index.html", {
                    "entries": filtered_entries,
                    "form": NewSearchForm(),
                    "header": "Search Results"
                })
            else:
                return HttpResponseRedirect('/wiki/' + search)

def new_page(request):
    return render(request, "encyclopedia/new.html", {
        "form": NewSearchForm(),
        "new_page_form": NewPageForm()
    })

def new_page_add(request):
    if request.method == 'POST':
        form = NewPageForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            markdown = form.cleaned_data["markdown"]
            if util.get_entry(title) is None:
                util.save_entry(title, markdown)
                return HttpResponseRedirect('/wiki/' + title)
            else:
                return HttpResponseRedirect('/new_error/')

def new_error(request):
    return render(request, "encyclopedia/new_error.html", {
        "form": NewSearchForm(),
    })

def edit(request, title):
    markdowner = Markdown()
    return render(request, "encyclopedia/edit.html", {
        "title": title,
        "content": util.get_entry(title),
        "form": NewSearchForm()
    })

def edit_save(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        util.save_entry(title, content)
        return HttpResponseRedirect('/wiki/' + title)

def random_page(request):
    random_title = random.choice(util.list_entries())
    return HttpResponseRedirect('/wiki/' + random_title)
        