from django.shortcuts import render, redirect
from .models import Insumos
from .forms import InsumosForm
from registration.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import xlwt
import pandas as pd
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO
from django.utils.translation import gettext as _

def carga_masiva_insumos(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'insumos/carga_masiva_insumos.html'
    return render(request, template_name, {'profiles': profiles})

@login_required
def carga_masiva_insumos_save(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    if request.method == 'POST':
        try:
            data = pd.read_excel(request.FILES['customFile'])
        except KeyError:
            messages.add_message(request, messages.ERROR, 'Debe seleccionar un archivo')
            return redirect('carga_masiva_insumos')
            
        df = pd.DataFrame(data)
        acc = 0
        for item in df.itertuples():
            nombre = str(item[1])
            cantidad = str(item[2])
            material = str(item[3])                
            insumo = Insumos(nombre=nombre, cantidad=cantidad, material=material)
            insumo.save()
            acc += 1
        messages.add_message(request, messages.SUCCESS, f'Carga masiva finalizada, se importaron {acc} registros')
        return redirect('carga_masiva_insumos')

@login_required
def import_file_insumos(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="archivo_importacion.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('carga_masiva')
    row_num = 0
    columns = ['Nombre', 'Cantidad', 'Material']
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/MM/yyyy'
    for row in range(1):
        row_num += 1
        for col_num in range(3):
            if col_num == 0:
                ws.write(row_num, col_num, 'Nombre del insumo', font_style)
            elif col_num == 1:
                ws.write(row_num, col_num, 'Cantidad disponible', font_style)
            elif col_num == 2:
                ws.write(row_num, col_num, 'Material del insumo', font_style)
    wb.save(response)
    return response    
def insumos_main(request):
    total_insumos = Insumos.total_insumos()
    return render(request, 'insumos/insumos_main.html', {'total_insumos': total_insumos})

def insumos_lista(request):
    q = request.GET.get('q')
    if q:
        insumos_lista = Insumos.objects.filter(nombre__icontains=q)
    else:
        insumos_lista = Insumos.objects.all()
    context = {'insumos_lista': insumos_lista}
    return render(request, "insumos/insumos_lista.html", context)

def insumos_form(request,id=0):
    if request.method == "GET":
        if id ==0:
            form = InsumosForm()
        else:
            insumos = Insumos.objects.get(pk=id)
            form = InsumosForm(instance=insumos)
        return render(request,"insumos/insumos_form.html",{'form':form})
    else:
        if id ==0 :
            form = InsumosForm(request.POST)
        else:
            insumos = Insumos.objects.get(pk=id)
            form = InsumosForm(request.POST,instance=insumos)
        if form.is_valid():
            form.save()
        return redirect('/insumos/list')

def insumos_eliminar(request,id):
    insumos = Insumos.objects.get(pk=id)
    insumos.delete()
    return redirect('/insumos/list')

def insumos_read(request, id):
    insumos = Insumos.objects.get(pk=id)
    context = {'insumos': insumos}
    return render(request, "insumos/insumos_read.html", context)

from django.http import HttpResponse
from reportlab.pdfgen import canvas
from io import BytesIO
from django.utils.translation import gettext as _

def generar_reporte_insumos(request):

    insumos_lista = Insumos.objects.all()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_insumos.pdf"'

    buffer = BytesIO()

    pdf = canvas.Canvas(buffer)

    # Encabezado del reporte
    pdf.drawString(100, 750, _("Reporte de Insumos"))

    # Encabezados de la tabla
    pdf.drawString(100, 700, _("Nombre"))
    pdf.drawString(250, 700, _("Cantidad"))
    pdf.drawString(400, 700, _("Material"))

    y = 680
    for insumo in insumos_lista:
        pdf.drawString(100, y, insumo.nombre)
        pdf.drawString(250, y, str(insumo.cantidad))
        pdf.drawString(400, y, insumo.material)
        y -= 20

    pdf.showPage()
    pdf.save()

    pdf = buffer.getvalue()
    buffer.close()

    response.write(pdf)

    return response

