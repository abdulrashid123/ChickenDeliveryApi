from rest_framework.serializers import ModelSerializer
from customer.models import User,Chicken,Company


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'

class ChickenSerializer(ModelSerializer):
    class Meta:
        model = Chicken
        fields = '__all__'
        depth=1
