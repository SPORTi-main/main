from .views import ProfileDetailView, activate_user_view
from django.conf.urls import url 

urlpatterns = [
url(r'^(?P<username>[\w-]+)/$', ProfileDetailView.as_view(), name ='profile'),
url(r'^activate/(?P<code>[a-z0-9].*)/$', activate_user_view, name='activate'),
]