from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
from django_prose_editor.fields import ProseEditorField
from bs4 import BeautifulSoup


class Hero(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Hero"
        verbose_name_plural = "Heroes"

    def __str__(self):
        return self.title

class QuienesSomos(models.Model):
    title = models.CharField(max_length=200)
    paragraphs = ProseEditorField(
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
            "Paragraph": True,
            "HardBreak": True,
        },
        sanitize=True,  # Server side sanitization is strongly recommended
        verbose_name="Contenido completo",
        help_text="Contenido completo con formato enriquecido. Presiona Enter para nuevo párrafo, Shift+Enter para salto de línea."
    )
    image_src = models.ImageField(upload_to='about/quienes-somos/', null=True, blank=True)
    image_alt = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Quiénes Somos"
        verbose_name_plural = "Quiénes Somos"

    def __str__(self):
        return self.title

    @property
    def paragraphs_list(self):
        """
        Retorna los párrafos como lista para el frontend
        """
        if self.paragraphs:
            return [p.strip() for p in self.paragraphs.split('\n\n') if p.strip()]
        return []

class NuestraHistoria(models.Model):
    title = models.CharField(max_length=200)
    paragraphs = ProseEditorField(
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
            "Paragraph": True,
            "HardBreak": True,
        },
        sanitize=True,  # Server side sanitization is strongly recommended
        verbose_name="Contenido completo",
        help_text="Contenido completo con formato enriquecido. Presiona Enter para nuevo párrafo, Shift+Enter para salto de línea."
    )
    image_src = models.ImageField(upload_to='about/historia/', null=True, blank=True)
    image_alt = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Nuestra Historia"
        verbose_name_plural = "Nuestra Historia"

    def __str__(self):
        return self.title

    # @property
    # def paragraphs_list(self):
    #     """
    #     Retorna el contenido HTML de ProseEditor para renderizado en el frontend
    #     """
    #     if not self.paragraphs:
    #         return []

    #     return self.paragraphs

class Mision(models.Model):
    title = models.CharField(max_length=200)
    description = ProseEditorField(
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
            "Paragraph": True,
            "HardBreak": True,
        },
        sanitize=True,  # Server side sanitization is strongly recommended
        verbose_name="Contenido completo",
        help_text="Contenido completo con formato enriquecido. Presiona Enter para nuevo párrafo, Shift+Enter para salto de línea."
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Misión"
        verbose_name_plural = "Misiones"

    def __str__(self):
        return self.title

class Vision(models.Model):
    title = models.CharField(max_length=200)
    description = ProseEditorField(
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
            "Paragraph": True,
            "HardBreak": True,
        },
        sanitize=True,  # Server side sanitization is strongly recommended
        verbose_name="Contenido completo",
        help_text="Contenido completo con formato enriquecido. Presiona Enter para nuevo párrafo, Shift+Enter para salto de línea."
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Visión"
        verbose_name_plural = "Visiones"

    def __str__(self):
        return self.title

class Valor(models.Model):
    title = models.CharField(max_length=100)
    description = ProseEditorField(
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
            "Paragraph": True,
            "HardBreak": True,
        },
        sanitize=True,  # Server side sanitization is strongly recommended
        verbose_name="Contenido completo",
        help_text="Contenido completo con formato enriquecido. Presiona Enter para nuevo párrafo, Shift+Enter para salto de línea."
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Valor"
        verbose_name_plural = "Valores"

    def __str__(self):
        return self.title

class Director(models.Model):
    name = models.CharField(max_length=200)
    position = models.CharField(max_length=200)
    image_src = models.ImageField(upload_to='about/directores/', null=True, blank=True)
    image_alt = models.CharField(max_length=200, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Director"
        verbose_name_plural = "Directores"

    def __str__(self):
        return f"{self.name} - {self.position}"

class CommunityCategory(models.Model):
    """
    Modelo para las categorías de apoyo comunitario
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Nombre")
    icon = models.CharField(
        max_length=50, 
        verbose_name="Icono",
        help_text="Nombre del icono de React Icons (ej: FaHeart, FaStar, FaUser). Consulta https://react-icons.github.io/react-icons/ para encontrar el icono correcto."
    )
    description = models.TextField(verbose_name="Descripción")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Categoría de Apoyo Comunitario"
        verbose_name_plural = "Categorías de Apoyo Comunitario"
        ordering = ['id']

    def __str__(self):
        return self.name

class CommunityInitiative(models.Model):
    """
    Modelo para las iniciativas de apoyo comunitario
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción")
    impact = models.TextField(verbose_name="Impacto")
    image_src = models.ImageField(
        upload_to='community/initiatives/',
        null=True,
        blank=True,
        verbose_name="Imagen"
    )
    image_alt = models.CharField(
        max_length=300,
        null=True,
        blank=True,
        verbose_name="Texto alternativo de imagen"
    )
    category = models.ForeignKey(
        CommunityCategory,
        on_delete=models.CASCADE,
        related_name='initiatives',
        verbose_name="Categoría"
    )
    year = models.IntegerField(
        verbose_name="Año",
        help_text="Año en que se realizó la iniciativa",
        null=True,
        blank=True
    )
    location = models.CharField(
        max_length=200,
        verbose_name="Ubicación",
        help_text="Nombre de la ubicación donde se realizó la iniciativa",
        null=True,
        blank=True
    )
    beneficiaries = models.CharField(
        max_length=200,
        verbose_name="Beneficiarios",
        help_text="Descripción de los beneficiarios de la iniciativa",
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Iniciativa de Apoyo Comunitario"
        verbose_name_plural = "Iniciativas de Apoyo Comunitario"
        ordering = ['category', 'id']

    def __str__(self):
        return self.title

class CommunitySupport(models.Model):
    """
    Modelo principal para la sección de Apoyo a la Comunidad
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción")
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Apoyo a la Comunidad"
        verbose_name_plural = "Apoyo a la Comunidad"

    def __str__(self):
        return self.title

class FinancialDocument(models.Model):
    """
    Modelo para documentos financieros (auditados y trimestrales)
    """
    DOCUMENT_TYPE_CHOICES = [
        ('audited', 'Auditado'),
        ('quarterly', 'Trimestral'),
    ]
    
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, verbose_name="Título")
    file = models.FileField(
        upload_to='financial_documents/',
        verbose_name="Archivo PDF",
        help_text="Subir archivo PDF del documento financiero",
        blank=True,
        null=True
    )
    quarter = models.CharField(
        max_length=2, 
        blank=True, 
        null=True, 
        verbose_name="Trimestre",
        help_text="1, 2, 3, 4 (solo para documentos trimestrales)"
    )
    document_type = models.CharField(
        max_length=10,
        choices=DOCUMENT_TYPE_CHOICES,
        verbose_name="Tipo de documento"
    )
    year = models.CharField(
        max_length=4, 
        verbose_name="Año",
        help_text="Ej: 2024, 2023, 2022",
        null=True,
        blank=True
    )
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Documento Financiero"
        verbose_name_plural = "Documentos Financieros"
        ordering = ['-year', 'document_type', 'quarter']
        unique_together = ['year', 'document_type', 'quarter']

    def __str__(self):
        if self.document_type == 'quarterly' and self.quarter:
            return f"{self.title} - Q{self.quarter} {self.year}"
        return f"{self.title} - {self.year}"

class FinancialStatementsConfig(models.Model):
    """
    Modelo para la configuración principal de estados financieros
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(
        max_length=200, 
        default="Estados Financieros",
        verbose_name="Título"
    )
    description = models.TextField(
        default="Consulta nuestros estados financieros auditados y trimestrales",
        verbose_name="Descripción"
    )
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Configuración de Estados Financieros"
        verbose_name_plural = "Configuración de Estados Financieros"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Asegurar que solo haya una configuración activa
        if self.is_active:
            FinancialStatementsConfig.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

class MemoryDocument(models.Model):
    """
    Modelo para documentos de memoria anual
    """
    id = models.AutoField(primary_key=True)
    file = models.FileField(
        upload_to='memory_documents/',
        verbose_name="Archivo PDF",
        help_text="Subir archivo PDF de la memoria anual",
        blank=True,
        null=True
    )
    year = models.CharField(
        max_length=4, 
        verbose_name="Año",
        help_text="Ej: 2023, 2022, 2021"
    )
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Documento de Memoria"
        verbose_name_plural = "Documentos de Memoria"
        ordering = ['-year']
        unique_together = ['year']

    def __str__(self):
        return f"Memoria {self.year}"

class MemoryConfig(models.Model):
    """
    Modelo para la configuración principal de memorias anuales
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(
        max_length=200, 
        default="Memorias",
        verbose_name="Título"
    )
    description = models.TextField(
        default="Un recorrido por nuestra historia y logros institucionales",
        verbose_name="Descripción"
    )
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Configuración de Memorias"
        verbose_name_plural = "Configuración de Memorias"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Asegurar que solo haya una configuración activa
        if self.is_active:
            MemoryConfig.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

class PolicyDocument(models.Model):
    """
    Modelo para documentos de políticas individuales
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, verbose_name="Título")
    description = models.TextField(verbose_name="Descripción")
    file = models.FileField(
        upload_to='policy_documents/',
        verbose_name="Archivo PDF",
        help_text="Subir archivo PDF de la política",
        blank=True,
        null=True
    )
    last_update = models.DateField(
        verbose_name="Última actualización",
        help_text="Fecha de la última actualización del documento"
    )
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Documento de Política"
        verbose_name_plural = "Documentos de Política"
        ordering = ['-last_update']

    def __str__(self):
        return self.title

class PolicyCategory(models.Model):
    """
    Modelo para categorías de políticas
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200, verbose_name="Título")
    icon = models.CharField(
        max_length=50, 
        verbose_name="Icono",
        help_text="Nombre del icono (ej: shield, cog, check-circle)"
    )
    description = models.TextField(verbose_name="Descripción")
    documents = models.ManyToManyField(
        PolicyDocument, 
        blank=True,
        verbose_name="Documentos",
        related_name="categories"
    )
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Categoría de Políticas"
        verbose_name_plural = "Categorías de Políticas"
        ordering = ['title']

    def __str__(self):
        return self.title

class PolicyConfig(models.Model):
    """
    Modelo para la configuración principal de políticas
    """
    id = models.AutoField(primary_key=True)
    title = models.CharField(
        max_length=200, 
        default="Políticas",
        verbose_name="Título"
    )
    description = models.TextField(
        default="Nuestras políticas institucionales garantizan la transparencia y eficiencia en nuestras operaciones.",
        verbose_name="Descripción"
    )
    download_text = models.CharField(
        max_length=100,
        default="Descargar documento",
        verbose_name="Texto de descarga"
    )
    last_update_text = models.CharField(
        max_length=100,
        default="Última actualización",
        verbose_name="Texto de última actualización"
    )
    all_policies_text = models.CharField(
        max_length=100,
        default="Todas las Políticas",
        verbose_name="Texto de todas las políticas"
    )
    is_active = models.BooleanField(default=True, verbose_name="Activo")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Fecha de actualización")

    class Meta:
        verbose_name = "Configuración de Políticas"
        verbose_name_plural = "Configuración de Políticas"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Asegurar que solo haya una configuración activa
        if self.is_active:
            PolicyConfig.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

# Ejemplo de datos iniciales (fixtures)
COMMUNITY_CATEGORIES_DATA = [
    {
        "name": "Responsabilidad Social",
        "icon": "FaHandHoldingHeart",
        "description": "Apoyo a organizaciones e instituciones que trabajan en beneficio de los más necesitados"
    },
    {
        "name": "Cultura",
        "icon": "FaPalette",
        "description": "Patrocinio de eventos culturales y publicaciones"
    },
    {
        "name": "Deportes",
        "icon": "FaFutbol",
        "description": "Apoyo a actividades y campeonatos deportivos"
    }
]

COMMUNITY_INITIATIVES_DATA = [
    {
        "title": "Apoyo a Instituciones Sociales",
        "description": "Contribuciones a organizaciones como el Albergue Educativo Infantil, parroquias, Centro Juvenil Don Bosco, Hogar Escuela La Milagrosa, y más.",
        "impact": "Beneficiando a múltiples instituciones en Moca, Gaspar Hernández, Cayetano Germosén, Villa Tapia y otras localidades.",
        "category_name": "Responsabilidad Social"
    },
    {
        "title": "Iniciativas Culturales",
        "description": "Patrocinio de publicaciones, libros, brochures, conciertos populares, fiestas de carnaval, fiestas patronales y ferias multiservicios.",
        "impact": "Fortalecimiento de la identidad cultural y las tradiciones locales.",
        "category_name": "Cultura"
    },
    {
        "title": "Apoyo al Deporte",
        "description": "Respaldo a campeonatos nacionales e internacionales en béisbol, ajedrez, damas, baloncesto, voleibol, fútbol y softball.",
        "impact": "Promoción del deporte y la actividad física en la comunidad.",
        "category_name": "Deportes"
    }
] 