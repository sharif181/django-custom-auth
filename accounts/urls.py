from django.urls import path
from accounts.views import profile, LoginView, RegistrationView

urlpatterns = [
    path('profile', profile),
    path('login/', LoginView.as_view()),
    path('signup/', RegistrationView.as_view()),
]
