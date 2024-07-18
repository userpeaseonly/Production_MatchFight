from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from django.db import models
from .models import Participant
from matches.models import Pair
from .serializers import ParticipantSerializer, GenerateParticipantsSerializer, FilterParticipantsSerializer
from matches.serializers import PairSerializer
from tournaments.models import Tournament
from competitions.models import Competition
from .algorithm import generate_pairs
from faker import Faker
import random
import string

class ParticipantViewSet(viewsets.ModelViewSet):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer

class GenerateParticipantsView(APIView):
    def post(self, request):
        serializer = GenerateParticipantsSerializer(data=request.data)
        if serializer.is_valid():
            competition_id = serializer.validated_data['competition_id']
            tournament_id = serializer.validated_data['tournament_id']
            number_of_participants = serializer.validated_data['number_of_participants']

            try:
                tournament = Tournament.objects.get(id=tournament_id)
                competition = Competition.objects.get(id=competition_id)
            except Tournament.DoesNotExist:
                return Response({'error': 'Tournament not found'}, status=status.HTTP_404_NOT_FOUND)
            except Competition.DoesNotExist:
                return Response({'error': 'Competition not found'}, status=status.HTTP_404_NOT_FOUND)

            fake = Faker()
            for _ in range(number_of_participants):
                name = fake.name()
                age = random.randint(tournament.min_age, tournament.max_age)
                weight = round(random.uniform(float(tournament.min_weight) + 0.01, float(tournament.max_weight)), 2)
                gender = tournament.gender

                participant = Participant(
                    name=name,
                    gender=gender,
                    age=age,
                    weight=weight,
                    competition=competition,
                    unique_id=''.join(random.choices(string.ascii_uppercase + string.digits, k=12))
                )
                participant.save()

            return Response({'status': 'Participants created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FilterParticipantsView(APIView):
    def post(self, request):
        serializer = FilterParticipantsSerializer(data=request.data)
        if serializer.is_valid():
            competition_id = serializer.validated_data['competition_id']
            tournament_id = serializer.validated_data['tournament_id']

            try:
                tournament = Tournament.objects.get(id=tournament_id)
                competition = Competition.objects.get(id=competition_id)
            except Tournament.DoesNotExist:
                return Response({'error': 'Tournament not found'}, status=status.HTTP_404_NOT_FOUND)
            except Competition.DoesNotExist:
                return Response({'error': 'Competition not found'}, status=status.HTTP_404_NOT_FOUND)

            participants = Participant.objects.filter(
                competition=competition,
                gender=tournament.gender,
                age__gte=tournament.min_age,
                age__lte=tournament.max_age,
                weight__gt=tournament.min_weight,
                weight__lte=tournament.max_weight
            )

            serializer = ParticipantSerializer(participants, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PairParticipantsView(APIView):
    def post(self, request):
        serializer = FilterParticipantsSerializer(data=request.data)
        if serializer.is_valid():
            competition_id = serializer.validated_data['competition_id']
            tournament_id = serializer.validated_data['tournament_id']

            try:
                tournament = Tournament.objects.get(id=tournament_id)
                competition = Competition.objects.get(id=competition_id)
            except Tournament.DoesNotExist:
                return Response({'error': 'Tournament not found'}, status=status.HTTP_404_NOT_FOUND)
            except Competition.DoesNotExist:
                return Response({'error': 'Competition not found'}, status=status.HTTP_404_NOT_FOUND)

            pairs = Pair.objects.filter(competition=competition, tournament=tournament)
            current_level = pairs.aggregate(models.Max('level'))['level__max'] or 0

            if pairs.filter(level=current_level, winner__isnull=True).exists():
                # There are unfinished pairs in the current level
                unfinished_pairs = pairs.filter(level=current_level, winner__isnull=True)
                serializer = PairSerializer(unfinished_pairs, many=True)
                return Response(serializer.data, status=status.HTTP_200_OK)

            # Get winners from the previous level
            previous_level_winners = pairs.filter(level=current_level).exclude(winner__isnull=True).values_list('winner', flat=True)
            participants = Participant.objects.filter(id__in=previous_level_winners)

            new_pairs = generate_pairs(participants, current_level + 1)
            new_pair_objects = []
            for p1, p2 in new_pairs:
                pair = Pair(
                    participant1=p1,
                    participant2=p2,
                    competition=competition,
                    tournament=tournament,
                    level=current_level + 1
                )
                if p2 is None:
                    pair.winner = p1
                new_pair_objects.append(pair)
            Pair.objects.bulk_create(new_pair_objects)

            serializer = PairSerializer(new_pair_objects, many=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PairsByLevelView(APIView):
    def post(self, request):
        competition_id = request.data.get('competition_id')
        tournament_id = request.data.get('tournament_id')
        level = request.data.get('level')

        try:
            tournament = Tournament.objects.get(id=tournament_id)
            competition = Competition.objects.get(id=competition_id)
        except Tournament.DoesNotExist:
            return Response({'error': 'Tournament not found'}, status=status.HTTP_404_NOT_FOUND)
        except Competition.DoesNotExist:
            return Response({'error': 'Competition not found'}, status=status.HTTP_404_NOT_FOUND)

        pairs = Pair.objects.filter(competition=competition, tournament=tournament, level=level)
        serializer = PairSerializer(pairs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
