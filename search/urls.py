from django.urls import path
from . import views

app_name = 'search'
urlpatterns = [
    path('', views.index, name='index'),
    path('find_DB/', views.find_DB, name='find_DB'),
    path('<str:t>/crawler/', views.crawler, name='crawler'),
    path('<int:isbn>/result/', views.result, name='result'),
    path('maptest/', views.maptest, name='maptest')
    # path('select/', views.select, name='select')
    # path('in_crawling/', views.in_crawling, name='in_crawling')
]