from django.db import models
from django.core.validators import MinValueValidator
from django_prose_editor.fields import ProseEditorField
from django.utils.text import slugify


class AccountBenefit(models.Model):
    """Modelo para los beneficios de las cuentas con iconos"""
    ICON_CHOICES = [
        # Iconos de dinero y finanzas
        ('FaMoneyBillWave', '💰 Dinero/Efectivo'),
        ('FaCreditCard', '💳 Tarjeta de Crédito'),
        ('FaChartLine', '📈 Gráficos/Inversiones'),
        
        # Iconos de dispositivos
        ('FaMobileAlt', '📱 Móvil/Banca Móvil'),
        
        # Iconos de préstamos
        ('FaHome', '🏠 Casa/Hipoteca'),
        ('FaCar', '🚗 Auto/Vehicular'),
        ('FaGraduationCap', '🎓 Estudios/Educación'),
        ('FaBuilding', '🏢 Empresa/Negocio'),
        
        # Iconos de beneficios
        ('FaShieldAlt', '🛡️ Seguridad/Protección'),
        ('FaGift', '🎁 Beneficios/Regalos'),
        ('FaStar', '⭐ Calidad/Excelencia'),
        ('FaHeart', '❤️ Amor/Preferencia'),
        ('FaUsers', '👥 Comunidad/Personas'),
        ('FaHandshake', '🤝 Acuerdos/Servicios'),
        ('FaLightbulb', '💡 Ideas/Innovación'),
        ('FaRocket', '🚀 Crecimiento/Progreso'),
        ('FaGem', '💎 Valor/Premium'),
        ('FaCrown', '👑 Liderazgo/Excelencia'),
        ('FaTrophy', '🏆 Logros/Éxito'),
        ('FaMedal', '🥇 Reconocimiento/Calidad'),
    ]
    
    account = models.ForeignKey('Account', on_delete=models.CASCADE, related_name='account_benefits')
    icon = models.CharField(
        max_length=50,
        choices=ICON_CHOICES,
        verbose_name="Icono",
        help_text="Icono de FontAwesome para el beneficio"
    )
    text = models.TextField(
        verbose_name="Texto del beneficio",
        help_text="Descripción del beneficio"
    )
    
    class Meta:
        verbose_name = "Beneficio de Cuenta"
        verbose_name_plural = "Beneficios de Cuenta"
        ordering = ['id']
    
    def __str__(self):
        return f"{self.get_icon_display()} - {self.text[:50]}"

class Account(models.Model):
    CATEGORY_CHOICES = [
        ('savings', 'Cuenta de Ahorros'),
        ('checking', 'Cuenta Corriente'),
        ('business', 'Cuenta Empresarial'),
        ('student', 'Cuenta Estudiantil'),
        ('classic_physical', 'Cuenta Física Clásica'),
    ]
    
    # Información básica
    title = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Título de la cuenta"
    )
    description = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción breve de la cuenta"
    )
    
    # Imágenes
    banner_image = models.ImageField(
        upload_to='products/accounts/banners/',
        null=True,
        blank=True,
        verbose_name="Imagen de banner",
        help_text="Imagen de banner para la cuenta"
    )
    account_image = models.ImageField(
        upload_to='products/accounts/',
        null=True,
        blank=True,
        verbose_name="Imagen de la cuenta",
        help_text="Imagen principal de la cuenta"
    )
    
    # Categoría
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        verbose_name="Categoría",
        help_text="Categoría de la cuenta"
    )
    

    
    # Características
    features = models.TextField(
        blank=True,
        verbose_name="Características",
        help_text="Características del producto separadas por /"
    )
    
    # Requisitos
    requirements = models.TextField(
        blank=True,
        verbose_name="Requisitos",
        help_text="Requisitos para abrir la cuenta separados por /"
    )
    
    # Estado
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si la cuenta está activa"
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

    class Meta:
        verbose_name = "Account"
        verbose_name_plural = "Accounts"
        ordering = ['category', 'title']

    def __str__(self):
        return f"{self.title} - {self.get_category_display()}"

    @property
    def banner_image_url(self):
        """
        Retorna la URL de la imagen de banner para el frontend
        """
        if self.banner_image:
            return self.banner_image.url
        return None

    @property
    def account_image_url(self):
        """
        Retorna la URL de la imagen de la cuenta para el frontend
        """
        if self.account_image:
            return self.account_image.url
        return None

    @property
    def features_list(self):
        """
        Retorna las características como lista para el frontend
        """
        if self.features:
            return [feature.strip() for feature in self.features.split('/') if feature.strip()]
        return []

    @property
    def requirements_list(self):
        """
        Retorna los requisitos como lista para el frontend
        """
        if self.requirements:
            return [req.strip() for req in self.requirements.split('/') if req.strip()]
        return []

    @property
    def benefits_list(self):
        """
        Retorna los beneficios como lista para el frontend
        """
        benefits = []
        for benefit in self.account_benefits.all():
            benefits.append({
                'icon': benefit.icon,
                'text': benefit.text
            })
        return benefits

    @property
    def slug(self):
        """
        Retorna el slug del título para URLs amigables
        """
        return slugify(self.title)

class LoanType(models.Model):
    """
    Modelo para gestionar los tipos de préstamos desde el admin
    """
    name = models.CharField(
        max_length=100,
        unique=True,
        verbose_name="Nombre",
        help_text="Nombre del tipo de préstamo"
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name="Slug",
        help_text="Identificador único para URLs (se genera automáticamente)"
    )
    description = models.TextField(
        blank=True,
        verbose_name="Descripción",
        help_text="Descripción del tipo de préstamo"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si este tipo de préstamo está disponible"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Orden",
        help_text="Orden de visualización (menor número = mayor prioridad)"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Fecha de creación"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Fecha de actualización"
    )

    class Meta:
        verbose_name = "Tipo de Préstamo"
        verbose_name_plural = "Tipos de Préstamos"
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def slug_auto(self):
        """
        Retorna el slug del nombre para URLs amigables
        """
        return slugify(self.name)


class Loan(models.Model):
    
    title = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Título del préstamo "
    )
    description = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción detallada del préstamo"
    )
    loan_type = models.ForeignKey(
        LoanType,
        on_delete=models.PROTECT,
        verbose_name="Tipo de préstamo",
        help_text="Selecciona el tipo de préstamo"
    )
    details = models.TextField(
        verbose_name="Detalles",
        help_text="Detalles del préstamo separados por /",
        default=""
    )
    requirements_title = models.CharField(
        max_length=200,
        default="Requisitos para Crédito",
        verbose_name="Título de requisitos",
        help_text="Título de la sección de requisitos"
    )
    requirements = models.TextField(
        verbose_name="Requisitos",
        help_text="Requisitos del préstamo separados por /"
    )
    banner_image = models.ImageField(
        upload_to='products/loans/',
        verbose_name="Imagen del banner",
        help_text="Imagen principal del préstamo para el banner",
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Préstamo"
        verbose_name_plural = "Préstamos"
        ordering = ['loan_type', 'title']

    def __str__(self):
        return f"{self.title} - {self.loan_type.name if self.loan_type else 'Sin tipo'}"

    @property
    def details_list(self):
        """
        Retorna los detalles como lista para el frontend
        """
        if self.details:
            return [detail.strip() for detail in self.details.split('/') if detail.strip()]
        return []

    @property
    def requirements_list(self):
        """
        Retorna los requisitos como lista para el frontend
        """
        if self.requirements:
            return [req.strip() for req in self.requirements.split('/') if req.strip()]
        return []

    @property
    def banner_image_url(self):
        """
        Retorna la URL de la imagen de banner para el frontend
        """
        if self.banner_image:
            return self.banner_image.url
        return None

    @property
    def slug(self):
        """
        Retorna el slug del título para URLs
        """
        from django.utils.text import slugify
        return slugify(self.title)

class CardBenefit(models.Model):
    """Modelo para los beneficios de las tarjetas con iconos"""
    ICON_CHOICES = [
        # Iconos de dinero y finanzas
        ('FaMoneyBillWave', '💰 Dinero/Efectivo'),
        ('FaCreditCard', '💳 Tarjeta de Crédito'),
        ('FaChartLine', '📈 Gráficos/Inversiones'),
        
        # Iconos de dispositivos
        ('FaMobileAlt', '📱 Móvil/Banca Móvil'),
        
        # Iconos de préstamos
        ('FaHome', '🏠 Casa/Hipoteca'),
        ('FaCar', '🚗 Auto/Vehicular'),
        ('FaGraduationCap', '🎓 Estudios/Educación'),
        ('FaBuilding', '🏢 Empresa/Negocio'),
        
        # Iconos de beneficios
        ('FaShieldAlt', '🛡️ Seguridad/Protección'),
        ('FaGift', '🎁 Beneficios/Regalos'),
        ('FaStar', '⭐ Calidad/Excelencia'),
        ('FaHeart', '❤️ Amor/Preferencia'),
        ('FaUsers', '👥 Comunidad/Personas'),
        ('FaHandshake', '🤝 Acuerdos/Servicios'),
        ('FaLightbulb', '💡 Ideas/Innovación'),
        ('FaRocket', '🚀 Crecimiento/Progreso'),
        ('FaGem', '💎 Valor/Premium'),
        ('FaCrown', '👑 Liderazgo/Excelencia'),
        ('FaTrophy', '🏆 Logros/Éxito'),
        ('FaMedal', '🥇 Reconocimiento/Calidad'),
        ('FaGlobeAmericas', '🌎 Aceptación Global'),
    ]
    
    card = models.ForeignKey('Card', on_delete=models.CASCADE, related_name='card_benefits')
    icon = models.CharField(
        max_length=50,
        choices=ICON_CHOICES,
        verbose_name="Icono",
        help_text="Icono de FontAwesome para el beneficio"
    )
    text = models.TextField(
        verbose_name="Texto del beneficio",
        help_text="Descripción del beneficio"
    )
    
    class Meta:
        verbose_name = "Beneficio de Tarjeta"
        verbose_name_plural = "Beneficios de Tarjeta"
        ordering = ['id']
    
    def __str__(self):
        return f"{self.get_icon_display()} - {self.text[:50]}"

class Card(models.Model):
    CARD_TYPE_CHOICES = [
        ('debit', 'Tarjeta de Débito'),
        ('credit', 'Tarjeta de Crédito'),
        ('prepaid', 'Tarjeta Prepago'),
        ('business', 'Tarjeta Empresarial'),
        ('student', 'Tarjeta Estudiantil'),
    ]
    
    # Información básica
    title = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Título de la tarjeta"
    )
    description = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción breve de la tarjeta"
    )
    
    # Imágenes
    banner_image = models.ImageField(
        upload_to='products/cards/banners/',
        null=True,
        blank=True,
        verbose_name="Imagen de banner",
        help_text="Imagen de banner para la tarjeta"
    )
    card_image = models.ImageField(
        upload_to='products/cards/',
        null=True,
        blank=True,
        verbose_name="Imagen de la tarjeta",
        help_text="Imagen principal de la tarjeta"
    )
    
    # Tipo de tarjeta
    card_type = models.CharField(
        max_length=20,
        choices=CARD_TYPE_CHOICES,
        default='debit',
        verbose_name="Tipo de tarjeta",
        help_text="Tipo de tarjeta"
    )
    
    # Características
    features = models.TextField(
        blank=True,
        verbose_name="Características",
        help_text="Características de la tarjeta separadas por /"
    )
    
    # Requisitos
    requirements = models.TextField(
        blank=True,
        verbose_name="Requisitos",
        help_text="Requisitos para obtener la tarjeta separados por /"
    )
    
    # Estado
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si la tarjeta está activa"
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

    class Meta:
        verbose_name = "Card"
        verbose_name_plural = "Cards"
        ordering = ['card_type', 'title']

    def __str__(self):
        return f"{self.title} - {self.get_card_type_display()}"

    @property
    def banner_image_url(self):
        """
        Retorna la URL de la imagen de banner para el frontend
        """
        if self.banner_image:
            return self.banner_image.url
        return None

    @property
    def card_image_url(self):
        """
        Retorna la URL de la imagen de la tarjeta para el frontend
        """
        if self.card_image:
            return self.card_image.url
        return None

    @property
    def features_list(self):
        """
        Retorna las características como lista para el frontend
        """
        if self.features:
            return [feature.strip() for feature in self.features.split('/') if feature.strip()]
        return []

    @property
    def requirements_list(self):
        """
        Retorna los requisitos como lista para el frontend
        """
        if self.requirements:
            return [req.strip() for req in self.requirements.split('/') if req.strip()]
        return []

    @property
    def benefits_list(self):
        """
        Retorna los beneficios como lista para el frontend
        """
        benefits = []
        for benefit in self.card_benefits.all():
            benefits.append({
                'icon': benefit.icon,
                'text': benefit.text
            })
        return benefits

    @property
    def slug(self):
        """
        Retorna el slug del título para URLs amigables
        """
        return slugify(self.title)

class CertificateBenefit(models.Model):
    """Modelo para los beneficios de los certificados financieros"""
    certificate = models.ForeignKey('Certificate', on_delete=models.CASCADE, related_name='certificate_benefits')
    title = models.CharField(
        max_length=200,
        verbose_name="Título del beneficio",
        help_text="Título del beneficio del certificado"
    )
    description = models.TextField(
        verbose_name="Descripción del beneficio",
        help_text="Descripción detallada del beneficio"
    )

    class Meta:
        verbose_name = "Beneficio de Certificado"
        verbose_name_plural = "Beneficios de Certificado"
        ordering = ['id']
    
    def __str__(self):
        return f"{self.title} - {self.certificate.title}"


class CertificateRate(models.Model):
    """Modelo para las tasas de los certificados financieros"""
    certificate = models.ForeignKey('Certificate', on_delete=models.CASCADE, related_name='certificate_rates')
    label = models.CharField(
        max_length=200,
        verbose_name="Etiqueta",
        help_text="Etiqueta de la tarifa (ej: Monto de apertura)"
    )
    value = models.CharField(
        max_length=100,
        verbose_name="Valor",
        help_text="Valor de la tarifa (ej: $5,000,000.00)"
    )
  
    class Meta:
        verbose_name = "Tarifa de Certificado"
        verbose_name_plural = "Tarifas de Certificado"
        ordering = ['id']
    
    def __str__(self):
        return f"{self.label}: {self.value}"


class CertificateDepositRate(models.Model):
    """Modelo para las tasas de depósito de los certificados financieros"""
    certificate = models.ForeignKey('Certificate', on_delete=models.CASCADE, related_name='certificate_deposit_rates')
    range = models.CharField(
        max_length=200,
        verbose_name="Rango",
        help_text="Rango de monto (ej: De 10,000.00 a 500,000.00)"
    )
    rate = models.CharField(
        max_length=50,
        verbose_name="Tasa",
        help_text="Tasa de interés (ej: 5%)"
    )
    term = models.CharField(
        max_length=100,
        verbose_name="Plazo",
        help_text="Plazo de la inversión (ej: de 30 a 90 días)"
    )
   
    class Meta:
        verbose_name = "Tasa de Depósito de Certificado"
        verbose_name_plural = "Tasas de Depósito de Certificado"
        ordering = ['id']
    
    def __str__(self):
        return f"{self.range} - {self.rate} - {self.term}"


class CertificateFAQ(models.Model):
    """Modelo para las preguntas frecuentes de los certificados financieros"""
    certificate = models.ForeignKey('Certificate', on_delete=models.CASCADE, related_name='certificate_faqs')
    question = models.TextField(
        verbose_name="Pregunta",
        help_text="Pregunta frecuente"
    )
    answer = models.TextField(
        verbose_name="Respuesta",
        help_text="Respuesta a la pregunta frecuente"
    )

    class Meta:
        verbose_name = "FAQ de Certificado"
        verbose_name_plural = "FAQs de Certificado"
        ordering = ['id']
    
    def __str__(self):
        return f"{self.question[:50]}..."


class Certificate(models.Model):
    CERTIFICATE_TYPE_CHOICES = [
        ('financial', 'Certificado Financiero'),
        ('investment', 'Certificado de Inversión'),
        ('savings', 'Certificado de Ahorro'),
        ('business', 'Certificado Empresarial'),
    ]
    
    # Información básica
    title = models.CharField(
        max_length=200,
        verbose_name="Título principal",
        help_text="Título principal del certificado"
    )
    subtitle = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Subtítulo",
        help_text="Subtítulo del certificado"
    )
    description = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción del certificado"
    )
    
    # Imágenes
    banner_image = models.ImageField(
        upload_to='products/certificates/banners/',
        null=True,
        blank=True,
        verbose_name="Imagen de banner",
        help_text="Imagen de banner para el certificado"
    )
    certificate_image = models.ImageField(
        upload_to='products/certificates/',
        null=True,
        blank=True,
        verbose_name="Imagen del certificado",
        help_text="Imagen principal del certificado"
    )
    
    # Tipo de certificado
    certificate_type = models.CharField(
        max_length=20,
        choices=CERTIFICATE_TYPE_CHOICES,
        default='financial',
        verbose_name="Tipo de certificado",
        help_text="Tipo de certificado"
    )
    
    # CTA (Call to Action)
    cta_apply = models.CharField(
        max_length=50,
        default="Solicitar",
        verbose_name="Texto del botón solicitar",
        help_text="Texto del botón de solicitar"
    )
    cta_rates = models.CharField(
        max_length=50,
        default="Tarifario",
        verbose_name="Texto del botón tarifario",
        help_text="Texto del botón de tarifario"
    )
    
    # Beneficios
    benefits_title = models.CharField(
        max_length=200,
        default="Beneficios de tu Certificado Financiero",
        verbose_name="Título de beneficios",
        help_text="Título de la sección de beneficios"
    )
    
    # Inversión
    investment_title = models.CharField(
        max_length=200,
        default="Tu nueva Inversión",
        verbose_name="Título de inversión",
        help_text="Título de la sección de inversión"
    )
    investment_subtitle = models.CharField(
        max_length=200,
        default="Especificaciones del depósito a plazo fijo para personas:",
        verbose_name="Subtítulo de inversión",
        help_text="Subtítulo de la sección de inversión"
    )
    investment_details = models.TextField(
        blank=True,
        verbose_name="Detalles de inversión",
        help_text="Detalles de la inversión separados por /"
    )
    
    # Tasas
    rates_title = models.CharField(
        max_length=200,
        default="Tarifas",
        verbose_name="Título de tarifas",
        help_text="Título de la sección de tarifas"
    )
    
    # Requisitos
    requirements_title = models.CharField(
        max_length=200,
        default="Requisitos",
        verbose_name="Título de requisitos",
        help_text="Título de la sección de requisitos"
    )
    requirements = models.TextField(
        blank=True,
        verbose_name="Requisitos",
        help_text="Requisitos separados por /"
    )
    
    # Tasas de depósito
    deposit_rates_title = models.CharField(
        max_length=200,
        default="Escala de Tasas de Captaciones de Depósitos",
        verbose_name="Título de tasas de depósito",
        help_text="Título de la sección de tasas de depósito"
    )
    deposit_rates_valid_from = models.CharField(
        max_length=200,
        default="Vigente desde el 31 de enero del 2023",
        verbose_name="Vigencia de tasas",
        help_text="Texto de vigencia de las tasas"
    )
    
    # FAQ
    faq_title = models.CharField(
        max_length=200,
        default="Preguntas Frecuentes Certificado Financiero",
        verbose_name="Título de FAQ",
        help_text="Título de la sección de preguntas frecuentes"
    )
    
    # Estado
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si el certificado está activo"
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

    class Meta:
        verbose_name = "Certificate"
        verbose_name_plural = "Certificates"
        ordering = ['certificate_type', 'title']

    def __str__(self):
        return f"{self.title} - {self.get_certificate_type_display()}"

    @property
    def banner_image_url(self):
        """
        Retorna la URL de la imagen de banner para el frontend
        """
        if self.banner_image:
            return self.banner_image.url
        return None

    @property
    def certificate_image_url(self):
        """
        Retorna la URL de la imagen del certificado para el frontend
        """
        if self.certificate_image:
            return self.certificate_image.url
        return None

    @property
    def investment_details_list(self):
        """
        Retorna los detalles de inversión como lista para el frontend
        """
        if self.investment_details:
            return [detail.strip() for detail in self.investment_details.split('/') if detail.strip()]
        return []

    @property
    def requirements_list(self):
        """
        Retorna los requisitos como lista para el frontend
        """
        if self.requirements:
            return [req.strip() for req in self.requirements.split('/') if req.strip()]
        return []

    @property
    def benefits_list(self):
        """
        Retorna los beneficios como lista para el frontend
        """
        benefits = []
        for benefit in self.certificate_benefits.all():
            benefits.append({
                'title': benefit.title,
                'description': benefit.description
            })
        return benefits

    @property
    def rates_list(self):
        """
        Retorna las tarifas como lista para el frontend
        """
        rates = []
        for rate in self.certificate_rates.all():
            rates.append({
                'label': rate.label,
                'value': rate.value
            })
        return rates

    @property
    def deposit_rates_list(self):
        """
        Retorna las tasas de depósito como lista para el frontend
        """
        deposit_rates = []
        for rate in self.certificate_deposit_rates.all():
            deposit_rates.append({
                'range': rate.range,
                'rate': rate.rate,
                'term': rate.term
            })
        return deposit_rates

    @property
    def faq_list(self):
        """
        Retorna las preguntas frecuentes como lista para el frontend
        """
        faqs = []
        for faq in self.certificate_faqs.all():
            faqs.append({
                'question': faq.question,
                'answer': faq.answer
            })
        return faqs

    @property
    def slug(self):
        """
        Retorna el slug del título para URLs amigables
        """
        return slugify(self.title)


class Banner(models.Model):
    """Modelo para banners promocionales con botones de acción"""
    
    # Información básica
    title = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Título principal del banner"
    )
    description = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción del banner"
    )
    
    # Botón 1
    button1_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Botón 1",
        help_text="Texto que aparecerá en el primer botón"
    )
    button1_url = models.URLField(
        verbose_name="URL del Botón 1",
        help_text="Enlace al que dirigirá el primer botón"
    )
    
    # Botón 2
    button2_name = models.CharField(
        max_length=100,
        verbose_name="Nombre del Botón 2",
        help_text="Texto que aparecerá en el segundo botón"
    )
    button2_url = models.URLField(
        verbose_name="URL del Botón 2",
        help_text="Enlace al que dirigirá el segundo botón"
    )
    
    # Estado y orden
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si el banner está activo"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Orden",
        help_text="Orden de visualización (menor número = mayor prioridad)"
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

    class Meta:
        verbose_name = "Banner"
        verbose_name_plural = "Banner"
        ordering = ['order', 'title']
        constraints = [
            models.UniqueConstraint(
                fields=['is_active'],
                condition=models.Q(is_active=True),
                name='unique_active_banner'
            )
        ]

    def __str__(self):
        return f"{self.title} - Orden: {self.order}"

    @property
    def slug(self):
        """
        Retorna el slug del título para URLs amigables
        """
        return slugify(self.title) 