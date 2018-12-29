from django.db import models
from django.utils import timezone


class Post(models.Model):
    # 다른 모델에 대한 링크를 의미한다.
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    # 글자 수가 제한된 텍스트를 정의할 때 사용한다.
    title = models.CharField(max_length=200)
    # 글자 수에 제한이 없는 긴 텍스트를 위한 속성이다.
    text = models.TextField()
    # 날짜와 시간을 의미하는 필드
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    # related_name은 Post 모델에서 댓글 목록(Comment)에 접근하기 위한 이름이다.
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.text