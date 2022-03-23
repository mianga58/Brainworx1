from django.shortcuts import render
from django.db.models import Count
from . import models
from django.http import JsonResponse

from django.contrib.auth.models import User

# Create your views here.
from .models import FlwPlanModel
from django.conf import settings
import requests

from datetime import timedelta


def home(request):
	pricing=models.SubPlan.objects.annotate(total_members=Count('subscription__id')).all().order_by('price')
	dfeatures=models.SubPlanFeature.objects.all();
	return render(request, 'payment/home.html',{'plans':pricing,'dfeatures':dfeatures})


def price(request):
    return render(request, 'payment/price.html')


# def pay(request):
def pay(request):
    pricing = models.SubPlan.objects.annotate(total_members=Count('subscription__id')).all().order_by('price')
    dfeatures = models.SubPlanFeature.objects.all()

    Basic = FlwPlanModel.objects.filter()[0]
    key = settings.RAVE_SANDBOX_PUBLIC_KEY
    logo = settings.WILDLIFE_LOGO
    return render(request, 'payment/pricing.html',
                  {'logo': logo, 'key': key, 'Basic': Basic, 'plans': pricing, 'dfeatures': dfeatures})


def pay1(request):
    Jobby = FlwPlanModel.objects.filter()[1]
    pricing = models.SubPlan.objects.annotate(total_members=Count('subscription__id')).all().order_by('price')
    dfeatures = models.SubPlanFeature.objects.all()
    key = settings.RAVE_SANDBOX_PUBLIC_KEY
    logo = settings.WILDLIFE_LOGO
    return render(request, 'payment/pricing1.html',
                  {'logo': logo, 'key': key, 'Jobby': Jobby, 'plans': pricing, 'dfeatures': dfeatures})


def pay2(request):
    Chaggy = FlwPlanModel.objects.filter()[2]
    pricing = models.SubPlan.objects.annotate(total_members=Count('subscription__id')).all().order_by('price')
    dfeatures = models.SubPlanFeature.objects.all()
    key = settings.RAVE_SANDBOX_PUBLIC_KEY
    logo = settings.WILDLIFE_LOGO
    return render(request, 'payment/pricing2.html',
                  {'logo': logo, 'key': key, 'Chaggy': Chaggy, 'plans': pricing, 'dfeatures': dfeatures})


# Success

# from django.db.models import Q

def pay_success(request):
    plan = models.SubPlan.objects.filter()[0]
    user = request.user
    models.Subscription.objects.create(
        plan=plan,
        user=user,
        price=plan.price
    )

    return render(request, 'payment/success.html')


def pay_success1(request):
    plan = models.SubPlan.objects.filter()[1]
    user = request.user
    models.Subscription.objects.create(
        plan=plan,
        user=user,
        price=plan.price
    )
    return render(request, 'payment/success1.html')


def pay_success2(request):
    plan = models.SubPlan.objects.filter()[2]
    user = request.user
    models.Subscription.objects.create(
        plan=plan,
        user=user,
        price=plan.price
    )
    return render(request, 'payment/success2.html')

