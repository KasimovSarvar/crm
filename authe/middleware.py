from    rest_framework.exceptions import AuthenticationFailed
from .models import User


class SuperUserMiddleware:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_model = User

    def get_user(self, validated_token):
        user_id = validated_token.get('user_id')
        user = User.objects.filter(id=user_id).first()
        if not user:
            raise AuthenticationFailed('User not found')
        if user.role == 1:
            raise AuthenticationFailed('Super user can  only admin panel ')
        return user