from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    output = "Welcome to Adbiz"
    return HttpResponse(output)
