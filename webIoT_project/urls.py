"""webIoT_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from chartApp import views
from accounts import views as accounts_views
from django.contrib.auth.views import logout, login
import settings


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^signup/$', accounts_views.signup, name='signup'),
    url(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    url(r'^login/$', login, {'template_name':'login.html'}, name='login'),
    url(r'^$',views.home, name='home'),
    url(r'^page/(?P<pk>\d+)/$', views.page, name='page'),
    url(r'^page/(?P<pk>\d+)/(?P<slug>[-\w]+)/$', views.page2, name='page2'),
    url(r'^setting/$', views.settingAcc, name='settingAcc'),
]
