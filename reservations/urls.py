from django.urls import path
from .views      import (ReservationView,
                        ReservationDetailView
                                            )
#from homes.views import ReviewView

urlpatterns = [
    path('', ReservationView.as_view()),
    path('/<int:reservation_pk>', ReservationDetailView.as_view()),
    #path('/<int:reservation_pk>/review', ReviewView.as_view()) 승재님 리뷰 기능 url
]

 
