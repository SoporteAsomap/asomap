from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from django.shortcuts import get_object_or_404
from .models import (
    AbandonedAccountsSection, AccountType, YearlyDocument,
    ContractCategory, AccountContractsSection, Contract, ClaimRequest, FraudReport, RightsAndDutiesPage, ServiceRatesPage, ServiceCategory, SuggestionBox, Province, SuggestionBoxPage, FraudReportPage, ClaimRequestPage
)
from .serializers import (
    AbandonedAccountsSectionSerializer,
    AccountTypeSerializer,
    YearlyDocumentSerializer,
    ContractCategorySerializer,
    AccountContractsSectionSerializer,
    ContractSerializer,
    ClaimRequestSerializer,
    FraudReportSerializer,
    RightsAndDutiesPageSerializer,
    ServiceRatesPageSerializer,
    ServiceCategorySerializer,
    SuggestionBoxSerializer,
    ProvinceSerializer,
    SuggestionBoxPageSerializer,
    FraudReportPageSerializer,
    ClaimRequestPageSerializer
)
from .utils import send_claim_confirmation_email, send_fraud_confirmation_email, send_suggestion_confirmation_email


class AbandonedAccountsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class AbandonedAccountsSectionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para manejar las secciones de cuentas abandonadas e inactivas
    """
    queryset = AbandonedAccountsSection.objects.filter(is_active=True)
    serializer_class = AbandonedAccountsSectionSerializer
    pagination_class = AbandonedAccountsPagination
    
    def get_queryset(self):
        """Retorna todas las secciones activas sin optimizaciones que limiten los documentos"""
        return super().get_queryset().prefetch_related('account_types')


class AccountTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para manejar los tipos de cuenta
    """
    queryset = AccountType.objects.filter(is_active=True)
    serializer_class = AccountTypeSerializer


class YearlyDocumentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para manejar los documentos anuales
    """
    queryset = YearlyDocument.objects.filter(is_active=True)
    serializer_class = YearlyDocumentSerializer
    
    def get_queryset(self):
        """Optimiza las consultas con select_related"""
        return super().get_queryset().select_related('account_type')
    
    @action(detail=False, methods=['get'])
    def by_year(self, request):
        """Obtiene documentos agrupados por año"""
        year = request.query_params.get('year')
        account_type = request.query_params.get('account_type')
        
        queryset = self.get_queryset()
        
        if year:
            queryset = queryset.filter(year=year)
        
        if account_type:
            queryset = queryset.filter(account_type__id=account_type)
        
        # Agrupar por año
        years_data = {}
        for doc in queryset:
            year = doc.year
            if year not in years_data:
                years_data[year] = {
                    'year': year,
                    'documents': {}
                }
            
            years_data[year]['documents'][doc.account_type.id] = {
                'title': doc.title,
                'url': doc.document_url,
                'date': doc.formatted_date,
                'type': doc.type
            }
        
        # Convertir a lista y ordenar por año descendente
        results = sorted(years_data.values(), key=lambda x: x['year'], reverse=True)
        
        return Response({
            'count': len(results),
            'results': results
        })


class ContractCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para manejar las categorías de contratos
    """
    queryset = ContractCategory.objects.filter(is_active=True)
    serializer_class = ContractCategorySerializer


class AccountContractsSectionViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para manejar las secciones de contratos de adhesión
    """
    queryset = AccountContractsSection.objects.filter(is_active=True)
    serializer_class = AccountContractsSectionSerializer
    pagination_class = AbandonedAccountsPagination


class ContractViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para manejar los contratos individuales
    """
    queryset = Contract.objects.filter(is_active=True)
    serializer_class = ContractSerializer
    
    def get_queryset(self):
        """Optimiza las consultas con select_related"""
        return super().get_queryset().select_related('category')
    
    @action(detail=False, methods=['get'])
    def by_category(self, request):
        """Obtiene contratos agrupados por categoría"""
        category_name = request.query_params.get('category')
        
        queryset = self.get_queryset()
        
        if category_name:
            queryset = queryset.filter(category__name=category_name)
        
        # Agrupar por categoría
        categories_data = {}
        for contract in queryset:
            category_name = contract.category.name
            if category_name not in categories_data:
                categories_data[category_name] = []
            
            categories_data[category_name].append({
                'title': contract.title,
                'url': contract.document_url,
                'category': contract.category.name
            })
        
        return Response({
            'count': len(categories_data),
            'results': categories_data
        })


class ClaimRequestViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar las solicitudes de reclamos
    Permite crear desde el frontend y gestionar desde el admin
    """
    queryset = ClaimRequest.objects.all()
    serializer_class = ClaimRequestSerializer
    
    def get_queryset(self):
        """Optimiza las consultas"""
        return super().get_queryset().order_by('-created_at')
    
    def create(self, request, *args, **kwargs):
        """Crear una nueva solicitud de reclamo"""
        serializer = self.get_serializer(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        claim_request = serializer.save()
        
        # Enviar email de confirmación
        try:
            send_claim_confirmation_email(claim_request)
        except Exception as e:
            print(f"Error enviando email: {str(e)}")
            # No fallar la creación si el email falla
        
        return Response(
            {
                'message': 'Solicitud de reclamo enviada exitosamente'
            },
            status=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        """Solo permitir actualizar desde el admin"""
        return Response(
            {'error': 'No se permite actualizar desde la API'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    def partial_update(self, request, *args, **kwargs):
        """Solo permitir actualizar desde el admin"""
        return Response(
            {'error': 'No se permite actualizar desde la API'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    def destroy(self, request, *args, **kwargs):
        """No permitir eliminar desde la API"""
        return Response(
            {'error': 'No se permite eliminar desde la API'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


class FraudReportViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar los reportes de fraude
    Permite crear desde el frontend y gestionar desde el admin
    """
    queryset = FraudReport.objects.all()
    serializer_class = FraudReportSerializer
    
    def get_queryset(self):
        """Optimiza las consultas"""
        return super().get_queryset().order_by('-created_at')
    
    def create(self, request, *args, **kwargs):
        """Crear un nuevo reporte de fraude"""
        print("=== DATOS RECIBIDOS ===")
        print(f"Content-Type: {request.content_type}")
        print(f"Data: {request.data}")
        print(f"Data type: {type(request.data)}")
        print(f"Data keys: {list(request.data.keys()) if hasattr(request.data, 'keys') else 'No keys'}")
        print(f"Files: {request.FILES}")
        print(f"Request headers: {dict(request.headers)}")
        print("=======================")
        
        # Crear datos combinados
        combined_data = {}
        
        # Intentar obtener datos del request.data
        if hasattr(request.data, 'dict'):
            combined_data.update(request.data.dict())
        elif isinstance(request.data, dict):
            combined_data.update(request.data)
        else:
            # Si es QueryDict, convertir a dict
            combined_data.update(dict(request.data))
        
        # Agregar archivos
        if request.FILES:
            combined_data.update(request.FILES)
        
        print(f"Data final: {combined_data}")
        
        # Si no hay datos, devolver error
        if not combined_data:
            return Response(
                {
                    'error': 'No se recibieron datos en la request',
                    'content_type': request.content_type,
                    'data_keys': list(request.data.keys()) if hasattr(request.data, 'keys') else []
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = self.get_serializer(data=combined_data)
        
        if not serializer.is_valid():
            print(f"Errores de validación: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        fraud_report = serializer.save()
        
        # Enviar email de confirmación
        try:
            send_fraud_confirmation_email(fraud_report)
        except Exception as e:
            print(f"Error enviando email: {str(e)}")
            # No fallar la creación si el email falla
        
        return Response(
            {
                'message': 'Reporte de fraude enviado exitosamente'
            },
            status=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        """Solo permitir actualizar desde el admin"""
        return Response(
            {'error': 'No se permite actualizar desde la API'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    def partial_update(self, request, *args, **kwargs):
        """Solo permitir actualizar desde el admin"""
        return Response(
            {'error': 'No se permite actualizar desde la API'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    def destroy(self, request, *args, **kwargs):
        """No permitir eliminar desde la API"""
        return Response(
            {'error': 'No se permite eliminar desde la API'},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


class RightsAndDutiesPageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para manejar la página de derechos y deberes
    Solo permite lectura (GET)
    """
    queryset = RightsAndDutiesPage.objects.filter(is_active=True)
    serializer_class = RightsAndDutiesPageSerializer
    
    def get_queryset(self):
        """Retorna solo la página activa"""
        return RightsAndDutiesPage.objects.filter(is_active=True)


class ServiceRatesPageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para manejar la página de tarifas de servicios
    Solo permite lectura (GET)
    """
    queryset = ServiceRatesPage.objects.filter(is_active=True)
    serializer_class = ServiceRatesPageSerializer
    
    def get_queryset(self):
        """Retorna solo la página activa"""
        return super().get_queryset().filter(
            is_active=True
        )


class ServiceCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para manejar categorías de servicios
    Solo permite lectura (GET)
    """
    queryset = ServiceCategory.objects.filter(is_active=True).prefetch_related('rates')
    serializer_class = ServiceCategorySerializer
    
    def get_queryset(self):
        """Retorna solo categorías activas con sus tarifas"""
        return super().get_queryset().prefetch_related(
            'rates'
        ).filter(
            is_active=True,
            rates__is_active=True
        ).distinct()


class ProvinceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para manejar provincias
    Solo permite lectura (GET)
    """
    queryset = Province.objects.filter(is_active=True)
    serializer_class = ProvinceSerializer
    
    def get_queryset(self):
        """Retorna solo provincias activas"""
        return super().get_queryset().filter(is_active=True)


class SuggestionBoxViewSet(viewsets.ModelViewSet):
    """
    ViewSet para manejar el buzón de sugerencias
    Permite crear desde el frontend, pero no actualizar/eliminar
    """
    queryset = SuggestionBox.objects.all()
    serializer_class = SuggestionBoxSerializer
    
    def create(self, request, *args, **kwargs):
        """Crear una nueva sugerencia desde el frontend"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        # Enviar email de confirmación
        try:
            send_suggestion_confirmation_email(serializer.instance)
        except Exception as e:
            print(f"Error enviando email de confirmación: {e}")
        
        return Response(
            {"message": "Sugerencia enviada exitosamente. Gracias por tu feedback."},
            status=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        """No permitir actualizaciones desde el frontend"""
        return Response(
            {"error": "No se permiten actualizaciones desde el frontend"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    def partial_update(self, request, *args, **kwargs):
        """No permitir actualizaciones parciales desde el frontend"""
        return Response(
            {"error": "No se permiten actualizaciones desde el frontend"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    def destroy(self, request, *args, **kwargs):
        """No permitir eliminaciones desde el frontend"""
        return Response(
            {"error": "No se permiten eliminaciones desde el frontend"},
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )


class SuggestionBoxPageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para manejar la página del buzón de sugerencias
    Solo permite lectura (GET)
    """
    queryset = SuggestionBoxPage.objects.filter(is_active=True)
    serializer_class = SuggestionBoxPageSerializer
    
    def get_queryset(self):
        """Retorna solo la página activa"""
        return SuggestionBoxPage.objects.filter(is_active=True)


class FraudReportPageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para manejar la página de reportes de fraude
    Solo permite lectura (GET)
    """
    queryset = FraudReportPage.objects.filter(is_active=True)
    serializer_class = FraudReportPageSerializer
    
    def get_queryset(self):
        """Retorna solo la página activa"""
        return FraudReportPage.objects.filter(is_active=True)


class ClaimRequestPageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para manejar la página de solicitudes de reclamaciones
    Solo permite lectura (GET)
    """
    queryset = ClaimRequestPage.objects.filter(is_active=True)
    serializer_class = ClaimRequestPageSerializer
    
    def get_queryset(self):
        """Retorna solo la página activa"""
        return ClaimRequestPage.objects.filter(is_active=True)
