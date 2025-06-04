"""
SEO template tags for the Ricas School Management System.
Provides tags for generating SEO meta tags, structured data, and social media tags.
"""

from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from django.urls import reverse
import json

register = template.Library()

@register.simple_tag(takes_context=True)
def seo_meta_tags(context, title=None, description=None, keywords=None, image=None, url=None):
    """Generate comprehensive SEO meta tags."""
    request = context.get('request')
    
    # Default values from settings
    site_name = getattr(settings, 'SITE_NAME', 'Ricas School Management System')
    default_description = getattr(settings, 'DEFAULT_META_DESCRIPTION', '')
    default_keywords = getattr(settings, 'DEFAULT_META_KEYWORDS', '')
    default_image = getattr(settings, 'DEFAULT_OG_IMAGE', '/static/img/og-image.jpg')
    canonical_base = getattr(settings, 'CANONICAL_URL_BASE', '')
    
    # Use provided values or defaults
    title = title or site_name
    description = description or default_description
    keywords = keywords or default_keywords
    image = image or default_image
    
    # Build canonical URL
    if url:
        canonical_url = f"{canonical_base}{url}"
    elif request:
        canonical_url = f"{canonical_base}{request.get_full_path()}"
    else:
        canonical_url = canonical_base
    
    # Build absolute image URL
    if image and not image.startswith('http'):
        if request:
            image = request.build_absolute_uri(image)
        else:
            image = f"{canonical_base}{image}"
    
    meta_tags = f'''
    <!-- SEO Meta Tags -->
    <title>{title}</title>
    <meta name="description" content="{description}">
    <meta name="keywords" content="{keywords}">
    <meta name="author" content="{getattr(settings, 'SITE_AUTHOR', 'Ricas School')}">
    <link rel="canonical" href="{canonical_url}">
    
    <!-- Open Graph Tags -->
    <meta property="og:title" content="{title}">
    <meta property="og:description" content="{description}">
    <meta property="og:image" content="{image}">
    <meta property="og:url" content="{canonical_url}">
    <meta property="og:type" content="{getattr(settings, 'DEFAULT_OG_TYPE', 'website')}">
    <meta property="og:site_name" content="{site_name}">
    
    <!-- Twitter Card Tags -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="{title}">
    <meta name="twitter:description" content="{description}">
    <meta name="twitter:image" content="{image}">
    
    <!-- Additional SEO Tags -->
    <meta name="robots" content="index, follow">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta charset="UTF-8">
    '''
    
    return mark_safe(meta_tags.strip())

@register.simple_tag
def structured_data_organization():
    """Generate JSON-LD structured data for the organization."""
    site_name = getattr(settings, 'SITE_NAME', 'Ricas School Management System')
    canonical_base = getattr(settings, 'CANONICAL_URL_BASE', '')
    social_media = getattr(settings, 'SOCIAL_MEDIA', {})
    
    # Build social media URLs
    social_urls = []
    for platform, url in social_media.items():
        if url:
            social_urls.append(url)
    
    structured_data = {
        "@context": "https://schema.org",
        "@type": "EducationalOrganization",
        "name": site_name,
        "url": canonical_base,
        "description": getattr(settings, 'SITE_DESCRIPTION', ''),
        "sameAs": social_urls
    }
    
    json_ld = f'<script type="application/ld+json">{json.dumps(structured_data, indent=2)}</script>'
    return mark_safe(json_ld)

@register.simple_tag
def structured_data_website():
    """Generate JSON-LD structured data for the website."""
    site_name = getattr(settings, 'SITE_NAME', 'Ricas School Management System')
    canonical_base = getattr(settings, 'CANONICAL_URL_BASE', '')
    
    structured_data = {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": site_name,
        "url": canonical_base,
        "description": getattr(settings, 'SITE_DESCRIPTION', ''),
        "potentialAction": {
            "@type": "SearchAction",
            "target": f"{canonical_base}/search?q={{search_term_string}}",
            "query-input": "required name=search_term_string"
        }
    }
    
    json_ld = f'<script type="application/ld+json">{json.dumps(structured_data, indent=2)}</script>'
    return mark_safe(json_ld)

@register.simple_tag
def structured_data_breadcrumb(breadcrumbs):
    """Generate JSON-LD structured data for breadcrumbs."""
    if not breadcrumbs:
        return ''
    
    canonical_base = getattr(settings, 'CANONICAL_URL_BASE', '')
    
    breadcrumb_list = {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": []
    }
    
    for index, breadcrumb in enumerate(breadcrumbs, 1):
        item = {
            "@type": "ListItem",
            "position": index,
            "name": breadcrumb.get('name', ''),
            "item": f"{canonical_base}{breadcrumb.get('url', '')}"
        }
        breadcrumb_list["itemListElement"].append(item)
    
    json_ld = f'<script type="application/ld+json">{json.dumps(breadcrumb_list, indent=2)}</script>'
    return mark_safe(json_ld)

@register.simple_tag(takes_context=True)
def canonical_url(context, url=None):
    """Generate canonical URL tag."""
    request = context.get('request')
    canonical_base = getattr(settings, 'CANONICAL_URL_BASE', '')
    
    if url:
        canonical = f"{canonical_base}{url}"
    elif request:
        canonical = f"{canonical_base}{request.get_full_path()}"
    else:
        canonical = canonical_base
    
    return mark_safe(f'<link rel="canonical" href="{canonical}">')

@register.simple_tag
def robots_meta(index=True, follow=True, archive=True, snippet=True):
    """Generate robots meta tag."""
    directives = []
    
    directives.append('index' if index else 'noindex')
    directives.append('follow' if follow else 'nofollow')
    
    if not archive:
        directives.append('noarchive')
    if not snippet:
        directives.append('nosnippet')
    
    content = ', '.join(directives)
    return mark_safe(f'<meta name="robots" content="{content}">')

@register.filter
def truncate_description(text, length=160):
    """Truncate text for meta descriptions (optimal length ~160 characters)."""
    if not text:
        return ''
    
    if len(text) <= length:
        return text
    
    # Find the last space before the limit to avoid cutting words
    truncated = text[:length]
    last_space = truncated.rfind(' ')
    
    if last_space > 0:
        truncated = truncated[:last_space]
    
    return f"{truncated}..."
