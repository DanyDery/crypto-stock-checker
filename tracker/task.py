from celery import shared_task
from yahoo_fin.stock_info import *
from threading import Thread
import queue

@shared_task(bind = True)
def update_stock(self, stocks):
    data = {}
    available_stocks = tickers_dow()
    num_threads = len(stocks)
    thread_list = []
    que = queue.Queue()

    for i in range(num_threads):
        thread = Thread(target=lambda q, arg: q.put({picker[i]: get_quote_table(arg)}), args=(que, picker[i]))
        thread_list.append(thread)
        thread_list[i].start()

    for thread in thread_list:
        thread.join()

    while not que.empty():
        description = que.get()
        data.update(description)

    print(data)

    return "Done"