from rest_framework import viewsets
from .models import Pair
from .serializers import PairSerializer, UpdateWinnerSerializer
from finals.models import FinalsParticipant
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from participants.models import Participant
from competitions.models import Competition
from tournaments.models import Tournament
from participants.algorithm import generate_pairs
from django.db.models import Max


class PairViewSet(viewsets.ModelViewSet):
    queryset = Pair.objects.all()
    serializer_class = PairSerializer


class PairParticipantsView(APIView):
    def post(self, request):
        competition_id = request.data.get("competition_id")
        tournament_id = request.data.get("tournament_id")

        try:
            tournament = Tournament.objects.get(id=tournament_id)
            competition = Competition.objects.get(id=competition_id)
        except Tournament.DoesNotExist:
            return Response(
                {"error": "Tournament not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Competition.DoesNotExist:
            return Response(
                {"error": "Competition not found"}, status=status.HTTP_404_NOT_FOUND
            )

        participants = Participant.objects.filter(
            competition=competition,
            gender=tournament.gender,
            age__gte=tournament.min_age,
            age__lte=tournament.max_age,
            weight__gt=tournament.min_weight,
            weight__lte=tournament.max_weight,
        )

        pairs = Pair.objects.filter(competition=competition, tournament=tournament)
        current_level = pairs.aggregate(Max("level"))["level__max"] or 0
        
        if current_level == 0:
            new_pairs = generate_pairs(participants, current_level + 1)
            new_pair_objects = []
            for p1, p2 in new_pairs:
                pair = Pair(
                    participant1=p1,
                    participant2=p2,
                    competition=competition,
                    tournament=tournament,
                    level=current_level + 1,
                )
                if p2 is None:
                    pair.winner = p1
                new_pair_objects.append(pair)
            Pair.objects.bulk_create(new_pair_objects)

            serializer = PairSerializer(new_pair_objects, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        if pairs.filter(level=current_level, winner__isnull=True).exists():
            # There are unfinished pairs in the current level
            unfinished_pairs = pairs.filter(level=current_level, winner__isnull=True)
            serializer = PairSerializer(unfinished_pairs, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        # Get winners from the previous level
        previous_level_winners = pairs.filter(level=current_level).exclude(winner__isnull=True).values_list("winner", flat=True)
        if not previous_level_winners.exists():
            return Response(
                {"error": "No winners found in the previous level"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if len(previous_level_winners) <= 4:
            for winner_id in previous_level_winners:
                participant = Participant.objects.get(id=winner_id)
                FinalsParticipant.objects.get_or_create(
                    participant=participant,
                    tournament=tournament,
                    competition=competition,
                    defaults={'place': None}
                )
            return Response(
                {"message": "Finals are done in api/final-pairs/"},
                status=status.HTTP_200_OK,
            )

        participants = Participant.objects.filter(id__in=previous_level_winners)

        new_pairs = generate_pairs(participants, current_level + 1)
        new_pair_objects = []
        for p1, p2 in new_pairs:
            pair = Pair(
                participant1=p1,
                participant2=p2,
                competition=competition,
                tournament=tournament,
                level=current_level + 1,
            )
            if p2 is None:
                pair.winner = p1
            new_pair_objects.append(pair)
        Pair.objects.bulk_create(new_pair_objects)

        serializer = PairSerializer(new_pair_objects, many=True)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PairsByLevelView(APIView):
    def post(self, request):
        competition_id = request.data.get("competition_id")
        tournament_id = request.data.get("tournament_id")
        level = request.data.get("level")

        if not competition_id or not tournament_id or level is None:
            return Response(
                {"error": "competition_id, tournament_id, and level are required."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            tournament = Tournament.objects.get(id=tournament_id)
            competition = Competition.objects.get(id=competition_id)
        except Tournament.DoesNotExist:
            return Response(
                {"error": "Tournament not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Competition.DoesNotExist:
            return Response(
                {"error": "Competition not found"}, status=status.HTTP_404_NOT_FOUND
            )

        pairs = Pair.objects.filter(
            competition=competition, tournament=tournament, level=level
        )
        if not pairs.exists():
            return Response(
                {
                    "error": "No pairs found for the given competition, tournament, and level."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = PairSerializer(pairs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateWinnerView(APIView):
    def post(self, request):
        serializer = UpdateWinnerSerializer(data=request.data)
        if serializer.is_valid():
            pair_id = serializer.validated_data["pair_id"]
            winner_id = serializer.validated_data["winner_id"]

            try:
                pair = Pair.objects.get(id=pair_id)
            except Pair.DoesNotExist:
                return Response(
                    {"error": "Pair not found"}, status=status.HTTP_404_NOT_FOUND
                )

            try:
                winner = Participant.objects.get(id=winner_id)
            except Participant.DoesNotExist:
                return Response(
                    {"error": "Participant not found"}, status=status.HTTP_404_NOT_FOUND
                )

            if winner != pair.participant1 and winner != pair.participant2:
                return Response(
                    {"error": "Winner must be one of the participants in the pair"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            pair.winner = winner
            pair.save()

            serializer = PairSerializer(pair)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
