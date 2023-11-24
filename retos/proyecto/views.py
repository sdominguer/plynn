from django.shortcuts import render

# Create your views here.

def home(request):
    grupo = request.GET.get('grupo', '')
    return render(request, 'home.html', {'grupo': grupo})

def login(request):
    grupos = ['B&A Beauty', 'La Molienda Panelera', 'Hotel MOA', 'Superverfru', 'INPRO', 'PETIT', 'ALNE', 'Alcaldía de Ronda', 'Mundopiel', 'TECH']

    if request.method == 'GET':
        return render(request, 'login.html', {'grupos': grupos})