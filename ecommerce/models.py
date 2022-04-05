from django.db import models
from pharmacy.models import CustomUser, Product
from django.utils import timezone


class Boleta(models.Model):

    total = models.DecimalField(decimal_places=2, max_digits=6)
    totalDesc = models.DecimalField(decimal_places=2, max_digits=6, default=0)
    totalOpGravada = models.DecimalField(decimal_places=2, max_digits=6)
    totalIGV = models.DecimalField(decimal_places=2, max_digits=6)
    precioEnvio = models.DecimalField(decimal_places=2, max_digits=6, default = 10)
    #detalleBoleta=models.ManyToManyField(BoletaDetalle, related_name='carritos')
    users = models.ForeignKey(CustomUser, related_name='usuarios2', on_delete=models.CASCADE, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pagado = models.BooleanField(default=False)

    def __str__ (self):
        return f'{self.users} - {self.pagado}'


class BoletaDetalle(models.Model):
    
    precioUni = models.DecimalField(decimal_places=2, max_digits=6, default=0)
    subtotal = models.DecimalField(decimal_places=2, max_digits=6)
    descuento = models.DecimalField(decimal_places=2, max_digits=6, default=0)
    opGravada = models.DecimalField(decimal_places=2, max_digits=6)
    igv = models.DecimalField(decimal_places=2, max_digits=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(CustomUser, related_name='usuarios', on_delete=models.CASCADE)
    productos = models.ForeignKey(Product, related_name='boletaDetalle', on_delete=models.CASCADE, default=0)
    cantidad = models.IntegerField(default=1, null=False)
    estado = models.BooleanField(default=False)
    boleta = models.ForeignKey(Boleta, related_name='boletas', on_delete=models.CASCADE, default =1)
    
    def __str__ (self):
        return f'{self.usuario} - {self.productos} - {self.cantidad} - {self.boleta.id}'

