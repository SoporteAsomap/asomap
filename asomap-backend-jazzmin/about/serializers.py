from rest_framework import serializers
from .models import (
    FinancialDocument, FinancialStatementsConfig, Hero, QuienesSomos, NuestraHistoria, Mision, Vision, 
    Valor, Director, CommunitySupport, CommunityCategory, CommunityInitiative,
    MemoryDocument, MemoryConfig, PolicyDocument, PolicyCategory, PolicyConfig
)

class HeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hero
        fields = '__all__'

class QuienesSomosSerializer(serializers.ModelSerializer):
    paragraphs = serializers.SerializerMethodField()
    
    class Meta:
        model = QuienesSomos
        fields = '__all__'

    def get_paragraphs(self, obj):
        """Retorna los párrafos como lista"""
        return obj.paragraphs_list

class NuestraHistoriaSerializer(serializers.ModelSerializer):

    class Meta:
        model = NuestraHistoria
        fields = '__all__'

class MisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mision
        fields = '__all__'

class VisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vision
        fields = '__all__'

class ValorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Valor
        fields = '__all__'

class DirectorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Director
        fields = '__all__'

class CommunityCategorySerializer(serializers.ModelSerializer):
    """
    Serializer para las categorías de apoyo comunitario
    """
    class Meta:
        model = CommunityCategory
        fields = [
            'id', 'name', 'icon', 'description', 
            'is_active', 'created_at', 'updated_at'
        ]

class CommunityInitiativeSerializer(serializers.ModelSerializer):
    """
    Serializer para las iniciativas de apoyo comunitario
    """
    category = CommunityCategorySerializer(read_only=True)
    category_id = serializers.IntegerField(write_only=True)
    
    class Meta:
        model = CommunityInitiative
        fields = [
            'id', 'title', 'description', 'impact', 
            'image_src', 'image_alt', 'category', 'category_id',
            'year', 'location', 'beneficiaries',
            'is_active', 'created_at', 'updated_at'
        ]

class CommunitySupportSerializer(serializers.ModelSerializer):
    """
    Serializer para la sección principal de apoyo comunitario
    """
    categories = CommunityCategorySerializer(many=True, read_only=True)
    initiatives = CommunityInitiativeSerializer(many=True, read_only=True)
    
    class Meta:
        model = CommunitySupport
        fields = [
            'id', 'title', 'description', 'categories', 'initiatives',
            'is_active', 'created_at', 'updated_at'
        ]

# Serializer para respuesta completa
class CommunitySupportCompleteSerializer(serializers.Serializer):
    """
    Serializer para la respuesta completa de apoyo comunitario
    """
    title = serializers.CharField()
    description = serializers.CharField()
    categories = CommunityCategorySerializer(many=True)
    initiatives = CommunityInitiativeSerializer(many=True)

class FinancialDocumentSerializer(serializers.ModelSerializer):
    """
    Serializer para documentos financieros individuales
    """
    class Meta:
        model = FinancialDocument
        fields = [
            'id', 'title', 'file', 'document_type', 'quarter',
            'is_active', 'created_at', 'updated_at'
        ]

class FinancialStatementsConfigSerializer(serializers.ModelSerializer):
    """
    Serializer para la configuración de estados financieros
    """
    class Meta:
        model = FinancialStatementsConfig
        fields = [
            'id', 'title', 'description', 
            'is_active', 'created_at', 'updated_at'
        ]

class FinancialStatementsCompleteSerializer(serializers.Serializer):
    """
    Serializer para la respuesta completa de estados financieros
    que coincide con la estructura del frontend
    """
    title = serializers.CharField()
    description = serializers.CharField()
    years = serializers.ListField(child=serializers.DictField())

class MemoryDocumentSerializer(serializers.ModelSerializer):
    """
    Serializer para documentos de memoria individuales
    """
    class Meta:
        model = MemoryDocument
        fields = [
            'id', 'file', 'year',
            'is_active', 'created_at', 'updated_at'
        ]

class MemoryConfigSerializer(serializers.ModelSerializer):
    """
    Serializer para la configuración de memorias
    """
    class Meta:
        model = MemoryConfig
        fields = [
            'id', 'title', 'description', 
            'is_active', 'created_at', 'updated_at'
        ]

class MemoriesCompleteSerializer(serializers.Serializer):
    """
    Serializer para la respuesta completa de memorias
    que coincide con la estructura del frontend
    """
    title = serializers.CharField()
    description = serializers.CharField()
    years = serializers.ListField(child=serializers.DictField())

class PolicyDocumentSerializer(serializers.ModelSerializer):
    """
    Serializer para documentos de políticas individuales
    """
    class Meta:
        model = PolicyDocument
        fields = [
            'id', 'title', 'description', 'file', 'last_update',
            'is_active', 'created_at', 'updated_at'
        ]

class PolicyCategorySerializer(serializers.ModelSerializer):
    """
    Serializer para categorías de políticas con documentos anidados
    """
    documents = PolicyDocumentSerializer(many=True, read_only=True)
    
    class Meta:
        model = PolicyCategory
        fields = [
            'id', 'title', 'icon', 'description', 'documents',
            'is_active', 'created_at', 'updated_at'
        ]

class PolicyConfigSerializer(serializers.ModelSerializer):
    """
    Serializer para la configuración de políticas
    """
    class Meta:
        model = PolicyConfig
        fields = [
            'id', 'title', 'description', 'download_text', 'last_update_text', 'all_policies_text',
            'is_active', 'created_at', 'updated_at'
        ]

class PoliciesCompleteSerializer(serializers.Serializer):
    """
    Serializer para la respuesta completa de políticas
    que coincide con la estructura del frontend
    """
    title = serializers.CharField()
    description = serializers.CharField()
    download_text = serializers.CharField()
    last_update_text = serializers.CharField()
    all_policies_text = serializers.CharField()
    categories = serializers.ListField(child=serializers.DictField()) 