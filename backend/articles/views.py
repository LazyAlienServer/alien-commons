from rest_framework import status
from rest_framework.viewsets import GenericViewSet
from rest_framework.decorators import action
from django_filters import rest_framework as filters
from django.db.models import OuterRef, Subquery

from core.utils.permissions import is_moderator
from core.views.viewsets import MyModelViewSet, MyReadOnlyModelViewSet, FormattedResponseMixin
from .filters import SourceArticleFilter
from .permissions import (
    SourceArticlePermission,
    PublishedArticlePermission,
    ArticleSnapshotPermission,
    ArticleEventPermission,
)
from .models import SourceArticle, PublishedArticle, ArticleSnapshot, ArticleEvent
from .serializers import (
    SourceArticleReadSerializer,
    SourceArticleWriteSerializer,
    ImageUploadSerializer,
    PublishedArticleSerializer,
    ArticleSnapshotSerializer,
    ArticleEventSerializer,
    ArticleActionInputSerializer,
    ArticleActionOutputSerializer,
)
from .services.articles import (
    submit, withdraw, approve, reject, unpublish, delete
)


class SourceArticleViewSet(MyModelViewSet):
    permission_classes = (SourceArticlePermission,)
    queryset = SourceArticle.objects.select_related("author")
    filter_backends = [filters.DjangoFilterBackend]
    filterset_class = SourceArticleFilter

    def get_serializer_class(self):
        # Author - Write Serializer | Moderators - Read Serializer
        if self.action in ('create', 'update', 'partial_update'):
            return SourceArticleWriteSerializer
        return SourceArticleReadSerializer

    def get_queryset(self):
        # Only authors can see his/her articles
        user = self.request.user
        queryset = super().get_queryset()

        if not user or user.is_anonymous:
            return queryset.none()

        queryset = queryset.filter(author=user)
        last_snapshot_id = ArticleSnapshot.objects.filter(article_id=OuterRef("pk")).order_by("-created_at").values("id")[:1]
        published_version_id = PublishedArticle.objects.filter(article_id=OuterRef("pk")).values("id")

        return queryset.annotate(
            last_snapshot_id=Subquery(last_snapshot_id),
            published_version_id=Subquery(published_version_id),
        )

    def create(self, request, *args, **kwargs):
        input_serializer = SourceArticleWriteSerializer(
            data=request.data,
            context=self.get_serializer_context(),
        )
        input_serializer.is_valid(raise_exception=True)

        instance = input_serializer.save(author=self.request.user)

        instance = self.get_queryset().get(pk=instance.pk)

        output_serializer = SourceArticleReadSerializer(
            instance=instance,
            context=self.get_serializer_context(),
        )

        return self.format_success_response(
            message="created",
            code='created',
            data=output_serializer.data,
            status_code=status.HTTP_201_CREATED,
        )

    @action(detail=False, methods=['post'], url_path='upload_article_image')
    def upload_article_image(self, request):
        serializer = ImageUploadSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        result = serializer.save()

        return self.format_success_response(
            message="uploaded",
            code='uploaded',
            data=result,
            status_code=status.HTTP_200_OK,
        )


class PublishedArticleViewSet(MyReadOnlyModelViewSet):
    queryset = PublishedArticle.objects.all()
    serializer_class = PublishedArticleSerializer
    permission_classes = (PublishedArticlePermission,)


class ArticleSnapshotViewSet(MyReadOnlyModelViewSet):
    queryset = ArticleSnapshot.objects.all()
    serializer_class = ArticleSnapshotSerializer
    permission_classes = (ArticleSnapshotPermission,)

    @action(detail=False, methods=['get'])
    def pending(self, request):
        """
        Return not moderated article snapshots
        """
        queryset = ArticleSnapshot.objects.filter(moderation_status=ArticleSnapshot.SnapshotStatus.PENDING)
        serializer = self.get_serializer(queryset, many=True)

        return self.format_success_response(
            message="pending articles listed",
            code='listed',
            data=serializer.data,
            status_code=status.HTTP_200_OK,
        )


class ArticleEventReadViewset(MyReadOnlyModelViewSet):
    queryset = ArticleEvent.objects.all()
    permission_classes = (ArticleEventPermission,)
    serializer_class = ArticleEventSerializer

    def get_queryset(self):
        user = self.request.user
        if is_moderator(user):
            return ArticleEvent.objects.all()
        return ArticleEvent.objects.filter(article__author=user)


class ArticleActionViewset(FormattedResponseMixin, GenericViewSet):
    queryset = SourceArticle.objects.all()
    lookup_field = "pk"

    @action(detail=True, methods=['post'], permission_classes=[SourceArticlePermission,])
    def submit(self, request, pk=None):
        input_serializer = ArticleActionInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        result = submit(
            article_id=pk,
            actor=request.user,
            annotation=input_serializer.validated_data.get("annotation", None)
        )

        output_serializer = ArticleActionOutputSerializer(result)

        return self.format_success_response(
            message="submitted",
            code='submitted',
            data=output_serializer.data,
            status_code=status.HTTP_200_OK,
        )

    @action(detail=True, methods=['post'], permission_classes=[SourceArticlePermission,])
    def withdraw(self, request, pk=None):
        input_serializer = ArticleActionInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        result = withdraw(
            article_id=pk,
            actor=request.user,
            annotation=input_serializer.validated_data.get("annotation", None)
        )

        output_serializer = ArticleActionOutputSerializer(result)

        return self.format_success_response(
            message="withdrawn",
            code='withdrawn',
            data=output_serializer.data,
            status_code=status.HTTP_200_OK,
        )

    @action(detail=True, methods=['post'], permission_classes=[SourceArticlePermission,])
    def approve(self, request, pk=None):
        input_serializer = ArticleActionInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        result = approve(
            article_id=pk,
            actor=request.user,
            annotation=input_serializer.validated_data.get("annotation", None)
        )

        output_serializer = ArticleActionOutputSerializer(result)

        return self.format_success_response(
            message="approved",
            code='approved',
            data=output_serializer.data,
            status_code=status.HTTP_200_OK,
        )

    @action(detail=True, methods=['post'], permission_classes=[SourceArticlePermission,])
    def reject(self, request, pk=None):
        input_serializer = ArticleActionInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        result = reject(
            article_id=pk,
            actor=request.user,
            annotation=input_serializer.validated_data.get("annotation", None)
        )

        output_serializer = ArticleActionOutputSerializer(result)

        return self.format_success_response(
            message="rejected",
            code='rejected',
            data=output_serializer.data,
            status_code=status.HTTP_200_OK,
        )

    @action(detail=True, methods=['post'], permission_classes=[SourceArticlePermission,])
    def unpublish(self, request, pk=None):
        input_serializer = ArticleActionInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        result = unpublish(
            article_id=pk,
            actor=request.user,
            annotation=input_serializer.validated_data.get("annotation", None)
        )

        output_serializer = ArticleActionOutputSerializer(result)

        return self.format_success_response(
            message="unpublished",
            code='unpublished',
            data=output_serializer.data,
            status_code=status.HTTP_200_OK,
        )

    @action(detail=True, methods=['post'], permission_classes=[SourceArticlePermission,])
    def delete(self, request, pk=None):
        input_serializer = ArticleActionInputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        result = delete(
            article_id=pk,
            actor=request.user,
            annotation=input_serializer.validated_data.get("annotation", None)
        )

        output_serializer = ArticleActionOutputSerializer(result)

        return self.format_success_response(
            message="deleted",
            code='deleted',
            data=output_serializer.data,
            status_code=status.HTTP_200_OK,
        )
