from django.urls import path
from . import views

urlpatterns = [
    path('', views.paginainicial, name='inicio'),  
    path('home/', views.home, name='home'),  
    path('cadastro/', views.cadastro, name='cadastro'), 
    path('login/', views.login_view, name='login'),  
    path('logout/', views.logout, name='logout'), 
    path('hidratacao/', views.hidratacao, name='hidratacao'),
    path('historicohidratacao/', views.historico_hidratacao, name='historicohidratacao'),
    path('meupeso/', views.calculo_imc, name='meupeso'),
    path('adicionartreino/', views.adicionar_treino, name='adicionartreino'),  
    path('meustreinos/', views.ver_treinos, name='meustreinos'), 
    path('remover-treino/<int:treino_id>/', views.remover_treino, name='remover_treino'),
    path('alongamento/', views.alongamento, name='alongamento'), 
    path('tecnicaspbemestar/', views.tecnicaspbemestar, name='tecnicaspbemestar'),  
    path('sentimento/', views.sentimento, name='sentimento'), 
    path('respiracaoguiada/', views.respiracaoguiada, name='respiracaoguiada'),  
    path('relaxamentomuscular/', views.relaxamentomuscular, name='relaxamentomuscular'), 
    path('historicohumor/', views.historico_humor, name='historicohumor'),
    path('saude/', views.saude, name='saude'),
    path('registrosaude/', views.registrosaude, name='registrosaude'),
    path('sono/', views.sono, name='sono'),
    path('horassono/', views.horassono, name='horassono'),
    path('alimentacao/', views.alimentacao_view, name='alimentacao'),
    path('veralimentacao/', views.veralimentacao_view, name='veralimentacao'),
]
