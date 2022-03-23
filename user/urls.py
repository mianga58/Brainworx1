from django.urls import path
from . import views
from .views import VerificationView, RequestPasswordResetEmail, CompletePasswordReset

app_name = 'user'

urlpatterns = [
    path('', views.indexUser, name='home'),
    path('signup/', views.signup, name='signup'),
    path('signup2/', views.UserFormView.as_view(), name='signup2'),
    path('signin/', views.SignInFormView.as_view(), name='signin'),
    path('home_user/', views.indexUser, name='home_user'),
    path('signout/', views.signout, name='signout'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='Profile'),
    path('dashboard/', views.dashboard, name='dashboard'),

    path('activate/<uidb64>/<token>/', VerificationView.as_view(), name='activate'),
    path('request-reset-link', RequestPasswordResetEmail.as_view(), name="request-password"),

    path('set-new-password<uidb64>/<token>/', CompletePasswordReset.as_view(), name='reset-user-password'),



]