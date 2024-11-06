from django.db import models    #type: ignore
from django.contrib.auth.models import User #type: ignore

class Tweet(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    text=models.TextField(max_length=255)
    photo=models.ImageField(upload_to="photo/",blank=True,null=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)


    def __str__(self) :
        return f'{self.user.username} -- {self.text[0:20]}'
