"""
Root URL Configuration for Swayamsevak Foundation.
"""

from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

# Customize Django Admin branding
admin.site.site_header = "Swayamsevak Foundation - Administrative Portal"
admin.site.site_title = "Swayamsevak Foundation Admin"
admin.site.index_title = "Foundation Operations & Service Management (स्वावलंबनातून समाजसेवा)"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

import sys
import traceback
from django.http import HttpResponse

def debug_500_handler(request):
    exc_type, exc_value, exc_traceback = sys.exc_info()
    if exc_type is not None:
        tb_lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
        tb_str = "".join(tb_lines)
    else:
        tb_str = "No sys.exc_info() recorded."
    return HttpResponse(
        f"<html><body><h1>Django 500 Debug Traceback</h1><pre>{tb_str}</pre></body></html>",
        status=500,
        content_type="text/html; charset=utf-8"
    )

handler404 = 'core.views.custom_404_view'
handler500 = 'config.urls.debug_500_handler'


