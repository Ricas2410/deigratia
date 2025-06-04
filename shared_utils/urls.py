"""
URLs for shared utilities including storage management.
"""

from django.urls import path
from . import views

app_name = 'shared_utils'

urlpatterns = [
    # Storage Management URLs
    path('storage/test-connection/', views.test_storage_connection, name='test-storage-connection'),
    path('storage/update-counts/', views.update_file_counts, name='update-file-counts'),
    path('storage/migrate/', views.storage_migration_view, name='storage-migration'),
    path('storage/status/', views.storage_status_api, name='storage-status'),
    path('storage/health/', views.storage_health_check, name='storage-health'),
    
    # Media file serving with fallback
    path('media/<path:file_path>', views.media_file_view, name='media-file'),
]
