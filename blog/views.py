from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import Http404
from django.contrib import messages
from random import randint
from .models import Post, Comment
from .forms import PostForm, CommentForm

# Create your views here.
def post_list(request):
    posts=Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
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

@login_required
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

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_list')

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_draft_list')

# 말씀하신대로 문자열만 출력되게 변경했습니다.
# 결과는 전과 같이 나오지만 좀 더 코드가 보기가 좋아졌습니다.
@login_required
def post_remove_duplicate_title(request):
    posts=Post.objects.filter(published_date__isnull=False).select_related('author')
    title=set(i.title for i in posts)
    return render(request, 'blog/post_set_list.html', {'posts':title})

# id 별로 title 필드의 글자 수 출력
@login_required
def id_and_title(request):
    posts=Post.objects.filter(published_date__isnull=False).select_related('author')
    # id와 title길이를 담을 딕셔너리
    i_and_t=dict()
    # 해당 id별로 title길이를 담는다.
    for i in posts:
        i_and_t[i.id]=str(len(i.title))
    return render(request, 'blog/id_and_title.html', {'len':i_and_t})

# id와 title문자열의 길이의 합을 구하는 함수
# 웹페이지에 오름차순으로 출력이 되야하는데 id 별로 된다...
@login_required
def sum_of_id_title(request):
    posts=Post.objects.filter(published_date__isnull=False).select_related('author')
    # 여기서 미리 title, id의 더한 값을 리스트로 변경한다.
    sum_list=list(i.id+len(i.title) for i in posts)
    # bubbleSort() 함수를 이용해서 오름차순으로 출력되게 만들어준다. 
    sum_list=bubbleSort(sum_list)
    return render(request, 'blog/sum_of_id_title.html', {'sum_list':sum_list})

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/edit_comment_to_post.html', {'form':form})

@login_required
def edit_comment_to_post(request, post_pk, pk):
    post = get_object_or_404(Post, pk=post_pk)
    comment = get_object_or_404(Comment, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/edit_comment_to_post.html', {'form':form})

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)

# 사용자 정의 함수
# 만약 x[i] 값이 x[i+1]의 값보다 크다면 바꿔주는 함수
def swap(x, i, j):
    x[i], x[j] = x[j], x[i]

# 값을 오름차순으로 정렬해주는 함수
def bubbleSort(x):
    # x(sum_list)의 길이만큼 반복하면서 0~(최대길이-2)의 값을 차례대로
    # size라는 변수에 하나씩 넣는다.
    for size in range(1, len(x)+1):
        # 
        for i in range(size-1):
            # 현재 요소가 다음 요소보다 크다면 서로 바꿔주는 함수 swap()을 호출
            if x[i] > x[i+1]:
                swap(x, i, i+1)
    return x