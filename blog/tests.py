from django.test import TestCase
from blog.models import Post
from django.utils import timezone
from random import randint
from django.contrib.auth.models import User
from django.db.models import Sum

# Create your tests here.
class PostSetCase(TestCase):
    def setUp(self):
        User.objects.create_superuser(username='admin', email='admin@admin.com', password='test')
        me=User.objects.get(username='admin')
        title=['ateam','flask','django','test','today','myhome','blog']
        for i in range(1,16):
            n=randint(0,6)
            Post.objects.create(author=me, title=title[n], text=str(i))
    
    def test(self):
        posts=Post.objects.select_related('author')
        
        