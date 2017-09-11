from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from .utils import code_generator
from django.core.mail import send_mail
from django.core.urlresolvers import reverse

User = settings.AUTH_USER_MODEL


class Badge(models.Model):
	owners 			= 	models.ManyToManyField(User, blank=True, null=True, related_name='badges')
	badge 			=	models.CharField(max_length=120)
	description		=	models.TextField(max_length=500)
	image 			= 	models.ImageField(upload_to='badge_images', default ='media/default.png')
	date_added 		= 	models.DateTimeField(auto_now_add=True)
	date_updated 	= 	models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.badge


class Profile(models.Model):
	user 			= models.OneToOneField(User)
	approved 		= models.BooleanField(default=False)
	date_added 		= models.DateTimeField(auto_now_add=True)
	date_updated 	= models.DateTimeField(auto_now=True)
	activation_key 	= models.CharField(max_length=120, null=True, blank=True)
	activated 		= models.BooleanField(default=False)

	def __str__(self):
		return self.user.username

	def send_activation_email(self):
		print('Activation Email Sent')
		if not self.activated:
			self.activation_key = code_generator()
			self.save()
			path_ = reverse('activate', kwargs={"code": self.activation_key})
			# full_path = "https://sporti.io" + path_
			subject = 'Activate Account'
			from_email = settings.DEFAULT_FROM_EMAIL
			message = f'Activate your account here: {path_}'
			recipient_list = [self.user.email]
			html_message = f'<p>Activate your account here: {path_}</p>'
			print(html_message)
			# sent_mail = send_mail(
			#                 subject, 
			#                 message, 
			#                 from_email, 
			#                 recipient_list, 
			#                 fail_silently=False, 
			#                 html_message=html_message)
			sent_mail = False
			return sent_mail

def post_save_user_reciever(sender, instance, created, *args, **kwargs):
	if created:
		profile, is_created = Profile.objects.get_or_create(user=instance)

post_save.connect(post_save_user_reciever, sender=User)

# Use this to create a Profile model which will link to everything else.
		

		

