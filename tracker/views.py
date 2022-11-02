from threading import Thread

from django.http import HttpResponse
from django.shortcuts import render
from yahoo_fin.stock_info import *
import time
import queue


def collector(request):
    stocks = tickers_dow()
    return render(request, 'collector.html', {'stocks': stocks})


def tracker(request):
    picker = request.GET.getlist('picker')
    data = {}
    available_stocks = tickers_dow()
    num_threads = len(picker)
    thread_list = []
    que = queue.Queue()
    start = time.time()
    for i in range(num_threads):
        thread = Thread(target=lambda q, arg: q.put({picker[i]: get_quote_table(arg)}), args=(que, picker[i]))
        thread_list.append(thread)
        thread_list[i].start()

    for thread in thread_list:
        thread.join()

    while not que.empty():
        description = que.get()
        data.update(description)

    # for i in picker:
    #     if i not in available_stocks:
    #         return HttpResponse('Error')
    # description = get_quote_table(i)
    # data[i] = description

    end = time.time()
    total_time = end - start
    print(total_time)
    print(data)

    return render(request, 'tracker.html', {'data': data})
