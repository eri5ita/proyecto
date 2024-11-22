from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpRequest
from .models import misiones, recompensas
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import CustomUserCreationForm


# Homepage
def index(request):
    tareas = misiones.objects.all()  # Obtén todas las misiones de la base de datos
    return render(request, 'index.html', {'tareas': tareas})
    # Verificar si el tema está activado en la sesión
    tema_activado = request.session.get('tema_activado', None)
    return render(request, 'index.html', {'tema_activado': tema_activado})

# Tienda
def tienda(request):
    tema_activado = request.session.get('tema_activado', None)
    productos = ['Producto 1', 'Producto 2', 'Producto 3']
    return render(request, 'tienda.html', {'tema_activado': tema_activado, 'productos': productos})

# Mi cuenta
def cuenta(request):
    tema_activado = request.session.get('tema_activado', False)
    return render(request, 'cuenta.html', {'tema_activado': tema_activado})

# signup


def signup(request):

    if request.method == 'GET':
        print('s')
        return render (request, 'signup.html', {'form': UserCreationForm})
        
    else:
        print('p')
        if request.POST['password1'] == request.POST['password2']:
            try: 
                user = User.objects.create_user(username=request.POST['username'],
                password=request.POST['password1'], email=request.POST['email'])
                user.save()
                return redirect('index')
            except IntegrityError :
                return HttpResponse('User ya existente')
        return HttpResponse ('password do not match')
   
    

# Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')  # Redirige a la página principal después de iniciar sesión
        else:
            return render(request, 'login.html', {'error': 'Credenciales inválidas'})
    return render(request, 'login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('index')  # Redirige a la página principal después de cerrar sesión

# Vista para activar el tema
def activar_tema_a(request):
    # Activar el tema y guardarlo en la sesión
    request.session['tema_activado'] = 'tema_a'
    return redirect('tienda')  # Redirige a la página principal

def activar_tema_o(request):
    # Activar el tema y guardarlo en la sesión
    request.session['tema_activado'] = 'tema_o'
    return redirect('tienda')  # Redirige a la página principal

# Vista para quitar el tema
def quitar_tema(request):
    # Eliminar el tema de la sesión
    if 'tema_activado' in request.session:
        del request.session['tema_activado']
    return redirect('tienda')  # Redirige a la página principal

#def home(request):
    #return HttpResponse("Schmoll baby so cute!")

# Create your views here.
#def hello_there(request, name):
    #print(request.build_absolute_uri()) #optional
    #return render(
        #request,
        #'hello/hello_there.html',
        #{
            #'name': name,
            #'date': datetime.now()
        #}
    #)
