import json, bcrypt, jwt, re, requests

from unittest.mock  import patch, MagicMock
from django.test    import TestCase, Client

from .models        import User

client = Client()

class UserSignUpTest(TestCase):
    def setUp(self):
        User.objects.create(
                id              = 1,
                first_name      = "hue",
                last_name       = "park",
                email           = "KCM_MEANS_KIMCHIMAN@lycos.com",
                password        = bcrypt.hashpw('12345678A'.encode("utf-8"), bcrypt.gensalt()).decode("utf-8"),
                birthday        = "1900-01-01",
                mailing_check   = "1",
                )
    def tearDown(self):
        User.objects.all().delete()

    def test_signup_post_success(self):

        user = {
                "first_name"    : "UU",
                "last_name"     : "park",
                "email"         : "KCM_MEANS_KIMCHIMAN1@lycos.com",
                "password"      : "123456789A",
                "birthdayYear"  : "1900",
                "birthdayMonth" : "1",
                "birthdayDate"  : "1",
                "mailing_check" : "1"
                }
        
        response = client.post("/users/signup", json.dumps(user), content_type="application/json")
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {"MESSAGE" : "SUCCESS"})

    def test_signup_post_user_already_exists(self):
        
        user2 = {
                "first_name"    : "hue",
                "last_name"     : "park",
                "email"         : "KCM_MEANS_KIMCHIMAN@lycos.com",
                "password"      : "12345678A",
                "birthdayYear"  : "1900",
                "birthdayMonth" : "1",
                "birthdayDate"  : "1",
                "mailing_check" : "1"
                }
        
        response = client.post("/users/signup", json.dumps(user2), content_type="application/json")

        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), {"MESSAGE" : "ALREADY_EXISTS"})
    
    def test_signup_post_invalid_email(self):

        user3 = {
                "first_name"    : "yoo",
                "last_name"     : "park",
                "email"         : "KCM_MEANS_KIMCHIMAN.com",
                "password"      : "123456789A",
                "birthdayYear"  : "1900",
                "birthdayMonth" : "1",
                "birthdayDate"  : "1",
                "mailing_check" : "1"
                }
        
        response = client.post("/users/signup", json.dumps(user3), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE" : "INVALID_EMAIL"})

    def test_signup_post_invalid_password(self):

        user4 = {
                "first_name"    : "hueyoo",
                "last_name"     : "park",
                "email"         : "KCM_MEANS_KIMCHIMAN1234@lycos.com",
                "password"      : "1A",
                "birthdayYear"  : "1990",
                "birthdayMonth" : "1",
                "birthdayDate"  : "1",
                "mailing_check" : "1"
                }
        
        response = client.post("/users/signup", json.dumps(user4), content_type="application/json")

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {"MESSAGE" : "INVALID_PASSWORD"})
