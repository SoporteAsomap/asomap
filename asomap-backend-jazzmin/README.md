# ASOMAP Backend - Documentación de la API

Este proyecto utiliza **drf-spectacular** (Swagger/OpenAPI 3.0) para generar documentación interactiva de todos los endpoints del backend Django REST.

## Configuración de Base de Datos

El proyecto está configurado para usar **SQLite local** (`asomap.db`) para simplificar el desarrollo.

## Acceso a la documentación interactiva

- **Documentación API:** [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)

## ¿Qué incluye la documentación?
- Todos los endpoints GET de About, Layout, Products, News
- Estructura de respuestas JSON
- Códigos de error y ejemplos de respuesta
- Parámetros de consulta y filtros
- Descripciones detalladas en docstrings
- Autenticación JWT (futuro)

## Instalación y Setup

1. **Instalar dependencias:**
```bash
pip install -r requirements.txt
```

2. **Ejecutar migraciones:**
```bash
python manage.py makemigrations
python manage.py migrate
```

3. **Crear superusuario (opcional):**
```bash
python manage.py createsuperuser
```

4. **Ejecutar servidor:**
```bash
python manage.py runserver
```

## Documentación de Endpoints

La documentación se genera automáticamente desde los docstrings de los métodos en los viewsets. Por ejemplo:

```python
@action(detail=False, methods=['get'], url_path='hero')
def hero(self, request):
    """
    Obtener información del Hero Section
    
    Retorna la información principal del hero section de ASOMAP
    """
    # código del endpoint
```

## Requisitos
- coreapi >= 2.3.3
- Django REST Framework
- SQLite3 (incluido con Python)

## Personalización
Puedes modificar la configuración en `settings.py` bajo la clave `REST_FRAMEWORK` para cambiar la configuración de la documentación.

---

**Equipo de desarrollo ASOMAP** # asomap-backend
# trigger backend deploy Mon Jun  1 02:06:09 PM -04 2026
# trigger backend deploy Mon Jun  1 02:19:33 PM -04 2026
