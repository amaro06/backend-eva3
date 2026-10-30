from django.contrib.auth.decorators import login_required
from .forms import DisciplinaForm, EtiquetaForm, RutinaForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Disciplina, Etiqueta, Rutina


# Create your views here.

def home(request):
    return render(request, 'home.html')

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

@login_required
def crear_rutina(request):
    if not request.user.groups.filter(name='Entrenador').exists():
        return redirect('home')
    
    if request.method == 'POST':
        form = RutinaForm(request.POST)

        if form.is_valid():
            rutina = form.save(commit=False)
            rutina.entrenador = request.user
            rutina.save()
            form.save_m2m()
            return redirect('home')
    else:
        form = RutinaForm()

    return render(request, 'crear_rutina.html', {
        'form':form
    })