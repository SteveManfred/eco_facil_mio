from django.urls import path,include
from . import views

urlpatterns = [
    path('insert', views.productos_form,name='productos_insert'), # get and post req. for insert operation
    path('<int:id>/', views.productos_form,name='productos_update'), # get and post req. for update operation
    path('read/<int:id>/', views.productos_read,name='productos_read'),
    path('delete/<int:id>/',views.productos_eliminar,name='productos_delete'),
    path('list/',views.productos_lista,name='productos_list'), # get req. to retrieve and display all records
    path('',views.productos_main,name='productos_main'),
    path('carga_masiva_productos/',views.carga_masiva_productos, name='carga_masiva_productos'),
    path('import_file_productos/',views.import_file_productos,name="import_file_productos"),
    path('carga_masiva_productos_save/',views.carga_masiva_productos_save,name="carga_masiva_productos_save"),
    path('reporte_pdf/', views.generar_reporte_pdf, name='reporte_pdf'),
    
]

