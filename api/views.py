from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from core.models import Taller
from .serializers import TallerReadSerializer, TallerWriteSerializer
from django.contrib.auth.decorators import login_required
import logging

logger = logging.getLogger(__name__)

class TallerViewSet(viewsets.ModelViewSet):
    queryset = Taller.objects.all()
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        """Filter queryset based on user permissions"""
        if self.request.user.is_staff:
            return Taller.objects.all()
        else:
            # Non-staff users can only see accepted workshops
            return Taller.objects.filter(estado='aceptado')
    
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return TallerReadSerializer
        return TallerWriteSerializer
    
    def perform_create(self, serializer):
        """Set default values for non-staff users"""
        if not self.request.user.is_staff:
            serializer.save(estado='pendiente', observacion='')
        else:
            serializer.save()
    
    def perform_update(self, serializer):
        """Only staff users can update status and observations"""
        if not self.request.user.is_staff:
            # Remove fields that non-staff users shouldn't modify
            if 'estado' in serializer.validated_data:
                del serializer.validated_data['estado']
            if 'observacion' in serializer.validated_data:
                del serializer.validated_data['observacion']
        serializer.save()
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def approve(self, request, pk=None):
        """Approve a workshop (admin only)"""
        try:
            taller = self.get_object()
            taller.estado = 'aceptado'
            taller.save()
            return Response({'status': 'workshop approved'})
        except Exception as e:
            logger.error(f"Error approving workshop: {e}")
            return Response(
                {'error': 'Error al aprobar el taller'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    @action(detail=True, methods=['post'], permission_classes=[IsAdminUser])
    def reject(self, request, pk=None):
        """Reject a workshop (admin only)"""
        try:
            taller = self.get_object()
            taller.estado = 'rechazado'
            taller.save()
            return Response({'status': 'workshop rejected'})
        except Exception as e:
            logger.error(f"Error rejecting workshop: {e}")
            return Response(
                {'error': 'Error al rechazar el taller'}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    