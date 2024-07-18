from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ParticipantViewSet, GenerateParticipantsView, FilterParticipantsView, PairParticipantsView, PairsByLevelView

router = DefaultRouter()
router.register(r'participants', ParticipantViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('generate-participants/', GenerateParticipantsView.as_view(), name='generate-participants'),
    path('filter-participants/', FilterParticipantsView.as_view(), name='filter-participants'),
    # path('pair-participants/', PairParticipantsView.as_view(), name='pair-participants'),
    # path('pairs-by-level/', PairsByLevelView.as_view(), name='pairs-by-level'),
]
