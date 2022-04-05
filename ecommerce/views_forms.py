import decimal
from email.policy import default
from logging import raiseExceptions
from operator import is_
from wsgiref.validate import validator
from django import forms
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib import messages
from .models import BoletaDetalle, Boleta
from django.db.models import Count
from pharmacy.models import CustomUser, Product, DosageForm
import re
from datetime import date
from django.db.models import Q,Sum


class ProductForm(forms.ModelForm):

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        length = len(first_name)
        if length <= 1:
            print(length)
            raise forms.ValidationError(
                    f'El nombre debe tener por lo menos 2 caracteres',
                )
        if length == 0:
            print(length)
            raise forms.ValidationError(
                    f'Nombre requerido',
                )
        return first_name


    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        length = len(last_name)

        if length <= 1:
            print(length)
            raise forms.ValidationError(
                    f'El apellido debe tener por lo menos 2 caracteres',
                )
        return last_name

    class Meta:

        model = Product
        fields = ['name', 'dci', 'tradename', 'dose', 'description', 'price', 'img', 'stock', 'dosageForm', 'valid_to' ]

        labels = {
            'name':'Nombre:',
            'dci':'Nombre Cientifico:',
            'tradename': 'Marca Comercial:',
            'dose': 'Dosis:',
            'description': 'Descripcion:',
            'price': 'Precio:',
            'img': 'Subir Imagen:',
            'stock': 'Stock:',
            'dosageForm': 'Forma Farmaceutica:',
            'valid_to': 'Fecha de Vencimiento:',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'dci': forms.TextInput(attrs={'class': 'form-control'}),
            'tradename': forms.TextInput(attrs={'class': 'form-control'}),
            'dose': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control'}),
            'price':forms.TextInput(attrs={'class': 'form-control'}),
            'img':forms.FileInput(attrs={'class': 'form-control'}),
            'stock':forms.TextInput(attrs={'class': 'form-control'}),
            'dosageForm':forms.Select(attrs={'class': 'form-control'}),
            'valid_to': forms.DateInput(attrs={'class': 'form-control', 'type':'date'}),


        }

class DosageFormForm(forms.ModelForm):

    def clean_name(self):
        name = self.cleaned_data['name']
        length = len(name)
        if length < 3:
            print(length)
            raise forms.ValidationError(
                    f'El nombre debe tener por lo menos 3 caracteres',
                )
        if length == 0:
            print(length)
            raise forms.ValidationError(
                    f'Nombre requerido',
                )
        return name

    class Meta:

        model = DosageForm
        fields = ['name']

        labels = {
            'name':'Nombre:',
        }

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
        }        

##### Metodos ###########


def logout(request):
    if 'usuario' in request.session:
        del request.session['usuario']
    return redirect('/')

def mainPage(request):
    if request.method == 'GET':
        productos = Product.objects.all()


        if 'usuario' in request.session:
            boletaid = Boleta.objects.filter(users = request.session['usuario']['id'], pagado = False).last()
            print(boletaid)
            cart = BoletaDetalle.objects.filter(usuario = request.session['usuario']['id'], boleta = boletaid)
            print(cart)
        else:
            cart = 0
        contexto = {
            'productos': productos,
            'cart':cart,
            }
        return render(request, 'ecommerce/mainPage.html', contexto)

def productGrid(request):
    if request.method == 'GET':
        allProduct = Product.objects.all()
        allProductCount = Product.objects.all().count()
        allCategories = DosageForm.objects.all()
        category1 = Product.objects.filter(dosageForm = 0)
        contexto={
            'productos':allProduct,
            'categories':allCategories,
            'allProductCount':allProductCount,

        }
    return render(request, 'ecommerce/products.html', contexto)

def productGridByCat(request, category):
    if request.method == 'GET':
        allProductCount = Product.objects.all().count()
        categories = DosageForm.objects.all()
        for cat in categories:
            if cat.name == category:
                filterProducts = Product.objects.filter(dosageForm = cat.id)
        contexto={
            'productos': filterProducts,
            'categories':categories,
            'allProductCount':allProductCount,

        }
    return render(request, 'ecommerce/products.html', contexto)

def productBySize(request, size):
    if request.method == 'GET':
        cat = DosageForm.objects.all()
        contexto = {
            'size':size,
            'categories':cat,
        }

        return render(request, 'ecommerce/productBySize.html', contexto)

#def productBySizeByCat(request, size, category):
#    prod = Product.objects.filter(size__in=size)
#    if request.method == 'GET':
#        print(size)
#        print(category)
#        prod = Product.objects.filter(prodCat__name= category).filter(size__contains=size)
#        contexto = {
#            'size':size,
#            'category':category,
#            'products':prod,
#        }
#        print(prod)
#        return render(request, 'ecommerce/productBySizeByCat.html', contexto)

subtotal = 0
descuento = 0
opGravada = 0
igv = 0.18
precioEnvio = 0

def addToShoppingCart(request, id):
    
    if request.method == 'POST':
        user = CustomUser.objects.get(id = request.session['usuario']['id'])
        product = Product.objects.get(id=id)
        cantidad = request.POST['cantidad']
        precioU = product.price
        subtotal = product.price * int(cantidad)
        igvProd = decimal.Decimal(subtotal) * decimal.Decimal(igv)
        opGravada = subtotal - igvProd
        existeBoleta = Boleta.objects.filter(users = request.session['usuario']['id'], pagado = False).last()
        print (existeBoleta)

        if existeBoleta:
            a = 0
        else:
            Boleta.objects.create(total = 0, totalDesc = 0, totalOpGravada = 0, totalIGV = 0, users = user )
        product.cantVendidos = product.cantVendidos+1
        product.stock = product.stock-1
        product.save()
        boletaid = Boleta.objects.filter(users = request.session['usuario']['id'], pagado = False).last()
        print(boletaid)
        BoletaDetalle.objects.create(subtotal = subtotal, descuento = descuento, opGravada = opGravada, igv = igvProd, precioUni=precioU , usuario = user,cantidad = cantidad, estado = True, productos = product, boleta = boletaid)


        #raise Exception('Prueba')


        messages.success(request, 'Producto agregado al carrito')
        return redirect(reverse('ecommerce:shoppingCart'))

def shoppingCart(request):
    if request.method == 'GET':
        boletaid = Boleta.objects.filter(users = request.session['usuario']['id'], pagado = False).last()
        cart = BoletaDetalle.objects.filter(usuario = request.session['usuario']['id'], boleta = boletaid)

        a = BoletaDetalle.objects.filter(usuario = request.session['usuario']['id'], boleta = boletaid).aggregate(total_subtotal = Sum('subtotal'))
        b = BoletaDetalle.objects.filter(usuario = request.session['usuario']['id'], boleta = boletaid).aggregate(total_dsc = Sum('descuento'))
        c = BoletaDetalle.objects.filter(usuario = request.session['usuario']['id'], boleta = boletaid).aggregate(total_igv = Sum('igv'))
        d = BoletaDetalle.objects.filter(usuario = request.session['usuario']['id'], boleta = boletaid).aggregate(total_op_grav = Sum('opGravada'))
        
        descuento = round(b['total_dsc'],2)
        igv = round(c['total_igv'],2)
        op_gravada = round(d['total_op_grav'],2)
        subtotal = round(a['total_subtotal'],2) + 10

        print(cart)
        print(subtotal)
        contexto={
            'cart':cart, 
            'op_gravada': op_gravada,
            'igv':igv,
            'subtotal':subtotal,
            'descuento':descuento,

        }
        return render(request, 'ecommerce/shoppingCart.html', contexto)


def shoppingCartempty(request):
    return render(request, 'ecommerce/shoppingCartEmpty.html')

def deleteProductFromCart(request, id):
    if request.method == 'POST':
        lastBoleta = Boleta.objects.all().filter(users = request.session['usuario']['id']).last()
        detalleProd = BoletaDetalle.objects.get(id=id)
        detalleProd.delete()
        messages.success(request,"Eliminado correctamente")
        if detalleProd.id ==  lastBoleta.id:
            return redirect(reverse('ecommerce:shoppingCart'))
        else:
            return redirect(reverse('ecommerce:shoppingCartempty'))

def buy(request):
    if request.method == 'POST':
        
        boletaid = Boleta.objects.filter(users = request.session['usuario']['id'], pagado = False).last()
        cart = BoletaDetalle.objects.filter(usuario = request.session['usuario']['id'])
        a = BoletaDetalle.objects.filter(usuario = request.session['usuario']['id'], boleta = boletaid).aggregate(total_subtotal = Sum('subtotal'))
        b = BoletaDetalle.objects.filter(usuario = request.session['usuario']['id'], boleta = boletaid).aggregate(total_dsc = Sum('descuento'))
        c = BoletaDetalle.objects.filter(usuario = request.session['usuario']['id'], boleta = boletaid).aggregate(total_igv = Sum('igv'))
        d = BoletaDetalle.objects.filter(usuario = request.session['usuario']['id'], boleta = boletaid).aggregate(total_op_grav = Sum('opGravada'))
        
        subtotal = round(a['total_subtotal'],2) + 10
        descuento = round(b['total_dsc'],2)
        igv = round(c['total_igv'],2)
        op_gravada = round(d['total_op_grav'],2)
        

        boletaid.total = subtotal
        boletaid.totalDesc = descuento
        boletaid.totalOpGravada = op_gravada
        boletaid.totalIGV = igv
        boletaid.pagado = True
        boletaid.save()
        messages.success(request, 'Compra efectuada correctamente')
        return redirect(reverse('patient_home'))

#Admin
def adminMainPage(request):
    #if request.session.usuario.typeUser == '1':
        if request.method == 'GET':
            return render(request, 'ecommerce/indexAdmin.html')


def adminShowProductsPage(request):
    if request.method == 'GET':
        prod = Product.objects.all()
        contexto = {
            'ProductForm'  : ProductForm(),
            'productos': prod
            }
        return render(request, 'ecommerce/adminProductsPage.html', contexto )

def addProduct(request):
    if request.method == 'GET':
        contexto = {
            'ProductForm'  : ProductForm(),
            }
        return render(request, 'ecommerce/addProduct.html', contexto )
    if request.method == "POST":
        form = ProductForm(request.POST)
        img = ProductForm(request.FILES)
        a = (request.FILES.get('img'))
        if form.is_valid():
            prod = form.save(commit=False)
            prod.img = a
            prod.save()
            print(prod)
            messages.success(request, 'Producto agregado correctamente')
            return redirect(reverse('ecommerce:showProducts'))
        else:
            messages.error(request, 'Con errores, solucionar.')
            return render(request, 'ecommerce/addProduct.html', {'ProductForm'  : form}) 

def editProd(request,id):
    prod = Product.objects.get(id=id)
    if request.method == 'GET':
        form = ProductForm(instance=prod)
        context = {
            'ProductForm':form,
            'product':prod
        }
        return render(request, 'ecommerce/editProduct.html', context)

    if request.method == "POST":
        prod = Product.objects.get(id=id)
        form = ProductForm(request.POST,instance=prod)
        img = request.FILES.get('img')
        print(img)
        if form.is_valid():
            p = form.save(commit=False)
            p.img = img
            p.save()
            messages.success(request, 'Producto editado correctamente')
            return redirect('ecommerce:showProducts')
        else:
            messages.error(request, 'Con errores, solucionar.')
            return render(request, 'ecommerce/storeKeeperProductsPage.html', {'ProductForm'  : form}) 

def deleteProd(request, id):
    if request.method == 'POST':
        prodD = Product.objects.get(id=id)
        print(prodD.name)
        prodD.delete()
        messages.success(request,"Eliminado correctamente")
        return redirect(reverse('ecommerce:showProducts'))

def addCategory(request):
    if request.method == 'GET':
        cat = DosageForm.objects.all()
        contexto = {
            'CategoryForm'  : DosageFormForm(),
            'categories':cat,
            }

        return render(request, 'ecommerce/addCategory.html' , contexto)
    if request.method == "POST":
        cat = DosageForm.objects.all()
        form = DosageFormForm(request.POST)
        if form.is_valid():
            tmp = form.save()
            messages.success(request, 'Categoria creada correctamente')
            return redirect(reverse('ecommerce:addCategory'))
        else:
            messages.error(request, 'Con errores, solucionar.')
            return render(request, 'ecommerce/addCategory.html', {'CategoryForm'  : form, 'categories':cat,}) 

def editCat(request,id):
    cat = DosageForm.objects.get(id=id)
    if request.method == 'GET':
        form = DosageFormForm(instance=cat)
        context = {
            'CategoryForm':form,
            'category':cat
        }
        return render(request, 'ecommerce/editCategory.html', context)

    if request.method == "POST":
        print(request.POST)
        cat = DosageForm.objects.get(id=id)
        form = DosageFormForm(request.POST,instance=cat)
        if form.is_valid():
            form.save()
            messages.success(request, 'Categoria editada correctamente')
            return redirect('ecommerce:addCategory')
        else:
            messages.error(request, 'Con errores, solucionar.')
            return render(request, 'ecommerce/addCategory.html', {'CategoryForm'  : form}) 

def deleteCat(request, id):
    if request.method == 'POST':
        catD = DosageForm.objects.get(id=id)
        print(catD.name)
        catD.delete()
        messages.success(request,"Eliminado correctamente")
        return redirect(reverse('ecommerce:addCategory'))

def showProductDetail(request,id):
    if request.method == 'GET':
        prod = Product.objects.get(id=id)
        contexto = {
            'producto':prod
        }
        print(prod.img)
        return render(request, 'ecommerce/showProductDetail.html', contexto) 


