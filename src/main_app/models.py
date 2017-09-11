from __future__ import unicode_literals
from django.db import models
from django.db.models import Q 
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models.signals import pre_save, post_save
from .utils import unique_slug_generator
from django.core.exceptions import ValidationError
from .validators import validate_choice
from django.conf import settings

User = settings.AUTH_USER_MODEL

# Create your models here.
class Sport(models.Model):
	name 			= models.CharField(max_length=500)
	date_added 		= models.DateTimeField(auto_now_add=True)
	date_updated 	= models.DateTimeField(auto_now=True)
	slug 			= models.SlugField(null=True, blank=True)

	def __str__(self):
		return self.name

def sport_pre_save_receiver(sender, instance, *args, **kwargs):
	print('saving...')
	print(instance.name)
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)

def sport_post_save_receiver(sender, instance, created, *args, **kwargs):
	print('saved')
	print(instance.date_added)		

pre_save.connect(sport_pre_save_receiver, sender = Sport)

post_save.connect(sport_post_save_receiver, sender = Sport)


class QuestionQuerySet(models.query.QuerySet):
	def search(self, query):
		if query:
			return self.filter(
				Q(name__icontains=query)|
				Q(slug__icontains=query)
				).distinct()
		return self
		
class QuestionManager(models.Manager):
	def get_queryset(self):
		return QuestionQuerySet(self.model, using=self.db)

	def search(self, query):	
		return self.get.queryset().search(query)

class Question(models.Model):
	user 			= models.ForeignKey(User)
	name 			= models.CharField(max_length=500)
	image 			= models.ImageField(upload_to='question_images', default ='media/default.png')
	category 		= models.ForeignKey(Sport, related_name='questions', default=None, blank=True, null=True)
	date_added 		= models.DateTimeField(auto_now_add=True)
	date_updated 	= models.DateTimeField(auto_now=True)
	slug 			= models.SlugField(null=True, blank=True)
	objects 		= QuestionManager() 

	def __str__(self):
		return self.name

def question_pre_save_receiver(sender, instance, *args, **kwargs):
	print('saving...')
	print(instance.name)
	if not instance.slug:
		instance.slug = unique_slug_generator(instance)

def question_post_save_receiver(sender, instance, created, *args, **kwargs):
	print('saved')
	print(instance.date_added)

pre_save.connect(question_pre_save_receiver, sender = Question)

post_save.connect(question_post_save_receiver, sender = Question)

class Choice(models.Model):
	question 		= 	models.ForeignKey(Question, related_name = 'choices')
	choice 			= 	models.CharField(max_length=500,validators=[validate_choice])
	approved 		= 	models.BooleanField(default=False)
	likes 			= 	models.ManyToManyField(User, blank=True, related_name='user_likes')
	date_added 		= 	models.DateTimeField(auto_now_add=True)
	date_updated 	= 	models.DateTimeField(auto_now=True)
	def __str__(self):
		return self.choice


class Comment(models.Model):
	question 		= models.ForeignKey(Question, related_name = 'comments')
	reply_to 		= models.ForeignKey('self', related_name='replies', null=True, blank=True)
	owner 			= models.ForeignKey(User)
	body 			= models.TextField()
	approved		= models.BooleanField(default=False)
	date_added 		= models.DateTimeField(auto_now_add=True)
	date_updated 	= models.DateTimeField(auto_now=True)

	def approved(self):
		self.approved=True
		self.save()

	def __str__(self):
		return self.body

