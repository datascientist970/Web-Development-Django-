from django.contrib import admin    #type: ignore
from .models import Tweet
# Register your models here.
admin.site.register(Tweet)
