"""
WSGI config for amulti_stream_feature_fusion_approach

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'amulti_stream_feature_fusion_approach.settings')
application = get_wsgi_application()
