from django.urls import path
from homes.views import HomeListView,HomeDetailView

urlpatterns = [
    path('',HomeListView.as_view()),
    path('/<int:home_pk>',HomeDetailView.as_view()),
]

