from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet, RecipeViewSet, TagViewSet

router = DefaultRouter()
router.register(r'ingredients', IngredientViewSet)
router.register(r'tags', TagViewSet)
# router.register(r'recipes', RecipeViewSet, basename='recipes')  #wip
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



urlpatterns = [
    # path('auth/signup/', SignUpView.as_view(), name='signup'),
    # path('auth/token/', TokenView.as_view(), name='token'),
    path('', include(router.urls))
    ]
