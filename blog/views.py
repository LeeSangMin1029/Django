from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.http import Http404
from django.contrib import messages
from .models import Post, Comment
from .forms import PostForm, CommentForm

# Create your views here.
def post_list(request):
    # 쿼리를 최적화하기 위해서 아래와 같이 설정해줬다.
    # 미리 필요한 데이터를 다 받아와서 템플릿으로 넘겼을 때 더 이상 쿼리가 발생하지 않도록 해줬다.
    posts=Post.objects.prefetch_related('comments').order_by('-created_date')
    return render(request, 'blog/post_list.html', {'posts':posts})

def post_detail(request, pk):
    # 각각의 pk에 해당되는 Post인스턴스를 불러온다. 만약 해당되는 Post가 없다면
    # 바로 페이지에서 에러를 일으킨다.
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post': post})

@login_required
def post_new(request):
    # 사용자가 데이터를 입력했을 때 그러니까
    # 저장버튼 save를 눌렀을 때 데이터를 보낸다.
    # 사용자가 보낸 요청의 형식이라고 해야하나..
    if request.method == "POST":
        # 그러면 폼에는 사용자가 입력한 데이터가 들어가게 된다.
        # request.POST에는 사용자가 입력한 데이터가 있다.
        form = PostForm(request.POST)
        # 폼에 입력한 데이터의 요소들을 검사한다. 맞으면 실행하고 아니면
        # 입력하라고 메시지를 띄워준다.
        if form.is_valid():
            # 해당 폼에 들어갈 데이터는 사용자가 다 입력을 했지만,
            # 로그인한 사용자의 정보도 필요하기 때문에 db에 저장하는 것을 지연시킨다.
            post = form.save(commit=False)
            # 해당 정보가 없으면 만약 admin이라는 유저에 대한
            # 정보가 없기 때문에 문제가 생긴다.
            post.author = request.user
            # 이제 필요한 정보가 저장되었으니, db에 저장시킨다.
            post.save()
            # 사용자가 저장한 정보를 보여주는 페이지로 이동한다.
            return redirect('post_detail', pk=post.pk)
    # 처음 글을 생성하려고 Add 버튼을 눌렀을 때 실행되는 조건문
    else:
        # 실행이 되면 빈 폼을 보여준다. 당연히 넘겨주는 데이터는 없다.
        form = PostForm()
    # 그렇게 되면 사용자가 폼에다가 데이터를 입력하기 전에 이미 함수는 실행이 된것이다.
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        # post_new함수와 비슷한데 두 번째 인수로 Post모델의 인스턴스를 넣어준다.
        # 수정하고 싶은 글의 내용을 불러와서 미리 넣어둔다.
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        # 이것도 마찬가지로 사용자가 입력한 데이터는 필요없고, 이전에 글을 만들 때
        # 입력한 데이터를 불러와서 미리 넣어둔다. 그럼 사용자는 해당 글을 수정하는 것처럼
        # 느낄 것이다.
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('post_list')

# 말씀하신대로 문자열만 출력되게 변경했습니다.
# 결과는 전과 같이 나오지만 좀 더 코드가 보기가 좋아졌습니다.
@login_required
def post_remove_duplicate_title(request):
    posts=Post.objects.select_related('author')
    title=set(i.title for i in posts)
    return render(request, 'blog/post_set_list.html', {'posts':title})

# id 별로 title 필드의 글자 수 출력
@login_required
def id_and_title(request):
    posts=Post.objects.select_related('author')
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
    posts=Post.objects.select_related('author')
    # 여기서 미리 title, id의 더한 값을 리스트로 변경한다.
    sum_list=list(i.id+len(i.title) for i in posts)
    # bubbleSort() 함수를 이용해서 오름차순으로 출력되게 만들어준다. 
    sum_list=bubbleSort(sum_list)
    return render(request, 'blog/sum_of_id_title.html', {'sum_list':sum_list})

@login_required
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
        for i in range(size-1):
            # 현재 요소가 다음 요소보다 크다면 서로 바꿔주는 함수 swap()을 호출
            if x[i] > x[i+1]:
                swap(x, i, i+1)
    return x