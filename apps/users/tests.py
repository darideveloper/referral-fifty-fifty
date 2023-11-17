from django.core import mail
from bs4 import BeautifulSoup
from users import models
from django.urls import reverse
from django.test import TestCase
from core import models as core_models
from referralfiftyfifty.settings import EMAIL_HOST_USER, HOST, PRICE_CHECKER_HOST

class TestReferralView (TestCase):

    def setUp(self):

        # Create sample user
        self.user = models.User.objects.create(
            name="test",
            last_name="test",
            email="test@test",
            phone="1234567890",
            active=True
        )

        # Create stores
        self.store = models.Store.objects.create(
            name="store"
        )

        # Create referral link
        self.referral = models.ReferralLink.objects.create(
            user=self.user,
            store=self.store,
            link="refid=12345"
        )

        # Create tolen
        self.token = core_models.Token.objects.create(
            name="test",
            token="test",
            is_active=True
        )

        # Endpoint url
        self.url = reverse("referral")

        # Request data
        self.get_data = {
            "phone": self.user.phone,
            "email": self.user.email,
            "hash": self.user.hash
        }

        self.post_data = {
            "name": "test",
            "last_name": "test",
            "email": "test@test",
            "phone": "1234567890",
            "stores": {
                self.store.name: "refid=12345",
                "fake_store": "refid=12345"
            }
        }

        self.client.defaults["HTTP_token"] = self.token.token

    def test_get_no_phone_no_email_no_hash(self):
        """ Try to get referral links without phone, email or hash
            Expected: 400
        """

        # Remove phone from data
        self.get_data.pop("phone")
        self.get_data.pop("email")
        self.get_data.pop("hash")

        # Make request
        response = self.client.get(
            self.url,
            data=self.get_data
        )

        # Check response
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {
            "status": "error",
            "message": "Phone or email or hash is required",
            "data": {}
        })

    def test_get_invalid_phone(self):
        """ Try to get referral links with invalid phone (no registered user)
            Expected: 404
        """

        # Change to wrong phone number
        self.get_data.pop("email")
        self.get_data.pop ("hash")
        self.get_data["phone"] = "0000000"

        # Make request
        response = self.client.get(
            self.url,
            data=self.get_data
        )

        # Check response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            "status": "error",
            "message": "User not found",
            "data": {}
        })

    def test_get_invalid_email(self):
        """ Try to get referral links with invalid email (no registered user)
            Expected: 404
        """

        # Change to wrong phone number
        self.get_data.pop("phone")
        self.get_data.pop ("hash")
        self.get_data["email"] = "fake@gmail.com"

        # Make request
        response = self.client.get(
            self.url,
            data=self.get_data
        )

        # Check response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            "status": "error",
            "message": "User not found",
            "data": {}
        })
        
    def test_get_invalid_hash(self):
        """ Try to get referral links with invalid hash (no registered user)
            Expected: 404
        """

        # Change to wrong phone number
        self.get_data.pop("phone")
        self.get_data.pop ("email")
        self.get_data["hash"] = "jhasgfyhsaty%/&GHashg"

        # Make request
        response = self.client.get(
            self.url,
            data=self.get_data
        )

        # Check response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            "status": "error",
            "message": "User not found",
            "data": {}
        })

    def test_get_disbaled_user_phone(self):
        """ Try to get referral links with a correct phone number but disable user 
            Expected: 404 
        """

        # Remove email from data
        self.get_data.pop("email")
        self.get_data.pop("hash")

        # Disable user
        self.user.active = False
        self.user.save()

        # Make request
        response = self.client.get(
            self.url,
            data=self.get_data
        )

        # Check response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            "status": "error",
            "message": "User not found",
            "data": {}
        })

    def test_get_disbaled_user_email(self):
        """ Try to get referral links with a correct email but disable user 
            Expected: 404 
        """

        # Remove phone from data
        self.get_data.pop("phone")
        self.get_data.pop("hash")

        # Disable user
        self.user.active = False
        self.user.save()

        # Make request
        response = self.client.get(
            self.url,
            data=self.get_data
        )

        # Check response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            "status": "error",
            "message": "User not found",
            "data": {}
        })
        
    def test_get_disbaled_user_hash(self):
        """ Try to get referral links with a correct hash but disable user 
            Expected: 404 
        """

        # Remove phone from data
        self.get_data.pop("phone")
        self.get_data.pop("email")

        # Disable user
        self.user.active = False
        self.user.save()

        # Make request
        response = self.client.get(
            self.url,
            data=self.get_data
        )

        # Check response
        self.assertEqual(response.status_code, 404)
        self.assertEqual(response.json(), {
            "status": "error",
            "message": "User not found",
            "data": {}
        })

    def test_get_phone(self):
        """ Try to get referral links with valid phone 
            Expected: 200
        """

        # Remove email from data
        self.get_data.pop("email")
        self.get_data.pop("hash")

        # Make request
        response = self.client.get(
            self.url,
            data=self.get_data
        )

        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "status": "success",
            "message": "User found",
            "data": {
                self.store.name: self.referral.link
            }
        })

    def test_get_email(self):
        """ Try to get referral links with valid email 
            Expected: 200
        """

        # Remove phone from data
        self.get_data.pop("phone")
        self.get_data.pop("hash")

        # Make request
        response = self.client.get(
            self.url,
            data=self.get_data
        )

        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "status": "success",
            "message": "User found",
            "data": {
                self.store.name: self.referral.link
            }
        })

    def test_get_hash(self):
        """ Try to get referral links with valid hash 
            Expected: 200
        """

        # Remove phone from data
        self.get_data.pop("phone")
        self.get_data.pop("email")

        # Make request
        response = self.client.get(
            self.url,
            data=self.get_data
        )

        # Check response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            "status": "success",
            "message": "User found",
            "data": {
                self.store.name: self.referral.link
            }
        })

class TestRegisterView (TestCase):

    def setUp(self):

        # Create stores
        self.stores = {}
        self.stores["amazon"] = models.Store.objects.create(
            name="amazon"
        )
        self.stores["ebay"] = models.Store.objects.create(
            name="ebay"
        )
        self.stores["walmart"] = models.Store.objects.create(
            name="walmart"
        )

        # Endpoint url
        self.url = reverse("register")
        
        self.form_data = {
            "first-name": "test",
            "last-name": "test",
            "email": EMAIL_HOST_USER,
            "phone": "1234567890",
            "amazon": "refid=12345",
            "ebay": "refid=6789",
            "walmart": "refid=0000"
        }
        
        self.user = models.User.objects.create (
            name="test",
            last_name="test",
            email="sample@gmail.com",
            phone="000000",
            active=True
        )

    def test_get(self):
        """ Validate loading the register form """

        response = self.client.get(
            self.url,
        )

        # Check response status
        self.assertEqual(response.status_code, 200)

        # Check response html
        soup = BeautifulSoup(response.content, "html.parser")
        self.assertIsNotNone(soup.find("h1", text="Sign Up"))
        self.assertNotEqual(soup.select("#first-name"), [])
        self.assertNotEqual(soup.select("#last-name"), [])
        self.assertNotEqual(soup.select("#email"), [])
        self.assertNotEqual(soup.select("#phone"), [])
        self.assertNotEqual(soup.select("#amazon"), [])
        self.assertNotEqual(soup.select("#ebay"), [])
        self.assertNotEqual(soup.select("#walmart"), [])
        self.assertNotEqual(soup.select("input.btn.cta"), [])
        
    def test_get_logged (self):
        """ Validate try to load login page when user is logged
            Expected: redirect to home
        """

        # Create session
        session = self.client.session
        session['user'] = self.user.id
        session.save()
        
        response = self.client.get(
            self.url,
        )

        # Validate redirect to home
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")
                
    def test_post_missing_data (self): 
        """ Try to submit form with missing required data
            Expected: error message
        """
        
        # Edit form data
        del self.form_data["first-name"]
        del self.form_data["last-name"]
        
        # Make request
        response = self.client.post (
            self.url,
            data=self.form_data
        )
        
        # Validate error in html
        error_message = 'const error = "Missing data|First name, last name, email and phone are required"'
        html_text = response.content.decode('utf-8')
        self.assertIn (error_message, html_text)
        
    def test_post_user_already_exist_email (self):
        """ Try to create a user with an email already registered
            Expected: error message
        """
        
        # Create user with desired email
        models.User.objects.create (
            name=self.form_data["first-name"],
            last_name=self.form_data["last-name"],
            email=self.form_data["email"],
            phone=self.form_data["phone"]
        )
        
        # Change phone
        self.form_data["phone"] = "0000000000"
        
        # Make request
        response = self.client.post (
            self.url,
            data=self.form_data
        )
        
        # Validate error in html
        error_message = 'const error = "Error creating user|Email or phone already exists. Do not forget to activate your email with the link we sent you after signing up."'
        html_text = response.content.decode('utf-8')
        self.assertIn (error_message, html_text)
    
    def test_post_user_already_exist_phone (self):
        """ Try to create a user with an email already registered
            Expected: error message
        """
        
        # Create user with desired email
        models.User.objects.create (
            name=self.form_data["first-name"],
            last_name=self.form_data["last-name"],
            email=self.form_data["email"],
            phone=self.form_data["phone"]
        )
        
        # change email
        self.form_data["email"] = "test2@test"
        
        # Make request
        response = self.client.post (
            self.url,
            data=self.form_data
        )
        
        # Validate error in html
        error_message = 'const error = "Error creating user|Email or phone already exists. Do not forget to activate your email with the link we sent you after signing up."'
        html_text = response.content.decode('utf-8')
        self.assertIn (error_message, html_text)
        
    def test_post_success (self):
        """ Validate user saved in database, store links saved and activation email sent 
            Expected: success message
        """ 
        
        # VALIDATE RESPONSE
        
        # Make request
        response = self.client.post (
            self.url,
            data=self.form_data
        )
        
        # Validate error in html
        info_message = 'const info = "We are almost done|Check your email to complete your registration"'
        html_text = response.content.decode('utf-8')
        self.assertIn (info_message, html_text)
        
        # VALIDATE MODELS
        
        # Validate user found in database
        users = models.User.objects.filter (
            email=self.form_data["email"],
        )
        self.assertEqual (users.count (), 1)
        
        # Validate user data
        user = users.first ()
        self.assertEqual (user.name, self.form_data["first-name"])
        self.assertEqual (user.last_name, self.form_data["last-name"])
        self.assertEqual (user.email, self.form_data["email"])
        self.assertEqual (user.phone, self.form_data["phone"])
        self.assertEqual (user.active, False)
        
        # Validate referral links
        user_refferral_links = models.ReferralLink.objects.filter (
            user=user
        )
        self.assertEqual (user_refferral_links.count (), 3)
        for refferral_link in user_refferral_links:
            store = refferral_link.store.name
            self.assertEqual (refferral_link.link, self.form_data[store])
        
        # VALIDATE EMAIL
        
        # Validate number of emails sent
        self.assertEqual(len(mail.outbox), 1)
        
        # Validate email content
        email = mail.outbox[0]
        self.assertEqual(email.subject, 'Complete your registration')
        activation_link = f"{HOST}/activate/{user.hash}"
        message = f"Click here to complete your registration:  {activation_link}"
        self.assertEqual(email.body, message)
        
class TestActivateView (TestCase):

    def setUp(self):
        
        # Create user
        self.user = models.User.objects.create (
            name="test",
            last_name="test",
            email=EMAIL_HOST_USER,
            phone="1234567890",
        )
    
    def test_invalid_hash (self):
        """ Try to open activate page with invalid hash 
            Expected: redirect to 404 page
        """
        
        # Make request
        response = self.client.get (
            reverse("activate", kwargs={"hash": "invalid_hash"})
        )
        
        # Validate response redirect to 404 page
        self.assertEqual (response.status_code, 302)
        self.assertEqual (response.url, "/404")
        
        # Validate user keep inactive
        self.assertEqual (self.user.active, False)
        
    def test_valid_hash (self): 
        """ Try to open activate page with valid hash 
            Expected: activate user and show success message
        """
                
        # Make request
        response = self.client.get (
            reverse("activate", kwargs={"hash": self.user.hash})
        )
        
        # Validate response
        self.assertEqual (response.status_code, 200)
        
        # Validate user keep inactive
        self.assertEqual (self.user.active, False)
        
        # Validate html content
        title = '<h1>Your accout is now active</h1>'
        link = '/login'
        html_text = response.content.decode('utf-8')
        self.assertIn (title, html_text)
        self.assertIn (link, html_text)
        
class TestLoginView (TestCase):
    
    def setUp(self):
        
        # Create user
        self.user = models.User.objects.create (
            name="test",
            last_name="test",
            email=EMAIL_HOST_USER,
            phone="000000",
            active=True
        )
        
        self.url = reverse("login")
        
        self.form_data = {
            "email": EMAIL_HOST_USER,
        }
        
    def test_get (self):
        """ Try load login page """
        
        # make request
        response = self.client.get (
            self.url
        )
        
        # Validate response
        self.assertEqual (response.status_code, 200)
        
        # Validate html content
        title = '<h1>Login</h1>'
        form = '<form action="." method="post">'
        input_email = '<input type="email" name="email" id="email" placeholder="sample@gmail.com" aria-describedby="emailHelp" required>'
        html_text = response.content.decode('utf-8')
        self.assertIn (title, html_text)
        self.assertIn (form, html_text)
        self.assertIn (input_email, html_text)
        
    def test_get_logged (self):
        """ Validate try to load login page when user is logged
            Expected: redirect to home
        """

        # Create session
        session = self.client.session
        session['user'] = self.user.id
        session.save()
        
        response = self.client.get(
            self.url,
        )

        # Validate redirect to home
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")
        
    def test_post_invalid_email (self):
        """ Try to login with no registered email 
            Expected: error message
        """
        
        # Change email
        self.form_data["email"] = "fake@gmail.com"
        
        # make request
        response = self.client.post (
            self.url,
            data=self.form_data
        )
        
        # Validate response
        self.assertEqual (response.status_code, 200)
        
        # Validate html content
        error_message = 'const error = "Email not found|Please check your email and try again"'
        html_text = response.content.decode('utf-8')
        self.assertIn (error_message, html_text)
    
    def test_post_no_activate_email (self):
        """ Try to login with no activate account
            Expected: error message
        """
        
        # Diable user
        self.user.active = False
        self.user.save()
        
        # make request
        response = self.client.post (
            self.url,
            data=self.form_data
        )
        
        # Validate response
        self.assertEqual (response.status_code, 200)
        
        # Validate html content
        error_message = 'const error = "Email not found|Please check your email and try again"'
        html_text = response.content.decode('utf-8')
        self.assertIn (error_message, html_text)
    
    def test_post_success (self):
        """ Try to login with correct email and valid account
            Expected: confirm email message
        """
        
        # make request
        response = self.client.post (
            self.url,
            data=self.form_data
        )
        
        # Validate response
        self.assertEqual (response.status_code, 200)
        
        # Validate html content
        error_message = 'const info = "Check you email|We send you a magic link to login"'
        html_text = response.content.decode('utf-8')
        self.assertIn (error_message, html_text)
        
        # Validate number of emails sent
        self.assertEqual(len(mail.outbox), 1)
        
        # Validate email content
        email = mail.outbox[0]
        login_code = models.LoginCodes.objects.filter (
            user=self.user
        ).first()
        self.assertEqual(email.subject, 'Login link referral fifty fifty')
        login_link = f"{HOST}/login-code/{login_code.hash}"        
        message = f"Click here to login:  {login_link}"
        self.assertEqual(email.body, message)
        
class TestLoginCodeView (TestCase):
    
    def setUp(self):
        
        # Create user
        self.user = models.User.objects.create (
            name="test",
            last_name="test",
            email=EMAIL_HOST_USER,
            phone="1234567890",
            active=True
        )
        
        # Generate login code
        self.login_code = models.LoginCodes.objects.create (
            user=self.user
        ).hash
                
    def test_invalid_hash (self):
        """ Try to open login link with invalid hash 
            Expected: redirect to 404 page
        """
        
        # Make request
        response = self.client.get (
            reverse("login-code", kwargs={"hash": "invalid_hash"})
        )
        
        # Validate response redirect to 404 page
        self.assertEqual (response.status_code, 302)
        self.assertEqual (response.url, "/404")
        
        # Validate the is not a cookie
        self.assertEqual (response.cookies, {})
        
        # Validte if login code was deleted
        login_code_match = models.LoginCodes.objects.filter (
            user=self.user
        )
        self.assertEqual (login_code_match.count (), 1)
        
    def test_invalid_user (self):
        """ Try to login with correct hash but invalid user
            Expected: redirect to 404 page
        """
        
        # Disable user
        self.user.active = False
        self.user.save()
        
        # Make request
        response = self.client.get (
            reverse("login-code", kwargs={"hash": self.login_code})
        )
        
        # Validate response redirect to 404 page
        self.assertEqual (response.status_code, 302)
        self.assertEqual (response.url, "/404")
        
        # Validate the is not a cookie
        self.assertEqual (response.cookies, {})
        
        # Validte if login code was deleted
        login_code_match = models.LoginCodes.objects.filter (
            user=self.user
        )
        self.assertEqual (login_code_match.count (), 1)
        
    def test_success (self):
        """ Try to login with correct user and hash 
            Expected: redirect to home and set cookie
        """
            
        # Make request
        response = self.client.get (
            reverse("login-code", kwargs={"hash": self.login_code})
        )
        
        # Validate response redirect to 404 page
        self.assertEqual (response.status_code, 302)
        self.assertEqual (response.url, "/")
        
        # Validate the is not a cookie
        session_data = self.client.session
        self.assertEqual(session_data['user'], self.user.id)
        
        # Validte if login code was deleted
        login_code_match = models.LoginCodes.objects.filter (
            user=self.user
        )
        self.assertEqual (login_code_match.count (), 0)
        
class TestLogout (TestCase): 
      
    def setUp(self):
        
        # Create user
        self.user = models.User.objects.create (
            name="test",
            last_name="test",
            email=EMAIL_HOST_USER,
            phone="1234567890",
            active=True
        )
        
    def test_logout (self):
        """ Try to logout
            Expected: redirect to login page and delete cookie
        """
        
        # Create session
        session = self.client.session
        session['user'] = self.user.id
        session.save()
        
        # Make request
        response = self.client.get (
            reverse("logout")
        )
        
        # Validate response redirect to 404 page
        self.assertEqual (response.status_code, 302)
        self.assertEqual (response.url, "/")
        
        # Validate the is not a cookie
        session_data = self.client.session
        self.assertEqual(session_data.get("user", ""), "")
        
class TestIndexView (TestCase):
    
    def setUp(self):
        
        # Create user
        self.user = models.User.objects.create (
            name="test",
            last_name="test",
            email=EMAIL_HOST_USER,
            phone="1234567890",
            active=True
        )
        
        self.url = reverse("index")
    
    def test_no_logged (self):
        """ Try to load index page without login
            Expected: redirect to login page
        """
        
        # Make request
        response = self.client.get (
            self.url
        )
        
        # Validate response redirect to 404 page
        self.assertEqual (response.status_code, 302)
        self.assertEqual (response.url, "/login")
    
    def test_logged (self):
        """ Try to load index page with login
            Expected: show referral link
        """
        
        # Create session
        session = self.client.session
        session['user'] = self.user.id
        session.save()
        
        # Make request
        response = self.client.get (
            self.url
        )
        
        # Validate response redirect to 404 page
        self.assertEqual (response.status_code, 200)

        # Validate login link
        user_hash = self.user.hash
        login_link = f"{PRICE_CHECKER_HOST}/referral/{user_hash}"
        soup = BeautifulSoup(response.content, "html.parser")
        self.assertIsNotNone(soup.find("a", href=login_link))
        
class TestLegal (TestCase):
    
    def test_get (self):
        """ Try to load legal page and validate content 
        Expected: show legal content
        """
        
        # Make request
        response = self.client.get (
            reverse("legal")
        )
        
        # Validate response
        self.assertEqual (response.status_code, 200)
        
        # Validate html content
        title = '<h1>Legals</h1>'
        html_text = response.content.decode('utf-8')
        self.assertIn (title, html_text)
        
class TestLegalFramework (TestCase):
    
    def test_get (self):
        """ Try to load legal framework page and validate content 
        Expected: show legal content
        """
        
        # Make request
        response = self.client.get (
            reverse("legal-framework")
        )
        
        # Validate response
        self.assertEqual (response.status_code, 200)
        
        # Validate html content
        title = '<h1>Legal Framework and Basis for Participation and Earnings in Commission Sharing Programs in the United States</h1>'
        html_text = response.content.decode('utf-8')
        self.assertIn (title, html_text)