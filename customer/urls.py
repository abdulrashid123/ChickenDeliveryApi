from django.urls import path
from customer.views import *
urlpatterns = [
    path('verify-phone/',VerifyPhoneNumberView.as_view()),
    path('add-phone/',MobileRegisterLoginView.as_view()),
    path('resend-otp/',ResendOtpView.as_view()),
    path('chicken-list/',ChickenList.as_view())
]