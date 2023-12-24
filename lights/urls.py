from django.urls import path
from . import views





urlpatterns = [
    path("",views.index, name="index"),
    path("search",views.search, name="search"),
    path("light-list",views.light_list,name="light_list"),
    path("light-edit/<int:id>", views.light_edit, name="light_edit"),
    path("<int:id>",views.details, name="light_details"),
    
    
    
]
