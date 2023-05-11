from django.shortcuts import render
from django.conf import settings #importa el archivo settings
from django.contrib import messages #habilita la mesajería entre vistas
from django.contrib.auth.decorators import login_required #habilita el decorador que se niega el acceso a una función si no se esta logeado
from django.contrib.auth.models import Group, User # importa los models de usuarios y grupos
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator #permite la paqinación
from django.db.models import Avg, Count, Q #agrega funcionalidades de agregación a nuestros QuerySets
from django.http import (HttpResponse, HttpResponseBadRequest,
                         HttpResponseNotFound, HttpResponseRedirect) #Salidas alternativas al flujo de la aplicación se explicará mas adelante
from django.shortcuts import redirect, render #permite renderizar vistas basadas en funciones o redireccionar a otras funciones
from django.template import RequestContext # contexto del sistema
from django.views.decorators.csrf import csrf_exempt #decorador que nos permitira realizar conexiones csrf

from registration.models import Profile #importa el modelo profile, el que usaremos para los perfiles de usuarios


def home(request):
    return render(request, 'core/home.html')


@login_required
def pre_check_profile(request):
    #por ahora solo esta creada pero aún no la implementaremos
    pass

@login_required
def check_profile(request):  
    try:
        profile = Profile.objects.get(user=request.user)
    except Profile.DoesNotExist:
        messages.add_message(request, messages.INFO, 'No se encontró un perfil asociado a su usuario.')
        return redirect('logout')
    except Exception as e:
        print(f"Hubo un error al obtener el perfil del usuario: {e}")
        messages.add_message(request, messages.INFO, 'Hubo un error al obtener su perfil, por favor contacte a los administradores')
        return redirect('logout')

    if profile.group_id == 1:        
        return redirect('admin_main')
    elif profile.group_id == 0:
        return redirect('home')
    else:
        return redirect('logout')


