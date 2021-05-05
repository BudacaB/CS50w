from django.shortcuts import render

from . import util
from markdown2 import Markdown
from django import forms
from django.http import HttpResponseRedirect

class NewSearchForm(forms.Form):
    search = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Search Encyclopedia'}))

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
        "form": NewSearchForm()
    })

def title(request, title):
    markdowner = Markdown()
    # check get_entry output
    if util.get_entry(title) is None:
        content = f'{title} Not Found'
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
                if not filtered_entries:
                    return render(request, "encyclopedia/search.html", {
                        "search": search,
                        "form": NewSearchForm()
                    })
                else:
                    return render(request, "encyclopedia/index.html", {
                        "entries": filtered_entries,
                        "form": NewSearchForm()
                    })
            else:
                return HttpResponseRedirect('/wiki/' + search)