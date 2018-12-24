from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('drafts/', views.post_draft_list, name='post_draft_list'),
    path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
    path('post/<int:pk>/remove/', views.post_remove, name='post_remove'),
    path('post/create/', views.post_random_create, name='post_random_create'),
    path('preview/remove/', views.preview_remove, name='preview_remove'),
    path('post/remove_duplicate/list', views.post_remove_duplicate_title, name='post_remove_duplicate_title'),
    path('id_title/',views.id_and_title, name='id_and_title'),
    path('sum_list/',views.sum_of_id_title, name='sum_of_id_title'),
]