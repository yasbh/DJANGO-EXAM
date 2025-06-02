from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, ResultViewSet

router = DefaultRouter()
router.register(r'api/tasks', TaskViewSet)
router.register(r'api/results', ResultViewSet)

urlpatterns = router.urls
