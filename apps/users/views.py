import os
from django.views import View
from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
from users import models 
from core.wrappers import validate_token
from referralfiftyfifty.settings import HOST, PRICE_CHECKER_HOST
from core.emails import submit_email

class Index (View):
    """ Home wep app page """
    
    def get (self, request): 
        """ render home template """               
        
        # Validate user session
        user_id = request.session.get ("user", None)
        if not user_id:
            # Redirect to login
            return HttpResponseRedirect ("/login")
        
        # Get user hash
        user = models.User.objects.get (id=user_id)
        user_hash = user.hash        
        referral_link = f"{PRICE_CHECKER_HOST}/referral/{user_hash}"    
        
        return render (request, "users/index.html", context={
            "referral_link":referral_link,
        })
    
def error404(request, exception):
    """ Error 404 page """
    return render(request, 'users/404.html', status=404, context={
        "subtitle": "error",
    })
    
def error404Preview(request):
    """ Error 404 page """
    return render(request, 'users/404.html', status=404, context={
        "subtitle": "error",
    })

class Referral (View):
    """ Referral links search user by phone number """
    
    @validate_token
    def get (self, request):
        """ Query referral links from specific user 
        (searching by phone or email) """
        
        # Get phone and email from get data
        phone = request.GET.get('phone', None)
        email = request.GET.get('email', None)
        hash = request.GET.get('hash', None)
        
        # If phone is None, return error
        if not phone and not email and not hash:
            return JsonResponse ({
                "status": "error",
                "message": "Phone or email or hash is required",
                "data": {}
            }, status=400)
            
        # Get user by phone
        if phone:
            users_match = models.User.objects.filter(phone=phone, active=True)
        elif email:
            users_match = models.User.objects.filter(email=email, active=True)
        else:
            users_match = models.User.objects.filter(hash=hash, active=True)
        
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
    
    subtitle = "register"
    default_script = True
    
    def get (self, request):         
        """ render rgister form """
        
        # Validate user session
        user_id = request.session.get ("user", None)
        if user_id:
            # Redirect to home
            return HttpResponseRedirect ("/")
                
        return render (request, "users/register.html", {
            "subtitle": Register.subtitle
        })
    
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
                "error": "Missing data|First name, last name, email and phone are required",
                "subtitle": Register.subtitle,
                "default_script": Register.default_script
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
                "error": "Error creating user|Email or phone already exists. Do not forget to activate your email with the link we sent you after signing up.",
                "subtitle": Register.subtitle,
                "default_script": Register.default_script
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
        activation_link = f"{HOST}/activate/{user.hash}"
        html_content = f'<p>Click here to complete your registration: <a href="{activation_link}"> {activation_link}</p>'
        submit_email ("Complete your registration", html_content, email)
            
        # redirect user to home page
        return render (request, "users/register.html", {
            "info": "We are almost done|Check your email to complete your registration",
            "subtitle": Register.subtitle,
            "default_script": Register.default_script
        })
        
class Activate (View):
    """ Activate account already created """
    
    def get (self, request, hash): 
        """ render rgister form """        
        
        # Get user by hash
        users_match = models.User.objects.filter(hash=hash)
        if not users_match:
            # redirect to not found
            return HttpResponseRedirect ("/404")
        
        user = users_match.first()
        
        # Activate user
        user.active = True
        user.save ()
        
        # Save login cookie
        request.session["user"] = user.id
        
        # Render success template       
        return render (request, "users/activate.html", {
            "subtitle": "activate",
            "name": user.name
        })
        
class Login (View):
    """ Login with dynamic link by email """
    
    subtitle = "login"
    default_script = True
    
    def get (self, request): 
        """ render register form """ 
        
        # Validate user session
        user_id = request.session.get ("user", None)
        if user_id:
            # Redirect to home
            return HttpResponseRedirect ("/")       
          
        # Render success template       
        return render (request, "users/login.html", {
            "subtitle": Login.subtitle,
            "default_script": Login.default_script
        })
    
    def post (self, request):
        """ submit login email """
        
        # Get email from post data
        email = request.POST.get ("email", None)
        
        # Validate user
        users_match = models.User.objects.filter(email=email, active=True)
        if not users_match:
            
            # reaload page with error
            return render (request, "users/login.html", {
                "error": "Email not found|Please check your email and try again",
                "subtitle": Login.subtitle,
                "default_script": Login.default_script
            })
            
        user = users_match.first()
        
        # Submit magic login link
        login_code = models.LoginCodes.objects.create (
            user=user
        )
        login_link = f"{HOST}/login-code/{login_code.hash}"        
        html_content = f'<p>Click here to login: <a href="{login_link}"> {login_link}</p>'
        submit_email ("Login link referral fifty fifty", html_content, email)
        
        return render (request, "users/login.html", {
            "info": "Check you email|We send you a magic link to login",
            "subtitle": Login.subtitle,
            "default_script": Login.default_script
        })
        
class LoginCode (View):
    """ Login with dynamic link by email """
        
    def get (self, request, hash):
        """ Validate login """
                        
        # Get login code
        login_code_math = models.LoginCodes.objects.filter(hash=hash)
        if not login_code_math:
            # redirect to not found
            return HttpResponseRedirect ("/404")

        user = login_code_math.first().user

        # Validate if the user is activate
        if not user.active:
            # redirect to not found
            return HttpResponseRedirect ("/404")

        # Save login cookie
        request.session["user"] = user.id
        
        # Delete login code
        login_code_math.delete ()
        
        # Rdirect to home page
        return HttpResponseRedirect ("/")

class Logout (View):
    """ Logout user """
    
    def get (self, request):
        """ Delete session """
        
        # Delete session data
        request.session.flush ()
        
        # Redirect to home page
        return HttpResponseRedirect ("/")
        