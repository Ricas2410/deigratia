"""
Dashboard-specific template filters.
These filters are specific to the dashboard app functionality.
"""

from django import template

register = template.Library()

@register.filter
def format_currency(value):
    """Format a number as currency (Ghana Cedis)."""
    try:
        return f"GHS {float(value):.2f}"
    except (ValueError, TypeError):
        return "GHS 0.00"

@register.filter
def dashboard_card_class(metric_type):
    """Return appropriate CSS class for dashboard cards based on metric type."""
    card_classes = {
        'students': 'border-left-primary',
        'teachers': 'border-left-success',
        'courses': 'border-left-info',
        'assignments': 'border-left-warning',
        'attendance': 'border-left-secondary',
        'fees': 'border-left-danger',
        'revenue': 'border-left-success',
        'expenses': 'border-left-danger',
    }
    return card_classes.get(metric_type.lower(), 'border-left-primary')

@register.filter
def progress_bar_class(percentage):
    """Return appropriate progress bar class based on percentage."""
    try:
        pct = float(percentage)
        if pct >= 80:
            return 'bg-success'
        elif pct >= 60:
            return 'bg-info'
        elif pct >= 40:
            return 'bg-warning'
        else:
            return 'bg-danger'
    except (ValueError, TypeError):
        return 'bg-secondary'
