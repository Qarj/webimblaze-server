# Create your views here.

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from itertools import chain

def index(request):
    return HttpResponse("Hello, world. You're at the Webinject Server index.")
