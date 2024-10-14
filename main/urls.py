from django.urls import path
from . import views

urlpatterns = [
    path('', views.paginainicial, name='inicio'),  
    path('home/', views.home, name='home'),  
    path('cadastro/', views.cadastro, name='cadastro'), 
    path('login/', views.login, name='login'),  
    path('logout/', views.logout, name='logout'), 
    path('hidratacao/', views.hidratacao, name='hidratacao'),
    path('historicohidratacao/', views.historico_hidratacao, name='historicohidratacao'),
]
