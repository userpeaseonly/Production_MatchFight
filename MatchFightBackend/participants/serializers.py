from rest_framework import serializers
from .models import Participant
from competitions.serializers import CompetitionSerializer
from tournaments.serializers import TournamentSerializer

class ParticipantSerializer(serializers.ModelSerializer):
    
            
    # competition = CompetitionSerializer()
    
    class Meta:
        model = Participant
        fields = '__all__'



class GenerateParticipantsSerializer(serializers.Serializer):
    competition_id = serializers.IntegerField()
    tournament_id = serializers.IntegerField()
    number_of_participants = serializers.IntegerField()


class FilterParticipantsSerializer(serializers.Serializer):
    competition_id = serializers.IntegerField()
    tournament_id = serializers.IntegerField()
