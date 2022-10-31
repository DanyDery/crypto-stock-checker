from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect


def collector(request):
    return render(request, 'collector.html')

def tracker(request):
    return render(request, 'tracker.html')


