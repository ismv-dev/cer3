from django.shortcuts import render
from rest_framework import viewsets
from core.models import Taller
from .serializers import TallerReadSerializer, TallerWriteSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class TallerViewSet(viewsets.ModelViewSet):
    queryset = Taller.objects.all()
    #filtrado de la data
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TallerReadSerializer
        return TallerWriteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]