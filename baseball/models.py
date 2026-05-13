from django.db import models

# 1. 팀 데이터 모델 (Team)
class Team(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="팀명")
    region = models.CharField(max_length=50, verbose_name="연고지")
    
    # 13개 팀 태그 (알고리즘 내적 계산용)
    tag_passion = models.IntegerField(default=0)
    tag_fan_culture = models.IntegerField(default=0)
    tag_story = models.IntegerField(default=0)
    tag_emotional = models.IntegerField(default=0)
    tag_dramatic = models.IntegerField(default=0)
    tag_winning = models.IntegerField(default=0)
    tag_stable = models.IntegerField(default=0)
    tag_traditional = models.IntegerField(default=0)
    tag_loyalty = models.IntegerField(default=0)
    tag_trendy = models.IntegerField(default=0)
    tag_popular = models.IntegerField(default=0)
    tag_underdog = models.IntegerField(default=0)
    tag_analytic = models.IntegerField(default=0)

    def __str__(self):
        return self.name

# 2. 선수 데이터 모델 (Player) - 디아즈 같은 선수들이 들어갈 테이블
class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='players')
    name_ko = models.CharField(max_length=50, verbose_name="선수 한글명")
    number = models.IntegerField(verbose_name="등번호")
    position = models.CharField(max_length=20, verbose_name="포지션")
    
    # 선수 전용 13개 태그
    tag_power = models.IntegerField(default=0)
    tag_contact = models.IntegerField(default=0)
    tag_speed = models.IntegerField(default=0)
    tag_defense = models.IntegerField(default=0)
    tag_ace = models.IntegerField(default=0)
    tag_closer = models.IntegerField(default=0)
    tag_clutch = models.IntegerField(default=0)
    tag_consistent = models.IntegerField(default=0)
    tag_charisma = models.IntegerField(default=0)
    tag_leader = models.IntegerField(default=0)
    tag_young = models.IntegerField(default=0)
    tag_underdog = models.IntegerField(default=0)
    tag_foreign = models.IntegerField(default=0)

    # 선수 정보 및 직관 포인트 (문자열 및 JSON 형태의 스탯)
    stats = models.JSONField(verbose_name="주요 스탯", default=dict)
    intro = models.CharField(max_length=100, verbose_name="한줄 소개")
    story = models.TextField(verbose_name="선수 스토리")
    watch_point = models.CharField(max_length=200, verbose_name="관전 포인트")
    cheer = models.TextField(verbose_name="응원가 가사")
    stadium_tip = models.CharField(max_length=200, verbose_name="직관 꿀팁")

    def __str__(self):
        return f"{self.name_ko} ({self.team.name})"

# 3. 팀 추천 질문 모델
class TeamQuestion(models.Model):
    number = models.IntegerField(unique=True, verbose_name="질문 번호")
    category = models.CharField(max_length=20, verbose_name="카테고리")
    question_text = models.CharField(max_length=200, verbose_name="질문 내용")
    left_choice = models.CharField(max_length=100, verbose_name="왼쪽 선택지(1점)")
    right_choice = models.CharField(max_length=100, verbose_name="오른쪽 선택지(5점)")

    def __str__(self):
        return f"Q{self.number}: {self.question_text}"

# 4. 선수 추천 질문 모델
class PlayerQuestion(models.Model):
    number = models.IntegerField(unique=True, verbose_name="질문 번호")
    category = models.CharField(max_length=20, verbose_name="카테고리")
    question_text = models.CharField(max_length=200, verbose_name="질문 내용")
    # 선수 질문은 버튼형 객관식이므로 JSON 형식으로 선택지와 가중치 데이터를 통째로 저장하는 것이 유리합니다.
    choices = models.JSONField(verbose_name="선택지 및 가중치 데이터", default=list)

    def __str__(self):
        return f"PQ{self.number}: {self.question_text}"