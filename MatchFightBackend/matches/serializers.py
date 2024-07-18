from rest_framework import serializers
from .models import Pair
from participants.serializers import ParticipantSerializer
from competitions.serializers import CompetitionSerializer
from tournaments.serializers import TournamentSerializer


# class PairSerializer(serializers.ModelSerializer):
    
#     participant1_weight = serializers.DecimalField(source='participant1.weight', max_digits=5, decimal_places=2, read_only=True)
#     participant2_weight = serializers.DecimalField(source='participant2.weight', max_digits=5, decimal_places=2, read_only=True)
#     participant1_name = serializers.CharField(source='participant1.name', read_only=True)
#     participant2_name = serializers.CharField(source='participant2.name', read_only=True)

#     class Meta:
#         model = Pair
#         fields = "__all__"
#         extra_fields = ['participant1_weight', 'participant2_weight', 'participant1_name', 'participant2_name']

class PairSerializer(serializers.ModelSerializer):
    participant1 = ParticipantSerializer()
    participant2 = ParticipantSerializer(allow_null=True)
    
    
    competition = CompetitionSerializer()
    tournament = TournamentSerializer()

    class Meta:
        model = Pair
        fields = '__all__'

    def validate(self, data):
        winner = data.get("winner")
        participant1 = data.get("participant1")
        participant2 = data.get("participant2")

        if participant2 is None:
            data["winner"] = participant1
        elif winner not in [participant1, participant2, None]:
            raise serializers.ValidationError(
                "Winner must be either participant1 or participant2."
            )

        return data


class UpdateWinnerSerializer(serializers.Serializer):
    pair_id = serializers.IntegerField()
    winner_id = serializers.IntegerField()
