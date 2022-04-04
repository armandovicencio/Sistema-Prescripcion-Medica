import os
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.contrib.auth.models import User, Group
# from rest_framework import viewsets
from pharmacy.forms import PrescriptionForm
from pharmacy.models import *


def link_callback(uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        result = finders.find(uri)
        if result:
                if not isinstance(result, (list, tuple)):
                        result = [result]
                result = list(os.path.realpath(path) for path in result)
                path=result[0]
        else:
                sUrl = settings.STATIC_URL        # Typically /static/
                sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
                mUrl = settings.MEDIA_URL         # Typically /media/
                mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

                if uri.startswith(mUrl):
                        path = os.path.join(mRoot, uri.replace(mUrl, ""))
                elif uri.startswith(sUrl):
                        path = os.path.join(sRoot, uri.replace(sUrl, ""))
                else:
                        return uri

        # make sure that file exists
        if not os.path.isfile(path):
                raise Exception(
                        'media URI must start with %s or %s' % (sUrl, mUrl)
                )
        return path

def procesar_pdf(contexto, template_name, archivo="receta.pdf", tipo="inline"):
        template_path = template_name
        context = contexto

        # Create a Django response object, and specify content_type as pdf
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'{tipo}; filename="{archivo}"'  
        # response['Content-Disposition'] = 'attachment; filename="receta.pdf"'
        # find the template and render it.
        template = get_template(template_path)
        html = template.render(context)

        # create a pdf
        pisa_status = pisa.CreatePDF(
                html, dest=response, link_callback=link_callback)
        # if error then show some funy view
        if pisa_status.err:
                return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response

def render_pdf_view(request, id):
        template_path = 'reportes/prueba.html'

        if id > 1:
                template_path = f'reportes/prueba{id}.html'

        context = {'patient': 'esto es desde el contexto'}
        return procesar_pdf(context, template_path)


def receta_pdf(request,pk):
    patient=Patients.objects.get(id=pk)
    prescrip=patient.prescription_set.all()

    context={
        "patient":patient,
        "prescription":prescrip,

    }
    return procesar_pdf(context,"reportes/receta.html","receta.pdf")
 
    
   

# def usuarios(request):

#         contexto = {
#                 'usuarios' : User.objects.all()
#         }

#         return procesar_pdf(contexto, "reportes/usuarios.html","usuarios.pdf")