from django.urls import path

from . import views

#setting up URL paths for the pages
urlpatterns = [
    path('', views.index, name='index'),
    path('searchresults', views.searchresults, name='searchresults'),
    path('info', views.info, name='info'),
    path('viewteam', views.viewteam, name='viewteam'),
    path('add', views.add, name='add'),
    path('delete', views.delete, name='delete')
]
