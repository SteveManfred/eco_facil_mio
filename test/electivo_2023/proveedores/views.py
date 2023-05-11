from django.shortcuts import render, redirect
from .models import Proveedores, Detalle_orden, Compras
from .forms import ProveedoresForm
from django.shortcuts import render, redirect
import xlwt
import pandas as pd
from django.http import HttpResponse
from registration.models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render
from datetime import date
from productos.models import Producto
from reportlab.pdfgen import canvas


from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from django.http import HttpResponse

def generar_pdf1(request):
    detalles_orden = Detalle_orden.objects.all()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_compras.pdf"'
    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setTitle("Reporte de Compras")

    font_size = 12
    y = 700
    x = 50

    pdf.setFont('Helvetica-Bold', font_size)
    pdf.drawString(x, y, "Reporte de Compras")
    pdf.setFont('Helvetica', font_size)
    y -= font_size + 10

    pdf.drawString(x, y, "Producto")
    pdf.drawString(x + 100, y, "Cantidad")
    pdf.drawString(x + 200, y, "Precio")
    pdf.drawString(x + 300, y, "Subtotal")
    pdf.drawString(x + 400, y, "Descuento")
    pdf.drawString(x + 500, y, "Total")
    y -= font_size + 10

    total_compras = 0

    for detalle in detalles_orden:
        producto = detalle.producto.nombre
        cantidad = detalle.cantidad
        precio = detalle.precio
        sub_total = detalle.sub_total_detalle
        descuento = detalle.descuento_detalle
        total = detalle.total_detalle

        pdf.drawString(x, y, str(producto))
        pdf.drawString(x + 100, y, str(cantidad))
        pdf.drawString(x + 200, y, str(precio))
        pdf.drawString(x + 300, y, str(sub_total))
        pdf.drawString(x + 400, y, str(descuento))
        pdf.drawString(x + 500, y, str(total))
        y -= font_size + 2

    pdf.setFont('Helvetica', 10)


    pdf.showPage()
    pdf.save()

    request.session['redirigir_despues_de_descargar'] = True

    return response





def carga_masiva_proveedores(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    template_name = 'proveedores/carga_masiva_proveedores.html'
    return render(request, template_name, {'profiles': profiles})

@login_required
def carga_masiva_proveedores_save(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')

    if request.method == 'POST':
        try:
            data = pd.read_excel(request.FILES['customFile'])
        except KeyError:
            messages.add_message(request, messages.ERROR, 'Debe seleccionar un archivo')
            return redirect('carga_masiva_proveedores')
            
        df = pd.DataFrame(data)
        acc = 0
        for item in df.itertuples():
            nombre = str(item[1])
            direccion = str(item[2])    
            proveedor = Proveedores(nombre=nombre, direccion=direccion)
            proveedor.save()
            acc += 1
        messages.add_message(request, messages.SUCCESS, f'Carga masiva finalizada, se importaron {acc} registros')
        return redirect('carga_masiva_proveedores')

@login_required
def import_file_proveedores(request):
    profiles = Profile.objects.get(user_id=request.user.id)
    if profiles.group_id != 1:
        messages.add_message(request, messages.INFO, 'Intenta ingresar a una area para la que no tiene permisos')
        return redirect('check_group_main')
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="archivo_importacion.xls"'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('carga_masiva')
    row_num = 0
    columns = ['Nombre', 'Direccion']
    font_style = xlwt.XFStyle()
    font_style.font.bold = True
    for col_num in range(len(columns)):
        ws.write(row_num, col_num, columns[col_num], font_style)
    font_style = xlwt.XFStyle()
    date_format = xlwt.XFStyle()
    date_format.num_format_str = 'dd/MM/yyyy'
    for row in range(1):
        row_num += 1
        for col_num in range(2):
            if col_num == 0:
                ws.write(row_num, col_num, 'Nombre del producto', font_style)
            elif col_num == 1:
                ws.write(row_num, col_num, 'Direccion', font_style)
    wb.save(response)
    return response

def proveedores_main(request):
    total_proveedores = Proveedores.total_proveedores()
    return render(request, 'proveedores/proveedores_main.html', {'total_proveedores': total_proveedores})

def prueba(request, id=None):
    proveedores = Proveedores.objects.all()
    productos = Producto.objects.all()

    template_name = 'proveedores/prueba.html'
    detalle_orden = {}

    if request.method == "GET":
        compra = Compras.objects.filter(pk=id).first()

        if not compra:
            encabezado = {
                'id': 0,
                'proveedor': 0,
                'subTotal': 0,
                'descuento': 0,
                'total': 0
            }

            detalle_orden = None
        else:
            encabezado = {
                'id': compra.id,
                'proveedor': compra.proveedores,
                'subTotal': compra.sub_total,
                'descuento': compra.descuento,
                'total': compra.total
            }

            detalle_orden = Detalle_orden.objects.filter(compra=compra)

        context = {
            "compra": encabezado,
            "detallecompra": detalle_orden,
            "proveedores": proveedores,
            "productos": productos,
        }

        return render(request, template_name, context)

    if request.method == "POST":
        idProveedor = request.POST.get("proveedor")
        proveedor = Proveedores.objects.get(pk=idProveedor)

        if not id:
            compra = Compras(proveedores=proveedor)

            if compra:
                compra.save()

                id = compra.id
        else:
            compra = Compras.objects.filter(pk=id).first()

            if compra:
                compra.proveedores = proveedor

                compra.save()

        id_producto= request.POST.get("producto")
        cantidad = request.POST.get("cantidad")
        precio = request.POST.get("precio")
        producto = Producto.objects.get(id=id_producto)

        sub_total_detalle = float(cantidad) * float(precio)
        descuento_detalle = float(request.POST.get("descuentoDetalle", 0))
        total_detalle = sub_total_detalle - descuento_detalle

        detalle_orden = Detalle_orden(compra=compra, producto=producto, cantidad=cantidad, precio=precio, sub_total_detalle=sub_total_detalle, descuento_detalle=descuento_detalle, total_detalle=total_detalle)

        if detalle_orden:
            detalle_orden.save()

        compra = Compras.objects.filter(pk=id).first()
        encabezado = {
            'id': compra.id,
            'proveedor': compra.proveedores,
            'subTotal': compra.sub_total,
            'descuento': compra.descuento,
            'total': compra.total
        }

        detalle_orden = Detalle_orden.objects.filter(compra=compra)

        context = {
            "compra": encabezado,
            "detallecompra": detalle_orden,
            "proveedores": proveedores,
            "productos": productos,
        }

        return render(request, template_name, context)

    return render(request, template_name, {'proveedores': proveedores, 'productos': productos})


def ver_orden_compra(request, id):
    compra = Compras.objects.get(pk=id)
    detalles = Detalle_orden.objects.filter(compra=compra)
    context = {'compra': compra, 'detalles': detalles}
    return render(request, 'proveedores/ver_orden_compra.html', context) 

def eliminar_orden_compra(request,id):
    compra = Compras.objects.get(pk=id)
    compra.delete()
    return redirect("/proveedores/prueba/")

def proveedores_lista(request):
    q = request.GET.get('q')
    if q:
        proveedores_lista = Proveedores.objects.filter(nombre__icontains=q)
    else:
        proveedores_lista = Proveedores.objects.all()
    context = {'proveedores_lista': proveedores_lista}
    return render(request, "proveedores/proveedores_lista.html", context)


def proveedores_form(request,id=0):
    if request.method == "GET":
        if id ==0:
            form = ProveedoresForm()
        else:
            proveedores = Proveedores.objects.get(pk=id)
            form = ProveedoresForm(instance=proveedores)
        return render(request,"proveedores/proveedores_form.html",{'form':form})
    else:
        if id ==0 :
            form = ProveedoresForm(request.POST)
        else:
            proveedores = Proveedores.objects.get(pk=id)
            form = ProveedoresForm(request.POST,instance=proveedores)
        if form.is_valid():
            form.save()
        return redirect('/proveedores/list')

def proveedores_eliminar(request,id):
    proveedores = Proveedores.objects.get(pk=id)
    proveedores.delete()
    return redirect('/proveedores/list')

def proveedores_read(request, id):
    proveedores = Proveedores.objects.get(pk=id)
    context = {'proveedores': proveedores}
    return render(request, "proveedores/proveedores_read.html", context)
from reportlab.lib.pagesizes import letter


def generar_pdf(request):

    proveedores_lista = Proveedores.objects.all()
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_proveedores.pdf"'
    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.drawString(100, 750, "Reporte de Proveedores")

    pdf = canvas.Canvas(response, pagesize=letter)
    pdf.setTitle("Reporte de proveedores")


    font_size = 12
    y = 700
    x = 50

    pdf.setFont('Helvetica-Bold', font_size)
    pdf.drawString(x, y, "Reporte de Proveedores")
    pdf.setFont('Helvetica', font_size)
    y -= font_size + 10


    pdf.drawString(x, y, "Nombre")
    pdf.drawString(x + 150, y, "Dirección")
    y -= font_size + 10

    for proveedor in proveedores_lista:
        pdf.drawString(x, y, proveedor.nombre)
        pdf.drawString(x + 150, y, proveedor.direccion)
        y -= font_size + 2


    pdf.showPage()
    pdf.save()


    request.session['redirigir_despues_de_descargar'] = True

    return response
