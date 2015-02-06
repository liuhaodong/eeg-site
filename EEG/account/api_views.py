from django.contrib.auth.models import User, Group
from EEG.account.serializers import UserSerializer, GroupSerializer
from rest_framework import viewsets

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    #queryset = User.objects.all()
    queryset=User.objects.all()[0:1]
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


