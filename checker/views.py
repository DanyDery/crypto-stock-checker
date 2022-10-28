from django.shortcuts import render
from django.http import HttpResponse

# def index_view(request):
#     context = {
#         'header': 'Web App'
#     }
#     return render(request, 'index.html', context)

def index(request):
    return HttpResponse("hello, world!")