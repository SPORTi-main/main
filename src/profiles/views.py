from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.views.generic import DetailView
from django.http import Http404

from main_app.models import Sport, Question, Comment, Choice
from .models import Profile, Badge


User = get_user_model()
# Create your views here.

def activate_user_view(request, code=None, *args, **kwargs):
    if code:
        qs = Profile.objects.filter(activation_key=code)
        if qs.exists() and qs.count() == 1:
            profile = qs.first()
            if not profile.activated:
                user_ = profile.user
                user_.is_active = True
                user_.save()
                profile.activated=True
                profile.activation_key=None
                profile.save()
                return redirect("/login")
    return redirect("/login")

class ProfileDetailView(DetailView):
	template_name = 'profile.html'

	def get_object(self):
		username = self.kwargs.get("username")
		if username is None:
			raise Http404
		return get_object_or_404(User, username__iexact = username , is_active = True)

	def get_context_data(self, *args, **kwargs):
		username = self.kwargs.get("username")
		user = User.objects.get(username=username)
		context = super(ProfileDetailView, self).get_context_data(*args,**kwargs)
		context['sports'] = Sport.objects.all()
		context['comments'] = Comment.objects.filter(owner_id=user.id)
		context['likes'] = Choice.objects.filter(likes=user.id)
		context['questions'] = Question.objects.filter(user_id=user.id)
		context['badges'] = Badge.objects.filter(owners=user.id)




		return context



