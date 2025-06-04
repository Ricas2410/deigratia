"""
Assignment-specific template filters.
These filters are specific to the assignments app functionality.
"""

from django import template

register = template.Library()

@register.filter
def get_assessment_grade(grades_dict, assessment_id):
    """Get a grade for a specific assessment by ID from a grades dictionary.
    
    This filter is used in the bulk grade entry template to retrieve grades
    for dynamic assessment columns.
    
    Args:
        grades_dict: Dictionary containing assessment grades keyed by assessment ID
        assessment_id: The ID of the assessment to retrieve the grade for
    
    Returns:
        The grade value if found, or empty string if not found
    """
    if not grades_dict or not assessment_id:
        return ""
    
    # Convert assessment_id to string since dictionary keys from template 
    # are often strings even if the original IDs are integers
    assessment_id_str = str(assessment_id)
    
    # Try to get the grade from the dictionary
    return grades_dict.get(assessment_id_str, "")

@register.filter
def get_assessment_grades_by_type(grades_dict, assessment_type):
    """Get all grades for assessments of a specific type.
    
    Used for calculating component totals in gradebook and report cards.
    
    Args:
        grades_dict: Dictionary containing all student grades
        assessment_type: The type of assessment to filter by (e.g., 'classwork', 'exam')
    
    Returns:
        Dictionary containing only grades for the specified assessment type
    """
    if not grades_dict or not assessment_type:
        return {}
    
    filtered_grades = {}
    for key, value in grades_dict.items():
        # Check if this is an assessment grade entry with the specified type
        if isinstance(key, str) and key.startswith(assessment_type + "_"):
            filtered_grades[key] = value
            
    return filtered_grades
