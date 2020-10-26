from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='datalogger.home'),
    path('log/', views.log, name='datalogger.log'),
    path('logOld/', views.logOld, name='datalogger.logOld'),
    path('logData/', views.logData, name='datalogger.logData'),
    path('logDelete/', views.logDelete, name='datalogger.logDelete'),
    path('charts/', views.charts, name='datalogger.charts')
]
