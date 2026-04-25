from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from .models import Location
from .serializers import LocationSerializer


# Create your views here.

class LocationViewSet(viewsets.ModelViewSet):
    """
    ViewSet para ubicaciones (sucursales y cajeros automáticos)
    """
    queryset = Location.objects.filter(is_active=True)
    serializer_class = LocationSerializer
    pagination_class = None  # Deshabilitar paginación para devolver todas las ubicaciones
    
    @extend_schema(
        summary="Listar ubicaciones",
        description="Retorna todas las ubicaciones activas",
        responses={200: LocationSerializer(many=True)},
        tags=['locations']
    )
    def list(self, request, *args, **kwargs):
        """
        Listar ubicaciones

        Retorna todas las ubicaciones activas ordenadas por tipo y nombre
        """
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    @extend_schema(
        summary="Obtener ubicación",
        description="Retorna una ubicación específica por ID",
        responses={200: LocationSerializer, 404: None},
        tags=['locations']
    )
    def retrieve(self, request, *args, **kwargs):
        """
        Obtener ubicación
        
        Retorna una ubicación específica por ID
        """
        return super().retrieve(request, *args, **kwargs)
    
    @extend_schema(
        summary="Obtener sucursales",
        description="Retorna todas las sucursales activas",
        responses={200: LocationSerializer(many=True)},
        tags=['locations']
    )
    @action(detail=False, methods=['get'], url_path='branches')
    def branches(self, request):
        """
        Obtener sucursales
        
        Retorna todas las sucursales activas
        """
        try:
            branches = Location.objects.filter(
                type='branch',
                is_active=True
            ).order_by('name')
            
            serializer = self.get_serializer(branches, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {
                    'error': 'Branches not found',
                    'debug_info': {
                        'exception': str(e),
                        'branches_count': Location.objects.filter(type='branch', is_active=True).count()
                    }
                },
                status=status.HTTP_404_NOT_FOUND
            )
    
    @extend_schema(
        summary="Obtener cajeros automáticos",
        description="Retorna todos los cajeros automáticos activos",
        responses={200: LocationSerializer(many=True)},
        tags=['locations']
    )
    @action(detail=False, methods=['get'], url_path='atms')
    def atms(self, request):
        """
        Obtener cajeros automáticos
        
        Retorna todos los cajeros automáticos activos
        """
        try:
            atms = Location.objects.filter(
                type='atm',
                is_active=True
            ).order_by('name')
            
            serializer = self.get_serializer(atms, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {
                    'error': 'ATMs not found',
                    'debug_info': {
                        'exception': str(e),
                        'atms_count': Location.objects.filter(type='atm', is_active=True).count()
                    }
                },
                status=status.HTTP_404_NOT_FOUND
            )
