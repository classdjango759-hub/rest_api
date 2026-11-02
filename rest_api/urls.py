"""
URL configuration for rest_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api.views import hello, HelloView, UserView, UserViewSet
from drf_spectacular.views import (
    SpectacularSwaggerView,
    SpectacularRedocView,
    SpectacularAPIView)
from rest_framework import routers
from school.views import SchoolAccreditedViewSet, SchoolViewSet

router = routers.DefaultRouter()
router.register("users", UserViewSet, "users")
router.register("schools", SchoolViewSet, "schools")
router.register("accredited-schools", SchoolAccreditedViewSet, "accredited-schools")

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/hello/",hello, name="hello" ),
    path("api/hello_with_class/", HelloView.as_view(), name="hello_with_class"),
    path("api/user/", UserView.as_view(), name='user'),
    path("api/schema", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"), # Swagger UI
    path("api/docs/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"), # Redoc UI

] + router.urls

# Serialization is the process of converting complex data types,
# such as Django models or Python objects, into a format that can
# be easily rendered into JSON, XML, or other content types.
#

# Deserialization is the reverse process, where data in a specific format
# (like JSON or XML) is converted back into complex data types, such as
# Django models or Python objects.


