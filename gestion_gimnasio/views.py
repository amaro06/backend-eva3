from django.contrib.auth.decorators import login_required
from .forms import DisciplinaForm, EtiquetaForm, RutinaForm, RegistroForm, InscripcionForm, PerfilForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Disciplina, Etiqueta, Rutina, Inscripcion
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from django.contrib import messages

# Create your views here.

def home(request):
    q = request.GET.get('q', '').strip()
        
    disciplina_id = request.GET.get('disciplina', '')
    rutinas = Rutina.objects.all().order_by('titulo')
        
    if q:
        rutinas = rutinas.filter(
                titulo__icontains=q
            )
        
    if disciplina_id.isdigit():
        rutinas = rutinas.filter(
                disciplina_id = disciplina_id
                )
    paginator = Paginator(rutinas, 2)
    page_obj = paginator.get_page(request.GET.get('page'))
        
    params = request.GET.copy()
    params.pop('page', None)
        
    return render(request, 'home.html', {
        'rutinas':page_obj,
        'disciplinas':Disciplina.objects.all(),
        'q':q,
        'disciplina_id':disciplina_id,
        'querystring':params.urlencode()
        })


@login_required
def crear_disciplina(request):
    if request.method == 'POST':
        form = DisciplinaForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('lista_disciplinas')
    else:
        form = DisciplinaForm()

    return render(request, 'crear_disciplina.html', {
        'form': form
        })


@login_required
def editar_disciplina(request, pk):
    disciplina = get_object_or_404(Disciplina, pk=pk)
    if request.method == 'POST':
        form = DisciplinaForm(request.POST, instance=disciplina)
        if form.is_valid():
            form.save()
            return redirect('lista_disciplinas')
    else:
        form = DisciplinaForm(instance=disciplina)
    return render(request, 'editar_disciplina.html', {
        'form':form
        })

@login_required
def eliminar_disciplina(request, pk):
    disciplina = get_object_or_404(Disciplina, pk=pk)
    if request.method == 'POST':
       disciplina.delete()
       return redirect('lista_disciplinas')
    return render(request, 'eliminar_disciplina.html', {
        'disciplina':disciplina
    })

def lista_disciplinas(request):
    disciplinas = Disciplina.objects.all()
    return render(request, 'lista_disciplinas.html', {'disciplinas':disciplinas})

@login_required
def crear_etiqueta(request):
    if request.method == 'POST':
        form = EtiquetaForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EtiquetaForm()
    return render(request, 'crear_etiqueta.html', {
        'form':form
    })

@login_required
def editar_etiqueta(request, pk):
    etiqueta = get_object_or_404(Etiqueta, pk=pk)
    if request.method == 'POST':
        form = EtiquetaForm(request.POST, instance=etiqueta)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = EtiquetaForm(instance=etiqueta)
    return render(request, 'editar_etiqueta.html', {
        'form':form
    })

@login_required
def eliminar_etiqueta(request, pk):
    etiqueta = get_object_or_404(Etiqueta, pk=pk)
    if request.method == 'POST':
        etiqueta.delete()
        return redirect('home')
    return render(request, 'eliminar_etiqueta.html', {
        'etiqueta':etiqueta
    })


def lista_etiquetas(request):
    etiqueta = Etiqueta.objects.all()
    return render(request, 'lista_etiquetas.html', {
        'etiqueta':etiqueta
    })

#-----------------------------------------------------------------------------#

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistroForm()

    return render(request, 'registro.html', {
        'form': form
    })


@login_required
def crear_rutina(request):
    if not request.user.groups.filter(name='Entrenador').exists():        #si el usuario no es un entrenador lo redirige al inicio
        return redirect('home')
    
    if request.method == 'POST':
        form = RutinaForm(request.POST)

        if form.is_valid():
            rutina = form.save(commit=False)
            rutina.entrenador = request.user
            rutina.save()
            form.save_m2m()
            messages.success(request, 'Rutina creada correctamente')
            return redirect('lista_rutinas')
    else:
        form = RutinaForm()

    return render(request, 'crear_rutina.html', {
        'form':form
    })

@login_required
def editar_rutina(request, pk):
    rutina = get_object_or_404(Rutina, pk=pk)

    if rutina.entrenador != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = RutinaForm(request.POST, instance=rutina)
        if form.is_valid():
            form.save()
            messages.success(request, 'Rutina actualizada correctamente')
            return redirect('lista_rutinas')
    else:
        form = RutinaForm(instance=rutina)
    return render(request, 'editar_rutina.html', {
        'form':form
    })

@login_required
def eliminar_rutina(request, pk):
    rutina = get_object_or_404(Rutina, pk=pk)

    if rutina.entrenador != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        rutina.delete()
        messages.success(request, 'Rutina eliminada correctamente')
        return redirect('lista_rutinas')
        
    return render(request, 'eliminar_rutina.html', {
        'rutina':rutina
    })

@login_required
def lista_rutinas(request):
    q = request.GET.get('q', '').strip()

    disciplina_id = request.GET.get('disciplina', '')
    rutinas = Rutina.objects.filter(entrenador = request.user).order_by('titulo')

    if q:
        rutinas = rutinas.filter(
            titulo__icontains=q
        )

    if disciplina_id.isdigit():
        rutinas = rutinas.filter(
            disciplina_id = disciplina_id
        )
    paginator = Paginator(rutinas, 2)
    page_obj = paginator.get_page(request.GET.get('page'))

    params = request.GET.copy()
    params.pop('page', None)

    return render(request, 'lista_rutinas.html', {
        'rutinas':page_obj,
        'disciplinas':Disciplina.objects.all(),
        'q':q,
        'disciplina_id':disciplina_id,
        'querystring':params.urlencode()
    })



@login_required
def crear_inscripcion(request):
    

    if not request.user.groups.filter(name='Socio').exists():
        return redirect('home')

    if request.method == 'POST':
        form = InscripcionForm(request.POST)

        if form.is_valid():
            rutina = form.cleaned_data['rutina']

            existe = Inscripcion.objects.filter(
                socio = request.user,
                rutina = rutina
            ).exists()

            if existe:
                return render(request, 'crear_inscripcion.html', {
                'form': form,
                'mensaje': 'Ya te encuentras inscrito en esta rutina.'
                })


            inscripcion = form.save(commit=False)
            inscripcion.socio = request.user
            inscripcion.save()
            form.save_m2m()
            messages.success(request, 'Inscripcion realizada')
            return redirect('home')
    else:
        form = InscripcionForm()
    return render(request, 'crear_inscripcion.html', {
            'form':form
            })

@login_required
def editar_inscripcion(request, pk):

    inscripcion = get_object_or_404(Inscripcion, pk=pk)

    if inscripcion.socio != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        form = InscripcionForm(request.POST, instance=inscripcion)
        if form.is_valid():
            form.save()
            messages.success(request, 'inscripcion actualizada')
            return redirect('perfil')
    else:
        form = InscripcionForm(instance=inscripcion)
    return render(request, 'editar_inscripcion.html', {
        'form':form
    })

@login_required
def eliminar_inscripcion(request, pk):
    inscripcion = get_object_or_404(Inscripcion, pk=pk)

    if inscripcion.socio != request.user:
            raise PermissionDenied

    if request.method == 'POST':
        inscripcion.delete()
        messages.success(request, 'inscripcion eliminada')
        return redirect('perfil')
    return render(request, 'eliminar_inscripcion.html', {
        'inscripcion':inscripcion
    })

@login_required
def lista_inscripciones(request):
    q = request.GET.get('q', '')

    inscripcion = Inscripcion.objects.filter(
        rutina__entrenador = request.user
    )

    if q:
        inscripcion = inscripcion.filter(
            socio__username__icontains = q
        )

    paginator = Paginator(inscripcion, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    params = request.GET.copy()
    params.pop('page', None)

    return render(request, 'lista_inscripciones.html', {
        'inscripciones':page_obj,
        'q':q,
        'querystring':params.urlencode(),
    })

@login_required
def mis_inscripciones(request):
    q = request.GET.get('q', '')

    if not request.user.groups.filter(name='Socio').exists():        
            return redirect('home')
    
    inscripcion = Inscripcion.objects.filter(socio = request.user).order_by('rutina__titulo')

    if q:
        inscripcion = inscripcion.filter(
            rutina__titulo__icontains=q
        )

    paginator = Paginator(inscripcion, 10)
    page_obj = paginator.get_page(request.GET.get('page'))

    params = request.GET.copy()
    params.pop('page', None)

    return render(request, 'mis_inscripciones.html', {
        'inscripciones':page_obj,
        'q':q,
        'querystring':params.urlencode()
    })


@login_required
def aceptar_rechazar_inscripcion(request, pk):
    if not request.user.groups.filter(name = 'Entrenador').exists():
        return redirect('home')

    inscripcion = get_object_or_404(Inscripcion, pk=pk)
    if inscripcion.rutina.entrenador != request.user:
        raise PermissionDenied

    if request.method == 'POST':
        estado_nuevo = request.POST.get('estado')

        if estado_nuevo in ['aceptada', 'rechazada']:
            inscripcion.estado = estado_nuevo
            inscripcion.save()

    return redirect('lista_inscripciones')


@login_required
def perfil(request):

    if request.method == 'POST':
        form = PerfilForm(request.POST, instance=request.user)

        if form.is_valid():
            form.save()
            messages.success(request, 'Perfil actualizado correctamente.')
            return redirect('perfil')

    else:
        form = PerfilForm(instance=request.user)

    return render(request, 'perfil.html', {
        'form': form
    })


class CambiarPasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'cambiar_contrasenia.html'
    success_url = reverse_lazy('perfil')
    success_message = 'Tu contraseña fue actualizada.'


