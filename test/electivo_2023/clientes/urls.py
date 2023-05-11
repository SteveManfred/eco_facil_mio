from django.urls import path,include
from . import views

urlpatterns = [
    path('insert', views.clientes_form,name='clientes_insert'), # get and post req. for insert operation
    path('<int:id>/', views.clientes_form,name='clientes_update'), # get and post req. for update operation
    path('read/<int:id>/', views.clientes_read,name='clientes_read'),
    path('delete/<int:id>/',views.clientes_eliminar,name='clientes_delete'),
    path('list/',views.clientes_lista,name='clientes_list'), # get req. to retrieve and display all records
    path('',views.clientes_main,name='clientes_main'),
    #path('carga_masiva_clientes/',views.carga_masiva_clientes, name='carga_masiva_clientes'),
    #path('import_file_clientes/',views.import_file_clientes,name="import_file_clientes"),
    #path('carga_masiva_clientes_save/',views.carga_masiva_clientes_save,name="carga_masiva_clientes_save"),
    #path('generar_pdf_clientes/', views.generar_pdf_clientes, name='generar_pdf_clientes'),
]    