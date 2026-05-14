from django.db import models


class Team(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="팀명")
    region = models.CharField(max_length=50, verbose_name="연고지")
    stadium = models.CharField(max_length=100, default="", verbose_name="홈구장")
    intro = models.TextField(default="", verbose_name="팀 소개")

    class Meta:
        verbose_name = "팀"
        verbose_name_plural = "팀 목록"

    def __str__(self):
        return self.name


class TeamTag(models.Model):
    team = models.OneToOneField(Team, on_delete=models.CASCADE, related_name="tag", verbose_name="팀")
    passion = models.IntegerField(default=0, verbose_name="열정")
    fan_culture = models.IntegerField(default=0, verbose_name="응원문화")
    story = models.IntegerField(default=0, verbose_name="서사")
    emotional = models.IntegerField(default=0, verbose_name="감성")
    dramatic = models.IntegerField(default=0, verbose_name="드라마틱")
    winning = models.IntegerField(default=0, verbose_name="승리지향")
    stable = models.IntegerField(default=0, verbose_name="안정")
    traditional = models.IntegerField(default=0, verbose_name="전통")
    loyalty = models.IntegerField(default=0, verbose_name="충성도")
    trendy = models.IntegerField(default=0, verbose_name="트렌디")
    popular = models.IntegerField(default=0, verbose_name="인기")
    underdog = models.IntegerField(default=0, verbose_name="언더독")
    analytic = models.IntegerField(default=0, verbose_name="분석")

    class Meta:
        verbose_name = "팀 태그"
        verbose_name_plural = "팀 태그 목록"

    def __str__(self):
        return f"{self.team.name} 태그"


class Player(models.Model):
    team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="players", verbose_name="소속 팀")
    name_ko = models.CharField(max_length=50, verbose_name="선수 한글명")
    number = models.IntegerField(verbose_name="등번호")
    position = models.CharField(max_length=20, verbose_name="포지션")
    is_active = models.BooleanField(default=True, verbose_name="현역 여부")
    is_recommendable = models.BooleanField(default=True, verbose_name="추천 대상 여부")
    intro = models.CharField(max_length=200, verbose_name="한줄 소개")
    story = models.TextField(verbose_name="선수 스토리")
    watch_point = models.CharField(max_length=300, verbose_name="관전 포인트")
    cheer = models.TextField(verbose_name="응원가 가사")
    stadium_tip = models.CharField(max_length=300, verbose_name="직관 꿀팁")

    class Meta:
        verbose_name = "선수"
        verbose_name_plural = "선수 목록"

    def __str__(self):
        return f"{self.name_ko} ({self.team.name})"


class PlayerTag(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE, related_name="tag", verbose_name="선수")
    power = models.IntegerField(default=0, verbose_name="파워")
    contact = models.IntegerField(default=0, verbose_name="컨택")
    speed = models.IntegerField(default=0, verbose_name="스피드")
    defense = models.IntegerField(default=0, verbose_name="수비")
    ace = models.IntegerField(default=0, verbose_name="에이스")
    closer = models.IntegerField(default=0, verbose_name="마무리")
    clutch = models.IntegerField(default=0, verbose_name="클러치")
    consistent = models.IntegerField(default=0, verbose_name="꾸준함")
    charisma = models.IntegerField(default=0, verbose_name="카리스마")
    leader = models.IntegerField(default=0, verbose_name="리더십")
    young = models.IntegerField(default=0, verbose_name="유망주")
    underdog = models.IntegerField(default=0, verbose_name="언더독")
    foreign = models.IntegerField(default=0, verbose_name="외국인")

    class Meta:
        verbose_name = "선수 태그"
        verbose_name_plural = "선수 태그 목록"

    def __str__(self):
        return f"{self.player.name_ko} 태그"


class PlayerSeasonStat(models.Model):
    player = models.OneToOneField(Player, on_delete=models.CASCADE, related_name="stat", verbose_name="선수")
    season_year = models.IntegerField(default=2025, verbose_name="시즌 연도")
    stats = models.JSONField(default=dict, verbose_name="시즌 기록")

    class Meta:
        verbose_name = "선수 시즌 기록"
        verbose_name_plural = "선수 시즌 기록 목록"

    def __str__(self):
        return f"{self.player.name_ko} {self.season_year}시즌"


class Question(models.Model):
    QUIZ_TYPE_CHOICES = [
        ("team", "팀 추천"),
        ("player", "선수 추천"),
    ]
    INPUT_TYPE_CHOICES = [
        ("slider", "슬라이더"),
        ("button", "버튼"),
    ]

    quiz_type = models.CharField(max_length=10, choices=QUIZ_TYPE_CHOICES, verbose_name="질문 유형")
    number = models.IntegerField(verbose_name="질문 번호")
    category = models.CharField(max_length=30, verbose_name="카테고리")
    question_text = models.CharField(max_length=300, verbose_name="질문 내용")
    input_type = models.CharField(max_length=10, choices=INPUT_TYPE_CHOICES, default="button", verbose_name="입력 방식")
    is_conditional = models.BooleanField(default=False, verbose_name="조건부 노출")
    condition_key = models.CharField(max_length=50, blank=True, default="", verbose_name="노출 조건 키")

    class Meta:
        unique_together = [("quiz_type", "number")]
        ordering = ["quiz_type", "number"]
        verbose_name = "질문"
        verbose_name_plural = "질문 목록"

    def __str__(self):
        return f"[{self.get_quiz_type_display()}] Q{self.number}: {self.question_text}"


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices", verbose_name="질문")
    label = models.CharField(max_length=200, verbose_name="선택지 텍스트")
    key = models.CharField(max_length=50, verbose_name="선택 키")
    display_order = models.IntegerField(default=0, verbose_name="노출 순서")

    class Meta:
        ordering = ["display_order"]
        verbose_name = "선택지"
        verbose_name_plural = "선택지 목록"

    def __str__(self):
        return f"{self.question} → {self.label}"
