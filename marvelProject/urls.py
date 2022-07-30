from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('searchresults', views.searchresults, name='searchresults'),
    path('info', views.info, name='info'),
    path('viewteam', views.viewteam, name='viewteam')
]
