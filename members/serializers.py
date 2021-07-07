from rest_framework import serializers
from .models import Member
from .models import MemberUser

class MemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Member
        fields = '__all__'

class MemberUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MemberUser
        fields = '__all__'