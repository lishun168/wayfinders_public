from rest_framework import viewsets
from .serializers import MemberSerializer
from .serializers import MemberUserSerializer
from .models import Member
from .models import MemberUser


class MemberAPI(viewsets.ModelViewSet):
    serializer_class = MemberSerializer
    http_method_names = ['get', 'head', 'post', 'put']
    queryset = Member.objects.all()

class MemberUserAPI(viewsets.ModelViewSet):
    serializer_class = MemberUserSerializer
    http_method_names = ['get', 'head', 'post', 'put']
    queryset = MemberUser.objects.all()