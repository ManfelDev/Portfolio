from django.shortcuts import render, redirect
from datetime import date
from .models import Post
from .forms import ComentarioForm, RatingForm, PostForm, AutorForm

def posts_view(request):
    context = {
        'posts': Post.objects.all().order_by('-data')
    }
    return render(request, 'artigos/posts.html', context)

def post_view(request, post_id):
    post = Post.objects.get(id=post_id)
    comentarios = post.comentarios.filter(comentario_pai__isnull=True)
    ratings = post.ratings.all()
    comentario_form = ComentarioForm()
    rating_form = RatingForm()

    if request.method == 'POST':
        if 'submit_comentario' in request.POST:
            comentario_form = ComentarioForm(request.POST)
            if comentario_form.is_valid():
                comentario = comentario_form.save(commit=False)
                comentario.post = post
                comentario.data = date.today()
                pai_id = request.POST.get('comentario_pai')
                if pai_id:
                    comentario.comentario_pai_id = int(pai_id)
                comentario.save()
                return redirect('artigos:post_path', post_id=post.id)

        elif 'submit_rating' in request.POST:
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                rating = rating_form.save(commit=False)
                rating.post = post
                rating.save()
                return redirect('artigos:post_path', post_id=post.id)

    context = {
        'post': post,
        'comentarios': comentarios,
        'ratings': ratings,
        'comentario_form': comentario_form,
        'rating_form': rating_form,
    }

    return render(request, 'artigos/post.html', context)
    
def novo_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            return redirect('artigos:posts')
    else:
        form = PostForm()

    context = {
        'form': form,
    }
    return render(request, 'artigos/novo_post.html', context)
    
def novo_autor_view(request):
    if request.method == 'POST':
        form = AutorForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            return redirect('artigos:novo_post')
    else:
        form = AutorForm()

    context = {
        'form': form,
    }
    return render(request, 'artigos/novo_autor.html', context)
    
def edita_post_view(request, post_id):
    post = Post.objects.get(id=post_id)

    form = PostForm(request.POST or None, request.FILES or None, instance=post)

    if form.is_valid():
        form.save()

        return redirect('artigos:post_path', post_id=post.id)

    context = {
        'form': form,
        'post': post,
    }

    return render(request, 'artigos/edita_post.html', context)
    
def apaga_post_view(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('artigos:posts')
    
