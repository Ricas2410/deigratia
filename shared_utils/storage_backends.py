"""
Custom storage backends for Ricas School Management System.
"""

from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
import os


class B2MediaStorage(S3Boto3Storage):
    """
    Backblaze B2 storage backend for media files.
    """
    bucket_name = getattr(settings, 'B2_BUCKET_NAME', 'ricas-school-media')
    region_name = getattr(settings, 'B2_REGION', 'us-west-000')
    endpoint_url = getattr(settings, 'B2_ENDPOINT_URL', 'https://s3.us-west-000.backblazeb2.com')
    access_key = getattr(settings, 'B2_ACCESS_KEY_ID', '')
    secret_key = getattr(settings, 'B2_SECRET_ACCESS_KEY', '')
    file_overwrite = False
    default_acl = 'public-read'
    
    # Custom settings for B2
    custom_domain = getattr(settings, 'B2_CUSTOM_DOMAIN', None)
    url_protocol = 'https:'
    
    def __init__(self, *args, **kwargs):
        kwargs['bucket_name'] = self.bucket_name
        kwargs['region_name'] = self.region_name
        kwargs['endpoint_url'] = self.endpoint_url
        kwargs['access_key'] = self.access_key
        kwargs['secret_key'] = self.secret_key
        kwargs['file_overwrite'] = self.file_overwrite
        kwargs['default_acl'] = self.default_acl
        
        if self.custom_domain:
            kwargs['custom_domain'] = self.custom_domain
            
        super().__init__(*args, **kwargs)


class B2StaticStorage(S3Boto3Storage):
    """
    Backblaze B2 storage backend for static files.
    """
    bucket_name = getattr(settings, 'B2_STATIC_BUCKET_NAME', 'ricas-school-static')
    region_name = getattr(settings, 'B2_REGION', 'us-west-000')
    endpoint_url = getattr(settings, 'B2_ENDPOINT_URL', 'https://s3.us-west-000.backblazeb2.com')
    access_key = getattr(settings, 'B2_ACCESS_KEY_ID', '')
    secret_key = getattr(settings, 'B2_SECRET_ACCESS_KEY', '')
    file_overwrite = True  # For static files, we want to overwrite
    default_acl = 'public-read'
    
    # Custom settings for B2
    custom_domain = getattr(settings, 'B2_STATIC_CUSTOM_DOMAIN', None)
    url_protocol = 'https:'
    
    def __init__(self, *args, **kwargs):
        kwargs['bucket_name'] = self.bucket_name
        kwargs['region_name'] = self.region_name
        kwargs['endpoint_url'] = self.endpoint_url
        kwargs['access_key'] = self.access_key
        kwargs['secret_key'] = self.secret_key
        kwargs['file_overwrite'] = self.file_overwrite
        kwargs['default_acl'] = self.default_acl
        
        if self.custom_domain:
            kwargs['custom_domain'] = self.custom_domain
            
        super().__init__(*args, **kwargs)


# Alternative direct B2 implementation (if S3 compatibility doesn't work)
class DirectB2Storage:
    """
    Direct Backblaze B2 storage implementation using b2sdk.
    """
    
    def __init__(self):
        from b2sdk.v2 import InMemoryAccountInfo, B2Api
        
        self.info = InMemoryAccountInfo()
        self.b2_api = B2Api(self.info)
        
        # Authorize with B2
        self.b2_api.authorize_account(
            'production',  # or 'production'
            getattr(settings, 'B2_APPLICATION_KEY_ID', ''),
            getattr(settings, 'B2_APPLICATION_KEY', '')
        )
        
        self.bucket_name = getattr(settings, 'B2_BUCKET_NAME', 'ricas-school-media')
        self.bucket = self.b2_api.get_bucket_by_name(self.bucket_name)
    
    def save(self, name, content):
        """Save file to B2."""
        try:
            file_info = self.bucket.upload_bytes(
                content.read(),
                name,
                content_type=getattr(content, 'content_type', 'application/octet-stream')
            )
            return name
        except Exception as e:
            raise Exception(f"Failed to upload to B2: {e}")
    
    def url(self, name):
        """Get URL for file."""
        try:
            file_info = self.bucket.get_file_info_by_name(name)
            return file_info.download_url
        except:
            return f"https://f000.backblazeb2.com/file/{self.bucket_name}/{name}"
    
    def exists(self, name):
        """Check if file exists."""
        try:
            self.bucket.get_file_info_by_name(name)
            return True
        except:
            return False
    
    def delete(self, name):
        """Delete file from B2."""
        try:
            file_info = self.bucket.get_file_info_by_name(name)
            self.bucket.delete_file_version(file_info.id_, name)
            return True
        except:
            return False
