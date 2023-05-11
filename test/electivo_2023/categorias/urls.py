from django.urls import path,include
from . import views

urlpatterns = [
    path('insert', views.categorias_form,name='categorias_insert'), # get and post req. for insert operation
    path('<int:id>/', views.categorias_form,name='categorias_update'), # get and post req. for update operation
    path('read/<int:id>/', views.categorias_read,name='categorias_read'),
    path('delete/<int:id>/',views.categorias_eliminar,name='categorias_delete'),
    path('list/',views.categorias_lista,name='categorias_list'), # get req. to retrieve and display all records
    path('',views.categorias_main,name='categorias_main'),
    path('carga_masiva_categorias/',views.carga_masiva_categorias,name='carga_masiva_categorias'),
    path('import_file_categorias/',views.import_file_categorias,name="import_file_categorias"),
    path('carga_masiva_categorias_save/',views.carga_masiva_categorias_save,name="carga_masiva_categorias_save"),
]