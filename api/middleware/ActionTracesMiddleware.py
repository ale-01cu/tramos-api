from django.utils.deprecation import MiddlewareMixin
from django.utils import timezone
from api.models import ActionTraces
from django.urls import resolve

ignored_paths = ('/admin/', '/static/', '/api/docs/', '/v1/token/')

class ActionTracesMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # Guardamos información básica de la solicitud
        if not request.path.startswith(ignored_paths):
            self.request_data = {
                'method': request.method,
                'path': request.path,
                'user': request.user if request.user.is_authenticated else None,
                'timestamp': timezone.now()
            }

    def process_response(self, request, response):
        if hasattr(self, 'request_data'):
            path = self.request_data['path']
            method = self.request_data['method']
            user = self.request_data['user']
            timestamp = self.request_data['timestamp']
            model_name = model_name = path.strip('/').split('/')[-1]

            # Intentamos extraer nombre de la vista y modelo (si está disponible)
            try:
                match = resolve(path)
                view_func = match.func
            except:
                pass

            ActionTraces.objects.create(
                model_name=model_name,
                row_id=0,  # No tenemos ID aún
                action=f"{method} request",
                user=user,
                changes={
                    'path': path,
                    'status_code': response.status_code,
                    'method': method
                }
            )
        return response
