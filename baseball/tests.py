from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status

from .models import Team, TeamTag, Question, Choice
from .algorithm import (
    _slider_to_tag_weights,
    _build_user_team_vector,
    _dot_product_team,
    _classify_persona,
    recommend_teams,
    TEAM_TAG_FIELDS,
)


# ── 헬퍼 ────────────────────────────────────────────────────────────────────

def _zero_vector():
    return {tag: 0 for tag in TEAM_TAG_FIELDS}


def _make_team(name, region, **tag_kwargs):
    """팀 + 태그를 생성하고 select_related된 인스턴스를 반환."""
    defaults = {t: 0 for t in TEAM_TAG_FIELDS}
    defaults.update(tag_kwargs)
    team = Team.objects.create(name=name, region=region, stadium=f"{region}구장")
    TeamTag.objects.create(team=team, **defaults)
    return Team.objects.select_related("tag").get(pk=team.pk)


# ── 1. 슬라이더 → 태그 점수 변환 ────────────────────────────────────────────

class SliderToTagWeightsTest(TestCase):

    def test_left_extreme_gives_4(self):
        # 값 1 → 왼쪽 태그에 |1-3|*2 = 4점
        result = _slider_to_tag_weights(1, 1)
        self.assertEqual(result, {"passion": 4})

    def test_right_extreme_gives_4(self):
        # 값 5 → 오른쪽 태그에 4점
        result = _slider_to_tag_weights(1, 5)
        self.assertEqual(result, {"stable": 4})

    def test_neutral_gives_empty(self):
        # 값 3 → 중립, 빈 dict
        result = _slider_to_tag_weights(1, 3)
        self.assertEqual(result, {})

    def test_left_mild_gives_2(self):
        # 값 2 → 왼쪽 태그에 |2-3|*2 = 2점
        result = _slider_to_tag_weights(1, 2)
        self.assertEqual(result, {"passion": 2})

    def test_right_mild_gives_2(self):
        # 값 4 → 오른쪽 태그에 2점
        result = _slider_to_tag_weights(1, 4)
        self.assertEqual(result, {"stable": 2})

    def test_q12_not_in_map_returns_empty(self):
        # Q12(지역)는 슬라이더 맵에서 제외
        result = _slider_to_tag_weights(12, 1)
        self.assertEqual(result, {})

    def test_unknown_question_returns_empty(self):
        result = _slider_to_tag_weights(99, 5)
        self.assertEqual(result, {})


# ── 2. 사용자 태그 벡터 생성 ─────────────────────────────────────────────────

class BuildUserTeamVectorTest(TestCase):

    def test_empty_answers_all_zero(self):
        vector = _build_user_team_vector({})
        self.assertEqual(sum(vector.values()), 0)

    def test_all_neutral_all_zero(self):
        vector = _build_user_team_vector({q: 3 for q in range(1, 12)})
        self.assertEqual(sum(vector.values()), 0)

    def test_q1_left_adds_passion(self):
        vector = _build_user_team_vector({1: 1})
        self.assertEqual(vector["passion"], 4)
        self.assertEqual(vector["stable"], 0)

    def test_q1_right_adds_stable(self):
        vector = _build_user_team_vector({1: 5})
        self.assertEqual(vector["passion"], 0)
        self.assertEqual(vector["stable"], 4)

    def test_string_keys_handled(self):
        # 프론트에서 JSON key가 문자열로 올 수 있음
        vector = _build_user_team_vector({"1": 1})
        self.assertEqual(vector["passion"], 4)

    def test_multiple_questions_accumulate(self):
        # Q1 left(passion+4) + Q9 left(passion+4) → passion 8
        vector = _build_user_team_vector({1: 1, 9: 1})
        self.assertEqual(vector["passion"], 8)

    def test_all_tag_fields_present(self):
        vector = _build_user_team_vector({})
        for tag in TEAM_TAG_FIELDS:
            self.assertIn(tag, vector)


# ── 3. 팀 태그 벡터와 내적 계산 ───────────────────────────────────────────────

class DotProductTeamTest(TestCase):

    def setUp(self):
        self.team = _make_team("테스트팀", "서울", passion=5)

    def test_single_matching_tag(self):
        user_vector = _zero_vector()
        user_vector["passion"] = 4
        score = _dot_product_team(user_vector, self.team)
        self.assertEqual(score, 20)  # 4 * 5

    def test_zero_user_vector_gives_zero(self):
        score = _dot_product_team(_zero_vector(), self.team)
        self.assertEqual(score, 0)

    def test_no_tag_returns_zero(self):
        team_no_tag = Team.objects.create(name="태그없음팀", region="서울", stadium="구장")
        user_vector = _zero_vector()
        user_vector["passion"] = 4
        score = _dot_product_team(user_vector, team_no_tag)
        self.assertEqual(score, 0)


# ── 4. 페르소나 분류 ──────────────────────────────────────────────────────────

class ClassifyPersonaTest(TestCase):

    def _vec(self, **kwargs):
        v = _zero_vector()
        v.update(kwargs)
        return v

    def test_dramatic_persona(self):
        persona = _classify_persona(self._vec(story=10, emotional=10, dramatic=10))
        self.assertEqual(persona, "낭만 드라마 추구형")

    def test_winning_persona(self):
        persona = _classify_persona(self._vec(winning=10, trendy=10, popular=10))
        self.assertEqual(persona, "세련된 강팀 팬")

    def test_underdog_persona(self):
        persona = _classify_persona(self._vec(underdog=10, loyalty=10))
        self.assertEqual(persona, "언더독 충성 팬")

    def test_traditional_persona(self):
        persona = _classify_persona(self._vec(traditional=10, loyalty=10))
        self.assertEqual(persona, "명문 DNA 추구형")

    def test_analytic_persona(self):
        persona = _classify_persona(self._vec(analytic=10))
        self.assertEqual(persona, "데이터 야구 신봉자")

    def test_returns_string(self):
        persona = _classify_persona(_zero_vector())
        self.assertIsInstance(persona, str)


# ── 5. recommend_teams() 전체 파이프라인 ─────────────────────────────────────

class RecommendTeamsTest(TestCase):

    def setUp(self):
        # 롯데 스타일: 열정·드라마틱 높음
        self.lotte = _make_team("롯데 자이언츠", "부산",
                                passion=5, fan_culture=5, story=5,
                                emotional=5, dramatic=5, winning=2)
        # NC 스타일: 분석·안정 높음
        self.nc = _make_team("NC 다이노스", "창원",
                             analytic=5, stable=3, winning=3)

    def _qs(self):
        return Team.objects.select_related("tag").all()

    def test_returns_all_teams_if_less_than_3(self):
        top3, _ = recommend_teams({q: 3 for q in range(1, 12)}, "상관없다", self._qs())
        self.assertEqual(len(top3), 2)

    def test_dramatic_user_prefers_lotte(self):
        # Q6 오른쪽(story+4), Q11 오른쪽(dramatic+4), Q4 왼쪽(emotional+4)
        answers = {1: 3, 2: 3, 3: 3, 4: 1, 5: 3, 6: 5, 7: 3, 8: 3, 9: 3, 10: 3, 11: 5}
        top3, _ = recommend_teams(answers, "상관없다", self._qs())
        self.assertEqual(top3[0]["team"].name, "롯데 자이언츠")

    def test_analytic_user_prefers_nc(self):
        # Q9 오른쪽(analytic+4), Q10 오른쪽(analytic+4)
        answers = {1: 3, 2: 3, 3: 3, 4: 3, 5: 3, 6: 3, 7: 3, 8: 3, 9: 5, 10: 5, 11: 3}
        top3, _ = recommend_teams(answers, "상관없다", self._qs())
        self.assertEqual(top3[0]["team"].name, "NC 다이노스")

    def test_region_bonus_raises_lotte_score(self):
        answers = {q: 3 for q in range(1, 12)}
        top_no_bonus, _ = recommend_teams(answers, "상관없다", self._qs())
        top_busan, _ = recommend_teams(answers, "부산", self._qs())

        lotte_no_bonus = next(i["score"] for i in top_no_bonus if i["team"].name == "롯데 자이언츠")
        lotte_busan = next(i["score"] for i in top_busan if i["team"].name == "롯데 자이언츠")
        self.assertGreater(lotte_busan, lotte_no_bonus)

    def test_top_team_match_percent_is_100(self):
        answers = {q: 1 for q in range(1, 12)}
        top3, _ = recommend_teams(answers, "상관없다", self._qs())
        self.assertEqual(top3[0]["match_percent"], 100)

    def test_second_team_percent_lte_100(self):
        answers = {q: 1 for q in range(1, 12)}
        top3, _ = recommend_teams(answers, "상관없다", self._qs())
        if len(top3) >= 2:
            self.assertLessEqual(top3[1]["match_percent"], 100)

    def test_persona_is_string(self):
        _, persona = recommend_teams({q: 3 for q in range(1, 12)}, "상관없다", self._qs())
        self.assertIsInstance(persona, str)
        self.assertGreater(len(persona), 0)


# ── 6. GET /api/questions/team/ ──────────────────────────────────────────────

class TeamQuestionListAPITest(APITestCase):

    def setUp(self):
        q = Question.objects.create(
            quiz_type="team", number=1, category="생활",
            question_text="테스트 질문", input_type="slider",
        )
        Choice.objects.create(question=q, label="왼쪽", key="left", display_order=0)
        Choice.objects.create(question=q, label="오른쪽", key="right", display_order=1)

    def test_status_200(self):
        res = self.client.get("/api/questions/team/")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_returns_list(self):
        res = self.client.get("/api/questions/team/")
        self.assertIsInstance(res.data, list)
        self.assertEqual(len(res.data), 1)

    def test_question_has_choices(self):
        res = self.client.get("/api/questions/team/")
        self.assertIn("choices", res.data[0])
        self.assertEqual(len(res.data[0]["choices"]), 2)

    def test_question_fields_present(self):
        res = self.client.get("/api/questions/team/")
        q = res.data[0]
        for field in ("id", "number", "category", "question_text", "input_type", "choices"):
            self.assertIn(field, q)

    def test_player_questions_excluded(self):
        Question.objects.create(
            quiz_type="player", number=1, category="포지션",
            question_text="선수 질문", input_type="button",
        )
        res = self.client.get("/api/questions/team/")
        for q in res.data:
            self.assertEqual(q["quiz_type"], "team")


# ── 7. POST /api/recommend/team/ ─────────────────────────────────────────────

class TeamRecommendAPITest(APITestCase):

    TEAM_DATA = [
        ("롯데 자이언츠", "부산",  {"passion": 5, "dramatic": 5, "emotional": 5}),
        ("NC 다이노스",   "창원",  {"analytic": 5, "stable": 3}),
        ("LG 트윈스",    "서울",  {"winning": 4, "popular": 5, "trendy": 4}),
    ]

    def setUp(self):
        for name, region, tags in self.TEAM_DATA:
            _make_team(name, region, **tags)

    def _answers(self, value=3):
        return {str(i): value for i in range(1, 12)}

    def test_status_200(self):
        res = self.client.post(
            "/api/recommend/team/",
            {"answers": self._answers(), "region": "상관없다"},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_response_has_top3(self):
        res = self.client.post(
            "/api/recommend/team/",
            {"answers": self._answers(), "region": "상관없다"},
            format="json",
        )
        self.assertIn("recommendations", res.data)
        self.assertEqual(len(res.data["recommendations"]), 3)

    def test_response_has_persona(self):
        res = self.client.post(
            "/api/recommend/team/",
            {"answers": self._answers(), "region": "상관없다"},
            format="json",
        )
        self.assertIn("persona", res.data)
        self.assertIsInstance(res.data["persona"], str)

    def test_recommendation_structure(self):
        res = self.client.post(
            "/api/recommend/team/",
            {"answers": self._answers(), "region": "상관없다"},
            format="json",
        )
        rec = res.data["recommendations"][0]
        self.assertEqual(rec["rank"], 1)
        self.assertIn("match_percent", rec)
        self.assertIn("team", rec)
        self.assertIn("name", rec["team"])

    def test_rank_order_is_sequential(self):
        res = self.client.post(
            "/api/recommend/team/",
            {"answers": self._answers(), "region": "상관없다"},
            format="json",
        )
        ranks = [r["rank"] for r in res.data["recommendations"]]
        self.assertEqual(ranks, [1, 2, 3])

    def test_region_busan_boosts_lotte(self):
        res = self.client.post(
            "/api/recommend/team/",
            {"answers": self._answers(), "region": "부산"},
            format="json",
        )
        first_team = res.data["recommendations"][0]["team"]["name"]
        self.assertEqual(first_team, "롯데 자이언츠")

    def test_empty_answers_returns_400(self):
        res = self.client.post(
            "/api/recommend/team/",
            {"answers": {}, "region": "상관없다"},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_missing_answers_returns_400(self):
        res = self.client.post(
            "/api/recommend/team/",
            {"region": "상관없다"},
            format="json",
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_top1_match_percent_is_100(self):
        res = self.client.post(
            "/api/recommend/team/",
            {"answers": self._answers(value=1), "region": "상관없다"},
            format="json",
        )
        self.assertEqual(res.data["recommendations"][0]["match_percent"], 100)
