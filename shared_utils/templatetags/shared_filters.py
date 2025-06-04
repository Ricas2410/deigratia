"""
Shared template filters for the Ricas School Management System.
This module consolidates common filters used across multiple apps to avoid
the Django warning about duplicate template tag module names.
"""

from django import template
from datetime import datetime, timedelta
import re

register = template.Library()

# =============================================================================
# MATHEMATICAL OPERATIONS
# =============================================================================

@register.filter
def mul(value, arg):
    """Multiply the value by the argument."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def div(value, arg):
    """Divide the value by the argument."""
    try:
        if float(arg) == 0:
            return 0
        return float(value) / float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def add(value, arg):
    """Add the arg to the value."""
    try:
        return float(value) + float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def subtract(value, arg):
    """Subtract the arg from the value."""
    try:
        return float(value) - float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def multiply(value, arg):
    """Multiply the value by the arg."""
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def divide(value, arg):
    """Divide the value by the arg."""
    try:
        if float(arg) == 0:
            return 0
        return float(value) / float(arg)
    except (ValueError, TypeError):
        return 0

@register.filter
def percentage(value, total):
    """Calculate percentage of value to total"""
    try:
        if float(total) == 0:
            return 0
        return (float(value) / float(total)) * 100
    except (ValueError, TypeError):
        return 0

@register.filter
def percentage_of(value, total):
    """Calculate what percentage the value is of the total."""
    try:
        if not total:
            return 0
        return (float(value) / float(total)) * 100
    except (ValueError, TypeError, ZeroDivisionError):
        return 0

# =============================================================================
# DATA TYPE CONVERSIONS
# =============================================================================

@register.filter
def to_int(value):
    """Convert value to integer."""
    try:
        return int(value)
    except (ValueError, TypeError):
        return 0

@register.filter
def to_float(value):
    """Convert value to float."""
    try:
        return float(value)
    except (ValueError, TypeError):
        return 0.0

# =============================================================================
# STRING OPERATIONS
# =============================================================================

@register.filter
def contains(value, arg):
    """Check if a string contains another string."""
    if not value:
        return False
    return str(arg) in str(value)

@register.filter
def endswith(value, arg):
    """Check if a string ends with another string."""
    if not value:
        return False
    return str(value).endswith(str(arg))

@register.filter
def startswith(value, arg):
    """Check if a string starts with another string."""
    if not value:
        return False
    return str(value).startswith(str(arg))

# =============================================================================
# COMPARISON OPERATIONS
# =============================================================================

@register.filter
def less_than(value, arg):
    """Check if a value is less than the argument."""
    try:
        return float(value) < float(arg)
    except (ValueError, TypeError):
        return False

@register.filter
def greater_than(value, arg):
    """Check if a value is greater than the argument."""
    try:
        return float(value) > float(arg)
    except (ValueError, TypeError):
        return False

@register.filter
def equal_to(value, arg):
    """Check if a value is equal to the argument."""
    try:
        return float(value) == float(arg)
    except (ValueError, TypeError):
        return str(value) == str(arg)

# =============================================================================
# DICTIONARY AND OBJECT OPERATIONS
# =============================================================================

@register.filter
def get_item(dictionary, key):
    """Get an item from a dictionary using the key."""
    if not dictionary:
        return None
    return dictionary.get(key)

@register.filter
def get_attribute(obj, attr):
    """Get an attribute of an object."""
    if not obj:
        return ''
    try:
        return getattr(obj, attr, '')
    except (AttributeError, TypeError):
        return ''

@register.filter
def getattr_safe(obj, attr):
    """Gets an attribute of an object dynamically from a string name"""
    if obj is None:
        return None
    try:
        return getattr(obj, attr)
    except (AttributeError, TypeError):
        return None

# =============================================================================
# FORMATTING OPERATIONS
# =============================================================================

@register.filter
def format_currency(value):
    """Format a number as currency."""
    try:
        return f"GHS {float(value):.2f}"
    except (ValueError, TypeError):
        return "GHS 0.00"

@register.filter
def format_duration(seconds):
    """Format duration in seconds to human readable format."""
    if not seconds:
        return "0 min"
    
    try:
        seconds = int(seconds)
        minutes = seconds // 60
        if minutes < 60:
            return f"{minutes} min"
        
        hours = minutes // 60
        remaining_minutes = minutes % 60
        
        if remaining_minutes == 0:
            return f"{hours} hr"
        else:
            return f"{hours} hr {remaining_minutes} min"
    except (ValueError, TypeError):
        return "0 min"

# =============================================================================
# URL AND MEDIA OPERATIONS
# =============================================================================

@register.filter
def extract_youtube_id(url):
    """Extract YouTube video ID from a URL."""
    if not url:
        return ""
    
    # Handle youtu.be format
    if 'youtu.be' in url:
        return url.split('/')[-1].split('?')[0]
    
    # Handle youtube.com format
    if 'youtube.com' in url:
        if 'v=' in url:
            return url.split('v=')[1].split('&')[0]
    
    # Return the original URL if no ID found
    return url

# =============================================================================
# ASSESSMENT AND GRADING OPERATIONS
# =============================================================================

@register.filter
def get_assessment_grade(grades_dict, assessment_id):
    """Get a grade for a specific assessment by ID from a grades dictionary."""
    if not grades_dict or not assessment_id:
        return ""
    
    # Convert assessment_id to string since dictionary keys from template 
    # are often strings even if the original IDs are integers
    assessment_id_str = str(assessment_id)
    
    # Try to get the grade from the dictionary
    return grades_dict.get(assessment_id_str, "")

@register.filter
def get_assessment_grades_by_type(grades_dict, assessment_type):
    """Get all grades for assessments of a specific type."""
    if not grades_dict or not assessment_type:
        return {}
    
    filtered_grades = {}
    for key, value in grades_dict.items():
        # Check if this is an assessment grade entry with the specified type
        if isinstance(key, str) and key.startswith(assessment_type + "_"):
            filtered_grades[key] = value
            
    return filtered_grades
