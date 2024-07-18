from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FinalsPairViewSet, FinalsParticipantViewSet

router = DefaultRouter()
router.register(r'finals-pairs', FinalsPairViewSet)
router.register(r'finals-participants', FinalsParticipantViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
