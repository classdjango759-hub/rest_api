from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from django.contrib.auth.models import User
from .serializers import ChangeUserFullName, HelloSerializer, UserModelSerializer, UserSerializer
from drf_spectacular.utils import extend_schema

# Function-based view
@extend_schema(request=HelloSerializer, methods=["POST"])
@api_view(['POST'])
def hello(request):
    """This endpoint display Hello + the username provided"""

    serializer = HelloSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    data = serializer.validated_data
    name = data.get("name")

    return Response({
        "data": f"Hello, {name}",
        "message": "Welcome to the Django REST API"
    })

# Class-based view
class HelloView(APIView):
    serializer_class = HelloSerializer

    def post(self, request):
        from datetime import datetime
        return Response({
            "data": "Hello, World!",
            "now": datetime.now(),
            "message": "Welcome to the Django REST API"
        })

class UserView(APIView):
    serializer_class = UserSerializer

    def post(self, request):
        srlizer = self.serializer_class(data=request.data)
        srlizer.is_valid(raise_exception=True)

        data = srlizer.validated_data
        # data["username"] KeyError
        # data.get("username", "Default value") # 
        return Response({
                "username": data.get("username"),
                "email": data['email'],
                "first_name": data['first_name'],
                "last_name": data['last_name']
        }, status=status.HTTP_201_CREATED)

class UserViewSet(ModelViewSet):
    serializer_class = UserModelSerializer
    queryset = User.objects.all()
    # permission_classes = []
     
    # get_object() handles how the endpoint retrieves single model object from the database
    def get_object(self):
        return self.request.user 

    def get_queryset(self):
        return super().get_queryset()
    # get_serializer_class()
    def get_serializer_class(self):
        if self.action in ['update', 'partial_update']:
            return ChangeUserFullName
        return super().get_serializer_class()

    def get_permissions(self):
        return super().get_permissions()

    # list() -> get
    def list(self, request, *args, **kwargs):
        users = self.queryset.exclude(username__iexact='rest_api')
        serializer = self.get_serializer(users, many=True)
        if (serializer.data == []):
            return Response({
                'detail': "No users available"
            })
        
        return Response({
            "data": serializer.data
        })
    # retrieve() -> get
    # create() -> post
    # update() -> PUT
    # partial_update() -> PATCH
    # destroy() -> DELETE


"""
App name: school
Endpoint name: /api/schools

Model: School
    - name
    - avg_student_per_year
    - is_accredited
    - established_since

Serializer:
    Use a general model serializer SchoolSerializer
    Use UpdateSchoolSerializer that has two fields:
        - avg_student_per_year
        - is_accredited

ModelViewSet
    - SchoolViewSet
    - SchoolAccreditedViewSet
"""