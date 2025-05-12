from django.shortcuts import render, redirect
from datetime import date
from .models import Projeto, Tecnologia
from .forms import ProjetoForm, FichaTecnicaForm, ImagemProjetoFormSet, TecnologiaForm, DisciplinaForm, DocenteForm

# Create your views here.
def index_view(request):
    context = {
        'data' : date.today().year
    }
    return render(request, "portfolio/index.html", context)

def sobre_view(request):
    context = {
        'data' : date.today().year
    }
    return render(request, "portfolio/sobre.html", context)

def interesses_view(request):
    context = {
        'data' : date.today().year
    }
    return render(request, "portfolio/interesses.html", context)

def projetos_view(request):
    context = {
        'data' : date.today().year,
        'projetos' : Projeto.objects.all(),
    }
    return render(request, 'portfolio/projetos.html', context)

def projeto_view(request, projeto_id):
    context = {
        'data' : date.today().year,
        'projeto' : Projeto.objects.get(id=projeto_id),
    }
    return render(request, 'portfolio/projeto.html', context)

def tecnologias_view(request):
    context = {
        'data' : date.today().year,
        'tecnologias' : Tecnologia.objects.all().order_by('id'),
    }
    return render(request, 'portfolio/tecnologias.html', context)

def tecnologia_view(request, tecnologia_id):
    context = {
        'data' : date.today().year,
        'tecnologia' : Tecnologia.objects.get(id=tecnologia_id),
    }
    return render(request, 'portfolio/tecnologia.html', context)

def cv_view(request):
    context = {
        'data' : date.today().year,
    }
    return render(request, 'portfolio/cv.html', context)

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
        'data': date.today().year
    }
    return render(request, 'portfolio/novo_projeto.html', context)

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
        'data': date.today().year
    }
    return render(request, 'portfolio/nova_tecnologia.html', context)

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
        'data': date.today().year
    }
    return render(request, 'portfolio/nova_disciplina.html', context)

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
        'data': date.today().year
    }
    return render(request, 'portfolio/novo_docente.html', context)

from django.contrib import messages  # Adicione se ainda não estiver no topo

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

            messages.success(request, "Projeto atualizado com sucesso!")
            return redirect('portfolio:projeto_path', projeto_id=projeto.id)

        else:
            # Mostra no terminal
            print("Formulários inválidos:")
            print("Erros do ProjetoForm:", projeto_form.errors)
            print("Erros do FichaTecnicaForm:", ficha_form.errors)
            print("Erros do ImagemProjetoFormSet:", imagem_formset.errors)

            # Mostra no template via messages (opcional, se usar messages no template)
            if projeto_form.errors:
                messages.error(request, f"Erros no formulário do projeto: {projeto_form.errors.as_text()}")
            if ficha_form.errors:
                messages.error(request, f"Erros na ficha técnica: {ficha_form.errors.as_text()}")
            if imagem_formset.errors:
                messages.error(request, f"Erros nas imagens: {imagem_formset.errors}")

    context = {
        'form': projeto_form,
        'ficha_form': ficha_form,
        'imagens': imagem_formset,
        'projeto': projeto,
        'data': date.today().year,
    }
    return render(request, 'portfolio/edita_projeto.html', context)

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
    }

    return render(request, 'portfolio/edita_tecnologia.html', context)

def apaga_projeto_view(request, projeto_id):
    projeto = Projeto.objects.get(id=projeto_id)
    projeto.delete()
    return redirect('portfolio:projetos')

def apaga_tecnologia_view(request, tecnologia_id):
    tecnologia = Tecnologia.objects.get(id=tecnologia_id)
    tecnologia.delete()
    return redirect('portfolio:tecnologias')


