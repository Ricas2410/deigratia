"""
Admin interface for shared utilities including storage management.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.utils import timezone
from .storage_manager import StorageSettings


@admin.register(StorageSettings)
class StorageSettingsAdmin(admin.ModelAdmin):
    """
    Admin interface for storage settings management.
    """
    
    list_display = [
        'active_storage_display',
        'storage_status',
        'file_counts_display',
        'storage_size_display',
        'last_migration_display',
        'actions_display'
    ]
    
    fieldsets = (
        ('Current Storage Configuration', {
            'fields': ('active_storage', 'auto_migrate_new_files'),
            'description': 'Select the storage backend to use for new file uploads.'
        }),
        ('Cloud Storage Settings', {
            'fields': (
                'cloud_access_key',
                'cloud_secret_key', 
                'cloud_bucket_name',
                'cloud_region',
                'cloud_endpoint_url',
                'cloud_custom_domain'
            ),
            'description': 'Configure cloud storage credentials (Backblaze B2, AWS S3, etc.)',
            'classes': ('collapse',)
        }),
        ('Storage Statistics', {
            'fields': (
                'local_files_count',
                'cloud_files_count',
                'total_storage_size_mb',
                'last_migration_date',
                'migration_in_progress'
            ),
            'description': 'Current storage usage and migration status',
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = [
        'local_files_count',
        'cloud_files_count', 
        'total_storage_size_mb',
        'last_migration_date',
        'migration_in_progress',
        'created_at',
        'updated_at'
    ]
    
    def has_add_permission(self, request):
        """Only allow one storage settings instance."""
        return not StorageSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Don't allow deletion of storage settings."""
        return False
    
    def active_storage_display(self, obj):
        """Display active storage with icon."""
        icons = {
            'local': '💾',
            'backblaze_b2': '☁️',
            'aws_s3': '🌐',
            'custom': '⚙️'
        }
        icon = icons.get(obj.active_storage, '❓')
        return format_html(
            '{} {}',
            icon,
            obj.get_active_storage_display()
        )
    active_storage_display.short_description = 'Active Storage'
    
    def storage_status(self, obj):
        """Display storage connection status."""
        if obj.migration_in_progress:
            return format_html(
                '<span style="color: orange;">🔄 Migration in Progress</span>'
            )
        
        # Test storage connection
        test_result = obj.test_storage_connection()
        if test_result['success']:
            return format_html(
                '<span style="color: green;">✅ Connected</span>'
            )
        else:
            return format_html(
                '<span style="color: red;">❌ Connection Failed</span>'
            )
    storage_status.short_description = 'Status'
    
    def file_counts_display(self, obj):
        """Display file counts."""
        return format_html(
            'Local: <strong>{}</strong><br>Cloud: <strong>{}</strong>',
            obj.local_files_count,
            obj.cloud_files_count
        )
    file_counts_display.short_description = 'File Counts'
    
    def storage_size_display(self, obj):
        """Display storage size."""
        if obj.total_storage_size_mb < 1024:
            return f"{obj.total_storage_size_mb:.1f} MB"
        else:
            return f"{obj.total_storage_size_mb / 1024:.1f} GB"
    storage_size_display.short_description = 'Total Size'
    
    def last_migration_display(self, obj):
        """Display last migration date."""
        if obj.last_migration_date:
            return obj.last_migration_date.strftime('%Y-%m-%d %H:%M')
        return 'Never'
    last_migration_display.short_description = 'Last Migration'
    
    def actions_display(self, obj):
        """Display action buttons."""
        buttons = []
        
        # Test Connection button
        buttons.append(
            '<a href="javascript:void(0)" onclick="testStorageConnection()" '
            'class="button" style="margin-right: 5px;">🔍 Test Connection</a>'
        )
        
        # Update Counts button
        buttons.append(
            '<a href="javascript:void(0)" onclick="updateFileCounts()" '
            'class="button" style="margin-right: 5px;">📊 Update Counts</a>'
        )
        
        # Migration buttons (if not in progress)
        if not obj.migration_in_progress:
            if obj.active_storage == 'local' and obj.local_files_count > 0:
                buttons.append(
                    '<a href="javascript:void(0)" onclick="migrateToCloud()" '
                    'class="button" style="margin-right: 5px;">☁️ Migrate to Cloud</a>'
                )
            elif obj.active_storage != 'local' and obj.cloud_files_count > 0:
                buttons.append(
                    '<a href="javascript:void(0)" onclick="migrateToLocal()" '
                    'class="button" style="margin-right: 5px;">💾 Migrate to Local</a>'
                )
        
        return format_html(''.join(buttons))
    actions_display.short_description = 'Actions'
    
    def save_model(self, request, obj, form, change):
        """Custom save logic."""
        # Update file counts when saving
        obj.update_file_counts()
        super().save_model(request, obj, form, change)
        
        messages.success(
            request,
            f'Storage settings updated. Active storage: {obj.get_active_storage_display()}'
        )
    
    def changelist_view(self, request, extra_context=None):
        """Custom changelist view with JavaScript for actions."""
        extra_context = extra_context or {}
        extra_context['custom_js'] = '''
        <script>
        function testStorageConnection() {
            if (confirm('Test storage connection?')) {
                fetch('/admin/storage/test-connection/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                        'Content-Type': 'application/json',
                    },
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('✅ Storage connection successful!');
                    } else {
                        alert('❌ Storage connection failed: ' + data.message);
                    }
                    location.reload();
                })
                .catch(error => {
                    alert('Error testing connection: ' + error);
                });
            }
        }
        
        function updateFileCounts() {
            if (confirm('Update file counts? This may take a moment.')) {
                fetch('/admin/storage/update-counts/', {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
                        'Content-Type': 'application/json',
                    },
                })
                .then(response => response.json())
                .then(data => {
                    alert('📊 File counts updated!');
                    location.reload();
                })
                .catch(error => {
                    alert('Error updating counts: ' + error);
                });
            }
        }
        
        function migrateToCloud() {
            if (confirm('Migrate all files to cloud storage? This may take a while and cannot be undone easily.')) {
                window.open('/admin/storage/migrate/?from=local&to=cloud', '_blank');
            }
        }
        
        function migrateToLocal() {
            if (confirm('Migrate all files to local storage? This may take a while.')) {
                window.open('/admin/storage/migrate/?from=cloud&to=local', '_blank');
            }
        }
        </script>
        '''
        return super().changelist_view(request, extra_context)
    
    class Media:
        css = {
            'all': ('admin/css/storage_admin.css',)
        }


# Register the model if not already registered
try:
    admin.site.register(StorageSettings, StorageSettingsAdmin)
except admin.sites.AlreadyRegistered:
    pass
