from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import FinalsPair, FinalsParticipant
from competitions.models import Competition
from tournaments.models import Tournament
from .serializers import FinalsPairSerializer, FinalsParticipantSerializer, FinalsPairReadSerializer, FinalsParticipantReadSerializer


# class FinalsPairViewSet(viewsets.ModelViewSet):
#     queryset = FinalsPair.objects.all()
#     serializer_class = FinalsPairSerializer

#     def create(self, request, *args, **kwargs):
#         participant1_id = request.data.get("participant1")
#         participant2_id = request.data.get("participant2")
#         stage = request.data.get("stage")
#         competition_id = request.data.get("competition")
#         tournament_id = request.data.get("tournament")

#         try:
#             participant1 = FinalsParticipant.objects.get(id=participant1_id)
#             participant2 = (
#                 FinalsParticipant.objects.get(id=participant2_id)
#                 if participant2_id
#                 else None
#             )
#             competition = Competition.objects.get(id=competition_id)
#             tournament = Tournament.objects.get(id=tournament_id)
#         except FinalsParticipant.DoesNotExist:
#             return Response(
#                 {"error": "FinalsParticipant not found"},
#                 status=status.HTTP_404_NOT_FOUND,
#             )
#         except Competition.DoesNotExist:
#             return Response(
#                 {"error": "Competition not found"}, status=status.HTTP_404_NOT_FOUND
#             )
#         except Tournament.DoesNotExist:
#             return Response(
#                 {"error": "Tournament not found"}, status=status.HTTP_404_NOT_FOUND
#             )

#         finals_pair = FinalsPair(
#             participant1=participant1,
#             participant2=participant2,
#             stage=stage,
#             competition=competition,
#             tournament=tournament,
#             winner=participant1 if participant2 is None else None,
#         )
#         finals_pair.save()

#         serializer = self.get_serializer(finals_pair)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)

class FinalsPairViewSet(viewsets.ModelViewSet):
    queryset = FinalsPair.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return FinalsPairReadSerializer
        return FinalsPairSerializer

    def create(self, request, *args, **kwargs):
        participant1_id = request.data.get('participant1')
        participant2_id = request.data.get('participant2')
        stage = request.data.get('stage')
        competition_id = request.data.get('competition')
        tournament_id = request.data.get('tournament')
        
        try:
            participant1 = FinalsParticipant.objects.get(id=participant1_id)
            participant2 = FinalsParticipant.objects.get(id=participant2_id) if participant2_id else None
            competition = Competition.objects.get(id=competition_id)
            tournament = Tournament.objects.get(id=tournament_id)
        except FinalsParticipant.DoesNotExist:
            return Response({"error": "FinalsParticipant not found"}, status=status.HTTP_404_NOT_FOUND)
        except Competition.DoesNotExist:
            return Response({"error": "Competition not found"}, status=status.HTTP_404_NOT_FOUND)
        except Tournament.DoesNotExist:
            return Response({"error": "Tournament not found"}, status=status.HTTP_404_NOT_FOUND)

        finals_pair = FinalsPair(
            participant1=participant1,
            participant2=participant2,
            stage=stage,
            competition=competition,
            tournament=tournament,
            winner=participant1 if participant2 is None else None
        )
        finals_pair.save()

        serializer = self.get_serializer(finals_pair)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


# class FinalsParticipantViewSet(viewsets.ModelViewSet):
#     queryset = FinalsParticipant.objects.all()
#     serializer_class = FinalsParticipantSerializer

#     def get_queryset(self):
#         queryset = super().get_queryset()
#         competition_id = self.request.query_params.get("competition", None)
#         tournament_id = self.request.query_params.get("tournament", None)

#         if competition_id:
#             queryset = queryset.filter(competition_id=competition_id)
#         if tournament_id:
#             queryset = queryset.filter(tournament_id=tournament_id)

#         return queryset
class FinalsParticipantViewSet(viewsets.ModelViewSet):
    queryset = FinalsParticipant.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return FinalsParticipantReadSerializer
        return FinalsParticipantSerializer
