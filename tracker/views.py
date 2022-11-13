from django.http.response import HttpResponse
from django.shortcuts import render
from yahoo_fin.stock_info import *
import queue

from threading import Thread
from asgiref.sync import sync_to_async


def collector(request):
    stocks = tickers_dow()
    return render(request, "collector.html", {"stocks": stocks})


@sync_to_async
def check_authenticated(request):
    if not request.user.is_authenticated:
        return False
    else:
        return True


async def tracker(request):
    is_logged = await check_authenticated(request)
    if not is_logged:
        return HttpResponse("Login First")
    picker = request.GET.getlist("picker")
    stock_share = str(picker)[1:-1]

    data = {}
    available_stocks = tickers_dow()
    for i in picker:
        if i in available_stocks:
            pass
        else:
            return HttpResponse("Error")

    num_threads = len(picker)
    thread_list = []
    que = queue.Queue()

    for i in range(num_threads):
        thread = Thread(
            target=lambda q, arg: q.put({picker[i]: get_quote_table(arg)}),
            args=(que, picker[i]),
        )
        thread_list.append(thread)
        thread_list[i].start()

    for thread in thread_list:
        thread.join()

    while not que.empty():
        description = que.get()
        data.update(description)

    return render(
        request,
        "tracker.html",
        {"data": data, "room_name": "track", "selected_stocks": stock_share},
    )
