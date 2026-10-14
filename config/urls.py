"""
Root URL Configuration for Swayamsevak Foundation.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Customize Django Admin branding
admin.site.site_header = "Swayamsevak Foundation - Administrative Portal"
admin.site.site_title = "Swayamsevak Foundation Admin"
admin.site.index_title = "Foundation Operations & Service Management (स्वावलंबनातून समाजसेवा)"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

handler404 = 'core.views.custom_404_view'
