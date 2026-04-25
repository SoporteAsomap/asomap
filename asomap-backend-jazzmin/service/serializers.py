from rest_framework import serializers
from typing import Optional, List
from .models import ServicesPage, ServiceInfo


class ServiceInfoSerializer(serializers.ModelSerializer):
    """Serializer para información detallada de servicios"""
    image_url = serializers.SerializerMethodField()
    pdf_url = serializers.SerializerMethodField()

    class Meta:
        model = ServiceInfo
        fields = [
            'id', 'title', 'description', 'steps',
            'image_url', 'image_alt', 'pdf_url'
        ]

    def get_image_url(self, obj) -> Optional[str]:
        value = obj.image_url() if callable(obj.image_url) else obj.image_url
        return value

    def get_pdf_url(self, obj) -> Optional[str]:
        pdf_url = obj.pdf_url() if callable(obj.pdf_url) else obj.pdf_url
        pdf_file_url = obj.pdf_file_url() if callable(obj.pdf_file_url) else obj.pdf_file_url

        if pdf_url:
            return pdf_url
        elif pdf_file_url:
            return pdf_file_url
        return None

    def get_steps(self, obj) -> str:
        """Retorna los pasos como HTML"""
        return obj.steps if obj.steps else ""


class ServicesPageSerializer(serializers.ModelSerializer):
    """Serializer para la página de servicios"""
    items = serializers.SerializerMethodField()
    item_details = ServiceInfoSerializer(many=True, read_only=True)

    class Meta:
        model = ServicesPage
        fields = [
            'id', 'title', 'subtitle', 'search_placeholder',
            'no_results_text', 'internet_banking_url', 'internet_banking_button',
            'items', 'item_details', 'is_active', 'created_at', 'updated_at'
        ]

    def get_items(self, obj) -> List[str]:
        """Obtener lista de títulos de servicios para búsqueda"""
        return [service.title for service in obj.item_details.filter(is_active=True)]
