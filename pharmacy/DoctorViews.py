from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.forms import  UserCreationForm
from django.views import View
from pharmacy.utils import render_to_pdf


from reportes.views import procesar_pdf
from .decorators import *

from .forms import *
from .models import *

def doctorHome(request): 
    prescip = Prescription.objects.all().count()

    context={
        "Prescription_total":prescip

    }
    return render(request,'doctor_templates/doctor_home.html',context)

def doctorProfile(request):
    customuser=CustomUser.objects.get(id=request.user.id)
    staff=Doctor.objects.get(admin=customuser.id)

    form=DoctorForm()
    if request.method == 'POST':
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')


        customuser=CustomUser.objects.get(id=request.user.id)
        customuser.first_name=first_name
        customuser.last_name=last_name
        customuser.save()

        staff=Doctor.objects.get(admin=customuser.id)
        form =DoctorForm(request.POST,request.FILES,instance=staff)

        staff.save()

        if form.is_valid():
            form.save()

    context={
        "form":form,
        "staff":staff,
        "user":customuser
    }

    return render(request,'doctor_templates/doctor_profile.html',context)

def managePatients(request):
    patients=Patients.objects.all()

    context={
        "patients":patients,

    }
    return render(request,'doctor_templates/manage_patients.html',context)

def addPrescription(request,pk):        
    patient=Patients.objects.get(id=pk)
    form=PrescriptionForm(initial={'patient_id':patient})
    if request.method == 'POST':
        try:
            form=PrescriptionForm(request.POST or None)
            if form.is_valid():
                form.save()
                messages.success(request,'Prescripción realizada con éxito')
                return redirect('manage_precrip_doctor')
        except:
            messages.error(request,'Prescripción no realizada')
            return redirect('manage_patient-doctor')


 
    
    context={
        "form":form
    }
    return render(request,'doctor_templates/prescribe_form.html',context)

def patient_personalDetails(request,pk):
    patient=Patients.objects.get(id=pk)
    prescrip=patient.prescription_set.all()

    context={
        "patient":patient,
        "prescription":prescrip

    }
    return render(request,'doctor_templates/patient_personalRecords.html',context)

def deletePrescription(request,pk):
    prescribe=Prescription.objects.get(id=pk)

    if request.method == 'POST':
        try:
            prescribe.delete()
            messages.success(request,'Prescrición eliminada con éxito')
            return redirect('manage_precrip_doctor')
        except:
            messages.error(request,'Prescripción no eliminada')
            return redirect('manage_precrip_doctor')




    context={
        "patient":prescribe
    }

    return render(request,'doctor_templates/sure_delete.html',context)
    
def managePrescription(request):
    precrip=Prescription.objects.all().order_by("-date_precribed") 

    patient = Patients.objects.all()
    
       
    context={
        "prescrips":precrip,
        "patient":patient
    }
    return render(request,'doctor_templates/manage_prescription.html' ,context)

def editPrescription(request,pk):
    prescribe=Prescription.objects.get(id=pk)
    form=PrescriptionForm(instance=prescribe)

    
    if request.method == 'POST':
        form=PrescriptionForm(request.POST ,instance=prescribe)

        try:
            if form.is_valid():
                form.save()

                messages.success(request,'Prescripción actualizada con éxito')
                return redirect('manage_precrip_doctor')
        except:
            messages.error(request,' Error!! Prescripción no actualizada')
            return redirect('manage_precrip_doctor')




    context={
        "patient":prescribe,
        "form":form
    }

    return render(request,'doctor_templates/edit_prescription.html',context)
    
    
def receta_pdf(request,pk):
    prescrip=Prescription.objects.get(id=pk)
    patient=Patients.objects.filter(patients=prescrip).last()
    print(prescrip)
    print(prescrip.prescribe)

    print(request.session['usuario']['first_name'] + request.session['usuario']['apellido'])
    customuser=CustomUser.objects.get(id=request.session['usuario']['id'])
    context={
        "patient":patient,
        "prescription":prescrip,
        "customUser":customuser

    }
    return procesar_pdf(context,"reportes/receta.html","receta.pdf")


        



