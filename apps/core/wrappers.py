from core.models import Token
from functools import wraps
from django.http import JsonResponse

def validate_token (function):
    """ View wrapper for return data only if the token it's valid """
    
    @wraps(function)
    def wrap (self, request, *args, **kwargs):
                
        # Get token and base endpoints
        token = request.headers.get ("token", None)
        token_found = Token.objects.filter (
            token=token,
        )
            
        # Valkdate token and return data
        if token_found and token_found.first().is_active:
            return function(self, request, *args, **kwargs)
        else:
            return JsonResponse ({
                "status": "error",
                "message": "Invalid token",
                "data": [],
            }, status=401)
        
    return wrap