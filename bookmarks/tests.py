import json, bcrypt, jwt, datetime

from django.test        import TestCase, Client
from users.models       import User,Host
from bookmarks.models   import BookMark
from homes.models       import (
    Home,
    HomeType, 
    BuildingType,Region
)

from my_settings        import JWT_ALGORITHM, SECRET_KEY

class BookmarkViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        user = User.objects.create(
            id           = 1,
            last_name    = "김",
            first_name   = "승재",
            email        = 'sj950902@naver.com',
            password     =  bcrypt.hashpw("a123456789".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            birthday     = '1592-01-11',
            profile_image= "abcd.jpg",
            mailing_check= 1
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
        home2 = Home.objects.create(
            id               = 2,
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
        BookMark.objects.create(
            id   = 2,
            home = home2,
            user = user

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
        BookMark.objects.all().delete()

    def test_BookmarkView_post_success(self):
        headers = {"HTTP_Authorization" : self.token}
        response = self.client.post('/bookmarks/1',content_type="application/json",**headers)
        self.assertEqual(response.status_code, 201)
    
    def test_BookmarkView_post_fail_without_token(self):
        response = self.client.post('/bookmarks/1',content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),{
            "message" : "NEED_LOGIN"
        })
    def test_BookmarkView_post_fail_with_expired_token(self):
        payload = {"id":1,"exp":datetime.datetime.now()-datetime.timedelta(1000)}
        headers = {"HTTP_AUTHORIZATION" : jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)}
        response = self.client.post('/bookmarks/1',content_type="application/json",**headers)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),{
            "message" : "EXPIRED_TOKEN"
        })
    
    def test_BookmarkView_post_fail_existing(self):
        headers = {"HTTP_Authorization" : self.token}
        response = self.client.post('/bookmarks/2',content_type="application/json",**headers)
        self.assertEqual(response.status_code, 400)

    def test_BookmarkView_delete_success(self):
        headers = {"HTTP_Authorization" : self.token}
        response = self.client.delete('/bookmarks/2',content_type="application/json",**headers)
        self.assertEqual(response.status_code, 200)
    
    def test_BookmarkView_delete_fail_not_found(self):
        headers = {"HTTP_Authorization" : self.token}
        response = self.client.delete('/bookmarks/3',content_type="application/json",**headers)
        self.assertEqual(response.status_code, 404)


class BookmarkListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        user = User.objects.create(
            id           = 1,
            last_name    = "김",
            first_name   = "승재",
            email        = 'sj950902@naver.com',
            password     =  bcrypt.hashpw("a123456789".encode('utf-8'), bcrypt.gensalt()).decode('utf-8'),
            birthday     = '1592-01-11',
            profile_image= "abcd.jpg",
            mailing_check= 1
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
        home2 = Home.objects.create(
            id               = 2,
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
        BookMark.objects.create(
            id   = 2,
            home = home2,
            user = user

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
        BookMark.objects.all().delete()
    
    def test_bookmarklist_get_success(self):
        headers = {"HTTP_Authorization" : self.token}
        response = self.client.get('/bookmarks',content_type="application/json",**headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["bookmarks"][0]["id"], 2)

    def test_bookmarklist_fail_not_found(self):
        headers = {"HTTP_Authorization" : self.token}
        response = self.client.get('/bookmarks?offset=100',content_type="application/json",**headers)
        self.assertEqual(response.status_code, 404)

    def test_bookmarklist_fail_without_token(self):
        response = self.client.get('/bookmarks',content_type="application/json")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),{
            "message" : "NEED_LOGIN"
        })

    def test_bookmarklist_fail_with_expired_token(self):
        payload = {"id":1,"exp":datetime.datetime.now()-datetime.timedelta(1000)}
        headers = {"HTTP_AUTHORIZATION" : jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)}
        response = self.client.get('/bookmarks',content_type="application/json",**headers)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(),{
            "message" : "EXPIRED_TOKEN"
        })        
