from django.contrib.auth.decorators import login_required
from .forms import DisciplinaForm
from django.shortcuts import render, redirect, get_object_or_404
from .models import Disciplina

# Create your views here.

def home(request):
    return render(request, 'home.html')

@login_required
def crear_disciplina(request):
    if request.method == 'POST':
        form = DisciplinaForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')
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
            return redirect('home')
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
       return redirect('home')
    return render(request, 'eliminar_disciplina.html', {
        'disciplina':disciplina
    })

def lista_disciplinas(request):
    pass