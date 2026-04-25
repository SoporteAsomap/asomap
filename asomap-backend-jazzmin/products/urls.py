from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductsViewSet, BannerViewSet, LoanTypeViewSet

# Router estándar (lowercase)
router = DefaultRouter()
router.register(r'products', ProductsViewSet, basename='products')
router.register(r'banners', BannerViewSet, basename='banners')
router.register(r'loan-types', LoanTypeViewSet, basename='loan-types')

# Router adicional para endpoints EXACTOS (mayúsculas, sin slash final)
class NoSlashRouter(DefaultRouter):
    trailing_slash = ''

router_caps = NoSlashRouter()
router_caps.register(r'products', ProductsViewSet, basename='products-exact')  # mismo path, sin slash

# URLs específicas para cuentas, tarjetas y certificados
urlpatterns = [
    # Rutas para cuentas por slug
    path('productos/cuenta/<str:slug>/', ProductsViewSet.as_view({
        'get': 'account_by_slug'
    }), name='account-by-slug'),
    
    # Rutas para cuentas por ID
    path('productos/cuenta/<int:pk>/', ProductsViewSet.as_view({
        'get': 'get_account_by_id'
    }), name='account-by-id'),
    
    # Rutas para tarjetas por slug
    path('productos/tarjeta/<str:slug>/', ProductsViewSet.as_view({
        'get': 'card_by_slug'
    }), name='card-by-slug'),
    
    # Rutas para tarjetas por ID
    path('productos/tarjeta/<int:pk>/', ProductsViewSet.as_view({
        'get': 'get_card_by_id'
    }), name='card-by-id'),
    
    # Rutas para préstamos por slug
    path('productos/prestamo/<str:slug>/', ProductsViewSet.as_view({
        'get': 'loan_by_slug'
    }), name='loan-by-slug'),
    
    # Rutas para préstamos por ID
    path('productos/prestamo/<int:pk>/', ProductsViewSet.as_view({
        'get': 'get_loan_by_id'
    }), name='loan-by-id'),
    
    # Rutas para certificados por slug
    path('productos/certificado/<str:slug>/', ProductsViewSet.as_view({
        'get': 'certificate_by_slug'
    }), name='certificate-by-slug'),
    
    # Rutas para certificados por ID
    path('productos/certificado/<int:pk>/', ProductsViewSet.as_view({
        'get': 'get_certificate_by_id'
    }), name='certificate-by-id'),
    
    # Rutas adicionales para compatibilidad con endpoints generales
    path('products/cards/<str:slug>/', ProductsViewSet.as_view({
        'get': 'card_by_slug'
    }), name='products-cards-by-slug'),
    
    path('products/accounts/<str:slug>/', ProductsViewSet.as_view({
        'get': 'account_by_slug'
    }), name='products-accounts-by-slug'),
    
    
    
    path('products/loans/<str:slug>/', ProductsViewSet.as_view({
        'get': 'loan_by_slug'
    }), name='products-loans-by-slug'),
    
    path('products/certificates/<str:slug>/', ProductsViewSet.as_view({
        'get': 'certificate_by_slug'
    }), name='products-certificates-by-slug'),
]

urlpatterns += router.urls
urlpatterns += router_caps.urls
