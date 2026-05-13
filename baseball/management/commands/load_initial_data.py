"""
초기 데이터 로드 커맨드
사용: python manage.py load_initial_data
"""
from django.core.management.base import BaseCommand
from baseball.models import Team, Player, TeamQuestion, PlayerQuestion


TEAMS = [
    dict(name="LG 트윈스",    region="서울",  tag_passion=3, tag_fan_culture=3, tag_story=2, tag_emotional=2, tag_dramatic=2, tag_winning=4, tag_stable=4, tag_traditional=3, tag_loyalty=3, tag_trendy=4, tag_popular=5, tag_underdog=1, tag_analytic=2),
    dict(name="두산 베어스",   region="서울",  tag_passion=2, tag_fan_culture=3, tag_story=3, tag_emotional=2, tag_dramatic=2, tag_winning=3, tag_stable=4, tag_traditional=5, tag_loyalty=4, tag_trendy=2, tag_popular=3, tag_underdog=2, tag_analytic=3),
    dict(name="KIA 타이거즈",  region="광주",  tag_passion=4, tag_fan_culture=5, tag_story=4, tag_emotional=4, tag_dramatic=3, tag_winning=4, tag_stable=3, tag_traditional=5, tag_loyalty=5, tag_trendy=3, tag_popular=4, tag_underdog=2, tag_analytic=2),
    dict(name="삼성 라이온즈", region="대구",  tag_passion=2, tag_fan_culture=2, tag_story=2, tag_emotional=2, tag_dramatic=2, tag_winning=3, tag_stable=5, tag_traditional=5, tag_loyalty=4, tag_trendy=2, tag_popular=3, tag_underdog=2, tag_analytic=3),
    dict(name="롯데 자이언츠", region="부산",  tag_passion=5, tag_fan_culture=5, tag_story=5, tag_emotional=5, tag_dramatic=5, tag_winning=2, tag_stable=1, tag_traditional=3, tag_loyalty=4, tag_trendy=3, tag_popular=3, tag_underdog=3, tag_analytic=2),
    dict(name="한화 이글스",   region="대전",  tag_passion=4, tag_fan_culture=3, tag_story=5, tag_emotional=5, tag_dramatic=4, tag_winning=2, tag_stable=2, tag_traditional=3, tag_loyalty=5, tag_trendy=2, tag_popular=2, tag_underdog=5, tag_analytic=2),
    dict(name="SSG 랜더스",    region="인천",  tag_passion=3, tag_fan_culture=3, tag_story=3, tag_emotional=3, tag_dramatic=2, tag_winning=4, tag_stable=3, tag_traditional=1, tag_loyalty=3, tag_trendy=5, tag_popular=4, tag_underdog=2, tag_analytic=2),
    dict(name="kt wiz",        region="수원",  tag_passion=2, tag_fan_culture=2, tag_story=2, tag_emotional=2, tag_dramatic=2, tag_winning=3, tag_stable=4, tag_traditional=2, tag_loyalty=3, tag_trendy=3, tag_popular=2, tag_underdog=2, tag_analytic=4),
    dict(name="NC 다이노스",   region="창원",  tag_passion=2, tag_fan_culture=2, tag_story=2, tag_emotional=2, tag_dramatic=2, tag_winning=3, tag_stable=3, tag_traditional=2, tag_loyalty=2, tag_trendy=3, tag_popular=2, tag_underdog=2, tag_analytic=5),
    dict(name="키움 히어로즈", region="서울",  tag_passion=3, tag_fan_culture=2, tag_story=3, tag_emotional=2, tag_dramatic=2, tag_winning=2, tag_stable=2, tag_traditional=2, tag_loyalty=3, tag_trendy=2, tag_popular=2, tag_underdog=5, tag_analytic=4),
]

TEAM_QUESTIONS = [
    dict(number=1,  category="생활",      question_text="스트레스가 쌓이면 나는 보통 어떻게 푸나요?",                  left_choice="친구들이랑 소리 지르며 논다",          right_choice="혼자 조용히 생각을 정리한다"),
    dict(number=2,  category="생활",      question_text="팀 프로젝트를 할 때 나는 어떤 스타일인가요?",                  left_choice="아이디어 내고 분위기를 이끈다",         right_choice="묵묵히 내 역할만 완벽하게 한다"),
    dict(number=3,  category="생활",      question_text="여행을 간다면 어떤 여행이 더 끌리나요?",                       left_choice="핫플·맛집 활기찬 도심",                right_choice="조용한 자연·역사 있는 곳"),
    dict(number=4,  category="생활",      question_text="응원하는 쪽이 지면 어떤 편인가요?",                            left_choice="감정이 상해 한동안 기억에 남는다",     right_choice="아쉽지만 금방 털어내는 편이다"),
    dict(number=5,  category="생활",      question_text="새로운 것을 선택할 때 나는 어떻게 하나요?",                    left_choice="남들이 좋다는 걸 믿고 따라간다",       right_choice="남들이 안 고르는 쪽에 끌린다"),
    dict(number=6,  category="가치관",    question_text="스포츠를 볼 때 무엇이 더 중요한가요?",                         left_choice="무조건 이기는 게 최고다",              right_choice="지더라도 서사와 과정이 중요하다"),
    dict(number=7,  category="가치관",    question_text="어떤 팀을 오래 응원하고 싶은가요?",                            left_choice="매년 우승권에 있는 강팀",              right_choice="약하지만 성장하는 팀"),
    dict(number=8,  category="가치관",    question_text="팀의 역사·전통이 얼마나 중요한가요?",                          left_choice="역사와 전통이 있어야 믿음직하다",      right_choice="역사보다 지금 잘하면 된다"),
    dict(number=9,  category="가치관",    question_text="응원할 때 어떤 분위기를 좋아하나요?",                          left_choice="다 같이 소리 지르는 뜨거운 응원",      right_choice="조용히 경기에 집중하는 분위기"),
    dict(number=10, category="경기스타일", question_text="어떤 야구 경기가 더 재미있을 것 같나요?",                      left_choice="홈런 터지는 시원한 타격전",            right_choice="0점 싸움 쫄깃한 투수전"),
    dict(number=11, category="경기스타일", question_text="경기 막판 어느 쪽이 더 두근거리나요?",                        left_choice="7회부터 리드 지키며 마무리",           right_choice="9회 역전 드라마틱한 결말"),
    dict(number=12, category="지역",      question_text="야구장 가기 편한 지역은?",                                     left_choice="서울/수도권/부산/대구/광주/대전",      right_choice="상관없다"),
]

PLAYER_QUESTIONS = [
    dict(
        number=1, category="포지션",
        question_text="어떤 포지션 선수를 응원하고 싶나요?",
        choices=[
            {"label": "타자 (공 치는 선수)",       "key": "타자"},
            {"label": "선발투수 (경기 시작하는 투수)", "key": "선발투수"},
            {"label": "마무리 (끝 막는 투수)",       "key": "마무리"},
            {"label": "상관없다",                    "key": "상관없다"},
        ]
    ),
    dict(
        number=2, category="타자스타일",
        question_text="타자라면 어떤 타격이 더 짜릿할 것 같나요? (타자 선택 시만 노출)",
        choices=[
            {"label": "펑! 담장 넘기는 홈런",          "key": "홈런"},
            {"label": "툭툭 안타로 출루하는 스타일",     "key": "안타"},
            {"label": "빠른 발로 도루",                  "key": "도루"},
            {"label": "수비가 화려한 선수",              "key": "수비"},
        ]
    ),
    dict(
        number=3, category="투수스타일",
        question_text="투수라면 어떤 스타일이 더 멋있어 보이나요? (투수 선택 시만 노출)",
        choices=[
            {"label": "9이닝 혼자 막는 에이스",          "key": "에이스"},
            {"label": "위기 때 나오는 마무리",            "key": "마무리"},
            {"label": "빠른 공으로 삼진",                 "key": "빠른공"},
            {"label": "변화구로 요리하는 스타일",         "key": "변화구"},
        ]
    ),
    dict(
        number=4, category="활약상황",
        question_text="어떤 경기 상황에서 활약하는 선수가 더 끌리나요?",
        choices=[
            {"label": "결정적 순간에 터뜨리는 선수",     "key": "결정적"},
            {"label": "매경기 꾸준히 잘하는 선수",       "key": "꾸준히"},
        ]
    ),
    dict(
        number=5, category="커리어서사",
        question_text="선수의 커리어 스토리 중 어떤 서사가 더 좋나요?",
        choices=[
            {"label": "고졸·저지명으로 자수성가한 선수", "key": "자수성가"},
            {"label": "어릴 때부터 주목받은 엘리트",     "key": "엘리트"},
            {"label": "오랜 경험의 베테랑",               "key": "베테랑"},
            {"label": "외국에서 온 외국인 선수",          "key": "외국인"},
        ]
    ),
    dict(
        number=6, category="커리어단계",
        question_text="선수의 나이와 커리어 단계 중 어디가 더 끌리나요?",
        choices=[
            {"label": "20대 초반 — 성장 지켜보는 재미",      "key": "유망주"},
            {"label": "전성기 20대 후반~30대 초반",          "key": "전성기"},
            {"label": "30대 중반 이상 — 베테랑의 연륜",      "key": "베테랑"},
        ]
    ),
    dict(
        number=7, category="응원기준",
        question_text="응원할 선수를 고를 때 가장 중요한 건 뭔가요?",
        choices=[
            {"label": "팀을 이끄는 존재감·카리스마",  "key": "카리스마"},
            {"label": "기록과 성적",                   "key": "기록"},
            {"label": "경기장 밖 인간적인 모습",       "key": "인간적"},
            {"label": "화려한 플레이 장면",            "key": "화려한"},
        ]
    ),
]

# 팀별 선수 데이터
PLAYERS = {
    "LG 트윈스": [
        dict(name_ko="오스틴 딘", number=7, position="외야수",
             tag_power=5, tag_contact=3, tag_speed=2, tag_defense=2, tag_ace=0, tag_closer=0,
             tag_clutch=4, tag_consistent=3, tag_charisma=3, tag_leader=2, tag_young=1, tag_underdog=1, tag_foreign=5,
             stats={"avg": ".285", "hr": 25, "rbi": 80, "ops": ".850"},
             intro="LG의 클린업 외국인 파워 타자",
             story="미국 출신으로 LG에서 강력한 장타력을 발휘하는 주포. 득점권에서 집중력이 돋보인다.",
             watch_point="득점권 타석에서의 승부근성이 압권입니다",
             cheer="딘 딘 오스틴 딘 홈런을 쳐라",
             stadium_tip="잠실구장 1루 내야석 — 딘의 타석을 정면으로 볼 수 있음"),
        dict(name_ko="홍창기", number=3, position="외야수",
             tag_power=2, tag_contact=5, tag_speed=4, tag_defense=4, tag_ace=0, tag_closer=0,
             tag_clutch=3, tag_consistent=5, tag_charisma=3, tag_leader=3, tag_young=2, tag_underdog=3, tag_foreign=0,
             stats={"avg": ".310", "hr": 5, "rbi": 50, "ops": ".800"},
             intro="정교한 타격과 선구안의 리드오프",
             story="꾸준한 출루율로 LG 타선의 시작점 역할. 고졸 출신으로 성실함으로 주전 자리 잡은 선수.",
             watch_point="1번 타자로서 경기 분위기를 여는 출루 장면",
             cheer="홍창기 홍창기 나가자 나가",
             stadium_tip="잠실구장 외야석 — 홍창기의 수비 장면을 가까이 볼 수 있음"),
        dict(name_ko="임찬규", number=15, position="선발투수",
             tag_power=0, tag_contact=0, tag_speed=0, tag_defense=0, tag_ace=4, tag_closer=2,
             tag_clutch=3, tag_consistent=4, tag_charisma=3, tag_leader=3, tag_young=2, tag_underdog=2, tag_foreign=0,
             stats={"era": "3.85", "ip": "150", "k": 130, "whip": "1.25"},
             intro="LG 선발진의 중심 베테랑 투수",
             story="다양한 구종으로 타자를 요리하는 베테랑. 중요한 경기에서 더욱 빛을 발한다.",
             watch_point="다양한 변화구 조합으로 타자를 무력화하는 투구",
             cheer="임찬규 임찬규 삼진을 잡아라",
             stadium_tip="잠실구장 3루 내야석 — 투수판 근처 공이 잘 보임"),
    ],
    "두산 베어스": [
        dict(name_ko="양석환", number=34, position="1루수",
             tag_power=5, tag_contact=3, tag_speed=1, tag_defense=3, tag_ace=0, tag_closer=0,
             tag_clutch=5, tag_consistent=4, tag_charisma=4, tag_leader=3, tag_young=1, tag_underdog=2, tag_foreign=0,
             stats={"avg": ".275", "hr": 30, "rbi": 95, "ops": ".870"},
             intro="두산의 클린업 홈런타자",
             story="강력한 장타력으로 두산 타선을 이끄는 핵심 선수. 결정적인 순간에 홈런이 나온다.",
             watch_point="풀스윙으로 담장을 넘기는 호쾌한 타구",
             cheer="양석환 양석환 홈런을 쳐라",
             stadium_tip="잠실구장 1루 내야석 — 양석환의 타격 자세를 가까이서 볼 수 있음"),
        dict(name_ko="김재호", number=2, position="유격수",
             tag_power=1, tag_contact=4, tag_speed=3, tag_defense=5, tag_ace=0, tag_closer=0,
             tag_clutch=3, tag_consistent=5, tag_charisma=4, tag_leader=5, tag_young=1, tag_underdog=2, tag_foreign=0,
             stats={"avg": ".265", "hr": 5, "rbi": 45, "ops": ".720"},
             intro="두산의 살아있는 전설, 베테랑 유격수",
             story="두산에서만 20년 가까이 활약한 원클럽맨. 수비와 리더십으로 팀을 이끈다.",
             watch_point="경험에서 나오는 노련한 수비와 주루 플레이",
             cheer="김재호 김재호 두산의 영웅",
             stadium_tip="잠실구장 3루 내야석 — 유격수 수비 장면이 잘 보임"),
        dict(name_ko="곽빈", number=22, position="선발투수",
             tag_power=0, tag_contact=0, tag_speed=0, tag_defense=0, tag_ace=4, tag_closer=1,
             tag_clutch=3, tag_consistent=4, tag_charisma=3, tag_leader=2, tag_young=4, tag_underdog=3, tag_foreign=0,
             stats={"era": "3.50", "ip": "160", "k": 150, "whip": "1.20"},
             intro="두산의 에이스 젊은 투수",
             story="강속구와 날카로운 변화구를 앞세워 두산 선발진의 에이스로 자리 잡은 투수.",
             watch_point="150km대 강속구와 슬라이더의 조합",
             cheer="곽빈 곽빈 삼진왕 곽빈",
             stadium_tip="잠실구장 포수 뒤 구역 — 투구 궤적을 가장 잘 볼 수 있음"),
    ],
    "KIA 타이거즈": [
        dict(name_ko="나성범", number=7, position="외야수",
             tag_power=4, tag_contact=4, tag_speed=3, tag_defense=3, tag_ace=0, tag_closer=0,
             tag_clutch=5, tag_consistent=4, tag_charisma=5, tag_leader=4, tag_young=1, tag_underdog=2, tag_foreign=0,
             stats={"avg": ".290", "hr": 20, "rbi": 85, "ops": ".860"},
             intro="KIA의 핵심 클러치 히터",
             story="결정적인 순간 강한 타격으로 팀을 이끄는 KIA의 중심 타자. 전통 명문의 계보를 잇는 선수.",
             watch_point="득점권에서 절대 무너지지 않는 강심장 타격",
             cheer="나성범 나성범 KIA의 영웅",
             stadium_tip="광주챔피언스필드 1루 내야석 — 나성범의 타석을 정면으로 볼 수 있음"),
        dict(name_ko="최형우", number=34, position="지명타자",
             tag_power=4, tag_contact=4, tag_speed=1, tag_defense=1, tag_ace=0, tag_closer=0,
             tag_clutch=5, tag_consistent=5, tag_charisma=5, tag_leader=5, tag_young=1, tag_underdog=1, tag_foreign=0,
             stats={"avg": ".300", "hr": 18, "rbi": 90, "ops": ".880"},
             intro="KIA의 살아있는 전설, 베테랑 타자",
             story="KBO 역사에 남을 안타 기록 보유자. 베테랑으로서 팀의 정신적 지주 역할.",
             watch_point="역대급 선구안과 타격 기술에서 나오는 안타",
             cheer="최형우 최형우 KIA의 레전드",
             stadium_tip="광주챔피언스필드 — KIA 응원석의 뜨거운 열기 체험 필수"),
        dict(name_ko="이의리", number=14, position="선발투수",
             tag_power=0, tag_contact=0, tag_speed=0, tag_defense=0, tag_ace=5, tag_closer=1,
             tag_clutch=4, tag_consistent=4, tag_charisma=4, tag_leader=2, tag_young=5, tag_underdog=2, tag_foreign=0,
             stats={"era": "3.20", "ip": "170", "k": 165, "whip": "1.15"},
             intro="KIA의 차세대 에이스",
             story="강속구와 구위로 타자를 압도하는 젊은 에이스. KIA의 미래를 책임질 간판 투수.",
             watch_point="150km 후반대 강속구로 타자를 제압하는 장면",
             cheer="이의리 이의리 KIA의 에이스",
             stadium_tip="광주챔피언스필드 포수 뒤 구역 — 투구 스피드를 가장 잘 느낄 수 있음"),
    ],
    "삼성 라이온즈": [
        dict(name_ko="구자욱", number=33, position="외야수",
             tag_power=3, tag_contact=5, tag_speed=3, tag_defense=4, tag_ace=0, tag_closer=0,
             tag_clutch=4, tag_consistent=5, tag_charisma=5, tag_leader=4, tag_young=1, tag_underdog=2, tag_foreign=0,
             stats={"avg": ".305", "hr": 15, "rbi": 75, "ops": ".850"},
             intro="삼성의 얼굴, 안정적인 핵심 타자",
             story="꾸준한 성적으로 삼성의 주축을 담당하는 선수. 수비와 타격 모두 수준급인 올라운더.",
             watch_point="넓은 수비 범위와 부드러운 타격 폼",
             cheer="구자욱 구자욱 삼성의 자랑",
             stadium_tip="대구삼성라이온즈파크 1루 내야석 — 구자욱의 외야 수비가 잘 보임"),
        dict(name_ko="피렐라", number=11, position="외야수",
             tag_power=5, tag_contact=3, tag_speed=3, tag_defense=3, tag_ace=0, tag_closer=0,
             tag_clutch=5, tag_consistent=3, tag_charisma=4, tag_leader=2, tag_young=1, tag_underdog=1, tag_foreign=5,
             stats={"avg": ".290", "hr": 28, "rbi": 94, "ops": ".870"},
             intro="결정적 순간에 강한 클러치 외국인 타자",
             story="베네수엘라 출신으로 삼성 클린업의 핵심. 9회 승부처에서 집중력이 폭발한다.",
             watch_point="9회 승부처 타석에서의 집중력과 폭발적인 타구",
             cheer="피렐라 피렐라 날려라 홈런",
             stadium_tip="대구삼성라이온즈파크 1루 내야석 — 피렐라 타석이 정면으로 보임"),
        dict(name_ko="원태인", number=35, position="선발투수",
             tag_power=0, tag_contact=0, tag_speed=0, tag_defense=0, tag_ace=5, tag_closer=1,
             tag_clutch=4, tag_consistent=4, tag_charisma=4, tag_leader=3, tag_young=4, tag_underdog=2, tag_foreign=0,
             stats={"era": "3.10", "ip": "175", "k": 170, "whip": "1.10"},
             intro="삼성의 간판 에이스 투수",
             story="강속구와 완성도 높은 구종으로 KBO 최고의 투수 반열에 오른 삼성의 에이스.",
             watch_point="150km대 강속구와 완벽한 제구의 조화",
             cheer="원태인 원태인 삼진왕 원태인",
             stadium_tip="대구삼성라이온즈파크 포수 뒤 구역 — 투구 폼을 정면으로 볼 수 있음"),
    ],
    "롯데 자이언츠": [
        dict(name_ko="전준우", number=27, position="외야수",
             tag_power=3, tag_contact=4, tag_speed=2, tag_defense=3, tag_ace=0, tag_closer=0,
             tag_clutch=4, tag_consistent=4, tag_charisma=5, tag_leader=5, tag_young=1, tag_underdog=3, tag_foreign=0,
             stats={"avg": ".285", "hr": 14, "rbi": 70, "ops": ".810"},
             intro="부산 갈매기의 영혼, 롯데의 상징",
             story="부산 팬들의 열렬한 사랑을 받는 롯데의 얼굴. 오랜 세월 팬들과 희로애락을 함께한 선수.",
             watch_point="뜨거운 사직구장 분위기 속에서 터지는 적시타",
             cheer="전준우 전준우 부산 갈매기",
             stadium_tip="사직구장 1루 응원석 — 롯데 응원단의 열기를 가장 잘 느낄 수 있음"),
        dict(name_ko="노진혁", number=5, position="유격수",
             tag_power=2, tag_contact=4, tag_speed=4, tag_defense=5, tag_ace=0, tag_closer=0,
             tag_clutch=3, tag_consistent=4, tag_charisma=3, tag_leader=3, tag_young=3, tag_underdog=3, tag_foreign=0,
             stats={"avg": ".270", "hr": 6, "rbi": 45, "ops": ".730"},
             intro="롯데의 수비형 유격수",
             story="화려한 수비로 팬들을 열광시키는 수비형 유격수. 빠른 발로 어려운 타구를 처리해낸다.",
             watch_point="광범위한 수비 범위와 날카로운 송구",
             cheer="노진혁 노진혁 수비왕 노진혁",
             stadium_tip="사직구장 3루 내야석 — 유격수 수비를 가장 가까이서 볼 수 있음"),
        dict(name_ko="박세웅", number=17, position="선발투수",
             tag_power=0, tag_contact=0, tag_speed=0, tag_defense=0, tag_ace=4, tag_closer=1,
             tag_clutch=4, tag_consistent=4, tag_charisma=3, tag_leader=3, tag_young=2, tag_underdog=4, tag_foreign=0,
             stats={"era": "3.70", "ip": "160", "k": 140, "whip": "1.30"},
             intro="롯데 선발진의 에이스",
             story="롯데 팬들의 기대를 짊어지고 마운드에 오르는 에이스. 어려운 상황에서 더욱 강해진다.",
             watch_point="결정적 상황에서 팀을 지키는 투지 넘치는 투구",
             cheer="박세웅 박세웅 롯데의 에이스",
             stadium_tip="사직구장 포수 뒤 구역 — 투수 투구를 정면으로 볼 수 있음"),
    ],
    "한화 이글스": [
        dict(name_ko="노시환", number=36, position="3루수",
             tag_power=5, tag_contact=3, tag_speed=2, tag_defense=3, tag_ace=0, tag_closer=0,
             tag_clutch=5, tag_consistent=3, tag_charisma=4, tag_leader=3, tag_young=5, tag_underdog=4, tag_foreign=0,
             stats={"avg": ".275", "hr": 35, "rbi": 100, "ops": ".900"},
             intro="한화 언더독 서사의 주인공, 홈런왕",
             story="역대급 홈런 페이스로 KBO를 지배하는 젊은 거포. 한화의 미래를 책임질 간판 선수.",
             watch_point="폭발적인 장타력으로 담장을 넘기는 홈런 장면",
             cheer="노시환 노시환 홈런왕 노시환",
             stadium_tip="한화생명이글스파크 1루 내야석 — 노시환의 파워풀한 스윙을 가장 잘 볼 수 있음"),
        dict(name_ko="채은성", number=8, position="외야수",
             tag_power=3, tag_contact=4, tag_speed=2, tag_defense=3, tag_ace=0, tag_closer=0,
             tag_clutch=4, tag_consistent=4, tag_charisma=4, tag_leader=5, tag_young=1, tag_underdog=4, tag_foreign=0,
             stats={"avg": ".280", "hr": 12, "rbi": 65, "ops": ".790"},
             intro="한화의 정신적 지주, 베테랑 리더",
             story="오랜 방황 끝에 한화에서 재기에 성공한 드라마틱한 선수. 팀의 정신적 지주 역할.",
             watch_point="경험에서 우러나오는 노련한 플레이와 리더십",
             cheer="채은성 채은성 한화의 리더",
             stadium_tip="한화생명이글스파크 응원 구역 — 대전의 뜨거운 응원 문화 체험"),
        dict(name_ko="문동주", number=21, position="선발투수",
             tag_power=0, tag_contact=0, tag_speed=0, tag_defense=0, tag_ace=5, tag_closer=1,
             tag_clutch=4, tag_consistent=3, tag_charisma=4, tag_leader=2, tag_young=5, tag_underdog=5, tag_foreign=0,
             stats={"era": "3.40", "ip": "165", "k": 175, "whip": "1.20"},
             intro="한화의 희망, 차세대 에이스",
             story="강력한 구위와 빠른 성장세로 한화 팬들에게 희망을 주는 젊은 에이스 투수.",
             watch_point="150km 후반대 강속구와 날카로운 변화구",
             cheer="문동주 문동주 한화의 에이스",
             stadium_tip="한화생명이글스파크 포수 뒤 구역 — 문동주의 빠른 공을 느낄 수 있음"),
    ],
    "SSG 랜더스": [
        dict(name_ko="최정", number=9, position="3루수",
             tag_power=5, tag_contact=4, tag_speed=2, tag_defense=4, tag_ace=0, tag_closer=0,
             tag_clutch=5, tag_consistent=5, tag_charisma=5, tag_leader=5, tag_young=1, tag_underdog=2, tag_foreign=0,
             stats={"avg": ".285", "hr": 40, "rbi": 110, "ops": ".950"},
             intro="KBO 홈런왕, 살아있는 레전드",
             story="KBO 역대 최다 홈런 기록을 경신한 레전드. SSG의 상징이자 KBO를 대표하는 선수.",
             watch_point="역대급 홈런 기록을 써 내려가는 역사적인 타석",
             cheer="최정 최정 홈런왕 최정",
             stadium_tip="인천SSG랜더스필드 1루 내야석 — 최정의 강력한 타구를 가까이서 볼 수 있음"),
        dict(name_ko="김광현", number=33, position="선발투수",
             tag_power=0, tag_contact=0, tag_speed=0, tag_defense=0, tag_ace=5, tag_closer=1,
             tag_clutch=5, tag_consistent=5, tag_charisma=5, tag_leader=5, tag_young=1, tag_underdog=1, tag_foreign=0,
             stats={"era": "2.80", "ip": "180", "k": 180, "whip": "1.05"},
             intro="KBO 최고의 에이스 투수",
             story="MLB에서 활약 후 돌아온 KBO 최정상급 투수. 완성도 높은 피칭으로 타자를 지배한다.",
             watch_point="완벽한 제구력과 날카로운 변화구로 타자를 요리하는 투구",
             cheer="김광현 김광현 SSG의 에이스",
             stadium_tip="인천SSG랜더스필드 포수 뒤 구역 — 김광현의 완벽한 투구를 정면으로 감상"),
        dict(name_ko="최지훈", number=51, position="외야수",
             tag_power=2, tag_contact=4, tag_speed=5, tag_defense=4, tag_ace=0, tag_closer=0,
             tag_clutch=3, tag_consistent=4, tag_charisma=3, tag_leader=2, tag_young=3, tag_underdog=3, tag_foreign=0,
             stats={"avg": ".290", "hr": 6, "rbi": 48, "ops": ".780"},
             intro="빠른 발과 수비로 빛나는 SSG의 테이블세터",
             story="빠른 발과 안정적인 수비로 SSG 타선의 촉매제 역할을 하는 선수.",
             watch_point="번개같은 도루와 넓은 수비 범위",
             cheer="최지훈 최지훈 달려라 달려",
             stadium_tip="인천SSG랜더스필드 외야석 — 최지훈의 빠른 수비를 가장 잘 볼 수 있음"),
    ],
    "kt wiz": [
        dict(name_ko="강백호", number=51, position="1루수",
             tag_power=5, tag_contact=4, tag_speed=2, tag_defense=3, tag_ace=0, tag_closer=0,
             tag_clutch=5, tag_consistent=4, tag_charisma=5, tag_leader=3, tag_young=4, tag_underdog=2, tag_foreign=0,
             stats={"avg": ".295", "hr": 28, "rbi": 90, "ops": ".890"},
             intro="kt의 간판 스타, 차세대 KBO 대표 타자",
             story="고교 시절부터 주목받은 엘리트 타자. 강력한 장타력과 카리스마로 kt를 이끈다.",
             watch_point="호쾌한 스윙에서 터지는 대형 홈런",
             cheer="강백호 강백호 kt의 스타",
             stadium_tip="수원KT위즈파크 1루 내야석 — 강백호의 파워풀한 타격을 가장 잘 볼 수 있음"),
        dict(name_ko="황재균", number=9, position="3루수",
             tag_power=3, tag_contact=4, tag_speed=2, tag_defense=4, tag_ace=0, tag_closer=0,
             tag_clutch=4, tag_consistent=5, tag_charisma=4, tag_leader=5, tag_young=1, tag_underdog=2, tag_foreign=0,
             stats={"avg": ".275", "hr": 16, "rbi": 72, "ops": ".800"},
             intro="kt의 주장, 안정적인 베테랑 리더",
             story="MLB 진출 후 돌아온 베테랑. 꾸준한 성적과 리더십으로 kt의 정신적 지주 역할.",
             watch_point="안정적인 수비와 노련한 타격 기술",
             cheer="황재균 황재균 kt의 주장",
             stadium_tip="수원KT위즈파크 3루 내야석 — 황재균의 수비를 가까이서 볼 수 있음"),
        dict(name_ko="고영표", number=20, position="선발투수",
             tag_power=0, tag_contact=0, tag_speed=0, tag_defense=0, tag_ace=4, tag_closer=1,
             tag_clutch=4, tag_consistent=5, tag_charisma=3, tag_leader=4, tag_young=1, tag_underdog=3, tag_foreign=0,
             stats={"era": "3.30", "ip": "170", "k": 145, "whip": "1.15"},
             intro="kt의 에이스, 변화구 마스터",
             story="다양한 변화구로 타자를 요리하는 kt의 에이스. 꾸준한 성적으로 팀을 이끈다.",
             watch_point="정교한 제구와 다양한 변화구 조합",
             cheer="고영표 고영표 kt의 에이스",
             stadium_tip="수원KT위즈파크 포수 뒤 구역 — 고영표의 정교한 투구를 정면에서 볼 수 있음"),
    ],
    "NC 다이노스": [
        dict(name_ko="손아섭", number=22, position="외야수",
             tag_power=3, tag_contact=5, tag_speed=3, tag_defense=4, tag_ace=0, tag_closer=0,
             tag_clutch=4, tag_consistent=5, tag_charisma=4, tag_leader=5, tag_young=1, tag_underdog=2, tag_foreign=0,
             stats={"avg": ".300", "hr": 12, "rbi": 68, "ops": ".820"},
             intro="NC의 정신적 지주, 안타 제조기",
             story="꾸준한 타격으로 2000안타를 눈앞에 둔 베테랑. NC 팬들의 영원한 사랑을 받는 선수.",
             watch_point="어떤 공이든 안타로 만들어내는 탁월한 타격 기술",
             cheer="손아섭 손아섭 NC의 레전드",
             stadium_tip="창원NC파크 1루 내야석 — 손아섭의 다양한 타격 기술을 볼 수 있음"),
        dict(name_ko="박민우", number=1, position="2루수",
             tag_power=1, tag_contact=4, tag_speed=5, tag_defense=5, tag_ace=0, tag_closer=0,
             tag_clutch=3, tag_consistent=4, tag_charisma=3, tag_leader=3, tag_young=2, tag_underdog=3, tag_foreign=0,
             stats={"avg": ".275", "hr": 3, "rbi": 42, "ops": ".730"},
             intro="빠른 발과 화려한 수비의 테이블세터",
             story="NC를 대표하는 수비형 2루수. 빠른 발과 안정적인 수비로 팀의 기반을 다진다.",
             watch_point="눈부신 수비 반응과 빠른 주루",
             cheer="박민우 박민우 NC의 수비왕",
             stadium_tip="창원NC파크 내야석 — 박민우의 화려한 2루 수비를 볼 수 있음"),
        dict(name_ko="구창모", number=13, position="선발투수",
             tag_power=0, tag_contact=0, tag_speed=0, tag_defense=0, tag_ace=5, tag_closer=1,
             tag_clutch=4, tag_consistent=4, tag_charisma=4, tag_leader=3, tag_young=3, tag_underdog=3, tag_foreign=0,
             stats={"era": "3.00", "ip": "165", "k": 160, "whip": "1.10"},
             intro="NC의 에이스, 분석야구의 상징",
             story="데이터 기반 피칭으로 타자를 분석하고 압도하는 NC의 간판 투수.",
             watch_point="정교한 구석 공략과 데이터 기반 피칭 전략",
             cheer="구창모 구창모 NC의 에이스",
             stadium_tip="창원NC파크 포수 뒤 구역 — 구창모의 정밀한 투구를 볼 수 있음"),
    ],
    "키움 히어로즈": [
        dict(name_ko="이주형", number=51, position="외야수",
             tag_power=3, tag_contact=4, tag_speed=4, tag_defense=4, tag_ace=0, tag_closer=0,
             tag_clutch=4, tag_consistent=4, tag_charisma=4, tag_leader=2, tag_young=5, tag_underdog=4, tag_foreign=0,
             stats={"avg": ".285", "hr": 12, "rbi": 60, "ops": ".800"},
             intro="키움의 차세대 에이스 야수",
             story="빠른 성장세로 키움의 핵심 선수로 자리잡은 유망주. 다재다능한 플레이로 팬들을 열광시킨다.",
             watch_point="빠른 발과 강한 어깨에서 나오는 화려한 외야 수비",
             cheer="이주형 이주형 키움의 미래",
             stadium_tip="고척스카이돔 1루 내야석 — 이주형의 외야 수비를 볼 수 있음"),
        dict(name_ko="안우진", number=30, position="선발투수",
             tag_power=0, tag_contact=0, tag_speed=0, tag_defense=0, tag_ace=5, tag_closer=1,
             tag_clutch=5, tag_consistent=4, tag_charisma=4, tag_leader=3, tag_young=4, tag_underdog=5, tag_foreign=0,
             stats={"era": "2.90", "ip": "175", "k": 185, "whip": "1.10"},
             intro="키움의 에이스, 삼진머신",
             story="강속구와 날카로운 변화구로 타자를 압도하는 키움의 에이스. 언더독 팀의 희망.",
             watch_point="폭발적인 삼진 능력과 강심장 피칭",
             cheer="안우진 안우진 키움의 에이스",
             stadium_tip="고척스카이돔 포수 뒤 구역 — 실내 구장의 투구 소리를 가장 잘 들을 수 있음"),
        dict(name_ko="김혜성", number=7, position="2루수",
             tag_power=2, tag_contact=4, tag_speed=5, tag_defense=5, tag_ace=0, tag_closer=0,
             tag_clutch=3, tag_consistent=4, tag_charisma=3, tag_leader=3, tag_young=3, tag_underdog=4, tag_foreign=0,
             stats={"avg": ".280", "hr": 5, "rbi": 45, "ops": ".750"},
             intro="키움의 수비형 2루수, 빠른 발의 소유자",
             story="데이터 야구를 몸소 실천하는 수비형 내야수. 빠른 발과 정확한 수비로 팀의 기반을 다진다.",
             watch_point="번개 같은 2루 수비와 빠른 주루 플레이",
             cheer="김혜성 김혜성 키움의 수비왕",
             stadium_tip="고척스카이돔 내야석 — 수비 장면을 가장 가까이서 볼 수 있음"),
    ],
}


class Command(BaseCommand):
    help = "PRD 기준 초기 데이터(팀, 질문, 선수) 로드"

    def handle(self, *args, **kwargs):
        self._load_teams()
        self._load_team_questions()
        self._load_player_questions()
        self._load_players()
        self.stdout.write(self.style.SUCCESS("초기 데이터 로드 완료!"))

    def _load_teams(self):
        created = 0
        for data in TEAMS:
            _, is_new = Team.objects.update_or_create(name=data['name'], defaults=data)
            if is_new:
                created += 1
        self.stdout.write(f"  팀: {len(TEAMS)}개 처리 ({created}개 신규)")

    def _load_team_questions(self):
        created = 0
        for data in TEAM_QUESTIONS:
            _, is_new = TeamQuestion.objects.update_or_create(number=data['number'], defaults=data)
            if is_new:
                created += 1
        self.stdout.write(f"  팀 질문: {len(TEAM_QUESTIONS)}개 처리 ({created}개 신규)")

    def _load_player_questions(self):
        created = 0
        for data in PLAYER_QUESTIONS:
            _, is_new = PlayerQuestion.objects.update_or_create(number=data['number'], defaults=data)
            if is_new:
                created += 1
        self.stdout.write(f"  선수 질문: {len(PLAYER_QUESTIONS)}개 처리 ({created}개 신규)")

    def _load_players(self):
        created = 0
        total = 0
        for team_name, players in PLAYERS.items():
            try:
                team = Team.objects.get(name=team_name)
            except Team.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"  팀 없음: {team_name}"))
                continue
            for data in players:
                total += 1
                _, is_new = Player.objects.update_or_create(
                    team=team, name_ko=data['name_ko'],
                    defaults=data,
                )
                if is_new:
                    created += 1
        self.stdout.write(f"  선수: {total}명 처리 ({created}명 신규)")
