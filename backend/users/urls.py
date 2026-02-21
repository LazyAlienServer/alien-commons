from rest_framework.routers import DefaultRouter

from .views import AuthViewSet, ProfileViewSet


router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')
router.register(r'auth', AuthViewSet, basename='auth')

urlpatterns = router.urls
