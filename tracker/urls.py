from django.urls import path
from . import views

urlpatterns = [
    path('', views.collector, name='collector'),
    path('tracker/', views.tracker, name='tracker'),

]
