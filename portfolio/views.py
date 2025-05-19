from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from datetime import date
from .models import Projeto, Tecnologia, UserProfile
from .forms import ProjetoForm, FichaTecnicaForm, ImagemProjetoFormSet, TecnologiaForm, DisciplinaForm, DocenteForm, RegistoForm
from .utils import registar_visitante, envia_email
from django.db.models import Avg
import secrets

# Create your views here.
def index_view(request):
    context = {
        'data': date.today().year,
        'num_visitantes': registar_visitante(request),
    }
    return render(request, "portfolio/index.html", context)

def sobre_view(request):
    context = {
        'data' : date.today().year,
        'num_visitantes': registar_visitante(request),
    }
    return render(request, "portfolio/sobre.html", context)

def interesses_view(request):
    context = {
        'data' : date.today().year,
        'num_visitantes': registar_visitante(request),
    }
    return render(request, "portfolio/interesses.html", context)

def projetos_view(request):
    context = {
        'data' : date.today().year,
        'projetos' : Projeto.objects.all(),
        'num_visitantes': registar_visitante(request),
    }
    return render(request, 'portfolio/projetos.html', context)

def projeto_view(request, projeto_id):
    context = {
        'data' : date.today().year,
        'projeto' : Projeto.objects.get(id=projeto_id),
        'num_visitantes': registar_visitante(request),
    }
    return render(request, 'portfolio/projeto.html', context)

def tecnologias_view(request):
    context = {
        'data' : date.today().year,
        'tecnologias' : Tecnologia.objects.all().order_by('id'),
        'num_visitantes': registar_visitante(request),
    }
    return render(request, 'portfolio/tecnologias.html', context)

def tecnologia_view(request, tecnologia_id):
    context = {
        'data' : date.today().year,
        'tecnologia' : Tecnologia.objects.get(id=tecnologia_id),
        'num_visitantes': registar_visitante(request),
    }
    return render(request, 'portfolio/tecnologia.html', context)

def cv_view(request):
    context = {
        'data' : date.today().year,
        'num_visitantes': registar_visitante(request),
    }
    return render(request, 'portfolio/cv.html', context)

@login_required
def novo_projeto_view(request):
    if request.method == 'POST':
        projeto_form = ProjetoForm(request.POST, request.FILES)
        ficha_form = FichaTecnicaForm(request.POST)
        imagem_formset = ImagemProjetoFormSet(request.POST, request.FILES, prefix='imagens')

        if projeto_form.is_valid() and ficha_form.is_valid() and imagem_formset.is_valid():
            projeto = projeto_form.save()
            ficha = ficha_form.save(commit=False)
            ficha.projeto = projeto
            ficha.save()
            imagens = imagem_formset.save(commit=False)
            for imagem in imagens:
                imagem.projeto = projeto
                imagem.save()
            return redirect('portfolio:projetos')
    else:
        projeto_form = ProjetoForm()
        ficha_form = FichaTecnicaForm()
        imagem_formset = ImagemProjetoFormSet(prefix='imagens')

    context = {
        'form': projeto_form,
        'ficha_form': ficha_form,
        'imagens': imagem_formset,
        'data': date.today().year,
        'num_visitantes': registar_visitante(request),
    }
    return render(request, 'portfolio/novo_projeto.html', context)

@login_required
def nova_tecnologia_view(request):
    if request.method == 'POST':
        form = TecnologiaForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            return redirect('portfolio:tecnologias')
    else:
        form = TecnologiaForm()

    context = {
        'form': form,
        'data': date.today().year,
        'num_visitantes': registar_visitante(request),
    }
    return render(request, 'portfolio/nova_tecnologia.html', context)

@login_required
def nova_disciplina_view(request):
    if request.method == 'POST':
        form = DisciplinaForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            return redirect('portfolio:novo_projeto')
    else:
        form = DisciplinaForm()

    context = {
        'form': form,
        'data': date.today().year,
        'num_visitantes': registar_visitante(request),
    }
    return render(request, 'portfolio/nova_disciplina.html', context)

@login_required
def novo_docente_view(request):
    if request.method == 'POST':
        form = DocenteForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            return redirect('portfolio:nova_disciplina')
    else:
        form = DocenteForm()

    context = {
        'form': form,
        'data': date.today().year,
        'num_visitantes': registar_visitante(request),
    }
    return render(request, 'portfolio/novo_docente.html', context)

@login_required
def edita_projeto_view(request, projeto_id):
    projeto = Projeto.objects.get(id=projeto_id)
    ficha_tecnica = getattr(projeto, 'ficha_tecnica', None)

    projeto_form = ProjetoForm(request.POST or None, request.FILES or None, instance=projeto)
    ficha_form = FichaTecnicaForm(request.POST or None, instance=ficha_tecnica)
    imagem_formset = ImagemProjetoFormSet(request.POST or None, request.FILES or None, instance=projeto, prefix='imagens')

    if request.method == 'POST':
        if projeto_form.is_valid() and ficha_form.is_valid() and imagem_formset.is_valid():
            projeto = projeto_form.save()
            ficha = ficha_form.save(commit=False)
            ficha.projeto = projeto
            ficha.save()

            imagens = imagem_formset.save(commit=False)
            for imagem in imagens:
                imagem.projeto = projeto
                imagem.save()

            for obj in imagem_formset.deleted_objects:
                obj.delete()

            return redirect('portfolio:projeto_path', projeto_id=projeto.id)

    context = {
        'form': projeto_form,
        'ficha_form': ficha_form,
        'imagens': imagem_formset,
        'projeto': projeto,
        'data': date.today().year,
        'num_visitantes': registar_visitante(request),
    }
    return render(request, 'portfolio/edita_projeto.html', context)

@login_required
def edita_tecnologia_view(request, tecnologia_id):
    tecnologia = Tecnologia.objects.get(id=tecnologia_id)

    form = TecnologiaForm(request.POST or None, request.FILES or None, instance=tecnologia)

    if form.is_valid():
        form.save()

        return redirect('portfolio:tecnologia_path', tecnologia_id=tecnologia.id)

    context = {
        'form': form,
        'tecnologia': tecnologia,
        'data': date.today().year,
        'num_visitantes': registar_visitante(request),
    }

    return render(request, 'portfolio/edita_tecnologia.html', context)

@login_required
def apaga_projeto_view(request, projeto_id):
    projeto = Projeto.objects.get(id=projeto_id)
    projeto.delete()
    return redirect('portfolio:projetos')

@login_required
def apaga_tecnologia_view(request, tecnologia_id):
    tecnologia = Tecnologia.objects.get(id=tecnologia_id)
    tecnologia.delete()
    return redirect('portfolio:tecnologias')

#################################### Login ########################################

def registo_view(request):
    form = RegistoForm(request.POST or None)

    if form.is_valid():
        form.save()
        return redirect('portfolio:login')

    context = {
        'form': form,
        'data': date.today().year,
        'num_visitantes': registar_visitante(request),
    }
    return render(request, 'portfolio/registo.html', context)

@login_required
def user_view(request):
    context = {
        'data': date.today().year,
        'num_visitantes': registar_visitante(request),
    }
    return render(request, 'portfolio/user.html', context)

def login_view(request):
    context = {
        'data': date.today().year,
        'num_visitantes': registar_visitante(request),
    }

    if request.user.is_authenticated:
        return render(request, 'portfolio/user.html', context)

    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST.get('username'),
            password=request.POST.get('password')
        )
        if user:
            login(request, user)
            return render(request, 'portfolio/index.html', context)
        else:
            context['mensagem'] = 'Credenciais inválidas'
            return render(request, 'portfolio/login.html', context)

    return render(request, 'portfolio/login.html', context)

def logout_view(request):
    logout(request)

    return redirect('portfolio:index')

def login_magic_link(request):
    email = request.GET.get('email')

    if User.objects.filter(email=email).exists():
        user = User.objects.get(email=email)
        profile, created = UserProfile.objects.get_or_create(user=user)

        profile.token = secrets.token_urlsafe(32)
        profile.save()

        envia_email(user, email, profile.token)

        return render(request, 'portfolio/login.html', {
            'mensagem': 'Email sent.'
        })

    else:
        return render(request, 'portfolio/login.html', {
            'mensagem': 'This email address is not registered.'
        })

def autentica_view(request):
    token = request.GET.get('token')
    if token:
        try:
            profile = UserProfile.objects.get(token=token)
            user = profile.user
            user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, user)
            profile.token = None
            profile.save()
            return redirect('portfolio:index')

        except UserProfile.DoesNotExist:
            return render(request, 'portfolio/login.html', {
                'mensagem': 'Invalid or expired link.',
                'data': date.today().year,
                'num_visitantes': registar_visitante(request),
            })
    else:
        return render(request, 'portfolio/login.html', {
            'mensagem': 'Token not supplied.',
            'data': date.today().year,
            'num_visitantes': registar_visitante(request),
        })

#################################### Artigos ########################################

from artigos.models import Post
from artigos.forms import ComentarioForm, RatingForm, PostForm, AutorForm

def posts_view(request):
    context = {
        'posts': Post.objects.all().order_by('-data'),
        'data': date.today().year,
        'num_visitantes': registar_visitante(request),
    }
    return render(request, 'portfolio/posts.html', context)

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
                return redirect('portfolio:post_path', post_id=post.id)

        elif 'submit_rating' in request.POST:
            rating_form = RatingForm(request.POST)
            if rating_form.is_valid():
                rating = rating_form.save(commit=False)
                rating.post = post
                rating.save()
                return redirect('portfolio:post_path', post_id=post.id)

    media_rating = ratings.aggregate(avg=Avg('pontuacao'))['avg'] or 0
    total_ratings = ratings.count()

    context = {
        'post': post,
        'comentarios': comentarios,
        'ratings': ratings,
        'media_rating': round(media_rating, 2),
        'total_ratings': total_ratings,
        'comentario_form': comentario_form,
        'rating_form': rating_form,
        'data': date.today().year,
        'num_visitantes': registar_visitante(request),
    }

    return render(request, 'portfolio/post.html', context)


@login_required
def novo_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('portfolio:posts')
    else:
        form = PostForm()

    context = {
        'form': form,
        'data': date.today().year,
        'num_visitantes': registar_visitante(request),
    }
    return render(request, 'portfolio/novo_post.html', context)

@login_required
def novo_autor_view(request):
    if request.method == 'POST':
        form = AutorForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()
            return redirect('portfolio:novo_post')
    else:
        form = AutorForm()

    context = {
        'form': form,
        'data': date.today().year,
        'num_visitantes': registar_visitante(request),
    }
    return render(request, 'portfolio/novo_autor.html', context)

@login_required
def edita_post_view(request, post_id):
    post = Post.objects.get(id=post_id)
    form = PostForm(request.POST or None, request.FILES or None, instance=post)

    if form.is_valid():
        form.save()
        return redirect('portfolio:post_path', post_id=post.id)

    context = {
        'form': form,
        'post': post,
        'data': date.today().year,
        'num_visitantes': registar_visitante(request),
    }

    return render(request, 'portfolio/edita_post.html', context)

@login_required
def apaga_post_view(request, post_id):
    post = Post.objects.get(id=post_id)
    post.delete()
    return redirect('portfolio:posts')