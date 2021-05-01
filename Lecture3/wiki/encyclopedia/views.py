from django.shortcuts import render

from . import util
from markdown2 import Markdown

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
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
        "content": content
    })

