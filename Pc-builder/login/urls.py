from django.urls import path
from . import views

app_name = 'login'

urlpatterns = [
    path('registration/', views.RegistrationFormView.as_view(), name='registration'),
    path('login/', views.SignInFormView.as_view(), name='login'),
    path('logout/', views.LogoutFormView.as_view(), name='logout')
]