import cloudinary.uploader
from django.conf import settings
import cloudinary

def configure_cloudinary():
    cloudinary.config(
        cloud_name=settings.CLOUDINARY_STORAGE['CLOUD_NAME'],
        api_key=settings.CLOUDINARY_STORAGE['API_KEY'],
        api_secret=settings.CLOUDINARY_STORAGE['API_SECRET'],
    )

def upload_evidence(file, folder='evidence'):
    """
    Upload a file to Cloudinary and return the secure URL.
    """
    configure_cloudinary()
    try:
        result = cloudinary.uploader.upload(
            file,
            folder=f'amakaziwatch/{folder}',
            resource_type='auto',
        )
        return {'success': True, 'url': result['secure_url']}
    except Exception as e:
        return {'success': False, 'error': str(e)}
