from rest_framework import viewsets
from .models import Competition
from .serializers import CompetitionSerializer

class CompetitionViewSet(viewsets.ModelViewSet):
    queryset = Competition.objects.all()
    serializer_class = CompetitionSerializer
