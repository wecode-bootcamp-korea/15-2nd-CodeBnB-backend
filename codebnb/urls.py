from django.urls import path,include

urlpatterns = [
    path('users', include('users.urls')),
    path('bookmarks', include('bookmarks.urls')),
    path("reservations",include("reservations.urls")),
    path('homes',include('homes.urls'))
]
