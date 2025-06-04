"""
Cache template tags for the Ricas School Management System.
Provides enhanced caching functionality for templates.
"""

from django import template
from django.core.cache import cache
from django.conf import settings
from django.utils.safestring import mark_safe
from django.template.loader import render_to_string
import hashlib

register = template.Library()

@register.simple_tag(takes_context=True)
def cache_key(context, *args):
    """Generate a cache key based on context and arguments."""
    request = context.get('request')
    user = getattr(request, 'user', None)
    
    # Build key components
    key_parts = []
    
    # Add user-specific info if authenticated
    if user and user.is_authenticated:
        key_parts.append(f"user_{user.id}")
        if hasattr(user, 'role'):
            key_parts.append(f"role_{user.role}")
    else:
        key_parts.append("anonymous")
    
    # Add provided arguments
    for arg in args:
        key_parts.append(str(arg))
    
    # Add request path for page-specific caching
    if request:
        key_parts.append(request.path)
    
    # Create hash of the key to ensure it's not too long
    key_string = "_".join(key_parts)
    key_hash = hashlib.md5(key_string.encode()).hexdigest()
    
    # Add cache prefix from settings
    prefix = getattr(settings, 'CACHE_MIDDLEWARE_KEY_PREFIX', 'ricas_school')
    return f"{prefix}_{key_hash}"

@register.simple_tag
def cache_timeout(timeout_type='default'):
    """Get cache timeout from settings."""
    timeouts = {
        'default': 300,  # 5 minutes
        'short': 60,     # 1 minute
        'medium': 900,   # 15 minutes
        'long': 3600,    # 1 hour
        'template': getattr(settings, 'TEMPLATE_CACHE_TIMEOUT', 3600),
        'page': getattr(settings, 'CACHE_MIDDLEWARE_SECONDS', 600),
    }
    
    return timeouts.get(timeout_type, timeouts['default'])

@register.inclusion_tag('shared_utils/cached_fragment.html', takes_context=True)
def cached_fragment(context, fragment_name, timeout='default', *args):
    """Cache a template fragment with automatic key generation."""
    cache_key_value = cache_key(context, fragment_name, *args)
    timeout_value = cache_timeout(timeout)
    
    return {
        'cache_key': cache_key_value,
        'timeout': timeout_value,
        'fragment_name': fragment_name,
    }

@register.simple_tag(takes_context=True)
def cache_buster(context, file_path):
    """Generate cache buster for static files."""
    # In production, you might want to use file modification time
    # or a version number from settings
    if settings.DEBUG:
        import time
        return f"{file_path}?v={int(time.time())}"
    else:
        # Use a version from settings or file hash
        version = getattr(settings, 'STATIC_VERSION', '1.0')
        return f"{file_path}?v={version}"

@register.simple_tag
def cache_vary_headers(*headers):
    """Generate Vary header for HTTP caching."""
    if not headers:
        return ''
    
    vary_header = ', '.join(headers)
    return mark_safe(f'<meta http-equiv="Vary" content="{vary_header}">')

@register.simple_tag
def cache_control(max_age=None, public=None, private=None, no_cache=None):
    """Generate Cache-Control header meta tag."""
    directives = []
    
    if max_age is not None:
        directives.append(f'max-age={max_age}')
    
    if public:
        directives.append('public')
    elif private:
        directives.append('private')
    
    if no_cache:
        directives.append('no-cache')
    
    if directives:
        content = ', '.join(directives)
        return mark_safe(f'<meta http-equiv="Cache-Control" content="{content}">')
    
    return ''
