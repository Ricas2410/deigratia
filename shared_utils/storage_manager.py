"""
Dynamic Storage Manager for Deigratia Montessori School Management System.
Provides flexible switching between local and cloud storage with migration capabilities.
"""

import os
import logging
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.db import models
from pathlib import Path
import shutil
from typing import Optional, List, Dict, Any

logger = logging.getLogger(__name__)


class StorageSettings(models.Model):
    """
    Model to store storage configuration settings.
    Allows admin to switch between storage backends.
    """
    STORAGE_CHOICES = [
        ('local', 'Local File System'),
        ('backblaze_b2', 'Backblaze B2 Cloud Storage'),
        ('aws_s3', 'Amazon S3'),
        ('custom', 'Custom Storage Backend'),
    ]
    
    # Storage Configuration
    active_storage = models.CharField(
        max_length=20,
        choices=STORAGE_CHOICES,
        default='local',
        help_text="Currently active storage backend"
    )
    
    # Cloud Storage Settings
    cloud_access_key = models.CharField(
        max_length=200,
        blank=True,
        help_text="Access key for cloud storage (B2 Application Key ID / AWS Access Key)"
    )
    cloud_secret_key = models.CharField(
        max_length=200,
        blank=True,
        help_text="Secret key for cloud storage (B2 Application Key / AWS Secret Key)"
    )
    cloud_bucket_name = models.CharField(
        max_length=100,
        blank=True,
        help_text="Bucket name for cloud storage"
    )
    cloud_region = models.CharField(
        max_length=50,
        blank=True,
        default='us-west-000',
        help_text="Region for cloud storage"
    )
    cloud_endpoint_url = models.URLField(
        blank=True,
        help_text="Custom endpoint URL (for B2 or S3-compatible services)"
    )
    cloud_custom_domain = models.CharField(
        max_length=200,
        blank=True,
        help_text="Custom domain for serving files (optional)"
    )
    
    # Migration Settings
    auto_migrate_new_files = models.BooleanField(
        default=False,
        help_text="Automatically migrate new uploads to active storage"
    )
    
    # Status Fields
    last_migration_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Last time files were migrated between storages"
    )
    migration_in_progress = models.BooleanField(
        default=False,
        help_text="Whether a migration is currently in progress"
    )
    
    # Statistics
    local_files_count = models.IntegerField(
        default=0,
        help_text="Number of files in local storage"
    )
    cloud_files_count = models.IntegerField(
        default=0,
        help_text="Number of files in cloud storage"
    )
    total_storage_size_mb = models.FloatField(
        default=0.0,
        help_text="Total storage size in MB"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Storage Settings"
        verbose_name_plural = "Storage Settings"
    
    def __str__(self):
        return f"Storage Settings - {self.get_active_storage_display()}"
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and StorageSettings.objects.exists():
            raise ValueError("Only one StorageSettings instance is allowed")
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """Get or create storage settings instance."""
        settings, created = cls.objects.get_or_create(
            pk=1,
            defaults={
                'active_storage': 'local',
                'auto_migrate_new_files': False,
            }
        )
        return settings
    
    def get_storage_backend(self):
        """Get the appropriate storage backend based on settings."""
        if self.active_storage == 'local':
            return FileSystemStorage(
                location=settings.MEDIA_ROOT,
                base_url=settings.MEDIA_URL
            )
        elif self.active_storage == 'backblaze_b2':
            return self._get_b2_storage()
        elif self.active_storage == 'aws_s3':
            return self._get_s3_storage()
        else:
            # Fallback to local storage
            logger.warning(f"Unknown storage type: {self.active_storage}, falling back to local")
            return FileSystemStorage(
                location=settings.MEDIA_ROOT,
                base_url=settings.MEDIA_URL
            )
    
    def _get_b2_storage(self):
        """Get Backblaze B2 storage backend."""
        try:
            from shared_utils.storage_backends import B2MediaStorage
            return B2MediaStorage()
        except Exception as e:
            logger.error(f"Failed to initialize B2 storage: {e}")
            return FileSystemStorage(
                location=settings.MEDIA_ROOT,
                base_url=settings.MEDIA_URL
            )
    
    def _get_s3_storage(self):
        """Get AWS S3 storage backend."""
        try:
            from storages.backends.s3boto3 import S3Boto3Storage
            return S3Boto3Storage(
                access_key=self.cloud_access_key,
                secret_key=self.cloud_secret_key,
                bucket_name=self.cloud_bucket_name,
                region_name=self.cloud_region,
                endpoint_url=self.cloud_endpoint_url if self.cloud_endpoint_url else None,
                custom_domain=self.cloud_custom_domain if self.cloud_custom_domain else None,
            )
        except Exception as e:
            logger.error(f"Failed to initialize S3 storage: {e}")
            return FileSystemStorage(
                location=settings.MEDIA_ROOT,
                base_url=settings.MEDIA_URL
            )
    
    def test_storage_connection(self) -> Dict[str, Any]:
        """Test connection to the configured storage backend."""
        try:
            storage = self.get_storage_backend()
            
            # Try to save a test file
            test_content = ContentFile(b"test", name="test_connection.txt")
            test_path = storage.save("test_connection.txt", test_content)
            
            # Try to read it back
            if storage.exists(test_path):
                url = storage.url(test_path)
                
                # Clean up test file
                storage.delete(test_path)
                
                return {
                    'success': True,
                    'message': 'Storage connection successful',
                    'test_url': url
                }
            else:
                return {
                    'success': False,
                    'message': 'Failed to verify file upload'
                }
                
        except Exception as e:
            return {
                'success': False,
                'message': f'Storage connection failed: {str(e)}'
            }
    
    def update_file_counts(self):
        """Update file count statistics."""
        try:
            # Count local files
            media_root = Path(settings.MEDIA_ROOT)
            if media_root.exists():
                local_files = list(media_root.rglob('*'))
                self.local_files_count = len([f for f in local_files if f.is_file()])
                
                # Calculate total size
                total_size = sum(f.stat().st_size for f in local_files if f.is_file())
                self.total_storage_size_mb = total_size / (1024 * 1024)  # Convert to MB
            else:
                self.local_files_count = 0
                self.total_storage_size_mb = 0.0
            
            # TODO: Add cloud file counting when cloud storage is active
            self.cloud_files_count = 0
            
            self.save()
            
        except Exception as e:
            logger.error(f"Failed to update file counts: {e}")


class DynamicStorage:
    """
    Dynamic storage class that uses the configured storage backend.
    """

    def __init__(self):
        self._settings = None
        self._storage = None
    
    @property
    def settings(self):
        """Get storage settings lazily."""
        if self._settings is None:
            try:
                self._settings = StorageSettings.get_settings()
            except Exception:
                # If database doesn't exist yet, return None
                return None
        return self._settings

    @property
    def storage(self):
        """Get the current storage backend."""
        if self._storage is None:
            storage_settings = self.settings
            if storage_settings:
                self._storage = storage_settings.get_storage_backend()
            else:
                # Fallback to local storage if no settings available
                from django.conf import settings as django_settings
                self._storage = FileSystemStorage(
                    location=django_settings.MEDIA_ROOT,
                    base_url=django_settings.MEDIA_URL
                )
        return self._storage
    
    def save(self, name, content, max_length=None):
        """Save file using current storage backend."""
        try:
            return self.storage.save(name, content, max_length)
        except Exception as e:
            logger.error(f"Failed to save file {name}: {e}")
            # Fallback to local storage
            from django.conf import settings as django_settings
            local_storage = FileSystemStorage(
                location=django_settings.MEDIA_ROOT,
                base_url=django_settings.MEDIA_URL
            )
            return local_storage.save(name, content, max_length)
    
    def url(self, name):
        """Get URL for file."""
        try:
            return self.storage.url(name)
        except Exception as e:
            logger.error(f"Failed to get URL for {name}: {e}")
            # Fallback to local URL
            from django.conf import settings as django_settings
            return f"{django_settings.MEDIA_URL}{name}"
    
    def exists(self, name):
        """Check if file exists."""
        try:
            return self.storage.exists(name)
        except Exception as e:
            logger.error(f"Failed to check existence of {name}: {e}")
            return False
    
    def delete(self, name):
        """Delete file."""
        try:
            return self.storage.delete(name)
        except Exception as e:
            logger.error(f"Failed to delete {name}: {e}")
            return False
    
    def size(self, name):
        """Get file size."""
        try:
            return self.storage.size(name)
        except Exception as e:
            logger.error(f"Failed to get size of {name}: {e}")
            return 0


# Global instance for use in models
dynamic_storage = DynamicStorage()
