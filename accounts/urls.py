from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    path("user_info/", views.UserGetView.as_view()),
    path("user_info_post/", views.UserPostView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("example_view/", views.ExampleView.as_view()),
    path("user_login/", views.UserLoginView.as_view()),
    path("user_logout/", views.UserLogoutView.as_view())
]
