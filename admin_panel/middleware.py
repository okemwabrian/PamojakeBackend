from .models import UserActivity

class ActivityLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        # Log activities for authenticated users
        if request.user.is_authenticated and request.method == 'POST':
            self.log_activity(request, response)
        
        return response
    
    def log_activity(self, request, response):
        if response.status_code in [200, 201]:
            activity_type = None
            description = ''
            
            if '/api/applications/' in request.path:
                activity_type = 'application_submitted'
                description = 'User submitted membership application'
            elif '/api/payments/' in request.path:
                activity_type = 'payment_made'
                description = 'User made a payment'
            elif '/api/claims/' in request.path:
                activity_type = 'claim_submitted'
                description = 'User submitted a claim'
            elif '/api/shares/buy/' in request.path:
                activity_type = 'shares_purchased'
                description = 'User purchased shares'
            elif '/api/auth/login/' in request.path:
                activity_type = 'login'
                description = 'User logged in'
            elif '/api/auth/logout/' in request.path:
                activity_type = 'logout'
                description = 'User logged out'
            
            if activity_type:
                UserActivity.objects.create(
                    user=request.user,
                    activity_type=activity_type,
                    description=description,
                    ip_address=self.get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', '')
                )
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip