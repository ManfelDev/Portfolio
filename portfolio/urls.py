from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    path('index/', views.index_view, name = 'index'),
    path('sobre/', views.sobre_view, name = 'sobre'),
    path('interesses/', views.interesses_view, name = 'interesses'),
    path('projetos/', views.projetos_view, name = 'projetos'),
    path('tecnologias/', views.tecnologias_view, name = 'tecnologias'),
]