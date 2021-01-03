import json, bcrypt, jwt  

from django.db import transaction
from django.test import TestCase, Client

from my_settings import JWT_ALGORITHM, SECRET_KEY
from users.models  import User,Host
from users.views   import LogInView
from reservations.models import (
     Reservation,
     Payment,
     PaymentMethod,
     ReservationGuest,
     Status,
     Guest
     )
from homes.models import (
    Home,
    HomeType, 
    BuildingType,Region
    )

class ReservationTest(TestCase):
    def setUp(self):
        self.client = Client()

        hashed_password = bcrypt.hashpw('a123456789'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        hash_card_number  = jwt.encode({"card_number" : "12121212121"}, "SECRET_KEY", algorithm='HS256')
        hash_expire_date  = jwt.encode({"expire_date" : "1212"}, "SECRET_KEY", algorithm='HS256')
        hash_post_code    = jwt.encode({"post_code" : "123"}, "SECRET_KEY", algorithm='HS256')
        hash_payment_date = jwt.encode({"payment_date" : "123"}, "SECRET_KEY", algorithm='HS256')
        hash_card_holder  = jwt.encode({"card_holder" : "leesuhan"}, "SECRET_KEY", algorithm='HS256')

        user1 = User.objects.create(
            id           = 1,
            last_name    = "김",
            first_name   = "수한",
            email        = 'sj950902@naver.com',
            password     = hashed_password,
            birthday     = '1592-01-11',
            profile_image= "abcd.jpg",
            mailing_check= 1
        )

        PaymentMethod.objects.create(
            id   = 1,
            name = "신용카드 또는 체크카드"
        )

        payment = Payment.objects.create(
            id           = 1,
            method       = PaymentMethod.objects.get(name="신용카드 또는 체크카드"),
            card_number  = hash_card_number,
            expire_date  = hash_expire_date,
            post_code    = hash_post_code,
            payment_date = hash_payment_date,
            card_holder  = hash_card_holder,
            total_cost   = "122000"
        )

        building_type = BuildingType.objects.create(
            name = '집 전체'
        )

        home_type = HomeType.objects.create(
            name = '다인실'
        )

        region = Region.objects.create(
            id              = 1,
            name            = "강남구",
            latitude        = "37.492465",
            longitude       = "127.068818",
            zoom_level      = 13,
            around_radius_m = 8000
        )

        home = Home.objects.create(
            id               = 1,
            name             = "승재's 오피스텔 #2 구일점",
            address          = "구로구, 서울, 대한민국",
            description      = "Welcome to my home. 저희 집에 오신것을 환영합니다.",
            capacity_guest   = 4,
            latitude         = 37.501670,
            longitude        = 127.035530,
            home_type        = home_type,
            building_type    = building_type,
            region           = region
        )

        Host.objects.create(
            id          = 1,
            contact     = "010-4321-1234",
            description = "안녕하세요 호스트입니다.",
            home        = home,
            user        = user1
        )
        
        status = Status.objects.create(
            id   = 2,
            name = "결제완료"
        )

        status2 = Status.objects.create(
            id   = 5,
            name = "예약취소"
        )

        Guest.objects.create(
        id   = 1,
        name = "성인"
        )

        Guest.objects.create(
        id   = 2,
        name = "어린이"
        )

        Guest.objects.create(
        id   = 3,
        name = "유아"
        )

        Reservation.objects.create(
            id        = 1,
            home_id   = home.id,
            check_in  = "2020-12-09",
            check_out = "2020-12-16",
            status    = status,
            user_id   = user1.id,
            payment   = payment
        )
        
        request_login = {
            "email" : "sj950902@naver.com",
            "password" : "a123456789"
        }

        response_login = self.client.post('/users/signin',json.dumps(request_login), content_type="application/json")
        self.token = response_login.json()["AUTHORIZATION"]

    def tearDown(self):
        User.objects.all().delete()
        Home.objects.all().delete()
        HomeType.objects.all().delete()
        BuildingType.objects.all().delete()
        Region.objects.all().delete()
        Host.objects.all().delete()
        Status.objects.all().delete()
        Guest.objects.all().delete()
        PaymentMethod.objects.all().delete()
    
    def test_ReservationView_post_success(self):
        
        request = {
            "card_number" : "12121212121",
            "expire_date" : "1212",
            "post_code"   : "123",
            "payment_date": "123",
            "card_holder" : "leesuhan",
            "total_cost"  : "122000",
            "method_id"   : "1",
            "user_id"     : "1",
            "home_id"     : "1",
            "check_in"    : "2020-12-10",
            "check_out"   : "2020-12-16",
            "status_id"   : "2",
            "adult"       : "2",
            "children"    : "2",
            "infant"      : "1"
        }
        headers = {"HTTP_Authorization" : self.token}
        response = self.client.post('/reservations',json.dumps(request),content_type="application/json",**headers)
        self.assertEqual(response.json(),
            {
                "MESSAGE":"SUCCESS"
            }
        )
        self.assertEqual(response.status_code, 200)
    
    def test_ReservationView_post_keyerror(self):

        request = {
            "expire_date" : "1212",
            "post_code"   : "123",
            "payment_date": "123",
            "card_holder" : "leesuhan",
            "total_cost"  : "122000",
            "method_id"   : "1",
            "user_id"     : "1",
            "home_id"     : "1",
            "check_in"    : "2020-12-10",
            "check_out"   : "2020-12-16",
            "status_id"   : "2",
            "adult"       : "2",
            "children"    : "2"
        }
        
        headers = {"HTTP_AUTHORIZATION": self.token}
        response = self.client.post('/reservations',json.dumps(request), content_type='application/json',**headers)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
            {
                "MESSAGE": "KEYERROR"
            }
        )
    
    def test_ReservationView_get_success(self):
        headers = {"HTTP_AUTHORIZATION": self.token}
        response = self.client.get('/reservations?status=upcomming',**headers)
        self.assertEqual(response.status_code, 200)
    
    def test_ReservationView_get_past_reservation_not_found(self):
        headers = {"HTTP_AUTHORIZATION": self.token}
        response = self.client.get('/reservations?status=past',**headers)
        self.assertEqual(response.status_code, 404)
    
class ReservationDetailTest(TestCase):
    def setUp(self):
        self.client = Client()

        hashed_password = bcrypt.hashpw('a123456789'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        hash_card_number  = jwt.encode({"card_number" : "12121212121"}, "SECRET_KEY", algorithm='HS256')
        hash_expire_date  = jwt.encode({"expire_date" : "1212"}, "SECRET_KEY", algorithm='HS256')
        hash_post_code    = jwt.encode({"post_code" : "123"}, "SECRET_KEY", algorithm='HS256')
        hash_payment_date = jwt.encode({"payment_date" : "123"}, "SECRET_KEY", algorithm='HS256')
        hash_card_holder  = jwt.encode({"card_holder" : "leesuhan"}, "SECRET_KEY", algorithm='HS256')

        user1 = User.objects.create(
            id           = 1,
            last_name    = "김",
            first_name   = "수한",
            email        = 'sj950902@naver.com',
            password     = hashed_password,
            birthday     = '1592-01-11'
        )

        PaymentMethod.objects.create(
            id   = 1,
            name = "신용카드 또는 체크카드"
        )

        payment = Payment.objects.create(
            id           = 1,
            method       = PaymentMethod.objects.get(name="신용카드 또는 체크카드"),
            card_number  = hash_card_number,
            expire_date  = hash_expire_date,
            post_code    = hash_post_code,
            payment_date = hash_payment_date,
            card_holder  = hash_card_holder,
            total_cost   = "122000"
        )

        building_type = BuildingType.objects.create(
            name = '집 전체'
        )

        home_type = HomeType.objects.create(
            name = '다인실'
        )

        status2 = Status.objects.create(
            id   = 5,
            name = "예약취소"
        )
        
        region = Region.objects.create(
            id              = 1,
            name            = "강남구",
            latitude        = "37.492465",
            longitude       = "127.068818",
            zoom_level      = 13,
            around_radius_m = 8000
        )

        home = Home.objects.create(
            id               = 1,
            name             = "승재's 오피스텔 #2 구일점",
            address          = "구로구, 서울, 대한민국",
            description      = "Welcome to my home. 저희 집에 오신것을 환영합니다.",
            capacity_guest   = 4,
            latitude         = 37.501670,
            longitude        = 127.035530,
            home_type        = home_type,
            building_type    = building_type,
            region           = region
        )
        Host.objects.create(
            id          = 1,
            contact     = "010-4321-1234",
            description = "안녕하세요 호스트입니다.",
            home        = home,
            user        = user1
        )
        

        Status.objects.create(
            id   = 2,
            name = "결제완료"
        )

        Guest.objects.create(
        id   = 1,
        name = "성인"
        )
        
        request_login = {
            "email"     : "sj950902@naver.com",
            "password"  : "a123456789"
        }

        response_login = self.client.post('/users/signin',json.dumps(request_login), content_type="application/json")
        self.token = response_login.json()["AUTHORIZATION"]
              
        Reservation.objects.create(
            id         = 1,
            user_id    = 1,
            home_id    = 1,
            check_in  = "2020-12-09",
            check_out = "2020-12-16",
            created_at = "2020-10-11",
            status_id  = 2,
            payment_id = 1
        )

        

    def tearDown(self):
        User.objects.all().delete()
        Home.objects.all().delete()
        HomeType.objects.all().delete()
        BuildingType.objects.all().delete()
        Region.objects.all().delete()
        Host.objects.all().delete()
        Status.objects.all().delete()
        Guest.objects.all().delete()
        PaymentMethod.objects.all().delete()
    
    def test_ReservationDetailView_get_success(self):
        headers = {"HTTP_AUTHORIZATION": self.token}
        response = self.client.get('/reservations/1',**headers)
        self.assertEqual(response.status_code, 200)

    def test_ReservationDetailView_get_reservation_not_found(self):
        headers = {"HTTP_AUTHORIZATION": self.token}
        response = self.client.get('/reservations/2',**headers)
        self.assertEqual(response.status_code, 404)
    
    def test_ReservationDetailView_delete_success(self):
        headers = {"HTTP_AUTHORIZATION": self.token}
        response = self.client.delete('/reservations/1',**headers)
        self.assertEqual(response.status_code, 200)

    def test_ReservationDetailView_delete_reservation_not_found(self):
        headers = {"HTTP_AUTHORIZATION": self.token}
        response = self.client.delete('/reservations/2',**headers)
        self.assertEqual(response.status_code, 404)
