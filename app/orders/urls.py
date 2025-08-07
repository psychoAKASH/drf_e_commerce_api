from .views import OrderViewSet,CartItemViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register(r'orders', OrderViewSet)
router.register(r'cart', CartItemViewSet)

urlpatterns = router.urls
