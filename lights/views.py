from django.shortcuts import get_object_or_404, redirect, render

from lights.forms import LightEditForm
from .models import Light
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required, user_passes_test
#forms
# GET => url = querystring
# POST=> 


def index(request):  
    lights = Light.objects.all()[:5]

    return render(request, "lights/index.html",{
        "lights":lights,
    })
    

    
def isAdmin(user):
    return user.is_superuser

    
@login_required()
def light_list(request):
    lights = Light.objects.all()
    return render(request, "lights/light-list.html",{
        "lights":lights
    })
    
def light_edit(request,id):
    light = get_object_or_404(Light,pk=id)
    
    if request.method == "POST":
        form = LightEditForm(request.POST ,instance=light)
        form.save()
        return redirect("light_list")
    else:    
        form = LightEditForm(instance=light)
    
    return render(request, "lights/edit-light.html", {"form":form})




def search(request):
    if "q" in request.GET and request.GET["q"]!="":
        q = request.GET["q"]
        lights = Light.objects.filter(name__contains=q).order_by("id")
    else:
        return redirect("/lights")
    
    
    return render(request, "lights/search.html",{
        "lights":lights,
    })



def details(request,id):
    light = get_object_or_404(Light, pk=id)
    context = {
        "light": light
    }
    return render(request, "lights/details.html", context)
