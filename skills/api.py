from rest_framework import viewsets
from .serializers import SkillSerializer
from .models import Skill

class SkillAPI(viewsets.ModelViewSet):
    serializer_class = SkillSerializer
    http_method_names = ['get', 'head', 'post', 'put']
    queryset = Skill.objects.all()