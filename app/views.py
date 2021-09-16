from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.shortcuts import render
from .models import Comunas

# Create your views here.
from django.views import View


class Inicio(LoginRequiredMixin, View):
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    def get(self, request):
        return render(request, 'inicio.html')


def handler404(request, exception):
    return render(request, 'page-404.html', status=404)

def handler500(request):
    return render(request, 'page-500.html', status=500)

def GetComunas(request):
    id_region = request.GET.get('region')
    try:
        comunas = Comunas.objects.filter(cod_provincia__cod_region_id=id_region)
        data = []
        for i in comunas:
            data.append({'id': i.id, 'comuna': i.nombre})
    except Exception as e:
        data['error'] =str(e)
    return JsonResponse(data, safe=False)