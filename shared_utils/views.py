"""
Views for storage management functionality.
"""

import json
import logging
from django.http import JsonResponse, HttpResponse
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.shortcuts import render
from django.contrib import messages
from .storage_manager import StorageSettings

logger = logging.getLogger(__name__)


@staff_member_required
@require_POST
@csrf_exempt
def test_storage_connection(request):
    """
    Test connection to the configured storage backend.
    """
    try:
        storage_settings = StorageSettings.get_settings()
        result = storage_settings.test_storage_connection()
        
        return JsonResponse(result)
        
    except Exception as e:
        logger.error(f"Error testing storage connection: {e}")
        return JsonResponse({
            'success': False,
            'message': f'Error testing connection: {str(e)}'
        })


@staff_member_required
@require_POST
@csrf_exempt
def update_file_counts(request):
    """
    Update file count statistics.
    """
    try:
        storage_settings = StorageSettings.get_settings()
        storage_settings.update_file_counts()
        
        return JsonResponse({
            'success': True,
            'message': 'File counts updated successfully',
            'local_files': storage_settings.local_files_count,
            'cloud_files': storage_settings.cloud_files_count,
            'total_size_mb': storage_settings.total_storage_size_mb
        })
        
    except Exception as e:
        logger.error(f"Error updating file counts: {e}")
        return JsonResponse({
            'success': False,
            'message': f'Error updating file counts: {str(e)}'
        })


@staff_member_required
def storage_migration_view(request):
    """
    View for managing storage migration.
    """
    from_storage = request.GET.get('from', 'local')
    to_storage = request.GET.get('to', 'cloud')
    
    if from_storage == to_storage:
        messages.error(request, "Source and destination storage cannot be the same")
        return render(request, 'admin/storage_migration_error.html')
    
    storage_settings = StorageSettings.get_settings()
    
    # Check if migration is already in progress
    if storage_settings.migration_in_progress:
        messages.warning(request, "A migration is already in progress")
        return render(request, 'admin/storage_migration_in_progress.html')
    
    context = {
        'from_storage': from_storage,
        'to_storage': to_storage,
        'storage_settings': storage_settings,
        'title': f'Migrate Files from {from_storage.title()} to {to_storage.title()}',
    }
    
    if request.method == 'POST':
        # Start migration process
        try:
            # Mark migration as in progress
            storage_settings.migration_in_progress = True
            storage_settings.save()
            
            # TODO: Implement async migration using Celery or similar
            # For now, show instructions for manual migration
            messages.success(
                request,
                f"Migration from {from_storage} to {to_storage} has been initiated. "
                "Please use the management command: "
                f"python manage.py migrate_storage --from {from_storage} --to {to_storage}"
            )
            
        except Exception as e:
            logger.error(f"Error starting migration: {e}")
            messages.error(request, f"Error starting migration: {str(e)}")
    
    return render(request, 'admin/storage_migration.html', context)


@staff_member_required
def storage_status_api(request):
    """
    API endpoint for storage status information.
    """
    try:
        storage_settings = StorageSettings.get_settings()
        
        # Test connection
        connection_test = storage_settings.test_storage_connection()
        
        return JsonResponse({
            'success': True,
            'active_storage': storage_settings.active_storage,
            'active_storage_display': storage_settings.get_active_storage_display(),
            'connection_status': connection_test,
            'local_files_count': storage_settings.local_files_count,
            'cloud_files_count': storage_settings.cloud_files_count,
            'total_storage_size_mb': storage_settings.total_storage_size_mb,
            'migration_in_progress': storage_settings.migration_in_progress,
            'last_migration_date': storage_settings.last_migration_date.isoformat() if storage_settings.last_migration_date else None,
        })
        
    except Exception as e:
        logger.error(f"Error getting storage status: {e}")
        return JsonResponse({
            'success': False,
            'message': f'Error getting storage status: {str(e)}'
        })


def media_file_view(request, file_path):
    """
    Serve media files with proper error handling.
    Falls back to different storage backends if file not found.
    """
    try:
        storage_settings = StorageSettings.get_settings()
        storage = storage_settings.get_storage_backend()
        
        # Try to serve from active storage
        if storage.exists(file_path):
            # Redirect to the file URL
            file_url = storage.url(file_path)
            return HttpResponse(
                status=302,
                headers={'Location': file_url}
            )
        
        # If not found in active storage, try local storage as fallback
        from django.core.files.storage import FileSystemStorage
        from django.conf import settings
        
        local_storage = FileSystemStorage(
            location=settings.MEDIA_ROOT,
            base_url=settings.MEDIA_URL
        )
        
        if local_storage.exists(file_path):
            file_url = local_storage.url(file_path)
            return HttpResponse(
                status=302,
                headers={'Location': file_url}
            )
        
        # File not found in any storage
        return HttpResponse(
            "File not found",
            status=404,
            content_type='text/plain'
        )
        
    except Exception as e:
        logger.error(f"Error serving media file {file_path}: {e}")
        return HttpResponse(
            f"Error serving file: {str(e)}",
            status=500,
            content_type='text/plain'
        )


@staff_member_required
def storage_health_check(request):
    """
    Comprehensive storage health check.
    """
    try:
        storage_settings = StorageSettings.get_settings()
        
        # Test active storage
        active_test = storage_settings.test_storage_connection()
        
        # Test local storage
        from django.core.files.storage import FileSystemStorage
        from django.conf import settings
        
        local_storage = FileSystemStorage(
            location=settings.MEDIA_ROOT,
            base_url=settings.MEDIA_URL
        )
        
        local_test = {'success': True, 'message': 'Local storage accessible'}
        try:
            # Test local storage write
            from django.core.files.base import ContentFile
            test_file = ContentFile(b"test", name="health_check.txt")
            test_path = local_storage.save("health_check.txt", test_file)
            if local_storage.exists(test_path):
                local_storage.delete(test_path)
            else:
                local_test = {'success': False, 'message': 'Local storage write test failed'}
        except Exception as e:
            local_test = {'success': False, 'message': f'Local storage error: {str(e)}'}
        
        # Get file counts
        storage_settings.update_file_counts()
        
        health_data = {
            'overall_status': 'healthy' if active_test['success'] and local_test['success'] else 'degraded',
            'active_storage': {
                'type': storage_settings.active_storage,
                'display': storage_settings.get_active_storage_display(),
                'status': active_test
            },
            'local_storage': {
                'status': local_test
            },
            'file_counts': {
                'local': storage_settings.local_files_count,
                'cloud': storage_settings.cloud_files_count,
                'total_size_mb': storage_settings.total_storage_size_mb
            },
            'migration_status': {
                'in_progress': storage_settings.migration_in_progress,
                'last_migration': storage_settings.last_migration_date.isoformat() if storage_settings.last_migration_date else None
            }
        }
        
        return JsonResponse({
            'success': True,
            'health': health_data
        })
        
    except Exception as e:
        logger.error(f"Error in storage health check: {e}")
        return JsonResponse({
            'success': False,
            'message': f'Health check failed: {str(e)}'
        })
