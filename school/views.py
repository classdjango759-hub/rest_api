from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.response import Response
from school.models import School
from school.serializers import (
    EstablishedSinceSerializer,
    SchoolSerializer,
    UpdateSchoolSerializer)
from rest_framework.mixins import (
    RetrieveModelMixin,
    ListModelMixin,
    UpdateModelMixin
)
from rest_framework.decorators import action
from rest_framework.permissions import (AllowAny,
IsAdminUser, IsAuthenticated, IsAuthenticatedOrReadOnly)
from rest_api.permissions import IsUserNameDjango2

class SchoolViewSet(ModelViewSet):
    serializer_class = SchoolSerializer
    queryset = School.objects.all()
    permission_classes = []

    def get_serializer_class(self):

        if self.action in ["update", "partial_update"]:
            return UpdateSchoolSerializer
        if self.action == "established_year":
            return EstablishedSinceSerializer

        return super().get_serializer_class()

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        if self.action == 'established_year':
            return [IsUserNameDjango2()]


        return super().get_permissions()

    # POST /schools/established-year
    @action(['POST'], detail=False, url_name="established-year", url_path='established-year')
    def established_year(self, request, *args, **kwargs):
        srlizer = self.get_serializer(data=request.data)
        srlizer.is_valid(raise_exception=True)

        year = srlizer.validated_data['established_year']
        schools = School.objects.filter(established_since=year)
        if not schools:
            return Response({"detail": "No schools found"}, status=404)

        srlized_school = self.serializer_class(schools, many=True)
        return Response(srlized_school.data)



class SchoolAccreditedViewSet(RetrieveModelMixin, ListModelMixin, 
                              UpdateModelMixin, GenericViewSet):
    serializer_class = SchoolSerializer

    queryset = School.objects.filter(is_accredited=True)

    def get_serializer_class(self):
        if self.action in ["update", "partial_update"]:
            return UpdateSchoolSerializer
        return super().get_serializer_class()