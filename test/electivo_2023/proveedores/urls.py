from django.urls import path,include
from . import views

urlpatterns = [
    path('insert', views.proveedores_form,name='proveedores_insert'), # get and post req. for insert operation
    path('<int:id>/', views.proveedores_form,name='proveedores_update'), # get and post req. for update operation
    path('read/<int:id>/', views.proveedores_read,name='proveedores_read'),
    path('delete/<int:id>/',views.proveedores_eliminar,name='proveedores_delete'),
    path('list/',views.proveedores_lista,name='proveedores_list'), # get req. to retrieve and display all records
    path('',views.proveedores_main,name='proveedores_main'),
    path('carga_masiva_proveedores/',views.carga_masiva_proveedores, name='carga_masiva_proveedores'),
    path('import_file_proveedores/',views.import_file_proveedores,name="import_file_proveedores"),
    path('carga_masiva_proveedores_save/',views.carga_masiva_proveedores_save,name="carga_masiva_proveedores_save"),
    path('prueba/',views.prueba,name="prueba"),
    path('generar_pdf/', views.generar_pdf, name='generar_pdf'),
    path('ver_orden_compra/<int:id>/',views.ver_orden_compra,name="ver_orden_compra"),
    path('eliminar_orden_compra/<int:id>/',views.eliminar_orden_compra,name="eliminar_orden_compra"),
    path('generar_pdf1/', views.generar_pdf1, name='generar_pdf1'),
    
]