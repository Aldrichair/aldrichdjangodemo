from django.urls import path
from apps.users.views import UsernameCountView, RegisterView, MobileCountView

urlpatterns = [
    path('usernames/<username:username>/count/', UsernameCountView.as_view()),
    path('register/', RegisterView.as_view()),
    path('mobiles/<mobile:mobile>/count/', MobileCountView.as_view())
]
