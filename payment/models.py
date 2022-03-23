from django.db import models

# Create your models here.
from django.db import models
from django.utils.html import mark_safe
from django.contrib.auth.models import User

from django.db.models.signals import post_save
from django.dispatch import receiver


import json

class SubPlan(models.Model):
	title=models.CharField(max_length=150)
	price=models.IntegerField()
	max_member=models.IntegerField(null=True)
	highlight_status=models.BooleanField(default=False,null=True)
	validity_days=models.IntegerField(null=True)

	def __str__(self):
		return self.title

# Subscription Plans Features
class SubPlanFeature(models.Model):
	# subplan=models.ForeignKey(SubPlan, on_delete=models.CASCADE,null=True)
	subplan=models.ManyToManyField(SubPlan)
	title=models.CharField(max_length=150)

	def __str__(self):
		return self.title

# Subscriber
class Subscriber(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	mobile=models.CharField(max_length=20)
	address=models.TextField()
	img=models.ImageField(upload_to="subs/",null=True)

	def __str__(self):
		return str(self.user)

	def image_tag(self):
		if self.img:
			return mark_safe('<img src="%s" width="80" />' % (self.img.url))
		else:
			return 'no-image'

@receiver(post_save,sender=User)
def create_subscriber(sender,instance,created,**kwrags):
	if created:
		Subscriber.objects.create(user=instance)

# Subscription
class Subscription(models.Model):
	user=models.ForeignKey(User, on_delete=models.CASCADE,null=True)
	plan=models.ForeignKey(SubPlan, on_delete=models.CASCADE,null=True)
	price=models.CharField(max_length=50)
	reg_date=models.DateField(auto_now_add=True,null=True)

#flutterwave
class FlwPlanModel(models.Model):
	"""Represents either a Plan or OnceOff payment type"""

	HOURLY = "hourly"
	DAILY = "daily"
	WEEKLY = "weekly"
	MONTHLY = "monthly"
	QUARTERLY = "quarterly"
	BI_ANNUALLY = "bi_annually"
	YEARLY = "yearly"
	INTERVAL_CHOICES = (
		(HOURLY, "Hourly"),
		(DAILY, "Daily"),
		(WEEKLY, "Weekly"),
		(MONTHLY, "Monthly"),
		(QUARTERLY, "Quarterly"),
		(BI_ANNUALLY, "Bi Annually"),
		(YEARLY, "Yearly"),
	)
	name = models.CharField(max_length=50, unique=True)
	amount = models.DecimalField(decimal_places=2, max_digits=9)
	flw_pla_id = models.PositiveIntegerField(
		unique=True,
		blank=True,
		null=True,
		help_text="Flutterwave plan id. Only required if this is a subscription plan.",
	)
	interval = models.CharField(
		max_length=11,
		blank=True,
		null=True,
		choices=INTERVAL_CHOICES,
		help_text="Payment frequency. Only required if this is a subscription plan.",
	)
	currency = models.CharField(max_length=3, default="ZMW")
	modal_logo_url = models.URLField(
		max_length=500,
		blank=True,
		null=True,
		help_text="URL to logo image to be displayed on payment modal.",
	)
	modal_title = models.CharField(
		max_length=200,
		blank=True,
		null=True,
		help_text="Title to be displayed on payment modal.",
	)
	pay_button_text = models.CharField(
		max_length=100,
		default="Sign Up",
		help_text="Text used for button when displayed in a template.",
	)
	pay_button_css_classes = models.CharField(
		max_length=200,
		blank=True,
		null=True,
		help_text="css classes to be applied to pay button in template.",
	)
	created_datetime = models.DateTimeField(auto_now_add=True)

	class Meta:
		verbose_name = "Pla"
		verbose_name_plural = "Plas"

	def __str__(self):
		return self.name
