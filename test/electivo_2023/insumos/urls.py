from django.urls import path,include
from . import views

urlpatterns = [
    path('insert', views.insumos_form,name='insumos_insert'), # get and post req. for insert operation
    path('<int:id>/', views.insumos_form,name='insumos_update'), # get and post req. for update operation
    path('read/<int:id>/', views.insumos_read,name='insumos_read'),
    path('delete/<int:id>/',views.insumos_eliminar,name='insumos_delete'),
    path('list/',views.insumos_lista,name='insumos_list'), # get req. to retrieve and display all records
    path('',views.insumos_main,name='insumos_main'),
    path('carga_masiva_insumos/',views.carga_masiva_insumos, name='carga_masiva_insumos'),
    path('import_file_insumos/',views.import_file_insumos,name="import_file_insumos"),
    path('carga_masiva_insumos_save/',views.carga_masiva_insumos_save,name="carga_masiva_insumos_save"),
    path('insumos_reporte_pdf/', views.generar_reporte_insumos, name='reporte_insumos_pdf'),
]