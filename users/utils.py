import jwt
import json
import re
from users.models import User
from my_settings  import SECRET_KEY,JWT_ALGORITHM
from django.http  import JsonResponse

def ConfirmLogin(original_function):
    def wrapper(self, request, *args, **kwargs):
        token = request.headers.get("Authorization", None)
        try:
            if token:
                token_payload = jwt.decode(token, SECRET_KEY, algorithms=JWT_ALGORITHM)
                user          = User.objects.get(id=token_payload['id'])
                request.user  = user.id
                return original_function(self, request, *args, **kwargs)
            return JsonResponse({'message':'NEED_LOGIN'}, status=401)
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message':'EXPIRED_TOKEN'}, status=401)
        except jwt.DecodeError:
            return JsonResponse({'message':'INVALID_DATA'}, status=401)
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=401)
    return wrapper

def CheckUser(original_function):
    def wrapper(self, request, *args, **kwargs):
        token = request.headers.get("Authorization", None)
        try:
            if token:
                token_payload = jwt.decode(token, SECRET_KEY, algorithms=JWT_ALGORITHM)
                user          = User.objects.get(id=token_payload['id'])
                request.user  = user
                return original_function(self, request, *args, **kwargs)
            request.user = None
            return original_function(self, request, *args, **kwargs)
        except jwt.DecodeError:
            return JsonResponse({'message':'INVALID_DATA'}, status=401)
    return wrapper
