from django import template
from django.urls import reverse
from django.utils.safestring import mark_safe
from ..models import SiteSettings

register = template.Library()


@register.simple_tag
def favicon_url():
    """
    Returns the URL for the dynamic favicon.
    """
    return reverse('website:favicon')


@register.simple_tag
def favicon_links():
    """
    Returns complete HTML for favicon links.
    Includes multiple formats for better browser compatibility.
    """
    favicon_url_path = reverse('website:favicon')

    html = f'''
    <!-- Favicon -->
    <link rel="icon" type="image/png" sizes="32x32" href="{favicon_url_path}?size=32">
    <link rel="icon" type="image/png" sizes="16x16" href="{favicon_url_path}?size=16">
    <link rel="shortcut icon" href="{favicon_url_path}">

    <!-- Apple Touch Icon -->
    <link rel="apple-touch-icon" sizes="180x180" href="{favicon_url_path}?size=180">

    <!-- Android Chrome Icons -->
    <link rel="icon" type="image/png" sizes="192x192" href="{favicon_url_path}?size=192">
    <link rel="icon" type="image/png" sizes="512x512" href="{favicon_url_path}?size=512">

    <!-- Microsoft Tiles -->
    <meta name="msapplication-TileImage" content="{favicon_url_path}?size=144">
    <meta name="msapplication-TileColor" content="#0a2351">

    <!-- Theme Color -->
    <meta name="theme-color" content="#0a2351">
    '''

    return mark_safe(html.strip())


@register.simple_tag
def site_title():
    """
    Returns the site title from settings or a default.
    """
    try:
        site_settings = SiteSettings.objects.first()
        if site_settings and site_settings.school_name:
            return site_settings.school_name
    except:
        pass
    return "Deigratia Montessori School"


@register.simple_tag
def site_logo_url():
    """
    Returns the URL of the uploaded school logo.
    """
    try:
        site_settings = SiteSettings.objects.first()
        if site_settings and site_settings.school_logo:
            return site_settings.school_logo.url
    except:
        pass
    return None
