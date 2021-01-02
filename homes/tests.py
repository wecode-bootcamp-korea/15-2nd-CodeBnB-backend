import json, bcrypt, jwt, datetime

from homes.models import Home, HomeType, BuildingType,Region,PriceCategory,HomePrice,Review
from users.models import User, Host
from reservations.models import (
     Reservation,
     Payment,
     PaymentMethod,
     ReservationGuest,
     Status,
     Guest
     )
from django.test  import TestCase, Client

from my_settings  import SECRET_KEY, JWT_ALGORITHM 

class HomeListTest(TestCase):
    def setUp(self):
        self.client = Client()
        building_type = BuildingType.objects.create(
            name = '집 전체'
        )
        
        home_type = HomeType.objects.create(
            name = '다인실'
        )
    
        region = Region.objects.create(
            id   = 1,
            name = "강남구",
            latitude = "37.492465",
            longitude = "127.068818",
            zoom_level = 13,
            around_radius_m = 8000
        )

        region2 = Region.objects.create(
            id = 2,
            name = "구로구",
            latitude = "37.392465",
            longitude = "127.168818",
            zoom_level = 13,
            around_radius_m = 8000
        )

        price = PriceCategory.objects.create(
            name = "1박비용"
        )

        home1 = Home.objects.create(
            id               = 1,
            name             = "승재's 오피스텔 #2 구일점",
            address          = "구로구, 서울, 대한민국",
            description      = "Welcome to my home. 저희 집에 오신것을 환영합니다.",
            capacity_guest   = 4,
            latitude         = 37.501670,
            longitude        = 127.035530,
            home_type        = home_type,
            building_type    = building_type,
            region           = region2
        )
        
        home2 = Home.objects.create(
            id               = 2,
            name             = "승재's 오피스텔 #2 강남점",
            address          = "강남구, 서울, 대한민국",
            description      = "Welcome to my home. 저희 집에 오신것을 환영합니다.",
            capacity_guest   = 4,
            latitude         = 37.301670,
            longitude        = 127.135530,
            home_type        = home_type,
            building_type    = building_type,
            region           = region
        )
        
        User.objects.create(
            first_name = "김",
            last_name = "승재",
            email = "12345@2naver.com",
            password = "a123456789",
            birthday = "2020-10-11"
        )

        HomePrice.objects.create(home=home1,price_category=price,cost=10000)
        HomePrice.objects.create(home=home2,price_category=price,cost=100000)
        
        
    def tearDown(self):
        Home.objects.all().delete()
        HomeType.objects.all().delete()
        BuildingType.objects.all().delete()
        Region.objects.all().delete()

    def test_homelistview_get_success(self):
        response = self.client.get('/homes')
        self.assertEqual(response.json()['homes'][0]['home_name'], "승재's 오피스텔 #2 구일점")
        self.assertEqual(response.status_code, 200)

    def test_homelistview_get_filtering_region(self):
        response = self.client.get('/homes?neighborhood_id=1')
        self.assertEqual(response.json()['homes'][0]['home_name'], "승재's 오피스텔 #2 강남점")
        self.assertEqual(response.status_code, 200)

    def test_homelistview_get_not_found(self):
        response = self.client.get('/homes?neighborhood_id=10')
        self.assertEqual(response.status_code, 404)

class HomeDetailTest(TestCase):
    def setUp(self):
        self.client = Client()
        building_type = BuildingType.objects.create(
            name = '집 전체'
        )
        
        home_type = HomeType.objects.create(
            name = '다인실'
        )
    
        region = Region.objects.create(
            id   = 1,
            name = "강남구",
            latitude = "37.492465",
            longitude = "127.068818",
            zoom_level = 13,
            around_radius_m = 8000
        )

        price = PriceCategory.objects.create(
            name = "1박비용"
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
        
        user = User.objects.create(
            id                  = 1,
            last_name           = "김",
            first_name          = "승재",
            email               = "sj950902@naver.com",
            password            = "a123456789",
            birthday            = "1995-9-2",
            mailing_check       = 1,
            created_at          = "2020-10-11",
            profile_image       = "https://i0.wp.com/prikachi.com/wp-content/uploads/2020/07/DPP1.jpg"
        )

        host = Host.objects.create(
            id              = 1,
            user_id         = 1,
            home_id         = 1,
            contact         = "010-1234-1234",
            is_valid        = 1,
            description     = "안녕하세요",
            commission_date = "2020-10-11",
            is_superhost    = 1
        )
        
        HomePrice.objects.create(home=home,price_category=price,cost=10000)

    def tearDown(self):
        Home.objects.all().delete()
        HomeType.objects.all().delete()
        BuildingType.objects.all().delete()
        Region.objects.all().delete()

    def test_homedetailview_get_success(self):
        home_id = Home.objects.get(id=1).id
        response = self.client.get(f'/homes/{home_id}')
        self.assertEqual(response.status_code, 200)

    def test_homedetailview_get_fail(self):
        response = self.client.get('/homes/2')
        self.assertEqual(response.json(),
            {'MESSAGE':'HOME_NOT_FOUND'}
        )
        self.assertEqual(response.status_code, 404)

    def test_homedetailview_get_not_found(self):
        response = self.client.get('homes/2')
        self.assertEqual(response.status_code, 404)

class ReviewTest(TestCase):
    def setUp(self):    
        self.client = Client()
        user = User.objects.create(
            id                  = 1,
            last_name           = "김",
            first_name          = "승재",
            email               = "sj950902@naver.com",
            password            = bcrypt.hashpw("a123456789".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            birthday            = "1995-9-2",
            mailing_check       = 1,
            created_at          = "2020-10-11",
            profile_image       = "https://i0.wp.com/prikachi.com/wp-content/uploads/2020/07/DPP1.jpg"
        )
        PaymentMethod.objects.create(
            id   = 1,
            name = "신용카드 또는 체크카드"
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
            user        = user
        )
        
        Status.objects.create(
            id   = 2,
            name = "결제완료"
        )

        Guest.objects.create(
            id   = 1,
            name = "성인"
        )

        payment = Payment.objects.create(
            method_id       = 1,
            card_number     = 123456789,
            expire_date     = "2021-10-20",
            post_code       = "123456789",
            payment_date    = "2021-01-11",
            card_holder     = 123,
            total_cost      = 123456  
        )
        
        reservation = Reservation.objects.create(
            id           = 1,
            user         = user,
            home         = home,
            status_id    = 2,
            payment      = payment,
        )
        
        request_login = {
            "email"    : "sj950902@naver.com",
            "password" : "a123456789"
        }

        response_login  = self.client.post('/users/signin',request_login,content_type="application/json")
        self.token      = response_login.json()["AUTHORIZATION"]
        
        payment2 = Payment.objects.create(
            method_id       = 1,
            card_number     = 123456789,
            expire_date     = "2021-10-20",
            post_code       = "123456789",
            payment_date    = "2021-01-11",
            card_holder     = 123,
            total_cost      = 123456  
        )
        reservation2 = Reservation.objects.create(
            id           = 2,
            user         = user,
            home         = home,
            status_id    = 2,
            payment      = payment2
        )

        review = Review.objects.create(
            id          = 2,
            user        = user,
            home        = home,
            reservation = reservation2,
            rating      = 3
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
        Payment.objects.all().delete()
        Reservation.objects.all().delete()
    
    def test_ReviewView_post_success(self):
        headers = {"HTTP_AUTHORIZATION":self.token}
        data = {
            "content" : "hi",
            "rating"  : 5
        }
        response = self.client.post("/reservations/1",data,content_type="application/json",**headers)
        print(response.status_code)
        self.assertEqual(response.status_code,200)

    def test_ReviewView_post_fail(self):
        headers = {"HTTP_AUTHORIZATION":self.token}
        data = {
            "content" : "hi",
            "rating"  : 5
        }
        response = self.client.post("/reservations/3",data,content_type="application/json",**headers)
        self.assertEqual(response.status_code,404)

    def test_ReviewView_post_fail_with_expired_token(self):
        
        payload = {"id":1,"exp":datetime.datetime.now()-datetime.timedelta(100)}
        headers = {"HTTP_AUTHORIZATION" : jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)}
        data = {
            "content" : "helloworld",
            "rating"  : 3
        }
        response = self.client.post("/reservations/1",data,content_type="application/json",**headers)
        self.assertEqual(response.status_code,401)
        self.assertEqual(response.json(),
                         {
                            "message" : "EXPIRED_TOKEN"
                         })

    def test_ReviewVIew_delete_success(self):
        headers = {"HTTP_AUTHORIZATION":self.token}
        response = self.client.delete("/reservations/2",**headers)
        self.assertEqual(response.status_code,200)    

    def test_ReviewView_delete_fail_without_token(self):
        response = self.client.delete("/reservations/4")
        self.assertEqual(response.status_code,401)

    def test_ReviewView_delte_fail_without_review(self):
        headers = {"HTTP_AUTHORIZATION":self.token}
        self.client.delete("/reservations/2",**headers)
        response = self.client.delete("/reservations/2",**headers)
        self.assertEqual(response.status_code,404)    


