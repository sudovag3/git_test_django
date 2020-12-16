"""tgbisadmin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path

from django.conf.urls import include, url
from django.contrib import admin
from django.urls import path
from ugs.views import ProccesHookView, hello, HomePageView, test, hello1


urlpatterns = [

    url(r'^hook/$', ProccesHookView.as_view(), name='webhook'),
    url(r'^admin/', admin.site.urls),
    url(r'^redirect2/$', hello, name='home'),
    url('^redirect/$', hello1, name='home'),
    # path('', include('template.pages.urls'))
    # url(r'^redirect/$', hello()),
]
#
# urlpatterns = [
#     path('admin/', admin.site.urls),
# ]
