from django.shortcuts import render
from django.shortcuts import HttpResponse

# Create your views here.
def index(request):
    return render(request, "hello/index.html")
    # return HttpResponse("Hello!")


def bog(request):
    return HttpResponse("Hello, Bog!")

def greet(request, name):
    return render(request, "hello/greet.html", {
        "name": name.capitalize()  # context provided for the template
    })
    # return HttpResponse(f"Hello, {name.capitalize()}!")
