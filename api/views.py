from rest_framework.decorators import api_view
from rest_framework.response import Response

from lights.models import Light

from .serializers import UserSerializer, LightSerializer
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from datetime import datetime

from django.shortcuts import get_object_or_404

@api_view(["POST"])
def login(request):
    print(request.__dict__)
    request.data["username"] = request.data["username"].replace(":",".")
    user = get_object_or_404(User, username=request.data["username"])
    if not user.check_password(request.data["password"]):
        return Response({"detail":"Not found",},status=status.HTTP_404_NOT_FOUND)
    token, created = Token.objects.get_or_create(user=user)
    serializer = UserSerializer(instance=user)
    user.is_active = True
    user.save()
    return Response({"token":token.key, "user":serializer.data},status=status.HTTP_200_OK)


@api_view(["POST"])
def signup(request):
    request.data["username"] = request.data["username"].replace(":",".")
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        user = User.objects.get(username=request.data["username"])
        user.set_password(request.data["password"])
        user.save()
        token = Token.objects.create(user=user)
        
        Light.objects.create(
            name=user.username,
            ip = request.META.get("REMOTE_ADDR"),
            is_on = False,
            is_active = False,
            creation_date = datetime.now(),
            last_communication_date = datetime.now()
                             )
        
        
        return Response({"token":token.key, "user":serializer.data},status=status.HTTP_200_OK)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def logout(request):
    try:
        request.user.auth_token.delete()
        request.user.is_active = True
        request.user.save()
        return Response(status=status.HTTP_200_OK)
    except:
        return Response(status=status.HTTP_401_UNAUTHORIZED)



from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

@api_view(["POST"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def test_token(request):
    print(request.data)
    name = request.data["name"]
    name = name.replace(":",".")
    try:
        light = Light.objects.get(name=name)
        
        light.last_communcation_date = datetime.now()
        light.save()

        is_on = light.is_on
        return Response({"is_on":is_on,})
    except:
        return Response({"errors":"not found"},status=status.HTTP_404_NOT_FOUND)

    
    






@api_view(["GET"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def lights(request):
    if request.user.is_authenticated:
        lights = Light.objects.all()
        serializer = LightSerializer(lights, many=True)
        return Response(serializer.data)


    

@api_view(["GET","PUT"])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def light(request):
    try:
        name = request.data["name"].replace(":",".")
        light = Light.objects.get(name=name)
        
    except:
        return Response({"error":"Eslesen bir kayit bulunmadi"}, status=status.HTTP_404_NOT_FOUND)
    
    if request.method == "GET":
        serializer = LightSerializer(light)
        return Response(serializer.data)
    elif request.method == "PUT":
        
        serializer = LightSerializer(light, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors)

