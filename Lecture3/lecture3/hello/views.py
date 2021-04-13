from django.shortcuts import render
from django.shortcuts import HttpResponse

# Create your views here.
def index(request):
    return HttpResponse("Hello!")

def bog(request):
    return HttpResponse("Hello, Bog!")

def greet(request, name):
    return HttpResponse(f"Hello, {name.capitalize()}!")
