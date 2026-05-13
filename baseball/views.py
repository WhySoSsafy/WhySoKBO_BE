from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Team, Player, TeamQuestion, PlayerQuestion
from .serializers import (
    TeamSerializer, PlayerSerializer,
    TeamQuestionSerializer, PlayerQuestionSerializer,
)
from .algorithm import recommend_teams, recommend_players


class TeamQuestionListView(APIView):
    def get(self, request):
        questions = TeamQuestion.objects.order_by('number')
        serializer = TeamQuestionSerializer(questions, many=True)
        return Response(serializer.data)


class PlayerQuestionListView(APIView):
    def get(self, request):
        questions = PlayerQuestion.objects.order_by('number')
        serializer = PlayerQuestionSerializer(questions, many=True)
        return Response(serializer.data)


class TeamListView(APIView):
    def get(self, request):
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)


class TeamDetailView(APIView):
    def get(self, request, pk):
        try:
            team = Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            return Response({'error': '팀을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = TeamSerializer(team)
        return Response(serializer.data)


class TeamPlayerListView(APIView):
    def get(self, request, pk):
        try:
            team = Team.objects.get(pk=pk)
        except Team.DoesNotExist:
            return Response({'error': '팀을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)
        players = Player.objects.filter(team=team)
        serializer = PlayerSerializer(players, many=True)
        return Response(serializer.data)


class TeamRecommendView(APIView):
    """
    POST /api/recommend/team/
    body: {
      "answers": {"1": 3, "2": 1, ..., "11": 5},
      "region": "서울"   // Q12 지역 선택
    }
    """
    def post(self, request):
        answers = request.data.get('answers', {})
        region = request.data.get('region', '상관없다')

        if not answers:
            return Response({'error': '답변이 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        teams = Team.objects.all()
        top3, persona = recommend_teams(answers, region, teams)

        result = {
            'persona': persona,
            'recommendations': [
                {
                    'rank': idx + 1,
                    'team': TeamSerializer(item['team']).data,
                    'match_percent': item['match_percent'],
                }
                for idx, item in enumerate(top3)
            ],
        }
        return Response(result)


class PlayerRecommendView(APIView):
    """
    POST /api/recommend/player/
    body: {
      "team_id": 1,
      "position": "타자",
      "answers": {"2": "홈런", "4": "결정적", "5": "자수성가", "6": "전성기", "7": "카리스마"}
    }
    """
    def post(self, request):
        team_id = request.data.get('team_id')
        position = request.data.get('position', '상관없다')
        answers = request.data.get('answers', {})

        if not team_id:
            return Response({'error': 'team_id가 필요합니다.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            team = Team.objects.get(pk=team_id)
        except Team.DoesNotExist:
            return Response({'error': '팀을 찾을 수 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        players = Player.objects.filter(team=team)
        if not players.exists():
            return Response({'error': '해당 팀의 선수 데이터가 없습니다.'}, status=status.HTTP_404_NOT_FOUND)

        top2 = recommend_players(position, answers, players)

        result = {
            'team': TeamSerializer(team).data,
            'recommendations': [
                {
                    'rank': idx + 1,
                    'player': PlayerSerializer(item['player']).data,
                    'match_percent': item['match_percent'],
                }
                for idx, item in enumerate(top2)
            ],
        }
        return Response(result)
