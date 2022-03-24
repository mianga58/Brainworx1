from django.urls import path
from . import views
from django.views.generic import TemplateView

app_name = 'chat'

urlpatterns = [

    path('', views.index, name='home'),
    #path('video_feed/', views.video_feed, name='video_feed'),
    path('forum/', views.forum, name='forum'),

]
