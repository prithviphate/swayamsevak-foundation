"""
WSGI config for config project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/6.1/howto/deployment/wsgi/
"""

import os
import sys
import traceback
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Initialize Django WSGI application
_django_app = get_wsgi_application()

# Auto-initialize database on Vercel serverless environment if tables are absent
if os.getenv('VERCEL'):
    try:
        from django.core.management import call_command
        from django.db import connection
        tables = connection.introspection.table_names()
        if 'core_foundationsetting' not in tables:
            print("Auto-running database migrations on Vercel...")
            call_command('migrate', interactive=False)
            try:
                print("Auto-seeding initial foundation data on Vercel...")
                call_command('seed_foundation_data')
            except Exception as se:
                print(f"Seed error: {se}")
    except Exception as dbe:
        print(f"Vercel DB initialization notice: {dbe}")

def application(environ, start_response):
    try:
        return _django_app(environ, start_response)
    except Exception:
        error_msg = traceback.format_exc()
        print("CRITICAL DJANGO ERROR:\n", error_msg, file=sys.stderr)
        status = '500 Internal Server Error'
        headers = [('Content-Type', 'text/plain; charset=utf-8')]
        start_response(status, headers)
        return [f"Server Error (500):\n{error_msg}".encode('utf-8')]

# Vercel serverless entrypoint
app = application

