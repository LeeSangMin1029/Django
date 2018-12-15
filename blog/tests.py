from django.test import TestCase
from blog.models import Post
from django.utils import timezone
from random import randint
from django.contrib.auth.models import User

# Create your tests here.
class PostSetCase(TestCase):
    def setUp(self):
        User.objects.create_superuser(username='admin', email='admin@admin.com', password='test')
        me=User.objects.get(username='admin')
        title=['ateam','flask','django','test','today','myhome','blog']
        for i in range(1,16):
            n=randint(0,6)
            Post.objects.create(author=me, title=title[n], text=str(i))
    
    def test_post_orderby(self):
        posts=Post.objects.order_by('id').filter(published_date__isnull=True)
        title_len=dict()
        for i in range(0,len(posts)):
            title_len[posts[i].id]=len(posts[i].title)
        k_v_sum=list()
        for k,v in title_len.items():
            k_v_sum.append(k+v)
        k_v_sum.sort()
        print(k_v_sum)