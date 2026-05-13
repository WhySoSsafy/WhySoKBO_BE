"""
팀/선수 추천 알고리즘 (태그 벡터 내적 기반)
"""

TEAM_TAG_FIELDS = [
    'tag_passion', 'tag_fan_culture', 'tag_story', 'tag_emotional',
    'tag_dramatic', 'tag_winning', 'tag_stable', 'tag_traditional',
    'tag_loyalty', 'tag_trendy', 'tag_popular', 'tag_underdog', 'tag_analytic',
]

PLAYER_TAG_FIELDS = [
    'tag_power', 'tag_contact', 'tag_speed', 'tag_defense',
    'tag_ace', 'tag_closer', 'tag_clutch', 'tag_consistent',
    'tag_charisma', 'tag_leader', 'tag_young', 'tag_underdog', 'tag_foreign',
]

# Q번호 → (왼쪽 태그, 오른쪽 태그) 매핑 (슬라이더 값 1=왼쪽, 5=오른쪽)
TEAM_QUESTION_TAG_MAP = {
    1:  ('tag_passion',      'tag_stable'),
    2:  ('tag_passion',      'tag_consistent'),
    3:  ('tag_trendy',       'tag_traditional'),
    4:  ('tag_emotional',    'tag_stable'),
    5:  ('tag_popular',      'tag_underdog'),
    6:  ('tag_winning',      'tag_story'),
    7:  ('tag_winning',      'tag_underdog'),
    8:  ('tag_traditional',  'tag_trendy'),
    9:  ('tag_passion',      'tag_analytic'),
    10: ('tag_winning',      'tag_analytic'),
    11: ('tag_stable',       'tag_dramatic'),
    # Q12(지역)은 보너스 처리 — 이 맵에서 제외
}

# 페르소나 분류 규칙 (사용자 태그 벡터 기준 상위 태그로 판별)
PERSONA_RULES = [
    {
        'name': '낭만 드라마 추구형',
        'tags': ['tag_story', 'tag_emotional', 'tag_dramatic'],
    },
    {
        'name': '언더독 충성 팬',
        'tags': ['tag_underdog', 'tag_loyalty'],
    },
    {
        'name': '세련된 강팀 팬',
        'tags': ['tag_winning', 'tag_trendy', 'tag_popular'],
    },
    {
        'name': '명문 DNA 추구형',
        'tags': ['tag_traditional', 'tag_loyalty'],
    },
    {
        'name': '데이터 야구 신봉자',
        'tags': ['tag_analytic'],
    },
    {
        'name': '합리적 스마트 팬',
        'tags': ['tag_stable', 'tag_analytic'],
    },
]

# 지역 → 팀명 매핑 (Q12 지역 보너스용)
REGION_TEAM_MAP = {
    '서울': ['LG 트윈스', '두산 베어스', '키움 히어로즈'],
    '수도권': ['LG 트윈스', '두산 베어스', '키움 히어로즈', 'SSG 랜더스', 'kt wiz'],
    '부산': ['롯데 자이언츠'],
    '대구': ['삼성 라이온즈'],
    '광주': ['KIA 타이거즈'],
    '대전': ['한화 이글스'],
    '인천': ['SSG 랜더스'],
    '수원': ['kt wiz'],
    '창원': ['NC 다이노스'],
}

REGION_BONUS = 5  # 지역 보너스 점수 (최종에 ×0.5 적용)


def _slider_to_tag_weights(question_number, slider_value):
    """슬라이더 값을 태그 가중치 딕셔너리로 변환"""
    if question_number not in TEAM_QUESTION_TAG_MAP:
        return {}
    left_tag, right_tag = TEAM_QUESTION_TAG_MAP[question_number]
    if slider_value == 3:
        return {}
    weight = (3 - slider_value) * 1 if slider_value < 3 else (slider_value - 3) * 1
    weight = weight * 2 // 2  # 1~2점 가중치
    if slider_value < 3:
        return {left_tag: weight * 2}
    else:
        return {right_tag: weight * 2}


def _build_user_team_vector(answers):
    """
    answers: {question_number(int): slider_value(1~5), ...}
    반환: {tag_field: score, ...}
    """
    user_vector = {tag: 0 for tag in TEAM_TAG_FIELDS}
    for q_num, value in answers.items():
        weights = _slider_to_tag_weights(int(q_num), int(value))
        for tag, score in weights.items():
            user_vector[tag] = user_vector.get(tag, 0) + score
    return user_vector


def _dot_product_team(user_vector, team):
    """사용자 벡터와 팀 태그 벡터의 내적합"""
    score = 0
    for tag in TEAM_TAG_FIELDS:
        score += user_vector.get(tag, 0) * getattr(team, tag, 0)
    return score


def _classify_persona(user_vector):
    """사용자 태그 벡터로 야구 페르소나 분류"""
    best_persona = '합리적 스마트 팬'
    best_score = -1
    for rule in PERSONA_RULES:
        score = sum(user_vector.get(tag, 0) for tag in rule['tags'])
        if score > best_score:
            best_score = score
            best_persona = rule['name']
    return best_persona


def recommend_teams(answers, region, teams):
    """
    팀 추천 알고리즘
    - answers: {str(question_number): int(slider_value 1~5)}
    - region: str (Q12 지역 선택, '서울' | '부산' | ... | '상관없다')
    - teams: Team 모델 QuerySet
    반환: [{'team': Team, 'score': int, 'match_percent': int}, ...] TOP3
    """
    user_vector = _build_user_team_vector(answers)

    scores = []
    bonus_teams = REGION_TEAM_MAP.get(region, [])

    for team in teams:
        base_score = _dot_product_team(user_vector, team)
        bonus = REGION_BONUS * 0.5 if team.name in bonus_teams else 0
        total = base_score + bonus
        scores.append({'team': team, 'score': total})

    scores.sort(key=lambda x: x['score'], reverse=True)

    top_score = scores[0]['score'] if scores and scores[0]['score'] > 0 else 1
    for item in scores:
        item['match_percent'] = round(item['score'] / top_score * 100) if top_score > 0 else 0

    persona = _classify_persona(user_vector)
    return scores[:3], persona


# ─── 선수 추천 ───────────────────────────────────────────────────────────────

# Q1 포지션 → 사전 가중치 태그
POSITION_WEIGHTS = {
    '타자':    {'tag_power': 1, 'tag_contact': 1, 'tag_speed': 1, 'tag_defense': 1},
    '선발투수': {'tag_ace': 1, 'tag_consistent': 1},
    '마무리':  {'tag_closer': 1, 'tag_clutch': 1},
    '상관없다': {},
}

# Q2 타자 스타일 선택지 → 태그
Q2_CHOICES = {
    '홈런':   {'tag_power': 2},
    '안타':   {'tag_contact': 2},
    '도루':   {'tag_speed': 2},
    '수비':   {'tag_defense': 2},
}

# Q3 투수 스타일 선택지 → 태그
Q3_CHOICES = {
    '에이스':  {'tag_ace': 2},
    '마무리':  {'tag_closer': 2},
    '빠른공':  {'tag_clutch': 2},
    '변화구':  {'tag_consistent': 2},
}

# Q4 활약 상황
Q4_CHOICES = {
    '결정적': {'tag_clutch': 2},
    '꾸준히': {'tag_consistent': 2},
}

# Q5 커리어 서사
Q5_CHOICES = {
    '자수성가': {'tag_underdog': 2},
    '엘리트':   {'tag_charisma': 2},
    '베테랑':   {'tag_leader': 2},
    '외국인':   {'tag_foreign': 2},
}

# Q6 커리어 단계
Q6_CHOICES = {
    '유망주':  {'tag_young': 2},
    '전성기':  {'tag_clutch': 1, 'tag_charisma': 1},
    '베테랑':  {'tag_leader': 2},
}

# Q7 응원 기준
Q7_CHOICES = {
    '카리스마': {'tag_charisma': 2},
    '기록':    {'tag_consistent': 2},
    '인간적':  {'tag_underdog': 1, 'tag_leader': 1},
    '화려한':  {'tag_clutch': 1, 'tag_power': 1},
}

# 선택지 키워드 → 태그 맵 (Q번호별)
PLAYER_CHOICE_MAP = {
    2: Q2_CHOICES,
    3: Q3_CHOICES,
    4: Q4_CHOICES,
    5: Q5_CHOICES,
    6: Q6_CHOICES,
    7: Q7_CHOICES,
}


def _build_user_player_vector(position, player_answers):
    """
    position: str ('타자' | '선발투수' | '마무리' | '상관없다')
    player_answers: {question_number(int): choice_keyword(str), ...}
    반환: {tag_field: score, ...}
    """
    user_vector = {tag: 0 for tag in PLAYER_TAG_FIELDS}

    for tag, weight in POSITION_WEIGHTS.get(position, {}).items():
        user_vector[tag] = user_vector.get(tag, 0) + weight

    for q_num, keyword in player_answers.items():
        choice_map = PLAYER_CHOICE_MAP.get(int(q_num), {})
        weights = choice_map.get(keyword, {})
        for tag, score in weights.items():
            user_vector[tag] = user_vector.get(tag, 0) + score

    return user_vector


def _dot_product_player(user_vector, player):
    score = 0
    for tag in PLAYER_TAG_FIELDS:
        score += user_vector.get(tag, 0) * getattr(player, tag, 0)
    return score


def recommend_players(position, player_answers, players):
    """
    선수 추천 알고리즘
    - position: str
    - player_answers: {str(q_num): str(keyword)}
    - players: 추천 팀 소속 Player QuerySet
    반환: [{'player': Player, 'score': int, 'match_percent': int}, ...] TOP2
    """
    user_vector = _build_user_player_vector(position, player_answers)

    scores = []
    for player in players:
        score = _dot_product_player(user_vector, player)
        scores.append({'player': player, 'score': score})

    scores.sort(key=lambda x: x['score'], reverse=True)

    top_score = scores[0]['score'] if scores and scores[0]['score'] > 0 else 1
    for item in scores:
        item['match_percent'] = round(item['score'] / top_score * 100) if top_score > 0 else 0

    return scores[:2]
