import json
import copy

from channels.generic.websocket import AsyncWebsocketConsumer
from urllib.parse import parse_qs

from asgiref.sync import sync_to_async
from django_celery_beat.models import PeriodicTask, IntervalSchedule

from tracker.models import StockDetail


class StockConsumer(AsyncWebsocketConsumer):

    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_group_name = None
        self.room_name = None

    @sync_to_async
    def add_to_beat(self, stocks):

        task = PeriodicTask.objects.filter(name="every-5-seconds")

        if len(task) > 0:
            task = task.first()
            args = json.loads(task.args)
            args = args[0]
            for x in stocks:
                if x not in args:
                    args.append(x)
            task.args = json.dumps([args])
            task.save()
        else:
            schedule, created = IntervalSchedule.objects.get_or_create(every=5, period=IntervalSchedule.SECONDS)
            task = PeriodicTask.objects.create(interval=schedule, name='every-5-seconds',
                                               task="tracker.tasks.update_stock", args=json.dumps([stocks]))

    @sync_to_async
    def add_details(self, stocks):
        user = self.scope["user"]
        for i in stocks:
            stock, created = StockDetail.objects.get_or_create(stock=i)
            stock.user.add(user)

    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'stock_%s' % self.room_name

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        query_params = parse_qs(self.scope["query_string"].decode())

        stocks = query_params['stocks']

        await self.add_to_beat(stocks)

        await self.add_details(stocks)

        await self.accept()

    @sync_to_async
    def helper(self):
        user = self.scope["user"]
        stocks = StockDetail.objects.filter(user__id=user.id)
        task = PeriodicTask.objects.get(name="every-5-seconds")
        args = json.loads(task.args)
        args = args[0]
        for i in stocks:
            i.user.remove(user)
            if i.user.count() == 0:
                args.remove(i.stock)
                i.delete()
        if args is None:
            args = []

        if len(args) == 0:
            task.delete()
        else:
            task.args = json.dumps([args])
            task.save()

    async def disconnect(self, close_code):
        await self.helper()

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_update',
                'message': message
            }
        )

    @sync_to_async
    def select_stocks(self):
        user = self.scope["user"]
        user_stocks = user.stockdetail_set.values_list('stock', flat=True)
        return list(user_stocks)

    async def send_stock_update(self, event):
        message = event['message']
        message = copy.copy(message)

        user_stocks = await self.select_stocks()

        keys = message.keys()
        for key in list(keys):
            if key in user_stocks:
                pass
            else:
                del message[key]

        await self.send(text_data=json.dumps(message))
