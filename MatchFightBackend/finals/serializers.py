from rest_framework import serializers
from .models import FinalsPair, FinalsParticipant
from participants.serializers import ParticipantSerializer
from competitions.serializers import CompetitionSerializer
from tournaments.serializers import TournamentSerializer


# class FinalsPairSerializer(serializers.ModelSerializer):
#     participant1_name = serializers.SerializerMethodField()
#     participant2_name = serializers.SerializerMethodField()

#     class Meta:
#         model = FinalsPair
#         fields = "__all__"
#         extra_fields = ["participant1_name", "participant2_name"]

#     def get_participant1_name(self, obj):
#         return obj.participant1.participant.name if obj.participant1 else None

#     def get_participant2_name(self, obj):
#         return obj.participant2.participant.name if obj.participant2 else None

#     def to_representation(self, instance):
#         representation = super().to_representation(instance)
#         representation["participant1_name"] = self.get_participant1_name(instance)
#         representation["participant2_name"] = self.get_participant2_name(instance)
#         return representation

#     def validate(self, data):
#         winner = data.get("winner")
#         participant1 = data.get("participant1")
#         participant2 = data.get("participant2")

#         if participant2 is None:
#             data["winner"] = participant1
#         elif winner not in [participant1, participant2, None]:
#             raise serializers.ValidationError(
#                 "Winner must be either participant1 or participant2."
#             )


#         return data

# class FinalsParticipantSerializer(serializers.ModelSerializer):
#     participant = ParticipantSerializer()

#     class Meta:
#         model = FinalsParticipant
#         fields = "__all__"


# class FinalsPairSerializer(serializers.ModelSerializer):
#     participant1 = ParticipantSerializer()
#     participant2 = ParticipantSerializer(allow_null=True)

#     class Meta:
#         model = FinalsPair
#         fields = "__all__"

#     def validate(self, data):
#         winner = data.get("winner")
#         participant1 = data.get("participant1")
#         participant2 = data.get("participant2")

#         if participant2 is None:
#             data["winner"] = participant1
#         elif winner not in [participant1, participant2, None]:
#             raise serializers.ValidationError(
#                 "Winner must be either participant1 or participant2."
#             )

#         return data


class FinalsParticipantReadSerializer(serializers.ModelSerializer):
    participant = ParticipantSerializer()

    competition = CompetitionSerializer()
    tournament = TournamentSerializer()
    class Meta:
        model = FinalsParticipant
        fields = "__all__"


class FinalsPairReadSerializer(serializers.ModelSerializer):
    participant1 = FinalsParticipantReadSerializer()
    participant2 = FinalsParticipantReadSerializer(allow_null=True)
    
    
    competition = CompetitionSerializer()
    tournament = TournamentSerializer()

    class Meta:
        model = FinalsPair
        fields = "__all__"


class FinalsParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalsParticipant
        fields = "__all__"


class FinalsPairSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinalsPair
        fields = "__all__"

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
