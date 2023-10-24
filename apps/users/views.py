from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from users import models 
from core.wrappers import validate_token

def index (request):
    return JsonResponse ({
        "status": "success", 
        "message": "Welcome to Referral Fifty Fifty", 
        "data": {}
    }, status=200)


class ReferralByPhone (View):
    """ Referral links search user by phone number """
    
    @validate_token
    def get (self, request):
        
        # Get phone from get data
        phone = request.GET.get('phone', None)
        
        # If phone is None, return error
        if phone is None:
            return JsonResponse ({
                "status": "error",
                "message": "Phone is required",
                "data": {}
            }, status=400)
            
        # Get user by phone
        users_match = models.User.objects.filter(phone=phone, active=True)
        
        if users_match.count() != 1:
            return JsonResponse ({
                "status": "error",
                "message": "User not found",
                "data": {}
            }, status=404)
            
        user = users_match.first()
        
        # Get referral links
        referral_links = models.ReferralLink.objects.filter(user=user)
        
        # Create response (replace storw with store name)
        data = {}
        for referral_link in referral_links:
            data[referral_link.store.name] = referral_link.link

        return JsonResponse ({
            "status": "success",
            "message": "User found",
            "data": data
        }, status=200)