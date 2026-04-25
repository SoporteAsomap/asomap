from django.db import models
from django.core.validators import FileExtensionValidator
from django_prose_editor.fields import ProseEditorField
from .widgets import TallProseEditorField


class AccountType(models.Model):
    """Modelo para tipos de cuenta (abandonadas, inactivas)"""
    id = models.AutoField(primary_key=True)
    label = models.CharField(
        max_length=200,
        verbose_name="Etiqueta",
        help_text="Nombre descriptivo del tipo de cuenta"
    )
    description = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción detallada del tipo de cuenta"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si el tipo de cuenta está activo"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tipo de Cuenta"
        verbose_name_plural = "Tipos de Cuenta"
        ordering = ['id']

    def __str__(self):
        return self.label


class AbandonedAccountsSection(models.Model):
    """Modelo principal para la sección de cuentas abandonadas e inactivas"""
    title = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Título de la sección de cuentas abandonadas"
    )
    description = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción de la sección"
    )
    account_types = models.ManyToManyField(
        AccountType,
        verbose_name="Tipos de Cuenta",
        help_text="Tipos de cuenta disponibles en esta sección"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si la sección está activa"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sección de Cuentas Abandonadas"
        verbose_name_plural = "Secciones de Cuentas Abandonadas"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Asegurar que solo haya una sección activa
        if self.is_active:
            AbandonedAccountsSection.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class YearlyDocument(models.Model):
    """Modelo para documentos anuales de cuentas abandonadas/inactivas"""
    
    TYPE_CHOICES = [
        ('abandoned', 'Abandonadas'),
        ('inactive', 'Inactivas'),
    ]
    
    year = models.CharField(
        max_length=4,
        verbose_name="Año",
        help_text="Año del documento"
    )
    account_type = models.ForeignKey(
        AccountType,
        on_delete=models.CASCADE,
        verbose_name="Tipo de Cuenta",
        help_text="Tipo de cuenta al que pertenece el documento"
    )
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='abandoned',
        verbose_name="Tipo",
        help_text="Tipo de documento (abandoned o inactive)"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Título del documento"
    )
    document = models.FileField(
        upload_to='documents/abandoned-accounts/',
        verbose_name="Documento",
        help_text="Archivo PDF del documento",
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        max_length=255
    )
    date = models.DateField(
        verbose_name="Fecha",
        help_text="Fecha del documento"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si el documento está activo"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Documento Anual"
        verbose_name_plural = "Documentos Anuales"
        ordering = ['-year', 'account_type', 'type']

    def __str__(self):
        return f"{self.title} - {self.year}"

    @property
    def document_url(self):
        """
        Retorna la URL del documento para el frontend
        """
        if self.document:
            return self.document.url
        return None
    
    @property
    def formatted_date(self):
        """
        Retorna la fecha formateada como YYYY-MM-DD
        """
        if self.date:
            return self.date.strftime('%Y-%m-%d')
        return None
    
    def clean(self):
        """Validación personalizada del modelo"""
        from django.core.exceptions import ValidationError
        
        super().clean()
        
        if self.document:
            # Verificar extensión del archivo
            file_name = self.document.name.lower()
            if not file_name.endswith('.pdf'):
                raise ValidationError({
                    'document': 'El archivo debe tener extensión .pdf'
                })
    
    def save(self, *args, **kwargs):
        """Sobrescribir save para ejecutar validaciones"""
        self.full_clean()
        super().save(*args, **kwargs)


class ContractCategory(models.Model):
    """Modelo para categorías de contratos"""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre",
        help_text="Nombre de la categoría de contratos"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si la categoría está activa"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Categoría de Contrato"
        verbose_name_plural = "Categorías de Contratos"
        ordering = ['name']

    def __str__(self):
        return self.name


class AccountContractsSection(models.Model):
    """Modelo principal para la sección de contratos de adhesión"""
    title = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Título de la sección de contratos"
    )
    description = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción de la sección de contratos"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si la sección está activa"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sección de Contratos de Adhesión"
        verbose_name_plural = "Secciones de Contratos de Adhesión"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Asegurar que solo haya una sección activa
        if self.is_active:
            AccountContractsSection.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class Contract(models.Model):
    """Modelo para contratos de adhesión"""
    title = models.CharField(
        max_length=300,
        verbose_name="Título",
        help_text="Título del contrato"
    )
    category = models.ForeignKey(
        ContractCategory,
        on_delete=models.CASCADE,
        verbose_name="Categoría",
        help_text="Categoría del contrato"
    )
    document = models.FileField(
        upload_to='documents/contracts/',
        verbose_name="Documento",
        help_text="Archivo PDF del contrato",
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        max_length=255,
        null=True,
        blank=True
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Orden",
        help_text="Orden de aparición del contrato"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si el contrato está activo"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Contrato"
        verbose_name_plural = "Contratos"
        ordering = ['category', 'order', 'title']

    def __str__(self):
        return f"{self.title} - {self.category.name}"
    
    @property
    def document_url(self):
        """
        Retorna la URL del documento para el frontend
        """
        if self.document:
            return self.document.url
        return None


class ClaimRequest(models.Model):
    """Modelo para solicitudes de reclamos"""
    
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('in_progress', 'En proceso'),
        ('resolved', 'Resuelto'),
        ('closed', 'Cerrado'),
        ('rejected', 'Rechazado'),
    ]
    
    # Información personal
    full_name = models.CharField(
        max_length=200,
        verbose_name="Nombre completo",
        help_text="Nombre completo del solicitante"
    )
    document = models.CharField(
        max_length=20,
        verbose_name="Documento de identidad",
        help_text="Número de documento de identidad"
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="Teléfono",
        help_text="Número de teléfono de contacto"
    )
    email = models.EmailField(
        verbose_name="Correo electrónico",
        help_text="Correo electrónico de contacto"
    )
    
    # Información del reclamo
    product_type = models.CharField(
        max_length=100,
        verbose_name="Tipo de producto",
        help_text="Tipo de producto relacionado con el reclamo"
    )
    claim_type = models.CharField(
        max_length=100,
        verbose_name="Tipo de reclamo",
        help_text="Tipo de reclamo o solicitud"
    )
    distribution_channel = models.CharField(
        max_length=100,
        verbose_name="Canal de distribución",
        help_text="Canal a través del cual se realizó la transacción"
    )
    message = models.TextField(
        verbose_name="Mensaje",
        help_text="Descripción detallada del reclamo o solicitud"
    )
    
    # Estado y seguimiento
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Estado",
        help_text="Estado actual del reclamo"
    )
    internal_notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Notas internas",
        help_text="Notas internas para el seguimiento del reclamo"
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de actualización"
    )
    resolved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de resolución",
        help_text="Fecha cuando se resolvió el reclamo"
    )

    class Meta:
        verbose_name = "Solicitud de Reclamo"
        verbose_name_plural = "Solicitudes de Reclamos"
        ordering = ['-created_at']

    def __str__(self):
        return f"Reclamo de {self.full_name} - {self.get_status_display()}"

    def save(self, *args, **kwargs):
        """Sobrescribir save para actualizar fecha de resolución"""
        if self.status in ['resolved', 'closed'] and not self.resolved_at:
            from django.utils import timezone
            self.resolved_at = timezone.now()
        super().save(*args, **kwargs)


class ServiceRatesPage(models.Model):
    """Modelo principal para la página de tarifas de servicios"""
    title = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Título de la página de tarifas"
    )
    description = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción general de las tarifas de servicios"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si la página está activa"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Página de Tarifas de Servicios"
        verbose_name_plural = "Páginas de Tarifas de Servicios"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Asegurar que solo haya una página activa
        if self.is_active:
            ServiceRatesPage.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class ServiceCategory(models.Model):
    """Modelo para categorías de servicios"""
    name = models.CharField(
        max_length=100,
        verbose_name="Nombre",
        help_text="Nombre de la categoría de servicios"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Orden",
        help_text="Orden de aparición de la categoría"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si la categoría está activa"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Categoría de Servicios"
        verbose_name_plural = "Categorías de Servicios"
        ordering = ['order', 'name']
        unique_together = ['name']

    def __str__(self):
        return self.name


class ServiceRate(models.Model):
    """Modelo para tarifas de servicios individuales"""
    category = models.ForeignKey(
        ServiceCategory,
        on_delete=models.CASCADE,
        related_name='rates',
        verbose_name="Categoría",
        help_text="Categoría a la que pertenece esta tarifa"
    )
    service = models.CharField(
        max_length=200,
        verbose_name="Servicio",
        help_text="Nombre del servicio"
    )
    description = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción detallada del servicio"
    )
    rate = models.CharField(
        max_length=100,
        verbose_name="Tarifa",
        help_text="Precio o tarifa del servicio (ej: RD$ 500.00, Gratis, 6%)"
    )
    details = TallProseEditorField(
        extensions={
            "Bold": True,
            "Italic": True,
            "Underline": True,
            "Strike": True,
            "Heading": True,
            "BulletList": True,
            "OrderedList": True,
            "Link": True,
            "Blockquote": True,
            "Code": True,
            "CodeBlock": True,
        },
        sanitize=True,
        verbose_name="Detalles",
        help_text="Detalles adicionales del servicio con formato rico"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Orden",
        help_text="Orden de aparición del servicio"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si la tarifa está activa"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tarifa de Servicio"
        verbose_name_plural = "Tarifas de Servicios"
        ordering = ['category', 'order', 'service']
        unique_together = ['category', 'service']

    def __str__(self):
        return f"{self.service} - {self.rate}"


class FraudReport(models.Model):
    """Modelo para reportes de fraude"""
    
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('in_progress', 'En proceso'),
        ('resolved', 'Resuelto'),
        ('closed', 'Cerrado'),
        ('rejected', 'Rechazado'),
    ]
    
    # Información personal
    full_name = models.CharField(
        max_length=200,
        verbose_name="Nombre completo",
        help_text="Nombre completo del denunciante"
    )
    document = models.CharField(
        max_length=20,
        verbose_name="Documento de identidad",
        help_text="Número de documento de identidad"
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="Teléfono",
        help_text="Número de teléfono de contacto"
    )
    email = models.EmailField(
        verbose_name="Correo electrónico",
        help_text="Correo electrónico de contacto"
    )
    
    # Información del fraude
    classification = models.CharField(
        max_length=100,
        verbose_name="Clasificación del fraude",
        help_text="Tipo de fraude reportado"
    )
    message = models.TextField(
        verbose_name="Descripción del fraude",
        help_text="Descripción detallada del fraude reportado"
    )
    
    # Archivo adjunto
    file = models.FileField(
        upload_to='fraud_reports/',
        verbose_name="Archivo adjunto",
        help_text="Archivo de evidencia (PDF, imagen, etc.)",
        validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'jpeg', 'png', 'doc', 'docx'])],
        max_length=255,
        null=True,
        blank=True
    )
    
    # Estado y seguimiento
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Estado",
        help_text="Estado actual del reporte"
    )
    internal_notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Notas internas",
        help_text="Notas internas para el seguimiento del reporte"
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de actualización"
    )
    resolved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de resolución",
        help_text="Fecha cuando se resolvió el reporte"
    )

    class Meta:
        verbose_name = "Reporte de Fraude"
        verbose_name_plural = "Reportes de Fraude"
        ordering = ['-created_at']

    def __str__(self):
        return f"Fraude de {self.full_name} - {self.classification}"

    def save(self, *args, **kwargs):
        """Sobrescribir save para actualizar fecha de resolución"""
        if self.status in ['resolved', 'closed'] and not self.resolved_at:
            from django.utils import timezone
            self.resolved_at = timezone.now()
        super().save(*args, **kwargs)
    
    @property
    def file_url(self):
        """
        Retorna la URL del archivo para el frontend
        """
        if self.file:
            return self.file.url
        return None


class RightsAndDutiesPage(models.Model):
    """Modelo principal para la página de Derechos y Deberes"""
    page_title = models.CharField(
        max_length=200,
        verbose_name="Título de la Página",
        help_text="Título principal de la página de derechos y deberes"
    )
    page_description = models.TextField(
        verbose_name="Descripción de la Página",
        help_text="Descripción general de la página de derechos y deberes"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si la página está activa"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Página de Derechos y Deberes"
        verbose_name_plural = "Páginas de Derechos y Deberes"
        ordering = ['-created_at']

    def __str__(self):
        return self.page_title
    
    def save(self, *args, **kwargs):
        # Asegurar que solo haya una página activa
        if self.is_active:
            RightsAndDutiesPage.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class RightsAndDutiesSection(models.Model):
    """Modelo para secciones de derechos y deberes"""
    SECTION_ID_CHOICES = [
        ('rightsAndDuties', 'Derechos y Deberes'),
        ('otherRights', 'Otros Derechos'),
    ]
    
    section_id = models.CharField(
        max_length=50,
        choices=SECTION_ID_CHOICES,
        verbose_name="ID de Sección",
        help_text="Identificador único de la sección"
    )
    title = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Título de la sección"
    )
    description = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción de la sección"
    )
    button_text = models.CharField(
        max_length=100,
        verbose_name="Texto del Botón",
        help_text="Texto que aparecerá en el botón de la sección"
    )
    additional_info = models.TextField(
        blank=True,
        null=True,
        verbose_name="Información Adicional",
        help_text="Información adicional de la sección (opcional)"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Orden",
        help_text="Orden de aparición de la sección"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si la sección está activa"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sección de Derechos y Deberes"
        verbose_name_plural = "Secciones de Derechos y Deberes"
        ordering = ['order', 'title']
        unique_together = ['section_id']

    def __str__(self):
        return f"{self.title} - {self.get_section_id_display()}"
    
    def save(self, *args, **kwargs):
        # Asegurar que solo haya una sección activa por section_id
        if self.is_active:
            RightsAndDutiesSection.objects.filter(
                section_id=self.section_id
            ).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class RightsAndDutiesImage(models.Model):
    """Modelo para imágenes de derechos y deberes"""
    section = models.ForeignKey(
        RightsAndDutiesSection,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="Sección",
        help_text="Sección a la que pertenece esta imagen"
    )
    image = models.ImageField(
        upload_to='user-support/rights/',
        verbose_name="Imagen",
        help_text="Imagen de la sección"
    )
    alt_text = models.CharField(
        max_length=200,
        verbose_name="Texto Alternativo",
        help_text="Texto alternativo para la imagen"
    )
    description = models.CharField(
        max_length=300,
        verbose_name="Descripción",
        help_text="Descripción de la imagen"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Orden",
        help_text="Orden de aparición de la imagen"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si la imagen está activa"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Imagen de Derechos y Deberes"
        verbose_name_plural = "Imágenes de Derechos y Deberes"
        ordering = ['section', 'order', 'alt_text']

    def __str__(self):
        return f"{self.alt_text} - {self.section.title}"
    
    @property
    def image_url(self):
        """
        Retorna la URL de la imagen para el frontend
        """
        if self.image:
            return self.image.url
        return None


class Province(models.Model):
    """Modelo para provincias de República Dominicana"""
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre",
        help_text="Nombre de la provincia"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si la provincia está activa"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Provincia"
        verbose_name_plural = "Provincias"
        ordering = ['name']

    def __str__(self):
        return self.name


class SuggestionBox(models.Model):
    """Modelo para el buzón de sugerencias"""
    
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('in_progress', 'En proceso'),
        ('resolved', 'Resuelto'),
        ('closed', 'Cerrado'),
        ('rejected', 'Rechazado'),
    ]
    
    # Información personal
    full_name = models.CharField(
        max_length=200,
        verbose_name="Nombre completo",
        help_text="Nombre completo del solicitante"
    )
    document = models.CharField(
        max_length=20,
        verbose_name="Documento de identidad",
        help_text="Número de documento de identidad"
    )
    phone = models.CharField(
        max_length=20,
        verbose_name="Teléfono",
        help_text="Número de teléfono de contacto"
    )
    email = models.EmailField(
        verbose_name="Correo electrónico",
        help_text="Correo electrónico de contacto"
    )
    province = models.ForeignKey(
        Province,
        on_delete=models.CASCADE,
        verbose_name="Provincia",
        help_text="Provincia de residencia"
    )
    
    # Información de la sugerencia
    classification = models.CharField(
        max_length=100,
        verbose_name="Clasificación",
        help_text="Tipo de sugerencia o comentario"
    )
    message = models.TextField(
        verbose_name="Sugerencia",
        help_text="Descripción detallada de la sugerencia o comentario"
    )
    
    # Estado y seguimiento
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Estado",
        help_text="Estado actual de la sugerencia"
    )
    internal_notes = models.TextField(
        blank=True,
        null=True,
        verbose_name="Notas internas",
        help_text="Notas internas para el seguimiento de la sugerencia"
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de actualización"
    )
    resolved_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name="Fecha de resolución",
        help_text="Fecha cuando se procesó la sugerencia"
    )

    class Meta:
        verbose_name = "Buzón de Sugerencias"
        verbose_name_plural = "Buzón de Sugerencias"
        ordering = ['-created_at']

    def __str__(self):
        return f"Sugerencia de {self.full_name} - {self.classification}"

    def save(self, *args, **kwargs):
        """Sobrescribir save para actualizar fecha de resolución"""
        if self.status in ['resolved', 'closed'] and not self.resolved_at:
            from django.utils import timezone
            self.resolved_at = timezone.now()
        super().save(*args, **kwargs)


class SuggestionBoxPage(models.Model):
    """Modelo principal para la página del buzón de sugerencias"""
    title = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Título de la página del buzón de sugerencias"
    )
    description = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción de la página del buzón de sugerencias"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si la página está activa"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Página del Buzón de Sugerencias"
        verbose_name_plural = "Páginas del Buzón de Sugerencias"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Asegurar que solo haya una página activa
        if self.is_active:
            SuggestionBoxPage.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class FraudReportPage(models.Model):
    """Modelo principal para la página de reportes de fraude"""
    title = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Título de la página de reportes de fraude"
    )
    description = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción de la página de reportes de fraude"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si la página está activa"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Página de Reportes de Fraude"
        verbose_name_plural = "Páginas de Reportes de Fraude"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Asegurar que solo haya una página activa
        if self.is_active:
            FraudReportPage.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class ClaimRequestPage(models.Model):
    """Modelo principal para la página de solicitudes de reclamaciones"""
    title = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Título de la página de solicitudes de reclamaciones"
    )
    description = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción de la página de solicitudes de reclamaciones"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si la página está activa"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Página de Solicitudes de Reclamaciones"
        verbose_name_plural = "Páginas de Solicitudes de Reclamaciones"
        ordering = ['-created_at']

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Asegurar que solo haya una página activa
        if self.is_active:
            ClaimRequestPage.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)
