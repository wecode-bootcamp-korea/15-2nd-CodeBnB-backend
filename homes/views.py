import json
import math
import datetime

from django.http         import JsonResponse, HttpResponse
from django.views        import View
from django.db.models    import Q, Avg

from homes.models        import Home,Review
from reservations.models import Reservation
from users.utils         import CheckUser, ConfirmLogin

class HomeListView(View):
    @CheckUser
    def get(self,request):
        query          = Q()
        limit          = int(request.GET.get("limit",15))
        offset         = int(request.GET.get("offset",0))
        home_types     = [int(home_type) for home_type in request.GET.getlist("room_types")]
        building_types = [int(building_type) for building_type in request.GET.getlist("property_type_id")]
        facilities     = [int(facility) for facility in request.GET.getlist("amenities")]
        adult          = int(request.GET.get("adult",0))
        child          = int(request.GET.get("child",0))
        baby           = int(request.GET.get("infant",0))
        regions        = [int(region) for region in request.GET.getlist("neighborhood_id")]
        minprices      = int(request.GET.get("price_min",1000))
        maxprices      = int(request.GET.get("price_max",1000000))
        minbedroom     = int(request.GET.get("min_bedrooms",0))
        minbathroom    = int(request.GET.get("min_bathrooms",0))
        minbed         = int(request.GET.get("min_beds",0))
        start_date     = request.GET.get("startdate")
        end_date       = request.GET.get("enddate") 

        homes = Home.objects.all()
        
        filter_set_MTO = {
            "home_type__in"     : home_types,
            "building_type__in" : building_types,
            "region__in"        : regions
        }

        for key in filter_set_MTO:
            if filter_set_MTO[key]:
                homes = homes.filter(**{f'{key}':filter_set_MTO[key]})
        
        for facility in facilities:
            homes = homes.filter(facility=facility)   
        
        if minbed:
            homes  = homes.filter(homeopiton__count__gte=minbed,
                                  homeopiton__option__name="침대")
        if minbathroom:
            homes  = homes.filter(homeopiton__count__gte=minbathroom,
                                  homeopiton__option__name="욕실") 
        if minbedroom:
            homes  = homes.filter(homeopiton__count__gte=minbedroom,
                                  homeopiton__option__name="침실")       
        
        query &= Q(Q(homeprice__cost__range=(minprices,maxprices))&Q(homeprice__price_category__name="1박비용"))
        query &= Q(capacity_guest__gte=adult+child)

        if start_date and end_date:
            query &= ~Q(Q(reservation__check_in__range=(start_date,end_date))
                        |Q(reservation__check_out__range=(start_date,end_date)))
            
        homes = homes.filter(query).prefetch_related(
            "images",
            "option",
            "homeopiton_set",
            "facility",
            "homefacility_set",
            "price",
            "homeprice_set",
            "reservation_set",
            "review_set",
            "bookmark_set"
        ).select_related('building_type','home_type',"region").distinct()
        
        if not homes.exists():
            return JsonResponse({"MESSAGE":"HOME_NOT_FOUND"},status=404)
        
        data = {
            "homes_count"    : homes.count(),
            "avg_price"      : 0,
            "homes"          : [{
                "home_id"           : home.id,
                "home_name"         : home.name,
                "home_capacity"     : home.capacity_guest,
                "home_type"         : home.home_type.name,
                "home_building"     : home.building_type.name,
                "avg_rating"        : round(home.review_set.aggregate(rating_avg=Avg("rating"))["rating_avg"],1) if home.review_set.exists() else 0,
                "review_count"      : home.review_set.count(),
                "home_images"       : [image.url for image in home.images.all()],
                "home_options"      : {
                    option.name : home_option.count for (option,home_option) in zip(home.option.all(),home.homeopiton_set.all())
                },
                "home_facilities"   : [facility.name for facility in home.facility.all()],
                "home_latitude"     : home.latitude,
                "home_longitutde"   : home.longitude,
                "price"             : {
                    price.name : homeprice.cost for (price,homeprice) in zip(home.price.all(),home.homeprice_set.all())
                },
                "home_region"       : {
                    "region_name"       : home.region.name,
                    "region_latitude"   : home.region.latitude,
                    "region_longtitude" : home.region.longitude,
                    "region_radius_m"   : home.region.around_radius_m,
                    "region_zoom"       : home.region.zoom_level
                },
                "bookmark" : int(home.bookmark_set.filter(user_id=request.user).exists()) if request.user else 0
            } for home in homes[offset:offset+limit]]

        }
        
        if not len(data["homes"]): 
            return JsonResponse({"MESSAGE":"HOME_NOT_FOUND"},status=404)    
        
        for home in data["homes"]:   
            data["avg_price"] += home["price"]["1박비용"]
        
        data["avg_price"] /= len(data["homes"])     
        return JsonResponse(data,status=200)

class HomeDetailView(View):
    @CheckUser
    def get(self, request, home_pk):
        try : 
            home = Home.objects.prefetch_related(
                "home_host",
                "home_host__user",
                "homefacility_set",
                "facility",
                "facility__facility_type",
                "homeopiton_set",
                "option",
                "homerule_set",
                "homerule_set__rule",
                "homerule_set__rule__rule_type",
                "images",
                "reservation_set",
                "review_set__user",
                "bookmark_set"
            ).select_related("home_type","building_type","region").get(id=home_pk)

            host = home.home_host.first()
            
            data = {
                "home_id"          : home.id,
                "name"             : home.name,
                "capacity"         : home.capacity_guest,
                "home_type"        : home.home_type.name,
                "home_building"    : home.building_type.name,
                "address"          : home.address,
                "host"             : {
                    "first_name"   : host.user.first_name,
                    "last_name"    : host.user.last_name,
                    "contact"      : host.contact,
                    "description"  : host.description,
                    "singup_date"  : host.commission_date,
                    "host_profile" : host.user.profile_image,
                    "is_valid"     : host.is_valid == True
                    },
                "images"            : [image.url for image in home.images.all()],
                "description"       : home.description,
                "facilities_list"   : [{
                    "name" : facility.name,
                    "url"  : facility.icon_url
                    } for facility in home.facility.all()],
                "facilities_detail" : [],
                "rules"             : [],
                "check_in"          : None,
                "check_out"         : None,
                "options"           : {
                    option.name : home_option.count for (option,home_option) in zip(home.option.all(),home.homeopiton_set.all())
                    },
                "home_latitude"     : home.latitude,
                "home_longitutde"   : home.longitude,
                "price" : {
                    price.name : homeprice.cost for (price,homeprice) in zip(home.price.all(),home.homeprice_set.all())
                    },
                "home_region"           : {
                    "region_name"       : home.region.name,
                    "region_latitude"   : home.region.latitude,
                    "region_longtitude" : home.region.longitude,
                    "region_radius_m"   : home.region.around_radius_m,
                    "region_zoom"       : home.region.zoom_level
                },
                "room_info" : [
                    {
                        "room_name" : room.name,
                        "bed_info"  : [{
                            "bed_name" : bed.bed.name,
                            "count"    : bed.count
                        } for bed in room.roombed_set.all()]

                    } for room in home.rooms.all()],
                "reservations" : list(home.reservation_set.values("check_in","check_out")),
                "avg_rating"   : round(home.review_set.aggregate(rating_avg=Avg("rating"))["rating_avg"],2) if home.review_set.exists() else 0,
                "review_count" : home.review_set.count(),
                "reviews"      : [{
                    "reviewer"   : review.user.last_name,
                    "content"    : review.contents,
                    "rating"     : review.rating,
                    "created_at" : review.created_at.date()
                } for review in home.review_set.all()],
                "bookmark"  : int(home.bookmark_set.filter(user_id=request.user).exists()) if request.user else 0
            }
            
            facility_detail = {}
            for facility in home.facility.all():
                if not facility.facility_type.name in facility_detail.keys():
                    facility_detail[facility.facility_type.name] = []
                facility_detail[facility.facility_type.name].append(facility.name)

            for key in facility_detail.keys():
                data["facilities_detail"].append({"category":key,"facility_list":facility_detail[key]})

            rule_list = {}
            for rule in home.homerule_set.all():
                if rule.rule.name == "체크인 시간":
                    data["check_in"] = rule.check_in
                elif rule.rule.name == "체크아웃 시간":
                    data['check_out'] = rule.check_out
                else:
                    if not rule.rule.rule_type.name in rule_list:
                        rule_list[rule.rule.rule_type.name] = []
                    rule_list[rule.rule.rule_type.name].append(rule.rule.name)

            for key in rule_list.keys():
                data["rules"].append({"category":key,"rule_list":rule_list[key]})

            return JsonResponse(data,status=200)
        
        except Home.DoesNotExist:
            return JsonResponse({"MESSAGE":"HOME_NOT_FOUND"},status=404)

class ReviewView(View):
    @ConfirmLogin
    def post(self,request,reservation_pk):
        try: 
            data    = json.loads(request.body)
            rating  = int(data["rating"])
            content = data["content"]

            if Review.objects.filter(user_id=request.user,reservation_id=reservation_pk).exists():
                return JsonResponse({'MESSAGE':'REVIEW_ALREADY_WRITTEN'}, status=400)
            
            used_reservation = Reservation.objects.select_related("home").get(id=reservation_pk)

            review       = Review.objects.create(
                reservation_id = reservation_pk,
                user_id        = request.user,
                home           = used_reservation.home,
                contents       = content,
                rating         = rating
            )
            return HttpResponse(status=200)

        except json.JSONDecodeError:
            return JsonResponse({"MESSAGE","INVALID_DATA"},status=400)
        except Reservation.DoesNotExist:
            return JsonResponse({"MESSAGE":"RESERVATION_NOT_FOUND"},status=404)
        except KeyError as e:
            return JsonResponse({"MESSAGE":"KEY_ERROR"},status=400)
    
    @ConfirmLogin
    def delete(self,request,reservation_pk):
        
        if not Review.objects.filter(user_id=request.user,reservation_id=reservation_pk).exists():
            return JsonResponse({"MESSAGE":'REVIEW_NOT_FOUND'},status=404)
            
        review = Review.objects.get(user_id=request.user,reservation_id=reservation_pk)
        review.delete()   
        return HttpResponse(status=200)

