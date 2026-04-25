from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from .models import (
    Hero, QuienesSomos, NuestraHistoria, 
    Mision, Vision, Valor, Director,
    CommunitySupport, CommunityCategory, CommunityInitiative,
    FinancialDocument, FinancialStatementsConfig, MemoryDocument, MemoryConfig,
    PolicyDocument, PolicyCategory, PolicyConfig
)
from .serializers import (
    FinancialStatementsCompleteSerializer, HeroSerializer, MemoriesCompleteSerializer, PoliciesCompleteSerializer, QuienesSomosSerializer, NuestraHistoriaSerializer,
    MisionSerializer, VisionSerializer, ValorSerializer, DirectorSerializer,
    CommunitySupportSerializer, CommunityCategorySerializer, CommunityInitiativeSerializer,
    CommunitySupportCompleteSerializer, FinancialStatementsConfigSerializer, MemoryDocumentSerializer, MemoryConfigSerializer,
    PolicyDocumentSerializer, PolicyCategorySerializer, PolicyConfigSerializer
)

class AboutPagination(PageNumberPagination):
    page_size = 30
    page_size_query_param = 'page_size'
    max_page_size = 100

@extend_schema_view(
    list=extend_schema(
        summary="Listar elementos del Hero",
        description="Retorna una lista paginada de elementos del Hero activos",
        tags=['about']
    ),
    retrieve=extend_schema(
        summary="Obtener elemento del Hero",
        description="Retorna un elemento específico del Hero por ID",
        tags=['about']
    ),
    create=extend_schema(
        summary="Crear elemento del Hero",
        description="Crea un nuevo elemento del Hero",
        tags=['about']
    ),
    update=extend_schema(
        summary="Actualizar elemento del Hero",
        description="Actualiza completamente un elemento del Hero",
        tags=['about']
    ),
    partial_update=extend_schema(
        summary="Actualización parcial del Hero",
        description="Actualiza parcialmente un elemento del Hero",
        tags=['about']
    ),
    destroy=extend_schema(
        summary="Eliminar elemento del Hero",
        description="Elimina un elemento del Hero",
        tags=['about']
    )
)
class AboutViewSet(viewsets.ModelViewSet):
    pagination_class = AboutPagination
    queryset = Hero.objects.all()
    serializer_class = HeroSerializer
    
    def get_queryset(self):
        """
        Retorna el queryset apropiado según la acción
        """
        return Hero.objects.filter(is_active=True)
    
    def list(self, request, *args, **kwargs):
        """
        Listar elementos del Hero
        
        Retorna una lista paginada de elementos del Hero activos
        """
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        """
        Obtener elemento del Hero
        
        Retorna un elemento específico del Hero por ID
        """
        return super().retrieve(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        """
        Crear nuevo elemento del Hero
        
        Crea un nuevo elemento del Hero
        """
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """
        Actualizar elemento del Hero
        
        Actualiza un elemento específico del Hero por ID
        """
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """
        Actualización parcial del Hero
        
        Actualiza parcialmente un elemento específico del Hero por ID
        """
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """
        Eliminar elemento del Hero
        
        Elimina un elemento específico del Hero por ID
        """
        return super().destroy(request, *args, **kwargs)
    
    @extend_schema(
        summary="Obtener Hero Section",
        description="Retorna la información principal del hero section de ASOMAP",
        responses={200: HeroSerializer, 404: None},
        tags=['about']
    )
    @action(detail=False, methods=['get'], url_path='hero')
    def hero(self, request):
        """
        Obtener información del Hero Section
        
        Retorna la información principal del hero section de ASOMAP
        """
        try:
            hero = get_object_or_404(Hero.objects.filter(is_active=True))
            serializer = HeroSerializer(hero)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': 'Hero section not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @extend_schema(
        summary="Obtener Quiénes Somos",
        description="Retorna la información detallada sobre la institución ASOMAP",
        responses={200: QuienesSomosSerializer, 404: None},
        tags=['about']
    )
    @action(detail=False, methods=['get'], url_path='quienes-somos')
    def quienes_somos(self, request):
        """
        Obtener información 'Quiénes Somos'
        
        Retorna la información detallada sobre la institución ASOMAP
        """
        try:
            quienes_somos = get_object_or_404(QuienesSomos.objects.filter(is_active=True))
            serializer = QuienesSomosSerializer(quienes_somos)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': 'Quienes Somos not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'], url_path='nuestra-historia')
    def nuestra_historia(self, request):
        """
        Obtener historia de la institución

        Retorna la historia completa de ASOMAP desde su fundación
        """
        try:
            historia = get_object_or_404(NuestraHistoria.objects.filter(is_active=True))
            serializer = NuestraHistoriaSerializer(historia)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': 'Historia not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'], url_path='mision')
    def mision(self, request):
        """
        Obtener misión de la empresa
        
        Retorna la misión institucional de ASOMAP
        """
        try:
            mision = get_object_or_404(Mision.objects.filter(is_active=True))
            serializer = MisionSerializer(mision)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': 'Mision not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'], url_path='vision')
    def vision(self, request):
        """
        Obtener visión de la empresa
        
        Retorna la visión institucional de ASOMAP
        """
        try:
            vision = get_object_or_404(Vision.objects.filter(is_active=True))
            serializer = VisionSerializer(vision)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': 'Vision not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'], url_path='valores')
    def valores(self, request):
        """
        Obtener valores corporativos
        
        Retorna la lista de valores corporativos de ASOMAP
        """
        try:
            valores = Valor.objects.filter(is_active=True).order_by('-created_at')
            page = self.paginate_queryset(valores)
            if page is not None:
                serializer = ValorSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = ValorSerializer(valores, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': 'Valores not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'], url_path='consejo-directores')
    def consejo_directores(self, request):
        """
        Obtener consejo directivo
        
        Retorna la lista de miembros del consejo directivo de ASOMAP
        """
        try:
            directores = Director.objects.filter(is_active=True).order_by('-created_at')
            page = self.paginate_queryset(directores)
            if page is not None:
                serializer = DirectorSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = DirectorSerializer(directores, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': 'Consejo de directores not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @extend_schema(
        summary="Obtener categorías de apoyo comunitario",
        description="Retorna todas las categorías de apoyo comunitario activas",
        responses={200: CommunityCategorySerializer(many=True), 404: None},
        tags=['about']
    )
    @action(detail=False, methods=['get'], url_path='community-categories')
    def community_categories(self, request):
        """
        Obtener categorías de apoyo comunitario
        
        Retorna todas las categorías de apoyo comunitario activas
        """
        try:
            categories = CommunityCategory.objects.filter(is_active=True).order_by('id')
            page = self.paginate_queryset(categories)
            if page is not None:
                serializer = CommunityCategorySerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = CommunityCategorySerializer(categories, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': 'Community categories not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @extend_schema(
        summary="Obtener iniciativas de apoyo comunitario",
        description="Retorna todas las iniciativas de apoyo comunitario activas",
        responses={200: CommunityInitiativeSerializer(many=True), 404: None},
        tags=['about']
    )
    @action(detail=False, methods=['get'], url_path='community-initiatives')
    def community_initiatives(self, request):
        """
        Obtener iniciativas de apoyo comunitario
        
        Retorna todas las iniciativas de apoyo comunitario activas
        """
        try:
            initiatives = CommunityInitiative.objects.filter(is_active=True).select_related('category').order_by('category', 'id')
            page = self.paginate_queryset(initiatives)
            if page is not None:
                serializer = CommunityInitiativeSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = CommunityInitiativeSerializer(initiatives, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': 'Community initiatives not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @extend_schema(
        summary="Obtener información completa de apoyo comunitario",
        description="Retorna información completa de apoyo comunitario con categorías e iniciativas",
        responses={200: CommunitySupportCompleteSerializer, 404: None},
        tags=['about']
    )
    @action(detail=False, methods=['get'], url_path='community-support')
    def community_support(self, request):
        """
        Obtener información completa de apoyo comunitario
        
        Retorna información completa de apoyo comunitario con categorías e iniciativas
        """
        try:
            # Obtener la información principal de CommunitySupport
            community_support = get_object_or_404(CommunitySupport.objects.filter(is_active=True))
            
            # Obtener todas las categorías activas
            categories = CommunityCategory.objects.filter(is_active=True).order_by('id')
            
            # Obtener todas las iniciativas activas con sus categorías
            initiatives = CommunityInitiative.objects.filter(is_active=True).select_related('category').order_by('category', 'id')
            
            # Preparar la respuesta exacta que espera el frontend
            response_data = {
                'title': community_support.title,
                'description': community_support.description,
                'categories': CommunityCategorySerializer(categories, many=True).data,
                'initiatives': CommunityInitiativeSerializer(initiatives, many=True).data
            }
            
            # Retornar directamente los datos sin validación adicional
            return Response(response_data)
            
        except Exception as e:
            return Response(
                {'error': 'Community support not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @extend_schema(
        summary="Obtener información completa de estados financieros",
        description="Retorna información completa de estados financieros con documentos auditados y trimestrales",
        responses={200: FinancialStatementsCompleteSerializer, 404: None},
        tags=['about']
    )
    @action(detail=False, methods=['get'], url_path='financial-statements')
    def financial_statements(self, request):
        """
        Obtener información completa de estados financieros
        
        Retorna información completa de estados financieros con documentos auditados y trimestrales
        que coincide con la estructura esperada por el frontend
        """
        try:
            # Obtener la configuración activa
            config = FinancialStatementsConfig.objects.filter(is_active=True).first()
            if not config:
                config = FinancialStatementsConfig.objects.create(
                    title="Estados Financieros",
                    description="Consulta nuestros estados financieros auditados y trimestrales"
                )
            
            # Obtener todos los documentos financieros activos ordenados por año
            documents = FinancialDocument.objects.filter(is_active=True).order_by('-year', 'document_type', 'quarter')
            
            # Preparar la respuesta que coincide con la estructura del frontend
            response_data = {
                'title': config.title,
                'description': config.description,
                'years': []
            }
            
            # Agrupar documentos por año
            years_dict = {}
            for doc in documents:
                year = doc.year
                # Saltar documentos sin año
                if not year:
                    continue
                    
                if year not in years_dict:
                    years_dict[year] = {
                        'year': year,
                        'documents': {
                            'audited': [],
                            'quarterly': []
                        }
                    }
                
                doc_data = {
                    'title': doc.title,
                    'url': doc.file.url if doc.file else None
                }
                
                if doc.document_type == 'quarterly' and doc.quarter:
                    doc_data['quarter'] = doc.quarter
                    years_dict[year]['documents']['quarterly'].append(doc_data)
                else:
                    years_dict[year]['documents']['audited'].append(doc_data)
            
            # Convertir a lista y ordenar por año descendente
            # Filtrar años que no sean None y ordenar
            valid_years = [year_data for year_data in years_dict.values() if year_data['year'] is not None]
            response_data['years'] = sorted(
                valid_years, 
                key=lambda x: x['year'], 
                reverse=True
            )
            
            return Response(response_data)
            
        except Exception as e:
            return Response(
                {
                    'error': 'Financial statements not found',
                    'debug_info': {
                        'exception': str(e),
                        'documents_count': FinancialDocument.objects.count(),
                        'active_documents_count': FinancialDocument.objects.filter(is_active=True).count(),
                        'config_exists': FinancialStatementsConfig.objects.filter(is_active=True).exists()
                    }
                }, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @extend_schema(
        summary="Obtener información completa de memorias anuales",
        description="Retorna información completa de memorias anuales con documentos por año",
        responses={200: MemoriesCompleteSerializer, 404: None},
        tags=['about']
    )
    @action(detail=False, methods=['get'], url_path='memories')
    def memories(self, request):
        """
        Obtener información completa de memorias anuales
        
        Retorna información completa de memorias anuales con documentos por año
        que coincide con la estructura esperada por el frontend
        """
        try:
            # Obtener la configuración activa
            config = MemoryConfig.objects.filter(is_active=True).first()
            if not config:
                config = MemoryConfig.objects.create(
                    title="Memorias",
                    description="Un recorrido por nuestra historia y logros institucionales"
                )
            
            # Obtener todos los documentos de memoria activos ordenados por año
            documents = MemoryDocument.objects.filter(is_active=True).order_by('-year')
            
            # Preparar la respuesta que coincide con la estructura del frontend
            response_data = {
                'title': config.title,
                'description': config.description,
                'years': []
            }
            
            # Agrupar documentos por año
            years_dict = {}
            for doc in documents:
                year = doc.year
                # Saltar documentos sin año
                if not year:
                    continue
                    
                if year not in years_dict:
                    years_dict[year] = {
                        'year': year,
                        'documents': []
                    }
                
                # Agregar documento al año correspondiente
                years_dict[year]['documents'].append({
                    'url': doc.file.url if doc.file else None
                })
            
            # Convertir a lista y ordenar por año descendente
            valid_years = [year_data for year_data in years_dict.values() if year_data['year'] is not None]
            response_data['years'] = sorted(
                valid_years, 
                key=lambda x: x['year'], 
                reverse=True
            )
            
            return Response(response_data)
            
        except Exception as e:
            return Response(
                {
                    'error': 'Memories not found',
                    'debug_info': {
                        'exception': str(e),
                        'documents_count': MemoryDocument.objects.count(),
                        'active_documents_count': MemoryDocument.objects.filter(is_active=True).count(),
                        'config_exists': MemoryConfig.objects.filter(is_active=True).exists()
                    }
                }, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @extend_schema(
        summary="Obtener información completa de políticas organizacionales",
        description="Retorna información completa de políticas organizacionales con categorías y documentos",
        responses={200: PoliciesCompleteSerializer, 404: None},
        tags=['about']
    )
    @action(detail=False, methods=['get'], url_path='policies')
    def policies(self, request):
        """
        Obtener información completa de políticas organizacionales
        
        Retorna información completa de políticas organizacionales con categorías y documentos
        que coincide con la estructura esperada por el frontend
        """
        try:
            # Obtener la configuración activa
            config = PolicyConfig.objects.filter(is_active=True).first()
            if not config:
                config = PolicyConfig.objects.create(
                    title="Políticas",
                    description="Nuestras políticas institucionales garantizan la transparencia y eficiencia en nuestras operaciones.",
                    download_text="Descargar documento",
                    last_update_text="Última actualización",
                    all_policies_text="Todas las Políticas"
                )
            
            # Obtener todas las categorías activas con sus documentos
            categories = PolicyCategory.objects.filter(is_active=True).prefetch_related(
                'documents'
            ).order_by('title')
            
            # Preparar la respuesta que coincide con la estructura del frontend
            response_data = {
                'title': config.title,
                'description': config.description,
                'download_text': config.download_text,
                'last_update_text': config.last_update_text,
                'all_policies_text': config.all_policies_text,
                'categories': []
            }
            
            for category in categories:
                category_data = {
                    'title': category.title,
                    'icon': category.icon,
                    'description': category.description,
                    'documents': []
                }
                
                # Agregar documentos activos de la categoría
                for doc in category.documents.filter(is_active=True):
                    document_data = {
                        'title': doc.title,
                        'description': doc.description,
                        'url': doc.file.url if doc.file else None,
                        'lastUpdate': doc.last_update.strftime('%Y-%m-%d') if doc.last_update else None
                    }
                    category_data['documents'].append(document_data)
                
                response_data['categories'].append(category_data)
            
            return Response(response_data)
            
        except Exception as e:
            return Response(
                {
                    'error': 'Policies not found',
                    'debug_info': {
                        'exception': str(e),
                        'categories_count': PolicyCategory.objects.count(),
                        'active_categories_count': PolicyCategory.objects.filter(is_active=True).count(),
                        'documents_count': PolicyDocument.objects.count(),
                        'active_documents_count': PolicyDocument.objects.filter(is_active=True).count(),
                        'config_exists': PolicyConfig.objects.filter(is_active=True).exists()
                    }
                }, 
                status=status.HTTP_404_NOT_FOUND
            ) 