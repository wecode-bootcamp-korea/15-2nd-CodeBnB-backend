from django.urls    import path
from users.views    import SignUpView, LogInView, KakaoSignInView

urlpatterns = [
        path('/signup', SignUpView.as_view()),
        path('/signin', LogInView.as_view()),
        path('/kakaologin', KakaoSignInView.as_view())
]


