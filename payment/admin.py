from django.contrib import admin
from .models import FlwPlanModel
# Register your models here.
from . import models

class SubPlanAdmin(admin.ModelAdmin):
	list_editable=('highlight_status','max_member')
	list_display=('title','price','max_member','validity_days','highlight_status')
admin.site.register(models.SubPlan,SubPlanAdmin)

class SubPlanFeatureAdmin(admin.ModelAdmin):
	list_display=('title','subplans')
	def subplans(self,obj):
		return " | ".join([sub.title for sub in obj.subplan.all()])
admin.site.register(models.SubPlanFeature,SubPlanFeatureAdmin)


class SubscriberAdmin(admin.ModelAdmin):
	list_display=('user','image_tag','mobile')
admin.site.register(models.Subscriber,SubscriberAdmin)


class SubscriptionAdmin(admin.ModelAdmin):
	list_display=('user','plan','reg_date','price')
admin.site.register(models.Subscription,SubscriptionAdmin)

class PlaAdmin(admin.ModelAdmin):
    list_display = ("name", "amount", "flw_pla_id", "interval")
    search_fields = ("name",)
    readonly_fields = ("created_datetime",)



admin.site.register(FlwPlanModel, PlaAdmin)

