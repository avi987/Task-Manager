from django.http import HttpResponse
from django.shortcuts import render

def default(request):

    return HttpResponse(render(request,'tasks/i.html'))