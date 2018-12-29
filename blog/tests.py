from django.test import TestCase
from blog.models import Post, Comment
from django.utils import timezone
from random import randint
from django.contrib.auth.models import User

# Create your tests here.
class ModelSetCase(TestCase):
    def setUp(self):
        User.objects.create_superuser(username='admin', email='admin@admin.com', password='test')
        me=User.objects.get(username='admin')
        title=['ateam','flask','django','test','today','myhome','blog']
        comments=['sdfsdf','sdfsdfddfd','hello my name is sangmin','what \'s your name?']
        for i in range(1,6):
            ti=randint(0,6)
            Post.objects.create(author=me, title=title[ti], text=str(i))
        
        posts=Post.objects.select_related('author')
        for i in range(1,len(posts)+1):
            post=posts.get(pk=i)
            for j in range(1,4):
                co=randint(0,3)
                Comment.objects.create(post=post, author='sang', text=comments[co])
    def test(self):
        pass