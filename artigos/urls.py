from django.urls import path
from . import views

app_name = 'artigos'

urlpatterns = [
    path('posts/', views.posts_view, name='posts'),
    path('post/<int:post_id>/', views.post_view, name='post_path'),
    path('posts/novo', views.novo_post_view, name='novo_post'),
    path('autor/novo', views.novo_autor_view, name='novo_autor'),
    path('post/<int:post_id>/edita', views.edita_post_view, name='edita_post'),
    path('post/<int:post_id>/apaga', views.apaga_post_view, name='apaga_post'),
]