from celery import shared_task
from yahoo_fin.stock_info import *
from threading import Thread
import queue

from channels.layers import get_channel_layer
import asyncio
import simplejson as json


@shared_task(bind=True)
def update_stock(self, stocks):
    data = {}
    all_stocks = tickers_dow()

    for i in stocks:
        if i in all_stocks:
            pass
        else:
            stocks.remove(i)

    num_threads = len(stocks)
    thread_list = []
    que = queue.Queue()

    for i in range(num_threads):
        thread = Thread(
            target=lambda q, arg: q.put({stocks[i]: json.loads(json.dumps(get_quote_table(arg), ignore_nan=True))}),
            args=(que, stocks[i]))
        thread_list.append(thread)
        thread_list[i].start()

    for thread in thread_list:
        thread.join()

    while not que.empty():
        result = que.get()
        data.update(result)

    # group data
    channel_layer = get_channel_layer()
    loop = asyncio.new_event_loop()

    asyncio.set_event_loop(loop)

    loop.run_until_complete(channel_layer.group_send("stock_track", {
        'type': 'send_stock_update',
        'message': data,
    }))

    return 'Completed'
