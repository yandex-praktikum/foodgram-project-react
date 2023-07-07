# from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
#                        ReviewViewSet, SignUpView, TitleViewSet, TokenView,
#                        UserViewSet)
from django.urls import include, path
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router_v1.register(r'categories', CategoryViewSet)
# router_v1.register(r'genres', GenreViewSet)
# router_v1.register(
#     r'titles/(?P<title_id>\d+)/reviews',
#     ReviewViewSet,
#     basename='reviews'
# )
# router_v1.register(
#     r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
#     CommentViewSet,
#     basename='comments'
# )
# router_v1.register(r'users', UserViewSet)
# router_v1.register(r'titles', TitleViewSet,
#                    basename='titles')


urlpatterns = [
    # path('auth/signup/', SignUpView.as_view(), name='signup'),
    # path('auth/token/', TokenView.as_view(), name='token'),
    path('', include(router.urls))
    ]
