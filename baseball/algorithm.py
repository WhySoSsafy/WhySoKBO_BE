"""
팀/선수 추천 알고리즘 (태그 벡터 내적 기반)
TeamTag / PlayerTag 모델의 필드명(prefix 없음)에 맞춤
"""

TEAM_TAG_FIELDS = [
    'passion', 'fan_culture', 'story', 'emotional',
    'dramatic', 'winning', 'stable', 'traditional',
    'loyalty', 'trendy', 'popular', 'underdog', 'analytic',
]

PLAYER_TAG_FIELDS = [
    'power', 'contact', 'speed', 'defense',
    'ace', 'closer', 'clutch', 'consistent',
    'charisma', 'leader', 'young', 'underdog', 'foreign',
]

# Q번호 → (왼쪽 태그, 오른쪽 태그) 매핑 (슬라이더 값 1=왼쪽, 5=오른쪽)
TEAM_QUESTION_TAG_MAP = {
    1:  ('passion',     'stable'),
    2:  ('passion',     'stable'),
    3:  ('trendy',      'traditional'),
    4:  ('emotional',   'stable'),
    5:  ('popular',     'underdog'),
    6:  ('winning',     'story'),
    7:  ('winning',     'underdog'),
    8:  ('traditional', 'trendy'),
    9:  ('passion',     'analytic'),
    10: ('winning',     'analytic'),
    11: ('stable',      'dramatic'),
    # Q12(지역)은 보너스 처리 — 이 맵에서 제외
}

PERSONA_RULES = [
    {'name': '낭만 드라마 추구형',  'tags': ['story', 'emotional', 'dramatic']},
    {'name': '언더독 충성 팬',      'tags': ['underdog', 'loyalty']},
    {'name': '세련된 강팀 팬',      'tags': ['winning', 'trendy', 'popular']},
    {'name': '명문 DNA 추구형',     'tags': ['traditional', 'loyalty']},
    {'name': '데이터 야구 신봉자',  'tags': ['analytic']},
    {'name': '합리적 스마트 팬',    'tags': ['stable', 'analytic']},
]

REGION_TEAM_MAP = {
    '서울':   ['LG 트윈스', '두산 베어스', '키움 히어로즈'],
    '수도권': ['LG 트윈스', '두산 베어스', '키움 히어로즈', 'SSG 랜더스', 'kt wiz'],
    '부산':   ['롯데 자이언츠'],
    '대구':   ['삼성 라이온즈'],
    '광주':   ['KIA 타이거즈'],
    '대전':   ['한화 이글스'],
    '인천':   ['SSG 랜더스'],
    '수원':   ['kt wiz'],
    '창원':   ['NC 다이노스'],
}

REGION_BONUS = 5


def _slider_to_tag_weights(question_number, slider_value):
    if question_number not in TEAM_QUESTION_TAG_MAP:
        return {}
    left_tag, right_tag = TEAM_QUESTION_TAG_MAP[question_number]
    if slider_value == 3:
        return {}
    weight = abs(slider_value - 3) * 2
    if slider_value < 3:
        return {left_tag: weight}
    return {right_tag: weight}


def _build_user_team_vector(answers):
    """answers: {question_number(int): slider_value(1~5), ...}"""
    user_vector = {tag: 0 for tag in TEAM_TAG_FIELDS}
    for q_num, value in answers.items():
        weights = _slider_to_tag_weights(int(q_num), int(value))
        for tag, score in weights.items():
            user_vector[tag] = user_vector.get(tag, 0) + score
    return user_vector


def _dot_product_team(user_vector, team):
    score = 0
    tag_obj = getattr(team, 'tag', None)
    if tag_obj is None:
        return 0
    for tag in TEAM_TAG_FIELDS:
        score += user_vector.get(tag, 0) * getattr(tag_obj, tag, 0)
    return score


def _classify_persona(user_vector):
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
    teams: Team QuerySet (select_related('tag') 권장)
    반환: ([{'team', 'score', 'match_percent'}, ...] TOP3, persona)
    """
    user_vector = _build_user_team_vector(answers)
    bonus_teams = REGION_TEAM_MAP.get(region, [])

    scores = []
    for team in teams:
        base_score = _dot_product_team(user_vector, team)
        bonus = REGION_BONUS * 0.5 if team.name in bonus_teams else 0
        scores.append({'team': team, 'score': base_score + bonus})

    scores.sort(key=lambda x: x['score'], reverse=True)

    top_score = scores[0]['score'] if scores and scores[0]['score'] > 0 else 1
    for item in scores:
        item['match_percent'] = round(item['score'] / top_score * 100) if top_score > 0 else 0

    persona = _classify_persona(user_vector)
    return scores[:3], persona


# ─── 선수 추천 ───────────────────────────────────────────────────────────────

POSITION_WEIGHTS = {
    '타자':    {'power': 1, 'contact': 1, 'speed': 1, 'defense': 1},
    '선발투수': {'ace': 1, 'consistent': 1},
    '마무리':  {'closer': 1, 'clutch': 1},
    '상관없다': {},
}

PLAYER_CHOICE_MAP = {
    2: {'홈런': {'power': 2},   '안타': {'contact': 2}, '도루': {'speed': 2},  '수비': {'defense': 2}},
    3: {'에이스': {'ace': 2},   '마무리': {'closer': 2}, '빠른공': {'clutch': 2}, '변화구': {'consistent': 2}},
    4: {'결정적': {'clutch': 2}, '꾸준히': {'consistent': 2}},
    5: {'자수성가': {'underdog': 2}, '엘리트': {'charisma': 2}, '베테랑': {'leader': 2}, '외국인': {'foreign': 2}},
    6: {'유망주': {'young': 2},  '전성기': {'clutch': 1, 'charisma': 1}, '베테랑': {'leader': 2}},
    7: {'카리스마': {'charisma': 2}, '기록': {'consistent': 2}, '인간적': {'underdog': 1, 'leader': 1}, '화려한': {'clutch': 1, 'power': 1}},
}


def _build_user_player_vector(position, player_answers):
    user_vector = {tag: 0 for tag in PLAYER_TAG_FIELDS}
    for tag, weight in POSITION_WEIGHTS.get(position, {}).items():
        user_vector[tag] = user_vector.get(tag, 0) + weight
    for q_num, keyword in player_answers.items():
        weights = PLAYER_CHOICE_MAP.get(int(q_num), {}).get(keyword, {})
        for tag, score in weights.items():
            user_vector[tag] = user_vector.get(tag, 0) + score
    return user_vector


def _dot_product_player(user_vector, player):
    score = 0
    tag_obj = getattr(player, 'tag', None)
    if tag_obj is None:
        return 0
    for tag in PLAYER_TAG_FIELDS:
        score += user_vector.get(tag, 0) * getattr(tag_obj, tag, 0)
    return score


def recommend_players(position, player_answers, players):
    """
    players: Player QuerySet (select_related('tag') 권장)
    반환: [{'player', 'score', 'match_percent'}, ...] TOP2
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
