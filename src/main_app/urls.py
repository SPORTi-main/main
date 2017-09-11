from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.views.generic import TemplateView
from django.views.static import serve
from main_app import views
from django.views.generic import TemplateView
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView

urlpatterns = [
    url(r'^(?P<pk>\d+)/add_comment/post_url/$', views.PostComment.as_view(), name='post_comment'),
    url(r'^create_question/$', views.CreateQuestion.as_view(), name = 'create_question'),
    url(r'^(?P<pk>\d+)/add_options/$', views.AddOptions.as_view(), name = 'add_options'),
    url(r'^(?P<pk>\d+)/$', views.details, name = 'question'),
]
