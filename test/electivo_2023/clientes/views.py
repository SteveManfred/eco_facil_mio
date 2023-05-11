from django.shortcuts import render, redirect
from .models import Clientes
from .forms import ClientesForm

def clientes_main(request):
    total_clientes = Clientes.total_clientes()
    return render(request, 'clientes/clientes_main.html', {'total_clientes': total_clientes})

def clientes_lista(request):
    q = request.GET.get('q')
    if q:
        clientes_lista = Clientes.objects.filter(nombre__icontains=q)
    else:
        clientes_lista = Clientes.objects.all()
    context = {'clientes_lista': clientes_lista}
    return render(request, "clientes/clientes_lista.html", context)


def clientes_form(request,id=0):
    if request.method == "GET":
        if id ==0:
            form = ClientesForm()
        else:
            clientes = Clientes.objects.get(pk=id)
            form = ClientesForm(instance=clientes)
        return render(request,"clientes/clientes_form.html",{'form':form})
    else:
        if id ==0 :
            form = ClientesForm(request.POST)
        else:
            clientes = Clientes.objects.get(pk=id)
            form = ClientesForm(request.POST,instance=clientes)
        if form.is_valid():
            form.save()
        return redirect('/clientes/list')

def clientes_eliminar(request,id):
    clientes = Clientes.objects.get(pk=id)
    clientes.delete()
    return redirect('/clientes/list')

def clientes_read(request, id):
    clientes = Clientes.objects.get(pk=id)
    context = {'clientes': clientes}
    return render(request, "clientes/clientes_read.html", context)