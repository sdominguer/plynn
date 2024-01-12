import io
import base64
from io import BytesIO
import matplotlib.pyplot as plt
from django.shortcuts import render, redirect
from .models import Calificacion

# Create your views here.


def home(request):
    grupo = request.GET.get("grupo", "")
    return render(request, "home.html", {"grupo": grupo})


def login(request):
    grupos = [
        "B&A Beauty",
        "La Molienda Panelera",
        "Hotel MOA",
        "Superverfru",
        "INPRO",
        "PETIT",
        "ALNE",
        "Alcaldía de Ronda",
        "Mundopiel",
        "TECH",
    ]

    if request.method == "GET":
        return render(request, "login.html", {"grupos": grupos})


def manejoCalificaciones(request):
    if request.method == "POST":
        grupo = request.POST["grupo"]

        for i in range(4):
            sumaFactible = 0.0
            sumaEstrategico = 0.0
            reto = request.POST[f"reto{i+1}"]

            for j in range(4):
                sumaFactible += float(request.POST[f"reto{i+1}_factible{j+1}"])
                sumaEstrategico += float(request.POST[f"reto{i+1}_estrategico{j+1}"])

            promedioFactible = sumaFactible / 4
            promedioEstrategico = sumaEstrategico / 4

            nuevaCalificacion = Calificacion.objects.create(
                reto=reto,
                promedioFactible=promedioFactible,
                promedioEstrategico=promedioEstrategico,
                grupo=grupo,
            )

        return redirect("graficas", grupo=grupo)


def graficas(request, grupo):
    calificaciones = Calificacion.objects.filter(grupo=grupo).order_by(
        "-idCalificacion"
    )[:4]

    # Obtener las coordenadas para la gráfica
    x = [calificacion.promedioFactible for calificacion in calificaciones]
    y = [calificacion.promedioEstrategico for calificacion in calificaciones]
    retos = [calificacion.reto for calificacion in calificaciones]

    # Crear la gráfica de puntos con etiquetas
    plt.figure(figsize=(8, 6))
    for i, reto in enumerate(retos):
        plt.scatter(x[i], y[i])
        plt.annotate(
            reto, (x[i], y[i]), textcoords="offset points", xytext=(0, 10), ha="center"
        )

    plt.xlabel("Promedio Factible")
    plt.ylabel("Promedio Estrategico")
    plt.title(f"Gráfica de Calificaciones - Grupo {grupo}")

    # Configurar los límites del eje x e y
    plt.xlim(0.0, 5.0)
    plt.ylim(0.0, 5.0)

    # Configurar los intervalos del eje x e y
    plt.xticks([i / 2.0 for i in range(11)])
    plt.yticks([i / 2.0 for i in range(11)])

    # Agregar líneas verticales y horizontales en el centro
    plt.axvline(
        x=2.5, color="red", linestyle="--", linewidth=1, label="Vertical Center"
    )
    plt.axhline(
        y=2.5, color="red", linestyle="--", linewidth=1, label="Horizontal Center"
    )

    # Agregar etiquetas a cada cuadrante
    plt.text(
        1.25,
        3.75,
        "Retos para análisis\n(Intraemprendimiento)",
        fontsize=10,
        color="blue",
    )
    plt.text(3.75, 3.75, "Retos priorizados", fontsize=10, color="blue")
    plt.text(1.25, 1.25, "Retos descartados", fontsize=10, color="blue")
    plt.text(
        3.75,
        1.25,
        "Retos para análisis\n(Innovación abierta)",
        fontsize=10,
        color="blue",
    )

    # Convertir la gráfica a base64
    buf = io.BytesIO()
    plt.savefig(buf, format="png")
    buf.seek(0)
    grafica_base64 = base64.b64encode(buf.read())

    return render(
        request,
        "graficas.html",
        {
            "calificaciones": calificaciones,
            "grupo": grupo,
            "grafica_base64": grafica_base64.decode("utf-8"),
        },
    )
