from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse, HttpRequest
from .models import misiones, recompensas, mision_completada, UsuarioLeafpoints, RecompensaComprada
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import CustomUserCreationForm
from django.contrib import messages


# Homepage
def index(request):
    if request.user.is_authenticated:  
        # Para mostrar misiones
        tareas=misiones.objects.all()
        misiones_c = mision_completada.objects.filter(usuario=request.user, completada=True).values_list('mision', flat=True)
        misiones_d = tareas.exclude(id__in=misiones_c)
        
        # Para controlar temas
        tema_activado = request.session.get('tema_activado', None)
        
        #Obtener el usuario actual
        user = request.user
        # Verificar si el usuario tiene un registro de leafpoints asociado
        usuario_leafpoints = user.usuarioleafpoints
        leafpoints = usuario_leafpoints.total_leafpoints
        
        return render(request, 'index.html', {'tareas': misiones_d, 'tema_activado':tema_activado, 'leafpoints':leafpoints})
    else:
        return redirect('login')

# Tienda
def tienda(request):
    tema_activado = request.session.get('tema_activado', None)
    productos = ['Producto 1', 'Producto 2', 'Producto 3']
    usuario = request.user  # Usuario actual
    recompensa_id = 3  # ID fijo para esta recompensa (ajústalo si es dinámico)
    comprada = RecompensaComprada.objects.filter(usuario=usuario, recompensa_id=recompensa_id).exists()
    #Obtener el usuario actual
    user = request.user
    # Verificar si el usuario tiene un registro de leafpoints asociado
    usuario_leafpoints = user.usuarioleafpoints
    leafpoints = usuario_leafpoints.total_leafpoints
    return render(request, 'tienda.html', {'tema_activado': tema_activado, 'productos': productos, 'comprada': comprada, 'leafpoints':leafpoints})

# Mi cuenta
def cuenta(request):
    tema_activado = request.session.get('tema_activado', False)
    #Obtener el usuario actual
    user = request.user
    # Verificar si el usuario tiene un registro de leafpoints asociado
    usuario_leafpoints = user.usuarioleafpoints
    leafpoints = usuario_leafpoints.total_leafpoints
    return render(request, 'cuenta.html', {'tema_activado': tema_activado, 'leafpoints': leafpoints})

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

def completar_mision(request, mision_id):
    # Buscar la misión por ID
    mision = get_object_or_404(misiones, id=mision_id)

    #Obtener el usuario actual
    user = request.user
    
    # Verificar si el usuario tiene un registro de leafpoints asociado
    usuario_leafpoints = user.usuarioleafpoints
    
    mision_lista = mision_completada.objects.filter(usuario=request.user, mision=mision).first()

    if not mision_lista:
        mision_lista = mision_completada(usuario=request.user, mision=mision, completada=False)
        mision_lista.save()
    
    if not mision_lista.completada:
        mision_lista.completada = True
        mision_lista.save()
        
    # Sumar los leafpoints al usuario
    usuario_leafpoints.total_leafpoints += mision.leafpoints
    usuario_leafpoints.save()  # Guardar los cambios

    # Mostrar un mensaje de éxito
    messages.success(request, f"¡Has completado la misión '{mision.titulo}' y ganado {mision.leafpoints} leafpoints!")

    # Redirigir de vuelta al listado de misiones
    return redirect('index')  # O la URL que prefieras

def canjear_recompensa(request, recompensa_id):
    # Obtener la recompensa
    recompensa = get_object_or_404(recompensas, id=recompensa_id)
    usuario = request.user
    
    #Obtener el usuario actual
    user = request.user
    
    # Verificar si el usuario tiene un registro de leafpoints asociado
    usuario_leafpoints = user.usuarioleafpoints
    
    if usuario_leafpoints.total_leafpoints >= recompensa.costo_lp:
        # Descontar los LeafPoints del usuario
        usuario_leafpoints.total_leafpoints -= recompensa.costo_lp
        usuario_leafpoints.save()

        # Registrar el canje en RecompensaComprada
        RecompensaComprada.objects.create(
            usuario=usuario,
            recompensa=recompensa,
            comprada=True
        )
        
    return redirect('tienda')
    

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
