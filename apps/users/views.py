import json
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


class Referral (View):
    """ Referral links search user by phone number """
    
    @validate_token
    def get (self, request):
        """ Query referral links from specific user 
        (searching by phone or email) """
        
        # Get phone and email from get data
        phone = request.GET.get('phone', None)
        email = request.GET.get('email', None)
        
        # If phone is None, return error
        if not phone and not email:
            return JsonResponse ({
                "status": "error",
                "message": "Phone or email is required",
                "data": {}
            }, status=400)
            
        # Get user by phone
        if phone:
            users_match = models.User.objects.filter(phone=phone, active=True)
        else:
            users_match = models.User.objects.filter(email=email, active=True)
        
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
        
    # @validate_token
    # def post (self, request):
    #     """ Save new user in database """
        
    #     # Get post data from json
    #     try:
    #         json_data = json.loads (request.body)
    #     except:
    #         return JsonResponse ({
    #             "status": "error",
    #             "message": "Invalid JSON",
    #             "data": []
    #         }, status=400)
            
    #     name = json_data.get ("name", None)
    #     last_name = json_data.get ("last_name", None)
    #     email = json_data.get ("email", None)
    #     phone = json_data.get ("phone", None)
    #     stores = json_data.get ("stores", None)
        
    #     # stores = {
    #     #     "store-1": "link",
    #     #     "store-2": "link"
    #     # }
        
    #     # Validate data
    #     if not (name and last_name and email and phone and stores):
    #         return JsonResponse ({
    #             "status": "error",
    #             "message": "Missing data",
    #             "data": {}
    #         }, status=400)
            
    #     # Valide if user already exists
    #     email_exists = models.User.objects.filter (
    #         email=email,
    #     ).count() > 0
    #     phone_exists = models.User.objects.filter (
    #         phone=phone,
    #     ).count() > 0
        
    #     if phone_exists or email_exists:
    #         return JsonResponse ({
    #             "status": "error",
    #             "message": "User already exists",
    #             "data": {}
    #         }, status=400)
            
    #     # Create user in database
    #     try:
    #         user = models.User.objects.create (
    #             name=name,
    #             last_name=last_name,
    #             email=email,
    #             phone=phone,
    #             active=True
    #         )
    #     except:
    #         return JsonResponse ({
    #             "status": "error",
    #             "message": "Error creating user",
    #             "data": {}
    #         }, status=400)
        
    #     # Validate stores data type
    #     if not isinstance (stores, dict):
    #         return JsonResponse ({
    #             "status": "error",
    #             "message": "Invalid stores data type",
    #             "data": {}
    #         }, status=400)
        
    #     # Save refreral links
    #     for store_name, link in stores.items():
            
    #         # Query store and skip if not exists
    #         store = models.Store.objects.filter (name=store_name.lower())
    #         if not store:
    #             continue
            
    #         # Save link
    #         store = store.first()
    #         models.ReferralLink.objects.create (
    #             user=user,
    #             store=store,
    #             link=link
    #         )
            

class Register (View):
    """ Register form to referral users """
    
    def get (self, request): 
        """ render rgister form """
        
        return render (request, "users/register.html")