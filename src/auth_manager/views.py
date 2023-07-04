from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings

from .serializers import RegisterUserSerializer, UpdateUserSerializer
from .utils import custom_payload_handler

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class CreateUserView(mixins.CreateModelMixin, GenericViewSet):
    """Registration view, creates user with password and saves to the database"""

    queryset = get_user_model().objects.all()
    serializer_class = RegisterUserSerializer

    def create(self, request, *args, **kwargs):
        """Override create method of CreateModelMixin to provide custom application logic"""

        response = super(CreateUserView, self).create(request, args, **kwargs)
        # Retrieve instance created above, returning JWT payload
        payload: dict = custom_payload_handler(response.data.serailizer.instance)
        # Attach custom claim in JWT
        payload["apiVersion"] = settings.API_VERSION
        # Encode payload for response
        token = jwt_encode_handler(payload)
        return Response({"token": token}, status=status.HTTP_201_CREATED)


class ManageUserView(
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    GenericViewSet,
):
    """CRUD endpoint to get/update/delete user"""

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)
    queryset = get_user_model().objects.all()
    serializer_class = UpdateUserSerializer

    def get_object(self):
        return self.request.user


class TestSecuredView(APIView):
    """Test view to verify that authorization works"""

    permission_classes = (IsAuthenticated,)
    authentication_classes = (JSONWebTokenAuthentication,)

    def get(sef, request, format=None):
        return Response({"ok": True})
