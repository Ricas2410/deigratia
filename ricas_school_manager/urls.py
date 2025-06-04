"""
URL Configuration for the integrated Ricas School Manager
This file combines URL patterns from both the DGMS website and SMS system.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from django.http import HttpResponse
from django.views.decorators.http import require_GET
from shared_utils.sitemaps import StaticViewSitemap, DashboardSitemap

# Sitemap configuration
sitemaps = {
    'static': StaticViewSitemap,
    'dashboard': DashboardSitemap,
}

@require_GET
def robots_txt(request):
    """Generate robots.txt file."""
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /dashboard/",
        "Disallow: /users/",
        "Disallow: /my-admin/",
        "",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")

urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),

    # DGMS Website URLs - mounted at the root for public access
    path('', include(('website.urls', 'website'), namespace='website')),

    # SMS System URLs
    path('users/', include('users.urls')),
    path('courses/', include('courses.urls')),
    path('assignments/', include('assignments.urls')),
    path('attendance/', include('attendance.urls')),
    path('communications/', include('communications.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('fees/', include(('fees.urls', 'fees'), namespace='fees')),
    path('payroll/', include(('payroll.urls', 'payroll'), namespace='payroll')),
    path('appointments/', include(('appointments.urls', 'appointments'), namespace='appointments')),

    # SMS custom admin route
    path('my-admin/', include(('users.urls', 'my_admin'), namespace='my_admin')),

    # TinyMCE
    path('tinymce/', include('tinymce.urls')),

    # Storage Management (Admin only)
    path('admin/', include('shared_utils.urls')),

    # SEO URLs
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', robots_txt, name='robots_txt'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
