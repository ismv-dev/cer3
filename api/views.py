from rest_framework import viewsets
from core.models import Taller
from .serializers import TallerReadSerializer, TallerWriteSerializer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.decorators import login_required

class TallerViewSet(viewsets.ModelViewSet):
    queryset = Taller.objects.all()
    permission_classes = [IsAuthenticated]
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TallerReadSerializer
        return TallerWriteSerializer
    