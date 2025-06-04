"""
Sitemap configuration for SEO optimization.
"""

from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages."""
    priority = 0.8
    changefreq = 'weekly'
    
    def items(self):
        return [
            'website:home',
            'website:about',
            'website:contact',
            'website:admissions',
            'website:academics',
            'website:gallery',
            'website:news',
            'users:login',
            'users:register',
        ]
    
    def location(self, item):
        return reverse(item)
    
    def lastmod(self, item):
        return timezone.now() - timedelta(days=1)


class DashboardSitemap(Sitemap):
    """Sitemap for dashboard pages (lower priority, authenticated required)."""
    priority = 0.3
    changefreq = 'daily'
    
    def items(self):
        return [
            'dashboard:index',
            'courses:course_list',
            'assignments:assignment_list',
            'attendance:attendance_list',
        ]
    
    def location(self, item):
        return reverse(item)
    
    def lastmod(self, item):
        return timezone.now()


# You can add more specific sitemaps for dynamic content like:
# - Course listings
# - News articles
# - Event pages
# - Staff profiles (if public)

# Example for dynamic content:
# class CourseSitemap(Sitemap):
#     changefreq = "weekly"
#     priority = 0.6
#     
#     def items(self):
#         from courses.models import Course
#         return Course.objects.filter(is_active=True)
#     
#     def lastmod(self, obj):
#         return obj.updated_at
