from .veiwsets import DeviceViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("device", DeviceViewSet, basename="device")
urlpatterns = router.urls
