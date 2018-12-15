from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import Http404
from django.contrib import messages
from random import randint
from .models import Post
from .forms import PostForm

# Create your views here.
def post_list(request):
    posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            # post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_list')

def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

def post_random_create(request):
    try:
        me=User.objects.get(username='admin')
        title=['ateam','flask','django','test','today','myhome','blog']
        for i in range(1,21):
            n=randint(0,6)
            Post.objects.create(author=me, title=title[n], text=str(i))
        messages.success(request, 'Create random post!!')
    except:
        pass
    return redirect('post_list')

# 공개 되지 않은 post를 filter로 걸러주고 그 데이터를 삭제한다.
def preview_remove(request):
    preview=Post.objects.filter(published_date__isnull=True)
    if len(preview) != 0:
        preview.delete()
        messages.success(request, 'Success deleted')
    else:
        messages.error(request, 'To delete a post, you must have one item.')
    return redirect('post_list')

# 공개 되지 않은 post까지 list에 나타나면 안되니까 filter로 걸러주고
# title의 중복을 제거한 결과를 보여줌
def post_deduplicate(request):
    posts=Post.objects.filter(published_date__isnull=False).order_by('published_date')
    title=set(posts[i].title for i in range(0,len(posts)))
    title_list=list()
    for i in title:
        title_list.append(posts.filter(title=i).first())
    return render(request, 'blog/post_set_list.html', {'posts':title_list})

def id_and_title(request):
    posts=Post.objects.filter(published_date__isnull=False).order_by('id')
    title_len=dict()
    for i in range(0,len(posts)):
        title_len[posts[i].id]=len(posts[i].title)
    id_title_sum=list()
    for k,v in title_len.items():
        id_title_sum.append(k+v)
    id_title_sum.sort()
    return render(request, 'blog/id_title.html', {'len':title_len, 'sum_list':id_title_sum})