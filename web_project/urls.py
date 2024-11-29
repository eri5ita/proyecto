"""
URL configuration for web_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path, include
from hello import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name = 'index'),
    path('activar-tema-a/', views.activar_tema_a, name='activar_tema_a'),
    path('activar-tema-o/', views.activar_tema_o, name='activar_tema_o'),
    path('quitar-tema/', views.quitar_tema, name='quitar_tema'),
    path('login/', views.user_login, name='login'),  # Vista de login
    path('logout/', views.user_logout, name='logout'), # Vista de logout
    path('Cuenta/', views.cuenta, name='micuenta'),
    path('Tienda/', views.tienda, name='tienda'),
    path('signup/', views.signup, name='signup'),
    path('completar_mision/<int:mision_id>/', views.completar_mision, name='completar_mision'),
    path('canjear_recompensa/<int:recompensa_id>/', views.canjear_recompensa, name='canjear_recompensa'),
]