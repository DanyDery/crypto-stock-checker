from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import TickerForm
from .tingo import get_meta_data, get_price_data
from .prediction import *

def index(request):
    if request.method == "POST":
        form = TickerForm(request.POST)
        if form.is_valid():
            data = request.POST["ticker"]
            return HttpResponseRedirect(data)
    else:
        form = TickerForm()
    return render(request, "index.html", {"form": form})


def ticker(request, tid):
    context = {"ticker": tid, "meta": get_meta_data(tid),
               "price": get_price_data(tid),
               "plot": plot_raw_data(load_data(tid))}
    return render(request, "ticker.html", context)
