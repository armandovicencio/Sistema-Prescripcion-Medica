from django.urls import path
from . import views
urlpatterns = [
    path('prueba/<int:id>',views.render_pdf_view,name='reportes_prueba'),
    
    path('receta/<int:pk>', views.receta_pdf, name='receta_pdf'),
]
