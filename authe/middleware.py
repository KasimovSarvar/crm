from rest_framework.response import Response
from .models import User
from rest_framework.exceptions import AuthenticationFailed

class SuperUserMiddle:
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.model = User

    def control(self,request,response,validated_token):
        user_id = validated_token.get('user_id')
        user_model = User.objects.filter(id=user_id).first()
        if not user_model:
            raise AuthenticationFailed('User not found')
        if user_model.role != 1:
            raise AuthenticationFailed('Super user only admin panel create')


        return response



