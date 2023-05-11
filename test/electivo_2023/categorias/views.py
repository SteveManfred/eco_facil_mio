from django.shortcuts import render, redirect
from .models import Categorias
from .forms import CategoriasForm
from registration.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import xlwt
import pandas as pd
from django.shortcuts import render, redirect
from django.http import HttpResponse


def carga_masiva_categorias(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    template_name = 'categorias/carga_masiva_categorias.html'
    return render(request, template_name, {'profiles': profiles})


@login_required
def carga_masiva_categorias_save(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    if request.method == 'POST':
        try:
            data = pd.read_excel(request.FILES['customFile'])
            df = pd.DataFrame(data)
            acc = 0
            for item in df.itertuples():
                nombre = str(item[1])
                categoria = Categorias(nombre=nombre)
                categoria.save()
                acc += 1
            messages.add_message(request, messages.INFO, f'Carga masiva finalizada, se importaron {acc} registros')
            return redirect('carga_masiva_categorias')
        except Exception as e:
            messages.add_message(request, messages.ERROR, f'Error en la carga masiva: {str(e)}')
            return redirect('carga_masiva_categorias')
    else:

        return render(request, 'categorias/carga_masiva_categorias.html')


@login_required
def import_file_categorias(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="archivo_importacion.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('carga_masiva')
    row_num = 0
    columns = ['Nombre']
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    for row in range(1):
        row_num += 1
        for col_num in range(1):
            if col_num == 0:
                ws.write(row_num, col_num, 'Nombre de la categoría', font_style)
    wb.save(response)
    return response


def categorias_main(request):
    total_categorias = Categorias.total_categorias()
    return render(request, 'categorias/categorias_main.html', {'total_categorias': total_categorias})

def categorias_lista(request):
    q = request.GET.get('q')
    if q:
        categorias_lista = Categorias.objects.filter(nombre__icontains=q)
    else:
        categorias_lista = Categorias.objects.all()
    context = {'categorias_lista': categorias_lista}
    return render(request, "categorias/categorias_lista.html", context)

def categorias_form(request,id=0):
    if request.method == "GET":
        if id ==0:
            form = CategoriasForm()
        else:
            categorias = Categorias.objects.get(pk=id)
            form = CategoriasForm(instance=categorias)
        return render(request,"categorias/categorias_form.html",{'form':form})
    else:
        if id ==0 :
            form = CategoriasForm(request.POST)
        else:
            categorias = Categorias.objects.get(pk=id)
            form = CategoriasForm(request.POST,instance=categorias)
        if form.is_valid():
            form.save()
        return redirect('/categorias/list')

def categorias_eliminar(request,id):
    categorias = Categorias.objects.get(pk=id)
    categorias.delete()
    return redirect('/categorias/list')

def categorias_read(request, id):
    categorias = Categorias.objects.get(pk=id)
    context = {'categorias': categorias}
    return render(request, "categorias/categorias_read.html", context)

