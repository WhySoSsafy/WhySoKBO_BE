from rest_framework import serializers
from .models import Team, TeamTag, Player, PlayerTag, PlayerSeasonStat, Question, Choice


class TeamTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamTag
        fields = [
            'passion', 'fan_culture', 'story', 'emotional', 'dramatic',
            'winning', 'stable', 'traditional', 'loyalty', 'trendy',
            'popular', 'underdog', 'analytic',
        ]


class TeamSerializer(serializers.ModelSerializer):
    tag = TeamTagSerializer(read_only=True)

    class Meta:
        model = Team
        fields = ['id', 'name', 'region', 'stadium', 'intro', 'tag']


class PlayerTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerTag
        fields = [
            'power', 'contact', 'speed', 'defense', 'ace', 'closer',
            'clutch', 'consistent', 'charisma', 'leader', 'young', 'underdog', 'foreign',
        ]


class PlayerSeasonStatSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayerSeasonStat
        fields = ['season_year', 'stats']


class PlayerSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.name', read_only=True)
    tag = PlayerTagSerializer(read_only=True)
    stat = PlayerSeasonStatSerializer(read_only=True)

    class Meta:
        model = Player
        fields = [
            'id', 'team', 'team_name', 'name_ko', 'number', 'position',
            'is_active', 'is_recommendable',
            'intro', 'story', 'watch_point', 'cheer', 'stadium_tip',
            'tag', 'stat',
        ]


class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ['id', 'label', 'key', 'display_order']


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, read_only=True)

    class Meta:
        model = Question
        fields = [
            'id', 'quiz_type', 'number', 'category', 'question_text',
            'input_type', 'is_conditional', 'condition_key', 'choices',
        ]
