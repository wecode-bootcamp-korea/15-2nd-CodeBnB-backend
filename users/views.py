import json
import re
import bcrypt
import jwt
import requests
from   datetime             import date

from django.http            import JsonResponse,HttpResponse
from django.views           import View

from my_settings            import SECRET_KEY, JWT_ALGORITHM
from users.models           import User

class SignUpView(View):
    def post(self, request):
        REGEX_EMAIL     = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        REGEX_PASSWORD  = '^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{6,}$'

        try:
            data                = json.loads(request.body)
            hashed_password     = bcrypt.hashpw(data["password"].encode("utf-8"), bcrypt.gensalt())
            crypted_password    = hashed_password.decode("utf-8")
            birth              = date(int(data["birthdayYear"]), int(data["birthdayMonth"]), int(data["birthdayDate"]))

            if not (data["first_name"] and data["last_name"]):
                return JsonResponse({"MESSAGE" : "INVALID_NAME"}, status=400)
            
            if not re.match(REGEX_EMAIL, data["email"]):
                return JsonResponse({"MESSAGE" : "INVALID_EMAIL"}, status=400)

            if not re.match(REGEX_PASSWORD, data["password"]):
                return JsonResponse({"MESSAGE" : "INVALID_PASSWORD"}, status=400)

            if User.objects.filter(email=data["email"]).exists():
                return JsonResponse({"MESSAGE" : "ALREADY_EXISTS"}, status=401)
            
            new_user = User.objects.create(
                    first_name      = data["first_name"],
                    last_name       = data["last_name"],
                    email           = data["email"],
                    password        = crypted_password,
                    birthday        = birth.isoformat(),
                    )
            
            if data["mailing_check"]:
                new_user.mailing_check = 1
                new_user.save()

            return JsonResponse({"MESSAGE" : "SUCCESS"}, status=201)              

        except KeyError:
            return JsonResponse({"MESSAGE" : "KEY_ERROR"}, status=400)
        except json.decoder.JSONDecodeError:
            return JsonResponse({"MESSAGE" : "INVALID_DATA"}, status=400)

class LogInView(View):
    def post(self, request):
        try:
            data    = json.loads(request.body)

            if User.objects.filter(email=data['email']).exists():
                user = User.objects.get(email=data['email'])
                if bcrypt.checkpw(data["password"].encode("utf-8"), user.password.encode("utf-8")) == True:
                    return JsonResponse({"MESSAGE" : "SUCCESS", "AUTHORIZATION" : jwt.encode({"id" : user.id},
                        SECRET_KEY, JWT_ALGORITHM).decode(), "email":data['email'], "profile":user.profile_image}, status=200)
                return JsonResponse({"MESSAGE" : "INVALID_PASSWORD"}, status=401)
            return JsonResponse({"MESSAGE" : "INVALID_USER"}, status=401)

        except KeyError:
            return JsonResponse({"MESSAGE" : "INVALID_KEY"}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({"MESSAGE" : "INVALID_DATA"}, status=400)

class KakaoSignInView(View):
    def post(self, request):
        try:
            data            = json.loads(request.body)
            access_token    = json.loads(request.body.decode("utf-8")).get("Authorization")
            headers         = {"Authorization":f"Bearer {access_token}"}
            kakao_response  = requests.get("https://kapi.kakao.com/v2/user/me", headers=headers)
            kakao_user      = kakao_response.json()
            email           = kakao_user["kakao_account"]["email"]
            name            = kakao_user["kakao_account"]["profile"]["nickname"]
           
            if User.objects.filter(email = email).exists():
                user            = User.objects.get(email = email)
                access_token    = jwt.encode({'id' : user.id}, SECRET_KEY, JWT_ALGORITHM).decode("utf-8")

                return JsonResponse({"MESSAGE" : "SUCCESS", 
                    "AUTHORIZATION" : access_token,"profile" : user.profile_image,"email" : email},status=200)

            birth = date(int(data["birthdayYear"]), int(data["birthdayMonth"]), int(data["birthdayDate"]))

            user = User.objects.create(
                    first_name      = name[1:],
                    last_name       = name[0],
                    email           = email,
                    birthday        = birth.isoformat(),
                    )
            return JsonResponse({"MESSAGE" : "SUCCESS", 
                "AUTHORIZATION" : access_token,"profile" : user.profile_image,"email" : email},status=200)

        except KeyError as e:
            return JsonResponse({"MESSAGE" : f"{e}"},status=400)

        except json.JSONDecodeError:
            return JsonResponse({"MESSAGE" : "INVALID_DATA"},status=400) 

