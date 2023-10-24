from django.urls import reverse
from django.test import TestCase
from users import models

class TestReferralByPhoneView (TestCase):
    
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
        
        self.url = reverse ("referral-by-phone")
    
    def test_get_no_phone (self):
        """ Try to get referral links without phone 
            Expected: 400
        """
        
        # Make request
        response = self.client.get (self.url)
        
        # Check response
        self.assertEqual (response.status_code, 400)
        self.assertEqual (response.json (), {
            "status": "error",
            "message": "Phone is required",
            "data": {}
        })
    
    def test_get_invalid_phone (self):
        """ Try to get referral links with invalid phone (no registered user)
            Expected: 404
        """
        
        # Make request
        phone = "0000000"
        response = self.client.get (
            self.url,
            data={"phone": phone}
        )
        
        # Check response
        self.assertEqual (response.status_code, 404)
        self.assertEqual (response.json (), {
            "status": "error",
            "message": "User not found",
            "data": {}
        })
    
    def test_get_disbale_user (self):
        """ Try to get referral links with a correct phone number but disable user 
            Expected: 404 
        """
        
        # Disable user
        self.user.active = False
        self.user.save ()
        
        # Make request
        response = self.client.get (
            self.url,
            data={"phone": self.user.phone}
        )
        
        # Check response
        self.assertEqual (response.status_code, 404)
        self.assertEqual (response.json (), {
            "status": "error",
            "message": "User not found",
            "data": {}
        })
    
    def test_get (self):
        """ Try to get referral links with valid phone 
            Expected: 200
        """
        
        # Make request
        response = self.client.get (
            self.url,
            data={"phone": self.user.phone}
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