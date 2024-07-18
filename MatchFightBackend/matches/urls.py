from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PairViewSet, PairParticipantsView, PairsByLevelView, UpdateWinnerView


router = DefaultRouter()
router.register(r'pairs', PairViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('pair-participants/', PairParticipantsView.as_view(), name='pair-participants'),
    path('pairs-by-level/', PairsByLevelView.as_view(), name='pairs-by-level'),
    path('update-winner/', UpdateWinnerView.as_view(), name='update-winner'),
]
