from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('search-results', views.searchresults, name='search-results'),
    path('info', views.info, name='info')
]
