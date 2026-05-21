from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import os

def optimize_image(uploaded_file, max_size=(1200, 1200), quality=85):
    """
    Optimiza imagen convirtiéndola a WebP.
    
    Args:
        uploaded_file: Archivo subido (request.FILES['image'])
        max_size: Tupla (ancho_max, alto_max) para redimensionar
        quality: Calidad WebP (1-100, recomendado 80-90)
    
    Returns:
        InMemoryUploadedFile: Imagen WebP optimizada
    """
    # Abrir y optimizar imagen
    img = Image.open(uploaded_file)
    
    # Redimensionar manteniendo aspect ratio
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    
    # Guardar en buffer como WebP
    output = BytesIO()
    img.save(
        output,
        format='WEBP',
        quality=quality,
        method=6  # Máxima compresión (0-6)
    )
    
    # Preparar archivo para Django
    output.seek(0)
    
    # Nombre original con extensión .webp
    original_name = os.path.splitext(uploaded_file.name)[0]
    new_name = f"{original_name}.webp"
    
    return InMemoryUploadedFile(
        output,
        'ImageField',
        new_name,
        'image/webp',
        output.getbuffer().nbytes,
        None
    )


def get_image_info(uploaded_file):
    """
    Obtiene información de la imagen (opcional, para debug)
    """
    img = Image.open(uploaded_file)
    return {
        'width': img.width,
        'height': img.height,
        'format': img.format,
        'size_kb': round(uploaded_file.size / 1024, 2)
    }
