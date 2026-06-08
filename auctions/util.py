from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
import os

def optimize_image(uploaded_file, max_size=(1200, 1200), quality=85):
    """
    Optimize the image by converting it to WebP.

    Args:
    uploaded_file: Uploaded file (request.FILES['image'])
    max_size: Tuple (max_width, max_height) to resize
    quality: WebP quality (1-100, recommended 80-90)
    Returns:
    InMemoryUploadedFile: Optimized WebP image
    """
    
    img = Image.open(uploaded_file)
    
    # Resize while maintaining aspect ratio
    img.thumbnail(max_size, Image.Resampling.LANCZOS)
    
    # Save as WebP
    output = BytesIO()
    img.save(
        output,
        format='WEBP',
        quality=quality,
        method=6  
    )
    
    output.seek(0)
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
    Retrieves information from the image 
    """
    img = Image.open(uploaded_file)
    return {
        'width': img.width,
        'height': img.height,
        'format': img.format,
        'size_kb': round(uploaded_file.size / 1024, 2)
    }
