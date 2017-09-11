from django.views import View
from django.views.generic import TemplateView, ListView, DetailView, FormView
from django.shortcuts import render, render_to_response, get_object_or_404
from django.views.generic import RedirectView
from .models import Question, Comment, Choice, Sport
from .forms import QuestionForm, CommentForm, ChoicesForm, UserCreateForm
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from .forms import LoginForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import JsonResponse
from .mixins import AjaxFormMixin

# Create your views here.

class Home(TemplateView):
	template_name = 'home.html'

	def get_context_data(self):
		context = super(Home, self).get_context_data()
		query = self.request.GET.get('query')
		context['sports'] = Sport.objects.all()
		context['trending'] = Question.objects.all()
		context['username'] = Comment.objects.all()
		context['comments'] = User.objects.all()
		qs = Question.objects.filter().search(query)
		context['questions'] = qs

		return context

def details(request, pk):
	questions = Question.objects.get(id=pk)
	similar = Question.objects.filter(category=questions.category)
	form = CommentForm()
	comments = Comment.objects.filter(question_id = pk, reply_to__isnull=True)
	reply = Comment.objects.filter(question_id = pk, reply_to__isnull=False)
	choices = Choice.objects.filter(question_id = pk)
	sports = Sport.objects.all()
	context = {	'sports':sports,
				'questions':questions, 
				'form':form, 
				'similar':similar,
				'comments': comments, 
				'reply': reply,
	   			'choices': choices
			}
	return render(request, 'details.html',context)

# class Profile(LoginRequiredMixin, DetailView):
# 	def get_queryset(self):
# 		return Question.objects.filter(user=self.request.user)
		


# def profile(request, username):
# 	sports = Sport.objects.all()
# 	user = User.objects.get(username = username)
# 	questions = Question.objects.filter(user=user)
# 	context= {	'sports':sports,
# 				'questions':questions,
# 				'username':username
# 				}
# 	return render(request, 'profile.html', context)


# class based views

class PostComment(LoginRequiredMixin, CreateView):
	form_class 	= CommentForm

	def get_context_data(self, *args, **kwargs):
		context = super(PostComment, self).get_context_data(*args, **kwargs)
		context['sports'] = Sport.objects.all()
		context['questions'] = Question.objects.get(id=self.kwargs['pk'])
		return context

	def form_valid(self,form):
		comment = form.save(commit = False)
		comment.owner = self.request.user
		comment.question_id = self.kwargs['pk']
		return super(PostComment, self).form_valid(form)

	def get_success_url(self, *args, **kwargs):
		return reverse_lazy('question', kwargs={ "pk": self.kwargs['pk'] })


class AddOptions(AjaxFormMixin, LoginRequiredMixin, CreateView):
	form_class = ChoicesForm
	login_url = '/login/'
	template_name = 'add_options.html'
	
	def get_context_data(self, *args, **kwargs):
		context = super(AddOptions, self).get_context_data(*args, **kwargs)
		context['sports'] = Sport.objects.all()
		context['questions'] = Question.objects.get(id=self.kwargs['pk'])
		return context

	def form_valid(self,form):
		choices = form.save(commit = False)
		choices.question_id = self.kwargs['pk']
		return super(AddOptions, self).form_valid(form)

	def get_success_url(self, *args, **kwargs):
		return reverse_lazy('question', kwargs={ "pk": self.kwargs['pk'] })


class CreateQuestion(LoginRequiredMixin, CreateView):
	form_class = QuestionForm
	success_url = '/'
	template_name = 'create_question.html'

	def form_valid(self,form):
		question = form.save(commit = False)
		question.user = self.request.user
		return super(CreateQuestion, self).form_valid(form)

	def get_context_data(self, *args, **kwargs):
		context = super(CreateQuestion, self).get_context_data(*args, **kwargs)
		context['sports'] = Sport.objects.all()
		return context


class LoginView(LoginView):
	def get (self, request):
		form = LoginForm()
		context= {'form': form
		}		
		sports = Sport.objects.all()
		extra_context = {'sports': sports}

		if extra_context is not None:
			context.update(extra_context)

		return render(request, 'login.html', context)

	def post(self,request, *args, **kwargs):
		form = LoginForm(request.POST)
		if request.POST and form.is_valid():
			user = form.login(request)
			if user:
				login(request, user)
				return HttpResponseRedirect("/")
		else:
			print('There was an error!')
			return HttpResponseRedirect("/login/")


class LogoutView(View):
	def get(self, request):
		logout(request)
		return HttpResponseRedirect("/")

class Join(CreateView):
	form_class = UserCreateForm
	template_name = 'join.html'
	success_url = '/welcome/'

class WelcomeView(TemplateView):
	template_name = 'welcome.html'
	
	def get_context_data(self):
		context = super(WelcomeView, self).get_context_data()
		context['sports'] = Sport.objects.all()
		return context


	# def get(self, request):
	# 	form = UserCreateForm()
	# 	sports = Sport.objects.all()
	# 	context = {	'sports': sports,
	# 				'form': form
	# 	}

	# 	return render(request,'join.html',context)

	# def post(self,request):
	# 	form = UserCreateForm(request.POST)
	# 	if form.is_valid():
	# 		form.save()
	# 		new_user = authenticate(username=form.cleaned_data['username'],password=form.cleaned_data['password1'],)
	# 		login(request, new_user)
	# 		return HttpResponseRedirect("/")


# class ChoiceLikeToggle(LoginRequiredMixin, View):
	
# 	def post(self, request, *args, **kwargs):
# 		user_to_toggle = request.POST.get('username')
# 		choice = Choice.objects.get(id = self.kwargs['pk'])
# 		user = request.user
# 		if user in choice.likes.all():
# 			choice.likes.remove(user)
# 		else:
# 			choice.likes.add(user)
# 		question = choice.question.id
# 		print (question)
		
# 		return HttpResponseRedirect(f"/questions/{question}/")

class ChoiceLikeToggle(View):
	def post(self, *args, **kwargs):
		choice = self.kwargs.get("pk")
		obj = get_object_or_404(Choice, pk=choice)
		user = self.request.user
		if user.is_authenticated():
			if user in obj.likes.all():
				obj.likes.remove(user)
			else:
				obj.likes.add(user)
		question = obj.question.id
		return HttpResponseRedirect(f"/questions/{question}/")

# TemplateViews

class TemplateViews(TemplateView):

	def get_context_data(self, *args, **kwargs):
		context = super(TemplateViews, self).get_context_data(*args,**kwargs)
		query = self.request.GET.get('query')
		context['sports'] = Sport.objects.all()
		context['questions'] = Question.objects.all()
		if query:
			context['questions'] = Question.objects.filter(name__icontains=query)
		# Need to also filter by user here
		return context

# ListViews tbc

def sports(request, slug):
	sports = Sport.objects.all()
	selected_sport = Sport.objects.get(slug = slug)
	questions = Question.objects.filter(category_id = selected_sport.id)
	context = {	'selected_sport':selected_sport,
				'questions':questions, 
				'sports':sports
	}
	return render(request, 'sports.html', context)
