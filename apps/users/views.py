from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from users import models 
from core.wrappers import validate_token
from django.core.mail import send_mail
from referralfiftyfifty.settings import EMAIL_HOST_USER, HOST

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

class Register (View):
    """ Register form to referral users """
    
    def get (self, request): 
        """ render rgister form """        
        return render (request, "users/register.html")
    
    def post (self, request):
        """ get register data and save user """
        
        # Get form data
        first_name = request.POST.get ("first-name", None)
        last_name = request.POST.get ("last-name", None)
        email = request.POST.get ("email", None)
        phone = request.POST.get ("phone", None)
        amazon_code = request.POST.get ("amazon", None)
        ebay_code = request.POST.get ("ebay", None)
        walmart_code = request.POST.get ("walmart", None)
        
        # Validate requiered data
        if not (first_name and last_name and email and phone):
            return render (request, "users/register.html", {
                "error": "Missing data|First name, last name, email and phone are required"
            })
        
        # Save user
        try:
            user = models.User.objects.create (
                name=first_name,
                last_name=last_name,
                email=email,
                phone=phone
            )
        except Exception as e:
            # Catch duplicated users
            print (e)
            return render (request, "users/register.html", {
                "error": "Error creating user|Email or phone already exists"
            })
        
        # Save referral links
        stores = {
            "amazon": amazon_code,
            "ebay": ebay_code,
            "walmart": walmart_code
        }
        for store_name, store_value in stores.items():
            if store_value:
                current_store = models.Store.objects.get (name=store_name)
                models.ReferralLink.objects.create (
                    user=user,
                    store=current_store,
                    link=store_value
                )
        
        # Submit activation link by email
        activation_link = f"{HOST}/activate-account/{user.id}"
        send_mail(
            "Complete your registration",
            f"Click here to complete your registration: {activation_link}",
            EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
         
        # redirect user to home page
        return render (request, "users/register.html", {
            "info": "We are almost done|Check your email to complete your registration"
        })