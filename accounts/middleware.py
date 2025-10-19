from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

class ActivationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        if request.user.is_authenticated and not getattr(request.user, 'is_activated', False):
            restricted_paths = ['/api/shares/', '/api/claims/', '/api/membership/']
            if any(request.path.startswith(path) for path in restricted_paths):
                return JsonResponse({'error': 'Account not activated'}, status=403)
        return None