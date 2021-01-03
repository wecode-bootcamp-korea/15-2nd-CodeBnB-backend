import json

from django.http        import JsonResponse
from django.views       import View

from django.db.models   import Avg
from homes.models       import Home
from users.models       import User
from bookmarks.models   import BookMark 
from users.utils        import ConfirmLogin

class BookmarkView(View):
    @ConfirmLogin
    def post(self, request, home_pk):
        try:
            user = User.objects.get(id=request.user)
            home = Home.objects.get(id=home_pk)
            if not home_pk in user.bookmarks.values_list("id",flat=True):
                user.bookmarks.add(home)
                return JsonResponse({"MESSAGE":"SUCCESS"},status=201)
            else:
                return JsonResponse({"MESSAGE":"ALREADY_BOOKED"},status=400)
        except User.DoesNotExist:
            return JsonResponse({"MESSAGE":"USER_NOT_FOUND"},status=404)
        except Home.DoesNotExist:
            return JsonResponse({"MESSAGE":"HOME_NOT_FOUND"},status=404)

    @ConfirmLogin
    def delete(self, request, home_pk):
        try:
            home = Home.objects.get(id=home_pk)
            bookmark = BookMark.objects.get(home=home,user_id=request.user).delete()
            return JsonResponse({"MESSAGE":"DELETE_SUCCESSFULLY"},status=200)
        except User.DoesNotExist:
            return JsonResponse({"MESSAGE":"USER_NOT_FOUND"},status=404)
        except BookMark.DoesNotExist:
            return JsonResponse({"MESSAGE":"BOOKMARK_NOT_FOUND"},status=404)
        except Home.DoesNotExist:
            return JsonResponse({"MESSAGE":"HOME_NOT_FOUND"},status=404)

class BookmarkListView(View):
    @ConfirmLogin
    def get(self, request):
        PRICE_CATEGORY_NAME = '1박비용'
        offset = int(request.GET.get("offset",0))
        limit  = int(request.GET.get("limit",15))
        bookmarks = Home.objects.filter(bookmark__user=request.user).prefetch_related(
                "homeopiton_set",
                "homeopiton_set__option",
                "images",
                "review_set",
                "homeprice_set",
                "homeprice_set__price_category"
            ).select_related("home_type").all()
        
        bookmark_list   = {
            "bookmarks_count" : bookmarks.count(),
            "bookmarks" : [{
            "id"                : home.id,
            "name"              : home.name,
            "address"           : home.address,
            "home_type"         : home.home_type.name,
            "latitude"          : home.latitude,
            "longitude"         : home.longitude,
            "home_images"       : [image.url for image in home.images.all()],
            "home_options"       : [{
                    "option_name"  : option.option.name,
                    "option_count" : option.count
                } for option in home.homeopiton_set.all()],
            "price_of_1day" : [
                {
                    "category" : home_price.price_category.name,
                    "cost"     : home_price.cost
                    }for home_price in home.homeprice_set.all() if home_price.price_category.name==PRICE_CATEGORY_NAME],
            "rating"        : round(home.review_set.aggregate(avg_rating=Avg("rating"))["avg_rating"],2) if home.review_set.exists() else 0,
            "review_count"  : home.review_set.count()
            } for home in bookmarks[offset:offset+limit]]}
         
        if not bookmark_list["bookmarks"]:
            return JsonResponse({"MESSAGE":"BOOKMARK_NOT_FOUND"},status=404)
    
        return JsonResponse(bookmark_list,status=200)
