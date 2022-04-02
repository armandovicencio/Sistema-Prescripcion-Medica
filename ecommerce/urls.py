from django.urls import path     
from . import views_forms
from django.conf import settings
from django.conf.urls.static import static

app_name = 'ecommerce'

urlpatterns = [
    path('', views_forms.mainPage, name='mainPage' ),
    path('products/<str:size> ', views_forms.productBySize, name='productBySize'),
    path('products/<str:size>/<str:category> ', views_forms.productBySizeByCat, name='productBySizeByCat'),
    path('logout/', views_forms.logout, name='logout' ),
    path('products/addToShoppingCart/<int:id>', views_forms.addToShoppingCart, name='addToShoppingCart'),
    path('shoppingCart/empty', views_forms.shoppingCartempty, name='shoppingCartempty'),
    path('shoppingCart/', views_forms.shoppingCart, name='shoppingCart'),
    path('shoppingCart/buy', views_forms.buy, name='buy'),
    path('products/', views_forms.productGrid, name='productGrid'),

]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)