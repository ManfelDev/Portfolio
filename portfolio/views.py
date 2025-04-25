from django.shortcuts import render
from datetime import date
from .models import Projeto, Tecnologia

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
        'projetos' : Projeto.objects.all().order_by('id'),
    }
    return render(request, 'portfolio/projetos.html', context)

def tecnologias_view(request):
    context = {
        'data' : date.today().year,
        'tecnologias' : Tecnologia.objects.all().order_by('id'),
    }
    return render(request, 'portfolio/tecnologias.html', context)

def cv_view(request):
    context = {
        'data' : date.today().year,
    }
    return render(request, 'portfolio/cv.html', context)