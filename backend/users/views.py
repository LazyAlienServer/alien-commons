from django.contrib.auth import get_user_model
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from core.views.mixins import (
    FormattedResponseMixin, MyCreateModelMixin, MyListModelMixin, MyRetrieveModelMixin, MyUpdateModelMixin
)
from .serializers import (
    ProfileCreateSerializer,
    ProfileListSerializer,
    ProfileRetrieveSerializer,
    ProfileUpdateSerializer,
    CustomLoginSerializer,
    CustomLoginRefreshSerializer,
)


User = get_user_model()


class AuthViewSet(FormattedResponseMixin, viewsets.ViewSet):
    """
    A viewset that collects 2 API endpoints which relates to user module

    Login, Refresh Login Token
    """
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def login(self, request):
        serializer = CustomLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return self.format_success_response(
            message="user login successfully",
            code="user_login",
            data=serializer.validated_data,
            status_code=status.HTTP_200_OK
        )

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def refresh_login_token(self, request):
        serializer = CustomLoginRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        return self.format_success_response(
            message="login token refreshed successfully",
            code="token_refreshed",
            data=serializer.validated_data,
            status_code=status.HTTP_200_OK
        )


class ProfileViewSet(MyCreateModelMixin,
                     MyListModelMixin,
                     MyRetrieveModelMixin,
                     FormattedResponseMixin,
                     viewsets.GenericViewSet):
    """
    A viewset that collects 4 API endpoints which relates to user module

    Register, User List, Profile Info, Update (username, signature, avatar)
    """
    queryset = User.objects.all()
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    serializer_class_mapping = {
        'create': ProfileCreateSerializer,
        'list': ProfileListSerializer,
        'retrieve': ProfileRetrieveSerializer,
    }

    def get_serializer_class(self):
        self.action: str
        return self.serializer_class_mapping[self.action]

    def get_permissions(self):
        self.action: str
        if self.action in ('create', 'list', 'retrieve'):
            return [AllowAny]
        if self.action in ('me',):
            return [IsAuthenticated]

    @action(detail=False, methods=['get', 'patch'], url_path='me')
    def me(self, request):
        user = request.user
        if request.method == 'GET':
            serializer = ProfileRetrieveSerializer(user)

            return self.format_success_response(
                message="my profile retrieved",
                code='my_profile_retrieved',
                data=serializer.data,
                status_code=status.HTTP_200_OK
            )

        serializer = ProfileUpdateSerializer(user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return self.format_success_response(
            message="my profile updated",
            code='my_profile_updated',
            data=serializer.data,
            status_code=status.HTTP_200_OK
        )
