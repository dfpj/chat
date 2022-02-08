from django.db import models
from django.contrib.auth.models import User


class Chat(models.Model):
    name = models.CharField(max_length=50,blank=True)
    members =models.ManyToManyField(User,null=True,blank=True,related_name='chats')

    def __str__(self):
        return self.name


class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    chat = models.ForeignKey(Chat,on_delete=models.CASCADE,blank=True,null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def username(self):
        return self.author.username + ""

    def __str__(self):
        return self.content[:50]
