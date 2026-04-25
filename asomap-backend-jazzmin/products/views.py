from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from drf_spectacular.utils import extend_schema, extend_schema_view
from .models import Account, Loan, LoanType, Card, Certificate, Banner
from .serializers import (
    AccountSerializer, LoanSerializer, LoanTypeSerializer,
    CardSerializer, CertificateSerializer, BannerSerializer
)

class ProductsPagination(PageNumberPagination):
    page_size = 6
    page_size_query_param = 'page_size'
    max_page_size = 100

@extend_schema_view(
    list=extend_schema(
        summary="Listar cuentas",
        description="Retorna una lista paginada de cuentas activas",
        tags=['products']
    ),
    retrieve=extend_schema(
        summary="Obtener cuenta",
        description="Retorna una cuenta específica por ID",
        tags=['products']
    ),
    create=extend_schema(
        summary="Crear cuenta",
        description="Crea una nueva cuenta",
        tags=['products']
    ),
    update=extend_schema(
        summary="Actualizar cuenta",
        description="Actualiza completamente una cuenta",
        tags=['products']
    ),
    partial_update=extend_schema(
        summary="Actualización parcial de cuenta",
        description="Actualiza parcialmente una cuenta",
        tags=['products']
    ),
    destroy=extend_schema(
        summary="Eliminar cuenta",
        description="Elimina una cuenta",
        tags=['products']
    )
)
class ProductsViewSet(viewsets.ModelViewSet):
    pagination_class = ProductsPagination
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    
    def get_queryset(self):
        """
        Retorna el queryset apropiado según la acción
        """
        return Account.objects.filter(is_active=True)
    
    def list(self, request, *args, **kwargs):
        """
        Listar cuentas
        
        Retorna una lista paginada de cuentas activas
        """
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, *args, **kwargs):
        """
        Obtener cuenta
        
        Retorna una cuenta específica por ID
        """
        return super().retrieve(request, *args, **kwargs)
    
    def create(self, request, *args, **kwargs):
        """
        Crear cuenta
        
        Crea una nueva cuenta
        """
        return super().create(request, *args, **kwargs)
    
    def update(self, request, *args, **kwargs):
        """
        Actualizar cuenta
        
        Actualiza completamente una cuenta
        """
        return super().update(request, *args, **kwargs)
    
    def partial_update(self, request, *args, **kwargs):
        """
        Actualización parcial de cuenta
        
        Actualiza parcialmente una cuenta
        """
        return super().partial_update(request, *args, **kwargs)
    
    def destroy(self, request, *args, **kwargs):
        """
        Eliminar cuenta
        
        Elimina una cuenta
        """
        return super().destroy(request, *args, **kwargs)
    
    @extend_schema(
        summary="Obtener productos de cuentas",
        description="Retorna todos los productos de cuentas disponibles en ASOMAP",
        responses={200: AccountSerializer(many=True), 404: None},
        tags=['products']
    )
    @action(detail=False, methods=['get'], url_path='accounts')
    def accounts(self, request):
        """
        Obtener productos de cuentas
        
        Retorna todos los productos de cuentas disponibles en ASOMAP
        """
        try:
            accounts = Account.objects.filter(is_active=True).order_by('-created_at')
            page = self.paginate_queryset(accounts)
            if page is not None:
                serializer = AccountSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = AccountSerializer(accounts, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': 'Accounts not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @extend_schema(
        summary="Obtener cuenta por slug",
        description="Retorna una cuenta específica por su slug (título convertido a URL amigable)",
        responses={200: AccountSerializer, 404: None},
        tags=['products']
    )
    @action(detail=False, methods=['get'], url_path='accounts/(?P<slug>[^/.]+)')
    def account_by_slug(self, request, slug=None):
        """
        Obtener cuenta por slug
        
        Retorna una cuenta específica por su slug (título convertido a URL amigable)
        """
        try:
            # Buscar por slug (título convertido a slug)
            account = Account.objects.filter(
                is_active=True,
                title__icontains=slug.replace('-', ' ')
            ).first()
            
            if not account:
                return Response(
                    {'error': f'Account with slug "{slug}" not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            serializer = AccountSerializer(account)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': 'Account not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    def get_account_by_id(self, request, pk=None):
        """
        Obtener cuenta por ID
        
        Retorna una cuenta específica por su ID
        """
        try:
            account = Account.objects.filter(
                is_active=True,
                id=pk
            ).first()
            
            if not account:
                return Response(
                    {'error': f'Account with ID "{pk}" not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            serializer = AccountSerializer(account)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': 'Account not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'], url_path='loans')
    def loans(self, request):
        """
        Obtener productos de préstamos hipotecarios

        Retorna todos los productos de préstamos hipotecarios disponibles en ASOMAP
        """
        try:
            loans = Loan.objects.filter(is_active=True).order_by('-created_at')
            page = self.paginate_queryset(loans)
            if page is not None:
                serializer = LoanSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = LoanSerializer(loans, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': 'Loans not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )


    @extend_schema(
        summary="Obtener préstamo por slug",
        description="Retorna un préstamo específico por su slug (título convertido a URL amigable)",
        responses={200: LoanSerializer, 404: None},
        tags=['products']
    )
    @action(detail=False, methods=['get'], url_path='loans/(?P<slug>[^/.]+)')
    def loan_by_slug(self, request, slug=None):
        """
        Obtener préstamo por slug
        
        Retorna un préstamo específico por su slug (título convertido a URL amigable)
        """
        try:
            # Buscar por slug (título convertido a slug)
            loan = Loan.objects.filter(
                is_active=True,
                title__icontains=slug.replace('-', ' ')
            ).first()
            
            if not loan:
                return Response(
                    {'error': f'Loan with slug "{slug}" not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            serializer = LoanSerializer(loan)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': 'Loan not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    def get_loan_by_id(self, request, pk=None):
        """
        Obtener préstamo por ID
        
        Retorna un préstamo específico por su ID
        """
        try:
            loan = Loan.objects.filter(
                is_active=True,
                id=pk
            ).first()
            
            if not loan:
                return Response(
                    {'error': f'Loan with ID "{pk}" not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            serializer = LoanSerializer(loan)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': 'Loan not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'], url_path='cards')
    def cards(self, request):
        """
        Obtener productos de tarjetas
        
        Retorna todos los productos de tarjetas disponibles en ASOMAP
        """
        try:
            cards = Card.objects.filter(is_active=True).order_by('-created_at')
            page = self.paginate_queryset(cards)
            if page is not None:
                serializer = CardSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = CardSerializer(cards, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': 'Cards not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @extend_schema(
        summary="Obtener tarjeta por slug",
        description="Retorna una tarjeta específica por su slug (título convertido a URL amigable)",
        responses={200: CardSerializer, 404: None},
        tags=['products']
    )
    @action(detail=False, methods=['get'], url_path='cards/(?P<slug>[^/.]+)')
    def card_by_slug(self, request, slug=None):
        """
        Obtener tarjeta por slug
        
        Retorna una tarjeta específica por su slug (título convertido a URL amigable)
        """
        try:
            # Buscar por slug (título convertido a slug)
            card = Card.objects.filter(
                is_active=True,
                title__icontains=slug.replace('-', ' ')
            ).first()
            
            if not card:
                return Response(
                    {'error': f'Card with slug "{slug}" not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            serializer = CardSerializer(card)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': 'Card not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    def get_card_by_id(self, request, pk=None):
        """
        Obtener tarjeta por ID
        
        Retorna una tarjeta específica por su ID
        """
        try:
            card = Card.objects.filter(
                is_active=True,
                id=pk
            ).first()
            
            if not card:
                return Response(
                    {'error': f'Card with ID "{pk}" not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            serializer = CardSerializer(card)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': 'Card not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    @action(detail=False, methods=['get'], url_path='certificates')
    def certificates(self, request):
        """
        Obtener certificados financieros
        
        Retorna todos los certificados financieros disponibles en ASOMAP
        """
        try:
            certificates = Certificate.objects.filter(is_active=True).order_by('-created_at')
            page = self.paginate_queryset(certificates)
            if page is not None:
                serializer = CertificateSerializer(page, many=True)
                return self.get_paginated_response(serializer.data)
            serializer = CertificateSerializer(certificates, many=True)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': 'Certificates not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    @extend_schema(
        summary="Obtener certificado por slug",
        description="Retorna un certificado específico por su slug (título convertido a URL amigable)",
        responses={200: CertificateSerializer, 404: None},
        tags=['products']
    )
    @action(detail=False, methods=['get'], url_path='certificates/(?P<slug>[^/.]+)')
    def certificate_by_slug(self, request, slug=None):
        """
        Obtener certificado por slug
        
        Retorna un certificado específico por su slug (título convertido a URL amigable)
        """
        try:
            # Buscar por slug (título convertido a slug)
            certificate = Certificate.objects.filter(
                is_active=True,
                title__icontains=slug.replace('-', ' ')
            ).first()
            
            if not certificate:
                return Response(
                    {'error': f'Certificate with slug "{slug}" not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            serializer = CertificateSerializer(certificate)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': 'Certificate not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

    def get_certificate_by_id(self, request, pk=None):
        """
        Obtener certificado por ID
        
        Retorna un certificado específico por su ID
        """
        try:
            certificate = Certificate.objects.filter(
                is_active=True,
                id=pk
            ).first()
            
            if not certificate:
                return Response(
                    {'error': f'Certificate with ID "{pk}" not found'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            
            serializer = CertificateSerializer(certificate)
            return Response(serializer.data)
        except Exception as e:
            return Response(
                {'error': 'Certificate not found'}, 
                status=status.HTTP_404_NOT_FOUND
            )

@extend_schema_view(
    list=extend_schema(
        summary="Listar banners",
        description="Retorna una lista de banners activos ordenados por prioridad",
        tags=["Banners"]
    ),
    retrieve=extend_schema(
        summary="Obtener banner",
        description="Retorna los detalles de un banner específico",
        tags=["Banners"]
    )
)
class BannerViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para manejar banners promocionales
    """
    queryset = Banner.objects.filter(is_active=True).order_by("order", "title")
    serializer_class = BannerSerializer
    pagination_class = None  # Los banners no necesitan paginación
    
    @extend_schema(
        summary="Obtener banner principal",
        description="Retorna el banner principal (el de mayor prioridad)",
        tags=["Banners"]
    )
    @action(detail=False, methods=["get"])
    def main(self, request):
        """
        Retorna el banner principal (el de mayor prioridad)
        """
        try:
            banner = self.queryset.first()
            if banner:
                serializer = BannerSerializer(banner)
                return Response(serializer.data)
            else:
                return Response(
                    {"error": "No active banners found"}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        except Exception as e:
            return Response(
                {"error": "Error retrieving main banner"}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


@extend_schema_view(
    list=extend_schema(
        summary="Listar tipos de préstamos",
        description="Retorna una lista de tipos de préstamos activos ordenados por prioridad",
        tags=["Tipos de Préstamos"]
    ),
    retrieve=extend_schema(
        summary="Obtener tipo de préstamo",
        description="Retorna los detalles de un tipo de préstamo específico",
        tags=["Tipos de Préstamos"]
    )
)
class LoanTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    ViewSet para manejar tipos de préstamos
    """
    queryset = LoanType.objects.filter(is_active=True).order_by("order", "name")
    serializer_class = LoanTypeSerializer
    pagination_class = None  # Los tipos de préstamos no necesitan paginación
