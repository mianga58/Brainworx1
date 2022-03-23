from django.urls import path
from . import views

app_name = 'videos'

urlpatterns = [
    path('stream/<int:pk>/', views.get_streaming_video, name='stream'),
    path('<int:pk>/', views.get_video, name='video'),
    #path('', views.get_list_video, name='home'),
    path('', views.index, name='hom'),

]