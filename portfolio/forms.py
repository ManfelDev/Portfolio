from django import forms
from django.forms import inlineformset_factory
from .models import Projeto, FichaTecnica, ImagemProjeto, Tecnologia, Disciplina, Docente
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class ProjetoForm(forms.ModelForm):
    class Meta:
        model = Projeto
        fields = '__all__'

        labels = {
            'titulo': 'Title',
            'descricao': 'Description',
            'link_itch': 'Link Itch.io',
            'link_github': 'Link GitHub',
            'link_video': 'Link Video',
            'aspetos_tecnicos': 'Technical Aspects',
            'conceitos_aplicados': 'Core Concepts',
            'disciplina': 'Course',
            'tecnologias': 'Technologies Used',
        }

class ImagemProjetoForm(forms.ModelForm):
    class Meta:
        model = ImagemProjeto
        fields = ('imagem', 'legenda')

        labels = {
            'imagem': 'Image',
            'legenda': 'Caption',
        }

ImagemProjetoFormSet = inlineformset_factory(
    Projeto,
    ImagemProjeto,
    form=ImagemProjetoForm,
    extra=3,
    max_num=3,
    can_delete=False,
)

class FichaTecnicaForm(forms.ModelForm):
    class Meta:
        model = FichaTecnica
        exclude = ['projeto']

        labels = {
            'plataforma': 'Platform',
            'duracao_desenvolvimento': 'Development Time',
            'equipa': 'Team Size',
        }

class TecnologiaForm(forms.ModelForm):
    class Meta:
        model = Tecnologia
        fields = '__all__'

        labels = {
            'nome': 'Name',
            'logotipo': 'Logo',
            'descricao': 'Description',
        }

class DisciplinaForm(forms.ModelForm):
    class Meta:
        model = Disciplina
        fields = '__all__'

        labels = {
            'nome': 'Name',
            'ano': 'Academic Year',
            'semestre': 'Semester',
            'docentes': 'Teachers',
            'link_moodle': 'Moodle Link',
            'link_pagina_ulusofona': 'ULusofona Link Page',
        }

class DocenteForm(forms.ModelForm):
    class Meta:
        model = Docente
        fields = '__all__'

        labels = {
            'nome': 'Name',
        }

class RegistoForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

        widgets = {
            'email': forms.EmailInput(attrs={'required': True}),
            'first_name': forms.TextInput(attrs={'required': True}),
            'last_name': forms.TextInput(attrs={'required': True}),
        }