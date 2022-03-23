"""BrainworX URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('user.urls', namespace='user')),
   # path('',include('Emp.urls', namespace='Emp')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('videos/',include('videos.urls', namespace='videos')),
    path('pp/',include('pp.urls', namespace='pp')),
    path('chat/',include('chat.urls', namespace='chat')),
    path('payment/',include('payment.urls', namespace='payment')),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)
    urlpatterns += static('/pp/assets/PDFjs/build/', document_root=(settings.BASE_DIR / 'media/book/'))