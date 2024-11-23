from django.urls import path
from . import views

urlpatterns = [
    #path("", views.home, name="home"),
    path("", views.lista_misiones, name="lista_misiones"),
    path('completar_mision/<int:mision_id>/', views.completar_mision, name='completar_mision'),
]
