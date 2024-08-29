from django.urls import include, path, re_path
from rest_framework import routers
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView, TokenVerifyView)

from .views import CommentViewSet, FollowViewSet, GroupViewSet, PostViewSet

router = routers.DefaultRouter()

router.register('v1/posts', PostViewSet)
router.register('v1/groups', GroupViewSet)
router.register('v1/follow', FollowViewSet, basename='follow')
router.register(
    r'v1/posts/(?P<post_pk>\d+)/comments',
    CommentViewSet,
    basename='comments')

urlpatterns = [
    re_path(r'^', include(router.urls)),
    path('v1/jwt/create/',
         TokenObtainPairView.as_view(),
         name='token_obtain_pair'),
    path('v1/jwt/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('v1/jwt/verify/', TokenVerifyView.as_view(), name='token_verify'),
]
