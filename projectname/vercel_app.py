
import os
import sys

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Point to the settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projectname.settings")

try:
    from django.core.wsgi import get_wsgi_application
    app = get_wsgi_application()
except Exception as e:
    # If the app fails to start (e.g. DB connection issues), this will print the error
    import traceback
    trace = traceback.format_exc()
    
    def app(environ, start_response):
        status = '500 Internal Server Error'
        response_headers = [('Content-type', 'text/plain')]
        start_response(status, response_headers)
        return [f"Error loading WSGI app:\n\n{trace}".encode('utf-8')]
