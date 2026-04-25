from django.contrib import admin
from .models import DebitCardPromo, EducationItem, EducationSection, PeKeAccountSummary, Product, ProductSection, SliderItem


@admin.register(DebitCardPromo)
class DebitCardPromoAdmin(admin.ModelAdmin):
    list_display = ['title', 'highlighted_title', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'highlighted_title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Información de la Promoción', {
            'fields': ('title', 'highlighted_title', 'description')
        }),
        ('Botones de Acción', {
            'fields': ('primary_button_text', 'primary_button_url', 'secondary_button_text', 'secondary_button_url')
        }),
        ('Imagen', {
            'fields': ('image', 'image_alt')
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Solo permitir crear si no hay promociones activas
        if DebitCardPromo.objects.filter(is_active=True).exists():
            return False
        return super().has_add_permission(request)


@admin.register(EducationItem)
class EducationItemAdmin(admin.ModelAdmin):
    list_display = ['description', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['description', 'alt']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['order', 'created_at']
    list_editable = ['order', 'is_active']
    
    fieldsets = (
        ('Información del Elemento', {
            'fields': ('image', 'alt', 'description')
        }),
        ('Configuración', {
            'fields': ('order', 'is_active')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(EducationSection)
class EducationSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'subtitle', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'subtitle', 'footer_text']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    filter_horizontal = ['education_items']
    
    fieldsets = (
        ('Información de la Sección', {
            'fields': ('title', 'subtitle', 'footer_text')
        }),
        ('Elementos Educativos', {
            'fields': ('education_items',)
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Solo permitir crear si no hay secciones activas
        if EducationSection.objects.filter(is_active=True).exists():
            return False
        return super().has_add_permission(request)


@admin.register(PeKeAccountSummary)
class PeKeAccountSummaryAdmin(admin.ModelAdmin):
    list_display = ['title', 'button_text', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'description', 'button_text']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Información del Resumen', {
            'fields': ('title', 'description')
        }),
        ('Botón de Acción', {
            'fields': ('button_text', 'button_url')
        }),
        ('Imagen', {
            'fields': ('image', 'image_alt')
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Solo permitir crear si no hay resúmenes activos
        if PeKeAccountSummary.objects.filter(is_active=True).exists():
            return False
        return super().has_add_permission(request)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'order', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    search_fields = ['title', 'description']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['order', 'created_at']
    list_editable = ['order', 'is_active']
    
    fieldsets = (
        ('Información del Producto', {
            'fields': ('title', 'description', 'category')
        }),
        ('Imagen', {
            'fields': ('image', 'image_width', 'image_height')
        }),
        ('Configuración', {
            'fields': ('order', 'is_active')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(ProductSection)
class ProductSectionAdmin(admin.ModelAdmin):
    list_display = ['title', 'subtitle', 'button_text', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['title', 'subtitle', 'button_text']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']
    filter_horizontal = ['products']
    
    fieldsets = (
        ('Información de la Sección', {
            'fields': ('title', 'subtitle', 'button_text')
        }),
        ('Productos', {
            'fields': ('products',)
        }),
        ('Estado', {
            'fields': ('is_active',)
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def has_add_permission(self, request):
        # Solo permitir crear si no hay secciones activas
        if ProductSection.objects.filter(is_active=True).exists():
            return False
        return super().has_add_permission(request)


@admin.register(SliderItem)
class SliderItemAdmin(admin.ModelAdmin):
    list_display = ['alt', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['alt']
    readonly_fields = ['created_at', 'updated_at']
    ordering = ['order', 'created_at']
    list_editable = ['order', 'is_active']
    
    fieldsets = (
        ('Información del Elemento', {
            'fields': ('alt',)
        }),
        ('Imágenes', {
            'fields': ('image_desktop', 'image_tablet', 'image_mobile'),
            'description': 'Sube imágenes optimizadas para cada dispositivo'
        }),
        ('Configuración', {
            'fields': ('order', 'is_active')
        }),
        ('Fechas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
