from django.urls import  path
from api import views

urlpatterns = [
    path("login",views.login,name="login"),
    path("signup",views.signup),
    path("logout",views.logout),
    path("test_token",views.test_token),
    path("lights",views.lights),
    path("light",views.light),

]
