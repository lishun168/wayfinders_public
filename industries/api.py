from rest_framework import viewsets
from .models import Industry
from .serializers import IndustrySerializer

class IndustryAPI(viewsets.ModelViewSet):
    serializer_class = IndustrySerializer
    http_method_names = ['get', 'head', 'post', 'put']
    queryset = Industry.objects.all()