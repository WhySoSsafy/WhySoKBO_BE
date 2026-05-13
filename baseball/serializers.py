from rest_framework import serializers
from .models import Team, Player, TeamQuestion, PlayerQuestion


class TeamQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamQuestion
        fields = ['id', 'number', 'category', 'question_text', 'left_choice', 'right_choice']


class PlayerQuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerQuestion
        fields = ['id', 'number', 'category', 'question_text', 'choices']


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = [
            'id', 'name', 'region',
            'tag_passion', 'tag_fan_culture', 'tag_story', 'tag_emotional',
            'tag_dramatic', 'tag_winning', 'tag_stable', 'tag_traditional',
            'tag_loyalty', 'tag_trendy', 'tag_popular', 'tag_underdog', 'tag_analytic',
        ]


class PlayerSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.name', read_only=True)

    class Meta:
        model = Player
        fields = [
            'id', 'team', 'team_name', 'name_ko', 'number', 'position',
            'tag_power', 'tag_contact', 'tag_speed', 'tag_defense',
            'tag_ace', 'tag_closer', 'tag_clutch', 'tag_consistent',
            'tag_charisma', 'tag_leader', 'tag_young', 'tag_underdog', 'tag_foreign',
            'stats', 'intro', 'story', 'watch_point', 'cheer', 'stadium_tip',
        ]
