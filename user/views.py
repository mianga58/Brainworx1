from django.shortcuts import render, redirect, HttpResponse

from user.models import UserRegistration
from django.contrib import messages
from validate_email import validate_email
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import View
from .forms import UserForm
#password reset and email activation
from django.core.mail import send_mail, BadHeaderError, EmailMessage
from django.contrib.auth.models import User
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import token_generator
from django.contrib.auth.tokens import PasswordResetTokenGenerator

from django.core.exceptions import ObjectDoesNotExist
from payment.models import Subscription

import threading
from datetime import timedelta

#speeding up background email services
class EmailThread(threading.Thread):

    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)



@login_required(login_url='/signin')
def index(request):
    return render(request, 'base.html')

@login_required(login_url='/signin')
def indexUser(request):
    username = request.user.username
    return render(request, 'user/index_user.html', {'username': username})


def signin(request):
    return render(request, 'user/signin.html')

def signup(request):
    return render(request, 'user/signup.html')


def signout(request):
    logout(request)
    return render(request, 'base.html')


@login_required(login_url='/signin')
def about(request):
    current_plan = ""
    try:
        current_plan = Subscription.objects.get(user=request.user)
    except ObjectDoesNotExist:
        return render(request, 'payment/home.html')

    return render(request, 'user/about.html' , {'current_plan': current_plan})


@login_required(login_url='/signin')
def profile(request):
    username = request.user.username
    if request.method == 'GET':
        all_data = UserRegistration.objects.all()
        for users in all_data:
            if username == users.username:
                fn = users.firstName
                ln = request.user.lastName
                add = users.address
                gen = users.gender
                dob = users.dob
                em = users.email
                mn = users.mobileNumber

                return render(request, 'user/profile.html',
                              {'username': username, 'firstName': fn, 'ln': ln, 'add': add, 'gen': gen, 'dob': dob, 'em': em,
                               'mn': mn})

    return render(request, 'user/profile.html', )

def dashboard(request):
    current_plan = ""
    enddate = ""
    try:
        current_plan = Subscription.objects.get(user=request.user)
        enddate = current_plan.reg_date + timedelta(days=current_plan.plan.validity_days)
    except ObjectDoesNotExist:
        return render(request, 'payment/home.html')
    #current_plan = Subscription.objects.get(user=request.user)
    # my_trainer=models.AssignSubscriber.objects.get(user=request.user)
   # enddate = current_plan.reg_date + timedelta(days=current_plan.plan.validity_days)

    return render(request, 'user/dashboard.html', {'current_plan':current_plan, 'enddate':enddate})


class UserFormView(View):
    form_class = UserForm
    template_name = 'user/signup.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        flag_userReg = 0

        if form.is_valid():
            firstName_r = request.POST.get('firstName')
            lastName_r = request.POST.get('lastName')
            username_r = request.POST.get('username')
            address_r = request.POST.get('address')
            gender_r = request.POST.get('gender')
            dob_r = request.POST.get('dob')
            email_r = request.POST.get('email')
            mobileNumber_r = request.POST.get('mobileNumber')
            ur = UserRegistration(firstName=firstName_r, lastName=lastName_r, username=username_r, address=address_r,
                                  gender=gender_r, dob=dob_r, email=email_r, mobileNumber=mobileNumber_r)
            ur.save()

            user = form.save(
                commit=False)  # this will save the entered data in user object but won't save in database

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user.set_password(password)
            user.is_active = False
            user.save()
            #email activation
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))

            domain = get_current_site(request).domain
            link = reverse('user:activate', kwargs={
                           'uidb64': uidb64, 'token': token_generator.make_token(user)})

            activate_url = 'http://' + domain + link

            email_body = 'Hello ' + user.username + '\n' + 'Please use this link to verify your account\n' + activate_url

            email_subject = 'Activate your account'

            email = EmailMessage(
                email_subject,
                email_body,
                'noreply@semycolon.com',
                [email_r],
            )
            EmailThread(email).start()
            flag_userReg = 1
            return render(request, 'user/signup.html', {'flag_userReg': flag_userReg})

        return render(request, self.template_name, {'form': form, 'flag_userReg': flag_userReg})

#Account activation continuation
class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            if not token_generator.check_token(user, token):
                return redirect('user:signin' + '?message=' + 'User already activated')

            if user.is_active:
                return redirect('user:signin')
            user.is_active = True
            user.save()

            messages.success(request, 'Account activated successfully')
            return redirect('user:signin')

        except Exception as ex:
            pass

        return redirect('user:signin')

class SignInFormView(View):
    form_class = UserForm
    template_name = 'user/signin.html'

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        flag_userSignIn = 0

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            flag_userSignIn = 1
            return render(request, 'user/index_user.html',
                          {'flag_userSignIn': flag_userSignIn, 'username': username})

        return render(request, self.template_name, {'form': form, 'flag_userSignIn': flag_userSignIn})

#Password Reset
class RequestPasswordResetEmail(View):
    def get(self, request):
        return render(request, 'user/reset-password.html')

    def post(self, request):
        email = request.POST['email']

        context = {
            'values': request.POST
        }

        if not validate_email(email):
            messages.error(request, 'Please supply a valid email')
            return render(request, 'user/reset-password.html', context)

        current_site = get_current_site(request)

        user = User.objects.filter(email=email)

        if user.exists():
            email_content = {
                'user': user[0],
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                'token': PasswordResetTokenGenerator().make_token(user[0]),
            }

            link = reverse('user:reset-user-password', kwargs={
                'uidb64': email_content['uid'], 'token': email_content['token']})

            email_subject = 'Password reset Instructions'

            reset_url = 'http://' + current_site.domain + link

            email = EmailMessage(
                email_subject,
                'Hi there, Please click the link below to reset your password \n' + reset_url,
                'noreply@semycolon.com',
                [email],
            )
            EmailThread(email).start()

        messages.success(request, 'We have sent you an email to reset your password.')

        return render(request, 'user/reset-password.html')

class CompletePasswordReset(View):
    def get(self, request, uidb64, token):

        context = {
            'uidb64': uidb64,
            'token': token
        }

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                messages.info(request, 'Password link was used, please request a new one')
                return render(request, 'user/reset-password.html')
        except Exception as identifier:

            pass

        return render(request, 'user/set-new-password.html', context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }

        password = request.POST['password']
        password2 = request.POST['password2']
        if password != password2:
            messages.error(request, 'Passwords do not match')
            return render(request, 'user/set-new-password.html', context)

        if len(password) < 8:
            messages.error(request, 'Password too short')
            return render(request, 'user/set-new-password.html', context)

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()

            messages.success(request, 'Password reset successfully, You can go ahead with the new password')
            return redirect('user:signin')
        except Exception as identifier:
            messages.info(request, 'Something went wrong, try again')
            return render(request, 'user/set-new-password.html', context)

