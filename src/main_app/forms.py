from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms 
from .models import Question, Comment, Choice, Sport
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from .validators import validate_choice

class QuestionForm(forms.ModelForm):
	class Meta:
		model = Question
		fields = ['name','category','image']

class ChoicesForm(forms.ModelForm):
	class Meta:
		model = Choice
		fields = ['choice']

class LoginForm(forms.Form):
	username = forms.CharField(max_length = 64,required=True)
	password = forms.CharField(widget = forms.PasswordInput(), required=True)

	def clean(self):
		username = self.cleaned_data.get('username') 
		password = self.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		if not user or not user.is_active:
		    raise forms.ValidationError("Sorry, that login was invalid. Please try again.")
		return self.cleaned_data

	def login(self, request):
		username = self.cleaned_data.get('username')
		password = self.cleaned_data.get('password')
		user = authenticate(username=username, password=password)
		return user

class CommentForm(forms.ModelForm):
	class Meta:
		model = Comment
		fields = ['body']


class UserCreateForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("username", "email",)

    def clean_username(self):
	    username = self.cleaned_data.get("username")
	    qs = User.objects.filter(username__iexact = username)  
	    if qs.exists():
	    	raise forms.ValidationError('This Username already exists.')
	    return username

    def clean_email(self):
	    email = self.cleaned_data.get("email")
	    qs = User.objects.filter(email__iexact = email)  
	    if qs.exists():
	    	raise forms.ValidationError('This Email already exists.')
	    return email

    def clean_password2(self):
    	password1 = self.cleaned_data.get('password1')
    	password2 = self.cleaned_data.get('password2')
    	if password1 and password2 and password1 != password2:
    		raise forms.ValidationError('Passwords do not match')

    def save(self, commit=True):
        user = super(UserCreateForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            user.profile.send_activation_email()
        return user



		




		
