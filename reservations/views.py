import json, jwt, bcrypt

from django.views import View
from django.http import JsonResponse
from django.db.models import Q
from django.db import transaction

from users.utils import ConfirmLogin, CheckUser
from codebnb.settings import SECRET_KEY
from users.models  import User
from reservations.models import (
    Reservation,
    Payment,
    PaymentMethod,
    ReservationGuest,
    Status,
    Guest
    )
from homes.models import Rule

class ReservationView(View):

    @ConfirmLogin
    def post(self, request):

        try:
            data = json.loads(request.body)

            user           = request.user
            adult_count    = data['adult']
            children_count = data['children']
            infant_count   = data['infant']

            hash_card_number  = jwt.encode({"card_number" : data['card_number']}, "SECRET_KEY", algorithm='HS256')
            hash_expire_date  = jwt.encode({"expire_date" : data['expire_date']}, "SECRET_KEY", algorithm='HS256')
            hash_post_code    = jwt.encode({"post_code" : data['post_code']}, "SECRET_KEY", algorithm='HS256')
            hash_payment_date = jwt.encode({"payment_date" : data['payment_date']}, "SECRET_KEY", algorithm='HS256')
            hash_card_holder  = jwt.encode({"card_holder" : data['card_holder']}, "SECRET_KEY", algorithm='HS256')
           
            with transaction.atomic():
                payment = Payment.objects.create( 
                    method       = PaymentMethod.objects.get(name="신용카드 또는 체크카드"),
                    card_number  = hash_card_number,
                    expire_date  = hash_expire_date,
                    post_code    = hash_post_code,
                    payment_date = hash_payment_date,
                    card_holder  = hash_card_holder,
                    total_cost   = data['total_cost']
                )
                
                reservation = Reservation.objects.create(
                    user_id   = user,
                    home_id   = data['home_id'],
                    check_in  = data['check_in'],
                    check_out = data['check_out'],
                    status    = Status.objects.get(name='결제완료'),
                    payment   = payment
                )
                
                ReservationGuest.objects.create(
                    guest        = Guest.objects.get(name='성인'),
                    reservations = reservation,
                    count        = adult_count
                )

                ReservationGuest.objects.create(
                    guest        = Guest.objects.get(name='어린이'),
                    reservations = reservation,
                    count        = children_count
                )
                
                ReservationGuest.objects.create(
                    guest        = Guest.objects.get(name='유아'),
                    reservations = reservation,
                    count        = infant_count
                )

            return JsonResponse({"MESSAGE":"SUCCESS"}, status=200)

        except KeyError:
            return JsonResponse({"MESSAGE": "KEYERROR"}, status=400)
            
    @ConfirmLogin        
    def get(self, request):

            user   = request.user
            status = request.GET.get("status","upcomming")
            limit  = int(request.GET.get("limit",10))
            offset = int(request.GET.get("offset",0))
            
            reservations = Reservation.objects.select_related(
                'status',
                ).prefetch_related(
                "home__images", 
                "home__home_host",
                "user",
                "home__home_host__user"
                ).filter(user_id=user)
            
            if status == "upcoming":                                      
                reservations = reservations.filter(status__name="결제완료") 
            if status == "past":                                           
                reservations = reservations.filter(status__name="이용완료")
            if status == "cancel":
                reservations = reservations.filter(status__name="예약취소")
            
            if not reservations:                                            
                return JsonResponse({"MESSAGE":"RESERVATION_NOT_FOUND"},status=404)
                
            context = [{                                                                
                'resrvation_id': reservation.id,   
                'home_id'      : reservation.home.id,                                           
                'status'       : reservation.status.name,
                'address'      : reservation.home.address,
                'start_date'   : reservation.check_in,
                'end_date'     : reservation.check_out,
                'home_image'   : [image.url for image in reservation.home.images.all()],
                'host'         : [{
                    "host_name" : host.user.last_name + host.user.first_name,
                    "host_profile_image" : host.user.profile_image} for host in reservation.home.home_host.all()]
                } for reservation in reservations[offset:offset+limit]]
                        
            return JsonResponse({'RESERVATIONS_LIST':context}, status=200)

class ReservationDetailView(View):

    @ConfirmLogin
    def get(self, request, reservation_pk):

        try :
            reservation = Reservation.objects.prefetch_related(
            "home",
            "home__homerule_set",
            "home__homerule_set__rule",         
            "home__images",
            "home__home_host"
            ).get(id=reservation_pk)
            
            Host = reservation.home.home_host.first() 

            context = {
                "reservation_id"    : reservation.id,           
                "home_id"           : reservation.home.id,      
                "start_date"        : reservation.check_in.date(),  
                "end_date"          : reservation.check_out.date(), 
                "host_name"         : Host.user.last_name + Host.user.first_name, 
                "host_profile_image": Host.user.profile_image, 
                "home_photo"        : [image.url for image in reservation.home.images.all()],
                "home_name"         : reservation.home.name, 
                "home_address"      : reservation.home.address, 
                "latitude"          : reservation.home.latitude, 
                "longitude"         : reservation.home.longitude, 
                "guest_number"      : sum([guest.count for guest in reservation.reservationguest_set.all()]),
                "room_type"         : reservation.home.home_type.name
                }

            for rule in reservation.home.homerule_set.all():
                if rule.rule.name == "체크인 시간":
                    context["check_in"] = rule.check_in
                elif rule.rule.name == "체크아웃 시간":
                    context["check_out"] = rule.check_out
            return JsonResponse({"data" : context}, status=200)

        except Reservation.DoesNotExist:
            return JsonResponse({"MESSAGE":"RESERVATION_NOT_FOUND"},status=404)

    @ConfirmLogin
    def delete(self, request, reservation_pk):
        
        try:
            reservation = Reservation.objects.get(id = reservation_pk)
            
            if not reservation.status.name in ["결제완료","예약요청"]:
                return JsonResponse({"MESSAGE":"Reservation_CANT_CANTCANCEL"})
            
            reservation.status = Status.objects.get(name="예약취소")
            reservation.save()
            
            return JsonResponse({"MESSAGE":"Reservation_CANCELLED"},status=200)

        except Reservation.DoesNotExist:
            return JsonResponse({"MESSAGE":"RESERVATION_NOT_FOUND"},status=404)
