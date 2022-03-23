from django.urls import path
from . import views


app_name = 'payment'

urlpatterns = [

    path('', views.home, name='home'),
    path('price', views.price, name='price'),
	path('pay', views.pay, name='pay'),
	path('pay1', views.pay1, name='pay1'),
	path('pay2', views.pay2, name='pay2'),
	path('pay_success',views.pay_success,name='pay_success'),
	path('pay_success1',views.pay_success1,name='pay_success1'),
	path('pay_success2',views.pay_success2,name='pay_success2'),


]