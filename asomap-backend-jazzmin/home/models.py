from django.db import models


class DebitCardPromo(models.Model):
    """
    Modelo para la promoción de tarjeta de débito en la página de inicio
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Título principal de la promoción"
    )
    highlighted_title = models.CharField(
        max_length=200,
        verbose_name="Título destacado",
        help_text="Parte del título que se destaca visualmente"
    )
    description = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción detallada de la promoción"
    )
    primary_button_text = models.CharField(
        max_length=100,
        verbose_name="Texto del botón principal",
        help_text="Texto del botón de acción principal"
    )
    secondary_button_text = models.CharField(
        max_length=100,
        verbose_name="Texto del botón secundario",
        help_text="Texto del botón de acción secundaria"
    )
    primary_button_url = models.URLField(
        verbose_name="URL del botón principal",
        help_text="URL a la que redirige el botón principal",
        blank=True,
        null=True
    )
    secondary_button_url = models.URLField(
        verbose_name="URL del botón secundario",
        help_text="URL a la que redirige el botón secundario",
        blank=True,
        null=True
    )
    image = models.ImageField(
        upload_to='home/debit_card_promo/',
        verbose_name="Imagen",
        help_text="Imagen de la promoción de tarjeta de débito",
        blank=True,
        null=True
    )
    image_alt = models.CharField(
        max_length=200,
        verbose_name="Texto alternativo de la imagen",
        help_text="Descripción de la imagen para accesibilidad"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si la promoción está activa"
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
        verbose_name = "Promoción de Tarjeta de Débito"
        verbose_name_plural = "Promociones de Tarjeta de Débito"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.highlighted_title}"

    @property
    def image_url(self):
        """
        Retorna la URL de la imagen para el frontend
        """
        if self.image:
            return self.image.url
        return None


class EducationItem(models.Model):
    """
    Modelo para elementos individuales de educación
    """
    id = models.AutoField(primary_key=True)
    image = models.ImageField(
        upload_to='home/education/',
        verbose_name="Imagen",
        help_text="Imagen del elemento educativo"
    )
    alt = models.CharField(
        max_length=200,
        verbose_name="Texto alternativo",
        help_text="Descripción de la imagen para accesibilidad"
    )
    description = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción del elemento educativo"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si el elemento está activo"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Orden",
        help_text="Orden de aparición del elemento"
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
        verbose_name = "Elemento Educativo"
        verbose_name_plural = "Elementos Educativos"
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.description[:50]}..."

    @property
    def image_url(self):
        """
        Retorna la URL de la imagen para el frontend
        """
        if self.image:
            return self.image.url
        return None


class EducationSection(models.Model):
    """
    Modelo para la sección de educación
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Título principal de la sección de educación"
    )
    subtitle = models.CharField(
        max_length=300,
        verbose_name="Subtítulo",
        help_text="Subtítulo descriptivo de la sección"
    )
    education_items = models.ManyToManyField(
        EducationItem,
        blank=True,
        verbose_name="Elementos educativos",
        related_name="sections"
    )
    footer_text = models.TextField(
        verbose_name="Texto del pie de página",
        help_text="Texto que aparece al final de la sección"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si la sección está activa"
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
        verbose_name = "Sección de Educación"
        verbose_name_plural = "Secciones de Educación"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Asegurar que solo haya una sección activa
        if self.is_active:
            EducationSection.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class PeKeAccountSummary(models.Model):
    """
    Modelo para el resumen de cuenta PeKe (cuenta especial para niños) en la página de inicio
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Título principal del resumen de cuenta PeKe"
    )
    description = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción del resumen de cuenta PeKe"
    )
    button_text = models.CharField(
        max_length=100,
        verbose_name="Texto del botón",
        help_text="Texto del botón de acción"
    )
    button_url = models.URLField(
        verbose_name="URL del botón",
        help_text="URL a la que redirige el botón",
        blank=True,
        null=True
    )
    image = models.ImageField(
        upload_to='home/peke_account_summary/',
        verbose_name="Imagen",
        help_text="Imagen del resumen de cuenta PeKe",
        blank=True,
        null=True
    )
    image_alt = models.CharField(
        max_length=200,
        verbose_name="Texto alternativo de la imagen",
        help_text="Descripción de la imagen para accesibilidad"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si el resumen está activo"
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
        verbose_name = "Resumen de Cuenta PeKe"
        verbose_name_plural = "Resúmenes de Cuenta PeKe"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    @property
    def image_url(self):
        """
        Retorna la URL de la imagen para el frontend
        """
        if self.image:
            return self.image.url
        return None

    def save(self, *args, **kwargs):
        # Asegurar que solo haya un resumen activo
        if self.is_active:
            PeKeAccountSummary.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class Product(models.Model):
    """
    Modelo para productos individuales en la sección de productos
    """
    CATEGORY_CHOICES = [
        ('prestamos', 'Préstamos'),
        ('cuentas', 'Cuentas'),
        ('tarjetas', 'Tarjetas'),
        ('certificados', 'Certificados'),
    ]
    
    id = models.AutoField(primary_key=True)
    title = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Título del producto"
    )
    description = models.TextField(
        verbose_name="Descripción",
        help_text="Descripción del producto"
    )
    image = models.ImageField(
        upload_to='home/products/',
        verbose_name="Imagen",
        help_text="Imagen del producto"
    )
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        verbose_name="Categoría",
        help_text="Categoría del producto"
    )
    image_width = models.PositiveIntegerField(
        default=600,
        verbose_name="Ancho de imagen",
        help_text="Ancho de la imagen en píxeles"
    )
    image_height = models.PositiveIntegerField(
        default=400,
        verbose_name="Alto de imagen",
        help_text="Alto de la imagen en píxeles"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si el producto está activo"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Orden",
        help_text="Orden de aparición del producto"
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
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.title} - {self.get_category_display()}"

    @property
    def image_url(self):
        """
        Retorna la URL de la imagen para el frontend
        """
        if self.image:
            return self.image.url
        return None


class ProductSection(models.Model):
    """
    Modelo para la sección de productos en la página de inicio
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(
        max_length=200,
        verbose_name="Título",
        help_text="Título principal de la sección de productos"
    )
    subtitle = models.CharField(
        max_length=300,
        verbose_name="Subtítulo",
        help_text="Subtítulo descriptivo de la sección"
    )
    button_text = models.CharField(
        max_length=100,
        verbose_name="Texto del botón",
        help_text="Texto del botón de acción"
    )
    products = models.ManyToManyField(
        Product,
        blank=True,
        verbose_name="Productos",
        related_name="sections"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si la sección está activa"
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
        verbose_name = "Sección de Productos"
        verbose_name_plural = "Secciones de Productos"
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Asegurar que solo haya una sección activa
        if self.is_active:
            ProductSection.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class SliderItem(models.Model):
    """
    Modelo para elementos del slider/carrusel en la página de inicio
    """
    id = models.AutoField(primary_key=True)
    # Imágenes para diferentes dispositivos
    image_desktop = models.ImageField(
        upload_to='home/slider/desktop/',
        verbose_name="Imagen Desktop",
        help_text="Imagen para dispositivos desktop (1920px width)"
    )
    image_tablet = models.ImageField(
        upload_to='home/slider/tablet/',
        verbose_name="Imagen Tablet",
        help_text="Imagen para dispositivos tablet (1024px width)"
    )
    image_mobile = models.ImageField(
        upload_to='home/slider/mobile/',
        verbose_name="Imagen Mobile",
        help_text="Imagen para dispositivos móviles (640px width)"
    )
    alt = models.CharField(
        max_length=200,
        verbose_name="Texto alternativo",
        help_text="Descripción de la imagen para accesibilidad"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Activo",
        help_text="Indica si el elemento del slider está activo"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Orden",
        help_text="Orden de aparición en el slider"
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
        verbose_name = "Elemento del Slider"
        verbose_name_plural = "Elementos del Slider"
        ordering = ['order', 'created_at']

    def __str__(self):
        return f"{self.alt} (Orden: {self.order})"

    @property
    def image_desktop_url(self):
        """
        Retorna la URL de la imagen desktop para el frontend
        """
        if self.image_desktop:
            return self.image_desktop.url
        return None

    @property
    def image_tablet_url(self):
        """
        Retorna la URL de la imagen tablet para el frontend
        """
        if self.image_tablet:
            return self.image_tablet.url
        return None

    @property
    def image_mobile_url(self):
        """
        Retorna la URL de la imagen mobile para el frontend
        """
        if self.image_mobile:
            return self.image_mobile.url
        return None
