from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from customer.models import User,Chicken
from rest_framework.authtoken.models import Token
from random import randint
from django.conf import settings
from twilio.rest import Client
from customer.serializers import *

# Create your views here.


class VerifyPhoneNumberView(APIView):
    def verify(self,number,otp):
        print(number)
        if User.objects.filter(mobile_no=number).exists():
            u = User.objects.get(mobile_no=number)
            if u.otp == otp:
                u.verified = True
                u.save()
                if Token.objects.filter(user=u).exists():
                    token = Token.objects.filter(user=u)[0]
                else:
                    token = Token.objects.create(user=u)
                return token
            else:
                return False
        return False

    def post(self,request):
        number = request.data.get('mobile_no')
        otp = request.data.get('otp')
        token = self.verify(number,otp)
        if token:
            return Response({'errorExists':False,'token':token.key},status=status.HTTP_200_OK)
        return Response({'errorExists':True},status=status.HTTP_400_BAD_REQUEST)


class MobileRegisterLoginView(APIView):

    def post(self,request):
        number = request.data.get('mobile_no',None)
        if number:
            u,created = User.objects.get_or_create(mobile_no=number,username='random')
            otp = str(randint(111111, 999999))
            u.otp = otp
            u.save()
            account_sid = settings.SID
            auth_token = settings.AUTH_TOKEN
            client = Client(account_sid, auth_token)
            message = client.messages.create(

                body=f'Given otp is {otp}',
                from_=settings.PHONE_NUMBER,
                to='+918237544102'
            )
            print(message.sid)
            return Response({'errorExists':False},status=status.HTTP_201_CREATED)
        return Response({'errorExists':True},status=status.HTTP_400_BAD_REQUEST)

class ResendOtpView(APIView):
    def post(self,request):
        number = request.data.get('mobile_no',None)
        if number:
            if User.objects.filter(mobile_no=number).exists():
                otp = User.objects.filter(mobile_no=number)[0].otp
                account_sid = settings.SID
                auth_token = settings.AUTH_TOKEN
                client = Client(account_sid, auth_token)
                message = client.messages.create(

                    body=f'Given otp is {otp}',
                    from_=settings.PHONE_NUMBER,
                    to='+918237544102'
                )
                print(message.sid)
                return Response({'errorExists': False}, status=status.HTTP_201_CREATED)
            return Response({'errorExists': True},status=status.HTTP_404_NOT_FOUND)
        return Response({'errorExists': True}, status=status.HTTP_400_BAD_REQUEST)

class ChickenList(APIView):

    def get(self,request):
        serializer = ChickenSerializer(Chicken.objects.all(),many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

