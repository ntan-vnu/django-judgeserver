"""judgeserver URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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

from judge import views as judge_views

urlpatterns = [
    path('', judge_views.home, name='home'),
    path('admin/', admin.site.urls, name='admin'),
    path('account/', include(('account.urls', 'account'), namespace='account')),
    path('judge/', include(('judge.urls', 'judge'), namespace='judge')),
    path('history/', include(('history.urls', 'history'), namespace='history')),
]
