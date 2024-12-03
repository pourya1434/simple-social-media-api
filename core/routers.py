# from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers

from core.user.viewsets import UserViewSets
from core.auth.viewsets.register import RegisterViewSet
from core.auth.viewsets.login import LoginViewSet
from core.auth.viewsets.refresh import RefreshViewSet
from core.post.viewsets import PostViewSet
from core.comment.viewsets import CommentViewSet

# router = DefaultRouter()
router = routers.SimpleRouter()

# user
router.register(r"user", UserViewSets, basename="user")
#####################
###### AUTH #########
#####################
router.register(r"auth/register", RegisterViewSet, basename="auth-register")
router.register(r"auth/login", LoginViewSet, basename="auth-login")
router.register(r"auth/refresh", RefreshViewSet, basename="auth-refresh")
#####################
###### POST #########
#####################
router.register(r"post", PostViewSet, basename="post")

# nested router
posts_router = routers.NestedSimpleRouter(router, r"post", lookup="post")
posts_router.register(r"comment", CommentViewSet, basename="post-comment")


urlpatterns = [
    *router.urls,
    *posts_router.urls,
]
