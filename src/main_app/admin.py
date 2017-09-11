from django.contrib import admin
from .models import Question, Sport, Comment, Choice

# Register your models here.



admin.site.register(Question)
admin.site.register(Sport)
admin.site.register(Comment)
admin.site.register(Choice)