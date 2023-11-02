import json
from django.urls import reverse
from django.test import TestCase
from users import models
from core import models as core_models

class TestReferralView (TestCase):
    
    def setUp (self):
        
        # Create sample user
        self.user = models.User.objects.create (
            name = "test",
            last_name = "test",
            email = "test@test",
            phone = "1234567890",
            active = True
        )
        
        # Create stores
        self.store = models.Store.objects.create (
            name = "store"
        )
        
        # Create referral link
        self.referral = models.ReferralLink.objects.create (
            user=self.user,
            store=self.store,
            link="refid=12345"
        )
        
        # Create tolen
        self.token = core_models.Token.objects.create (
            name="test",
            token="test",
            is_active=True
        )
        
        # Endpoint url
        self.url = reverse ("referral")
        
        # Request data
        self.get_data = {
            "phone": self.user.phone,
            "email": self.user.email
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
    
    def test_get_no_phone_no_email (self):
        """ Try to get referral links without phone and email
            Expected: 400
        """
        
        # Remove phone from data
        self.get_data.pop ("phone")
        self.get_data.pop ("email")
        
        # Make request
        response = self.client.get (
            self.url,
            data=self.get_data
        )
        
        # Check response
        self.assertEqual (response.status_code, 400)
        self.assertEqual (response.json (), {
            "status": "error",
            "message": "Phone or email is required",
            "data": {}
        })
    
    def test_get_invalid_phone (self):
        """ Try to get referral links with invalid phone (no registered user)
            Expected: 404
        """
        
        # Change to wrong phone number
        self.get_data.pop ("email")
        self.get_data["phone"] = "0000000"
        
        # Make request
        response = self.client.get (
            self.url,
            data=self.get_data
        )
        
        # Check response
        self.assertEqual (response.status_code, 404)
        self.assertEqual (response.json (), {
            "status": "error",
            "message": "User not found",
            "data": {}
        })
        
    def test_get_invalid_email (self):
        """ Try to get referral links with invalid email (no registered user)
            Expected: 404
        """
        
        # Change to wrong phone number
        self.get_data.pop ("phone")
        self.get_data["email"] = "fake@gmail.com"
        
        
        # Make request
        response = self.client.get (
            self.url,
            data=self.get_data
        )
        
        # Check response
        self.assertEqual (response.status_code, 404)
        self.assertEqual (response.json (), {
            "status": "error",
            "message": "User not found",
            "data": {}
        })
    
    def test_get_disbaled_user_phone (self):
        """ Try to get referral links with a correct phone number but disable user 
            Expected: 404 
        """
        
        # Remove email from data
        self.get_data.pop ("email")
        
        # Disable user
        self.user.active = False
        self.user.save ()
        
        # Make request
        response = self.client.get (
            self.url,
            data=self.get_data
        )
        
        # Check response
        self.assertEqual (response.status_code, 404)
        self.assertEqual (response.json (), {
            "status": "error",
            "message": "User not found",
            "data": {}
        })
        
    def test_get_disbaled_user_email (self):
        """ Try to get referral links with a correct email but disable user 
            Expected: 404 
        """
        
        # Remove phone from data
        self.get_data.pop ("phone")
        
        # Disable user
        self.user.active = False
        self.user.save ()
        
        # Make request
        response = self.client.get (
            self.url,
            data=self.get_data
        )
        
        # Check response
        self.assertEqual (response.status_code, 404)
        self.assertEqual (response.json (), {
            "status": "error",
            "message": "User not found",
            "data": {}
        })
    
    def test_get_phone (self):
        """ Try to get referral links with valid phone 
            Expected: 200
        """
        
        # Remove email from data
        self.get_data.pop ("email")
                
        # Make request
        response = self.client.get (
            self.url,
            data=self.get_data
        )
        
        # Check response
        self.assertEqual (response.status_code, 200)
        self.assertEqual (response.json (), {
            "status": "success",
            "message": "User found",
            "data": {
                self.store.name: self.referral.link
            }
        })
        
    def test_get_email (self):
        """ Try to get referral links with valid email 
            Expected: 200
        """
        
        # Remove phone from data
        self.get_data.pop ("phone")
                        
        # Make request
        response = self.client.get (
            self.url,
            data=self.get_data
        )
        
        # Check response
        self.assertEqual (response.status_code, 200)
        self.assertEqual (response.json (), {
            "status": "success",
            "message": "User found",
            "data": {
                self.store.name: self.referral.link
            }
        })