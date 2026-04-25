from rest_framework import serializers
from .models import DebitCardPromo, EducationItem, EducationSection, PeKeAccountSummary, Product, ProductSection, SliderItem


class DebitCardPromoSerializer(serializers.ModelSerializer):
    """
    Serializer para la promoción de tarjeta de débito
    """
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = DebitCardPromo
        fields = [
            'id', 'title', 'highlighted_title', 'description',
            'primary_button_text', 'secondary_button_text',
            'primary_button_url', 'secondary_button_url',
            'image_url', 'image_alt', 'is_active',
            'created_at', 'updated_at'
        ]
    
    def get_image_url(self, obj):
        """
        Retorna la URL de la imagen para el frontend
        """
        return obj.image_url


class EducationItemSerializer(serializers.ModelSerializer):
    """
    Serializer para elementos educativos individuales
    """
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = EducationItem
        fields = [
            'id', 'image', 'alt', 'description',
            'is_active', 'order', 'created_at', 'updated_at'
        ]
    
    def get_image(self, obj):
        """
        Retorna la URL de la imagen para el frontend
        """
        return obj.image_url


class EducationSectionSerializer(serializers.ModelSerializer):
    """
    Serializer para la sección de educación con elementos anidados
    """
    education_items = EducationItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = EducationSection
        fields = [
            'id', 'title', 'subtitle', 'education_items', 'footer_text',
            'is_active', 'created_at', 'updated_at'
        ]


class EducationSectionCompleteSerializer(serializers.Serializer):
    """
    Serializer para la respuesta completa de la sección de educación
    que coincide con la estructura del frontend
    """
    data = serializers.DictField()


class PeKeAccountSummarySerializer(serializers.ModelSerializer):
    """
    Serializer para el resumen de cuenta PeKe
    """
    image_url = serializers.SerializerMethodField()
    
    class Meta:
        model = PeKeAccountSummary
        fields = [
            'id', 'title', 'description', 'button_text', 'button_url',
            'image_url', 'image_alt', 'is_active',
            'created_at', 'updated_at'
        ]
    
    def get_image_url(self, obj):
        """
        Retorna la URL de la imagen para el frontend
        """
        return obj.image_url


class ProductSerializer(serializers.ModelSerializer):
    """
    Serializer para productos individuales
    """
    image = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'image', 'category',
            'image_width', 'image_height', 'is_active', 'order',
            'created_at', 'updated_at'
        ]
    
    def get_image(self, obj):
        """
        Retorna la URL de la imagen para el frontend
        """
        return obj.image_url


class ProductSectionSerializer(serializers.ModelSerializer):
    """
    Serializer para la sección de productos con productos anidados
    """
    products = ProductSerializer(many=True, read_only=True)
    
    class Meta:
        model = ProductSection
        fields = [
            'id', 'title', 'subtitle', 'button_text', 'products',
            'is_active', 'created_at', 'updated_at'
        ]


class ProductSectionCompleteSerializer(serializers.Serializer):
    """
    Serializer para la respuesta completa de la sección de productos
    que coincide con la estructura del frontend
    """
    data = serializers.DictField()


class SliderItemSerializer(serializers.ModelSerializer):
    """
    Serializer para elementos del slider
    """
    image = serializers.SerializerMethodField()
    imageTablet = serializers.SerializerMethodField()
    imageMobile = serializers.SerializerMethodField()
    
    class Meta:
        model = SliderItem
        fields = [
            'id', 'image', 'imageTablet', 'imageMobile', 'alt',
            'is_active', 'order', 'created_at', 'updated_at'
        ]
    
    def get_image(self, obj):
        """
        Retorna la URL de la imagen desktop para el frontend
        """
        return obj.image_desktop_url
    
    def get_imageTablet(self, obj):
        """
        Retorna la URL de la imagen tablet para el frontend
        """
        return obj.image_tablet_url
    
    def get_imageMobile(self, obj):
        """
        Retorna la URL de la imagen mobile para el frontend
        """
        return obj.image_mobile_url
