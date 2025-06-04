"""
Attendance-specific template filters.
These filters are specific to the attendance app functionality.
"""

from django import template

register = template.Library()

# Note: The original attendance custom_filters.py only had generic filters
# that are now available in shared_utils.templatetags.shared_filters
# This file is kept for future attendance-specific filters

@register.filter
def attendance_status_class(status):
    """Return CSS class for attendance status."""
    status_classes = {
        'present': 'text-success',
        'absent': 'text-danger',
        'late': 'text-warning',
        'excused': 'text-info',
    }
    return status_classes.get(status.lower(), 'text-muted')

@register.filter
def attendance_percentage(present_count, total_count):
    """Calculate attendance percentage."""
    if not total_count or total_count == 0:
        return 0
    try:
        return round((present_count / total_count) * 100, 1)
    except (ValueError, TypeError, ZeroDivisionError):
        return 0
