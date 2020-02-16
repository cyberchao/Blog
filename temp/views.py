from django.http import HttpResponse
from django.shortcuts import render
from temp.models import Home
import json

def temp(request):
    return render(request,'temp.html')

def data(request):
    if request.method == 'POST':
        temperature = request.POST.get('temperature')
        humidity = request.POST.get('humidity')
        print(temperature,humidity)
        Home.objects.create(temperature=temperature,humidity=humidity)
        return HttpResponse(status=200)
    else:
        print(333)
        return HttpResponse(status=404)

