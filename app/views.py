from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, Group
from usuarios.utilidades import estado_auth
import bcrypt
from app.email import send_user_mail, EmailThread


def index(request):

    if 'usuario' not in request.session:
        messages.error(request,"NO estas logeado.")
        return redirect("/login/")

    id = request.session['usuario']['id']
    user = User.objects.get(id=id)

    # send_user_mail(request,user)

    EmailThread("Correo de Prueba ASINCRONICA", 
                'correo.html', 
                ['python.quince@gmail.com', 'fboisier@munipro.cl', 'susana.pavez@gmail.com']
                ).start()

    context = {
    }
    
    return render(request, 'index.html', context)



def add(request):
    context = {
    }
# Tambien se puede redirigir a principal o display
    return render(request, 'add.html', context)



def display(request, id):
    context = {
        'id' : id 
    }
    return render(request, 'display.html', context)



def edit(request, id):
    context = {
        'id' : id 
    }
    return render(request, 'edit.html', context)



def delete(request, id):
    context = {
        'id' : id 
    }
    return render(request, 'delete.html', context)


def other(request, id):
    context = {
        'id' : id 
    }
    return render(request, 'other.html', context)


def registro(request):
    if request.method == 'GET':

        if 'usuario' in request.session:
            messages.warning(request,"Ya estás registrado.")
            return redirect("/")


        context = {}
        return render(request, 'registro.html', context)

    if request.method == 'POST':
        print("POST DEL REGISTRO: ", request.POST)

        pass_encriptada = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        print(f"la contraseña '{request.POST['password']}' con bcrypt quedo en: {pass_encriptada}")

        user = User.objects.create(
            firstname = request.POST['nombre'],
            lastname = request.POST['apellido'],
            email = request.POST['email'],
            password = pass_encriptada,
        )


        usuario_session = {
            'id' : user.id,
            'nombre' : user.firstname + ' ' + user.lastname,
            'email' : user.email
        }

        print(usuario_session)
        request.session['usuario'] = usuario_session

        messages.success(request, "Usuario creado exitosamente.")
        return redirect("/")

def login(request):
    if request.method == 'GET':

        if 'usuario' in request.session:
            messages.warning(request,"Ya estás logeado.")
            return redirect("/")

        context = {}
        return render(request, 'login.html', context)

    if request.method == 'POST':
        print("POST DEL LOGIN: ", request.POST)

        usuarios = User.objects.filter(email=request.POST['email']) 
        if usuarios: 
            usuario = usuarios[0] 
            print(usuario)

            if bcrypt.checkpw(request.POST['password'].encode(), usuario.password.encode()):
                
                print("PASSWORD COINCIDEN!!!")

                usuario_session = {
                    'id' : usuario.id,
                    'nombre' : usuario.firstname + ' ' + usuario.lastname,
                    'email' : usuario.email
                }

                print(usuario_session)
                request.session['usuario'] = usuario_session
                messages.success(request, "Logeado Correctamente")
                return redirect('/')
            else:
                messages.error(request, "La contraseña o el correo NO COINCIDE")
                return redirect("/login/")

        else:
            messages.error(request,"El correo o la contraseña indicado no EXISTE")
            return redirect("/login/")
        
        

def logout(request):
    if 'usuario' in request.session:
        del request.session['usuario']

    return redirect("/login/")
