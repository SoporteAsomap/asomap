from rest_framework import serializers
from .models import (
    AccountType, AbandonedAccountsSection, YearlyDocument,
    ContractCategory, AccountContractsSection, Contract, ClaimRequest, FraudReport,
    RightsAndDutiesImage, RightsAndDutiesSection, RightsAndDutiesPage,
    ServiceRate, ServiceCategory, ServiceRatesPage, SuggestionBox, Province, SuggestionBoxPage, FraudReportPage, ClaimRequestPage
)


class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = ['id', 'label', 'description']


class YearlyDocumentSerializer(serializers.ModelSerializer):
    document_url = serializers.SerializerMethodField()
    
    class Meta:
        model = YearlyDocument
        fields = ['title', 'document_url', 'date', 'type']
    
    def get_document_url(self, obj):
        """Retorna la URL del documento"""
        return obj.document_url


class YearDocumentsSerializer(serializers.Serializer):
    """Serializer para agrupar documentos por año"""
    year = serializers.CharField()
    documents = serializers.SerializerMethodField()
    
    def get_documents(self, obj):
        """Agrupa documentos por tipo de cuenta para un año específico"""
        documents = {}
        for doc in obj:
            account_type_id = doc.account_type.id
            documents[account_type_id] = {
                'title': doc.title,
                'url': doc.document_url,
                'date': doc.formatted_date,
                'type': doc.type
            }
        return documents


class AbandonedAccountsSectionSerializer(serializers.ModelSerializer):
    account_types = AccountTypeSerializer(many=True, read_only=True)
    years = serializers.SerializerMethodField()
    
    class Meta:
        model = AbandonedAccountsSection
        fields = [
            'id', 'title', 'description', 'account_types', 
            'years', 'is_active', 'created_at', 'updated_at'
        ]
    
    def get_years(self, obj):
        """Obtiene los años con sus documentos agrupados"""
        # Obtener todos los documentos relacionados con los tipos de cuenta de esta sección
        account_type_ids = obj.account_types.values_list('id', flat=True)
        yearly_docs = YearlyDocument.objects.filter(
            account_type__id__in=account_type_ids,
            is_active=True
        ).select_related('account_type').order_by('-year')

        # Agrupar por año
        years_data = {}
        for doc in yearly_docs:
            year = doc.year
            if year not in years_data:
                years_data[year] = {
                    'year': year,
                    'documents': {}
                }

            # Crear clave única para cada documento: account_type_id + type + id
            doc_key = f"{doc.account_type.id}_{doc.type}_{doc.id}"

            # Agregar documento al año correspondiente
            years_data[year]['documents'][doc_key] = {
                'id': doc.id,
                'title': doc.title,
                'url': doc.document_url,
                'date': doc.formatted_date,
                'type': doc.type
            }

        # Convertir a lista y ordenar por año descendente
        return sorted(years_data.values(), key=lambda x: x['year'], reverse=True)


class ContractCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ContractCategory
        fields = ['id', 'name']


class ContractSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name', read_only=True)
    document_url = serializers.SerializerMethodField()
    
    class Meta:
        model = Contract
        fields = ['id', 'title', 'document_url', 'category', 'order']
    
    def get_document_url(self, obj):
        """Retorna la URL del documento"""
        return obj.document_url


class AccountContractsSectionSerializer(serializers.ModelSerializer):
    contracts = serializers.SerializerMethodField()
    categories = serializers.SerializerMethodField()
    
    class Meta:
        model = AccountContractsSection
        fields = [
            'id', 'title', 'description', 'contracts', 
            'categories', 'is_active', 'created_at', 'updated_at'
        ]
    
    def get_contracts(self, obj):
        """Obtiene todos los contratos activos agrupados por categoría"""
        contracts = Contract.objects.filter(
            is_active=True
        ).select_related('category').order_by('category__name', 'order', 'title')
        
        contracts_data = []
        for contract in contracts:
            contracts_data.append({
                'title': contract.title,
                'url': contract.document_url,
                'category': contract.category.name
            })
        
        return contracts_data
    
    def get_categories(self, obj):
        """Obtiene todas las categorías activas"""
        categories = ContractCategory.objects.filter(
            is_active=True
        ).order_by('name')
        
        return [category.name for category in categories]


class ClaimRequestSerializer(serializers.ModelSerializer):
    """Serializer para solicitudes de reclamos"""
    
    class Meta:
        model = ClaimRequest
        fields = [
            'id', 'full_name', 'document', 'phone', 'email',
            'product_type', 'claim_type', 'distribution_channel',
            'message', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']
    
    def to_internal_value(self, data):
        """Mapear campos camelCase a snake_case"""
        # Crear una copia de los datos para no modificar el original
        mapped_data = data.copy()
        
        # Mapear campos camelCase a snake_case
        field_mapping = {
            'fullName': 'full_name',
            'productType': 'product_type',
            'claimType': 'claim_type',
            'distributionChannel': 'distribution_channel'
        }
        
        for camel_case, snake_case in field_mapping.items():
            if camel_case in mapped_data:
                mapped_data[snake_case] = mapped_data.pop(camel_case)
        
        return super().to_internal_value(mapped_data)


class FraudReportSerializer(serializers.ModelSerializer):
    """Serializer para reportes de fraude"""
    
    class Meta:
        model = FraudReport
        fields = [
            'id', 'full_name', 'document', 'phone', 'email',
            'classification', 'message', 'file', 'file_url', 'status', 
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'updated_at', 'file_url']
    
    def to_internal_value(self, data):
        """Mapear campos camelCase a snake_case"""
        print("=== SERIALIZER DEBUG ===")
        print(f"Data recibida: {data}")
        print(f"Data type: {type(data)}")
        
        # Crear una copia de los datos para no modificar el original
        mapped_data = data.copy()
        
        # Mapear campos camelCase a snake_case
        field_mapping = {
            'fullName': 'full_name'
        }
        
        for camel_case, snake_case in field_mapping.items():
            if camel_case in mapped_data:
                mapped_data[snake_case] = mapped_data.pop(camel_case)
        
        # Manejar archivo que viene como objeto JSON
        if 'file' in mapped_data:
            file_data = mapped_data['file']
            if isinstance(file_data, dict) and 'name' in file_data:
                print("⚠️ Archivo recibido como objeto JSON, ignorando...")
                print(f"Archivo: {file_data}")
                mapped_data.pop('file')
            elif not hasattr(file_data, 'read'):
                print("⚠️ Archivo recibido como string, ignorando...")
                mapped_data.pop('file')
        
        print(f"Data mapeada: {mapped_data}")
        print("=======================")
        
        return super().to_internal_value(mapped_data)


class RightsAndDutiesImageSerializer(serializers.ModelSerializer):
    """Serializer para imágenes de derechos y deberes"""
    src = serializers.SerializerMethodField()
    
    class Meta:
        model = RightsAndDutiesImage
        fields = ['id', 'src', 'alt_text', 'description']
    
    def get_src(self, obj):
        """Retorna la URL completa de la imagen"""
        return obj.image_url


class RightsAndDutiesSectionSerializer(serializers.ModelSerializer):
    """Serializer para secciones de derechos y deberes"""
    id = serializers.CharField(source='section_id')
    images = RightsAndDutiesImageSerializer(many=True, read_only=True)
    
    class Meta:
        model = RightsAndDutiesSection
        fields = [
            'id', 'title', 'description', 'button_text', 
            'additional_info', 'images'
        ]


class RightsAndDutiesPageSerializer(serializers.ModelSerializer):
    """Serializer para la página de derechos y deberes"""
    pageTitle = serializers.CharField(source='page_title')
    pageDescription = serializers.CharField(source='page_description')
    sections = serializers.SerializerMethodField()
    
    class Meta:
        model = RightsAndDutiesPage
        fields = [
            'id', 'pageTitle', 'pageDescription', 'sections',
            'is_active', 'created_at', 'updated_at'
        ]
    
    def get_sections(self, obj):
        """Obtener todas las secciones activas"""
        from .models import RightsAndDutiesSection
        sections = RightsAndDutiesSection.objects.filter(is_active=True).prefetch_related('images')
        return RightsAndDutiesSectionSerializer(sections, many=True).data


class ServiceRateSerializer(serializers.ModelSerializer):
    """Serializer para tarifas de servicios individuales"""
    
    class Meta:
        model = ServiceRate
        fields = ['id', 'service', 'description', 'rate', 'details']


class ServiceCategorySerializer(serializers.ModelSerializer):
    """Serializer para categorías de servicios"""
    rates = ServiceRateSerializer(many=True, read_only=True)
    
    class Meta:
        model = ServiceCategory
        fields = ['id', 'name', 'rates']


class ServiceRatesPageSerializer(serializers.ModelSerializer):
    """Serializer para la página de tarifas de servicios"""
    categories = serializers.SerializerMethodField()
    
    class Meta:
        model = ServiceRatesPage
        fields = [
            'id', 'title', 'description', 'categories',
            'is_active', 'created_at', 'updated_at'
        ]
    
    def get_categories(self, obj):
        """Obtener todas las categorías activas"""
        from .models import ServiceCategory
        categories = ServiceCategory.objects.filter(is_active=True).prefetch_related('rates')
        return ServiceCategorySerializer(categories, many=True).data


class SuggestionBoxSerializer(serializers.ModelSerializer):
    """Serializer para el buzón de sugerencias"""
    
    class Meta:
        model = SuggestionBox
        fields = [
            'id', 'full_name', 'document', 'phone', 'email', 'province',
            'classification', 'message', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'status', 'created_at', 'updated_at']
    
    def to_internal_value(self, data):
        """Convertir camelCase a snake_case y manejar conversiones de tipos"""
        # Mapear campos camelCase a snake_case
        field_mapping = {
            'fullName': 'full_name',
            'productType': 'product_type',
            'claimType': 'claim_type',
            'distributionChannel': 'distribution_channel',
        }
        
        # Crear nueva data con snake_case
        mapped_data = {}
        for key, value in data.items():
            if key in field_mapping:
                mapped_data[field_mapping[key]] = value
            else:
                mapped_data[key] = value
        
        # Convertir province de string a integer si es necesario
        if 'province' in mapped_data and isinstance(mapped_data['province'], str):
            try:
                mapped_data['province'] = int(mapped_data['province'])
            except (ValueError, TypeError):
                pass  # Dejar que el validador maneje el error
        
        return super().to_internal_value(mapped_data)


class ProvinceSerializer(serializers.ModelSerializer):
    """Serializer para provincias"""
    
    class Meta:
        model = Province
        fields = ['id', 'name']


class SuggestionBoxPageSerializer(serializers.ModelSerializer):
    """Serializer para la página del buzón de sugerencias"""
    
    class Meta:
        model = SuggestionBoxPage
        fields = [
            'id', 'title', 'description',
            'is_active', 'created_at', 'updated_at'
        ]


class FraudReportPageSerializer(serializers.ModelSerializer):
    """Serializer para la página de reportes de fraude"""
    
    class Meta:
        model = FraudReportPage
        fields = [
            'id', 'title', 'description',
            'is_active', 'created_at', 'updated_at'
        ]


class ClaimRequestPageSerializer(serializers.ModelSerializer):
    """Serializer para la página de solicitudes de reclamaciones"""
    
    class Meta:
        model = ClaimRequestPage
        fields = [
            'id', 'title', 'description',
            'is_active', 'created_at', 'updated_at'
        ]
