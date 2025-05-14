
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from user.models import User
from django.db import transaction
from utils.constants.choices import Roles
from rest_framework.response import Response
from rest_framework import status

class UserLoginView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request):
        response_data = {}
        try:
           
            # Get username and password from request data
            username = request.data.get("username")
            password = request.data.get("password")

            # Validate presence of username and password
            if not username and not password:
                response_data = {
                    "message": "Username and password are required.",
                    "status": False
                }
                return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            with transaction.atomic():
            # Authenticate the user
                user = User.objects.user_authentication(username)
            if not user:
                response_data = {
                    "message": "Invalid Email address",
                    "status": False
                }
                return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)

            # Verify password
            if not user.check_password(password):
                response_data = {
                    "message": "Invalid password.",
                    "status": False
                }
                return Response(response_data, status=status.HTTP_401_UNAUTHORIZED)

            # Handle deactivated user case
            if not user.is_active:
                response_data = {
                    "message": "You have been deactivated by super admin.",
                    "status": False
                }
                return Response(response_data, status=status.HTTP_403_FORBIDDEN)

            # Handle active user and generate JWT tokens
            refresh = RefreshToken.for_user(user)
            role = Roles[user.role]
            group_names = list(user.groups.values_list('name', flat=True))
            response_data = {
                "message": "Login successfully.",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "status": True,
                "userdata": {
                    "role": role.value,
                    "is_active": user.is_active,
                    "name": user.name,
                    "email": user.email,
                    "groups": group_names
                }
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            response_data = {
                "message": str(e),
                "status": False
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
