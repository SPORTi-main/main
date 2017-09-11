"""sporti URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from django.views.static import serve
from main_app import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView



urlpatterns = [
    url(r'^$', views.Home.as_view(), name = 'home'),
    url(r'^admin/', admin.site.urls),
    url(r'^profile/', include('profiles.urls')),
    url(r'^questions/', include('main_app.urls')),
    url(r'^like/(?P<pk>\d+)/$', views.ChoiceLikeToggle.as_view(), name ='like'),
    url(r'^login/$', LoginView.as_view(), name = 'login'),
    url(r'^password_reset/$', PasswordResetView.as_view(), name = 'password_reset'),
    url(r'^password_reset_sent/$', PasswordResetDoneView.as_view(), name = 'password_reset_done'),
    url(r'^logout/$', views.LogoutView.as_view(), name = 'logout'),
    url(r'^join/$', views.Join.as_view(), name = 'join'),
    url(r'^sports/(?P<slug>[\w-]+)/$', views.sports, name = 'sports'),
    url(r'^about/$',views.TemplateView.as_view(template_name='about.html'),name='about'),
    url(r'^careers/$',views.TemplateView.as_view(template_name='careers.html'),name='careers'),
    url(r'^advertise/$',views.TemplateView.as_view(template_name='advertise.html'),name='advertise'),
    url(r'^contact/$',views.TemplateView.as_view(template_name='contact.html'), name='contact'),
    url(r'^welcome/$', views.WelcomeView.as_view(), name='welcome'),
]

if settings.DEBUG:
    urlpatterns += [
    url(r'^media/(?P<path>.*)$', serve,
        {'document_root': settings.MEDIA_ROOT,}),
    ]