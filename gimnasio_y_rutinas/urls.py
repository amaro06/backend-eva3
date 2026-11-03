"""
URL configuration for gimnasio_y_rutinas project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from gestion_gimnasio import views as gestion_view
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name = 'login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page = 'home'), name='logout'),
    path('', gestion_view.home, name='home'),

    path('disciplinas/crear/', gestion_view.crear_disciplina, name='crear_disciplina'),
    path('disciplinas/editar/<int:pk>/', gestion_view.editar_disciplina, name='editar_disciplina'),
    path('disciplinas/eliminar/<int:pk>/', gestion_view.eliminar_disciplina, name='eliminar_disciplina'),
    path('disciplinas/', gestion_view.lista_disciplinas, name='lista_disciplinas'),
    path('etiquetas/crear/', gestion_view.crear_etiqueta, name='crear_etiqueta'),
    path('etiquetas/editar/<int:pk>/', gestion_view.editar_etiqueta, name='editar_etiqueta'),
    path('etiquetas/eliminar/<int:pk>', gestion_view.eliminar_etiqueta, name='eliminar_etiqueta'),

    path('rutinas/crear/', gestion_view.crear_rutina, name='crear_rutina'),
    path('rutinas/editar/<int:pk>/', gestion_view.editar_rutina, name='editar_rutina'),
    path('rutinas/eliminar/<int:pk>/', gestion_view.eliminar_rutina, name='eliminar_rutina'),
    path('rutinas/', gestion_view.lista_rutinas, name='lista_rutinas'),
    
]
