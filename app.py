from textwrap import dedent
from pathlib import Path

app_code = dedent(r'''
import streamlit as st
import requests
from datetime import datetime

# =========================================================
# LUMINA SOUL — APP.PY PHASE 2
# Full copy-paste ready version
# - Keeps original brand tone / style
# - Keeps Google Sheets logging
# - Keeps balloons on successful submit
# - Keeps bilingual TH/EN
# - Adds deeper content engine:
#   core / shadow / love / career / money / wound / gift / lesson / next_step / warning / healing
# - Free layer + Locked premium layer
# =========================================================

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="LUMINA SOUL",
    page_icon="🔮",
    layout="centered"
)

# -----------------------------
# Session state
# -----------------------------
if "lang" not in st.session_state:
    st.session_state.lang = "th"

if "premium_unlocked" not in st.session_state:
    st.session_state.premium_unlocked = False

if "used_code" not in st.session_state:
    st.session_state.used_code = ""

if "latest_result" not in st.session_state:
    st.session_state.latest_result = {}

# -----------------------------
# Translation helper
# -----------------------------
def tr(th_text: str, en_text: str) -> str:
    return th_text if st.session_state.lang == "th" else en_text


# -----------------------------
# Query params language switch
# -----------------------------
query_params = st.query_params
if "lang" in query_params:
    qp_lang = str(query_params["lang"]).lower()
    if qp_lang in ["th", "en"]:
        st.session_state.lang = qp_lang

# -----------------------------
# CSS
# -----------------------------
st.markdown("""
<style>
html, body, [class*="css"] {
    color: #2f1f38 !important;
}
.stApp {
    background-image: linear-gradient(135deg, #fdfcfb 0%, #e7d7fb 38%, #fdfbfb 68%, #fff2ec 100%);
    color: #2f1f38 !important;
}
p, span, div, label, li, small {
    color: #2f1f38 !important;
}
h1, h2, h3, h4, h5, h6 {
    margin: 0 !important;
}
div.stButton > button:first-child,
div[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(to right, #ba68c8 0%, #f06292 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 25px !important;
    padding: 0.78rem 1.3rem !important;
    font-weight: 700 !important;
    font-size: 1.02rem !important;
    transition: 0.25s all ease !important;
    box-shadow: 0 6px 18px rgba(186, 104, 200, 0.28) !important;
    width: 100% !important;
    margin-top: 10px !important;
}
div.stButton > button:first-child:hover,
div[data-testid="stFormSubmitButton"] > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 22px rgba(186, 104, 200, 0.38);
    color: white !important;
}
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] > div {
    border-radius: 14px !important;
    border: 1px solid #d9cfe6 !important;
    background-color: rgba(255,255,255,0.94) !important;
    color: #2f1f38 !important;
    -webkit-text-fill-color: #2f1f38 !important;
}
input::placeholder,
textarea::placeholder {
    color: #8d7b9a !important;
    opacity: 1 !important;
    -webkit-text-fill-color: #8d7b9a !important;
}
label, .stMarkdown, .stTextInput label, .stNumberInput label, .stSelectbox label, .stTextArea label {
    color: #4a3557 !important;
}
div[data-baseweb="select"] * {
    color: #2f1f38 !important;
}
.stAlert {
    border-radius: 14px !important;
    border: none !important;
}
.hero-header-box {
    position: relative;
}
.hero-title-wrap {
    text-align: left;
    margin-top: 6px;
    margin-bottom: 12px;
}
.hero-brand {
    font-size: 3.0rem;
    font-weight: 800;
    line-height: 1.02;
    color: #3f234f !important;
    letter-spacing: -1px;
    margin-bottom: 10px;
}
.hero-subtitle {
    font-size: 2.0rem;
    font-weight: 700;
    line-height: 1.22;
    color: #3f234f !important;
}
.top-floating-lang {
    position: absolute;
    top: -33px;
    right: 0;
    z-index: 10;
    display: flex;
    gap: 8px;
}
.lang-chip {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    min-width: 38px;
    height: 28px;
    padding: 0 10px;
    border-radius: 999px;
    background: rgba(255,255,255,0.88);
    color: #6e4a7d !important;
    text-decoration: none !important;
    font-size: 12px;
    font-weight: 700;
    border: 1px solid rgba(186, 104, 200, 0.18);
    box-shadow: 0 4px 14px rgba(186, 104, 200, 0.12);
    backdrop-filter: blur(8px);
    transition: all 0.22s ease;
}
.lang-chip:hover {
    background: rgba(255,255,255,0.98);
    transform: translateY(-1px);
    box-shadow: 0 6px 18px rgba(186, 104, 200, 0.18);
}
.lang-chip.active {
    background: linear-gradient(to right, #ba68c8, #f06292);
    color: white !important;
    border: none;
    box-shadow: 0 0 12px rgba(186, 104, 200, 0.35);
}
.hero-card {
    background: rgba(255,255,255,0.58) !important;
    backdrop-filter: blur(6px);
    padding: 20px 18px !important;
    border-radius: 24px !important;
    box-shadow: 0 8px 24px rgba(126, 87, 194, 0.10) !important;
    margin-top: 10px !important;
    margin-bottom: 16px !important;
}
.glow-box {
    background: linear-gradient(135deg, rgba(214,228,255,0.95), rgba(234,223,255,0.95)) !important;
    border-radius: 18px !important;
    padding: 18px !important;
    box-shadow: 0 6px 20px rgba(126, 87, 194, 0.10) !important;
    margin-top: 8px !important;
    margin-bottom: 18px !important;
}
.result-card {
    background: rgba(255,255,255,0.85) !important;
    padding: 22px !important;
    border-radius: 20px !important;
    box-shadow: 0 10px 28px rgba(126, 87, 194, 0.12) !important;
    margin-top: 10px !important;
    margin-bottom: 12px !important;
    color: #2f1f38 !important;
}
.mini-card {
    background: rgba(255,255,255,0.80) !important;
    padding: 16px !important;
    border-radius: 18px !important;
    box-shadow: 0 4px 16px rgba(126, 87, 194, 0.10) !important;
    margin-bottom: 12px !important;
    color: #2f1f38 !important;
}
.stat-card {
    background: rgba(255,255,255,0.78) !important;
    padding: 14px 12px !important;
    border-radius: 18px !important;
    text-align: center !important;
    box-shadow: 0 4px 14px rgba(126, 87, 194, 0.08) !important;
    margin-bottom: 10px !important;
    min-height: 120px;
}
.review-card {
    background: rgba(255,255,255,0.78) !important;
    padding: 16px !important;
    border-radius: 18px !important;
    box-shadow: 0 4px 14px rgba(126, 87, 194, 0.08) !important;
    margin-bottom: 12px !important;
}
.lock-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.84), rgba(246,235,255,0.95)) !important;
    padding: 20px !important;
    border-radius: 22px !important;
    box-shadow: 0 10px 28px rgba(126, 87, 194, 0.12) !important;
    border: 1px solid rgba(186, 104, 200, 0.18) !important;
    margin-top: 16px !important;
    margin-bottom: 16px !important;
}
.center-text {
    text-align: center !important;
    color: #5a3d5c !important;
}
.soft-note {
    color: #6b5876 !important;
    font-size: 0.95rem !important;
}
.cta-note {
    text-align: center;
    color: #6e4a7d !important;
    font-size: 0.95rem;
    margin-top: 6px;
    margin-bottom: 8px;
}
.premium-btn a {
    display: block;
    text-align: center;
    padding: 14px 18px;
    border-radius: 999px;
    font-weight: 600;
    font-size: 14px;
    background: linear-gradient(135deg, #ff4d8d, #7b61ff);
    color: white !important;
    box-shadow: 0 8px 20px rgba(123, 97, 255, 0.3);
    text-decoration: none;
    transition: all 0.25s ease;
}
.premium-btn a:hover {
    transform: translateY(-2px) scale(1.02);
    box-shadow: 0 12px 28px rgba(123, 97, 255, 0.4);
}
hr {
    border: none !important;
    border-top: 1px solid rgba(126, 87, 194, 0.15) !important;
}
* {
    -webkit-text-fill-color: inherit;
}
@media (max-width: 768px) {
    .hero-brand {
        font-size: 2.25rem !important;
        line-height: 1.02 !important;
        letter-spacing: -0.4px !important;
        margin-bottom: 12px !important;
    }
    .hero-subtitle {
        font-size: 1.15rem !important;
        line-height: 1.32 !important;
        font-weight: 700 !important;
    }
    .hero-card {
        padding: 16px 14px !important;
        border-radius: 20px !important;
    }
    .glow-box {
        padding: 15px !important;
        border-radius: 16px !important;
    }
    .result-card, .mini-card, .stat-card, .review-card, .lock-card {
        border-radius: 16px !important;
    }
    .soft-note {
        font-size: 0.92rem !important;
    }
    .top-floating-lang {
        top: -33px;
        right: 0;
        gap: 6px;
    }
    .lang-chip {
        min-width: 34px;
        height: 24px;
        padding: 0 8px;
        font-size: 11px;
    }
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Links / endpoints
# -----------------------------
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbztgbRuGYMGMC41V8QHgNl2wnNTgJ5ZhRckVoiUXpVNTkSA-U75MFg-GRZNiCiIjrQeGg/exec"
LINE_LINK = "https://lin.ee/uDDXuWN"

# -----------------------------
# Manual Soul Codes
# -----------------------------
MANUAL_CODES = {
    "SOUL111": {"type": "ebook"},
    "AWAKE222": {"type": "ebook"},
    "LUMINA333": {"type": "ebook"},
    "OVERSOUL777": {"type": "premium"},
}

# -----------------------------
# Helpers
# -----------------------------
def reduce_number(n: int) -> int:
    while n > 9 and n not in (11, 22, 33):
        n = sum(int(d) for d in str(n))
    return n

def life_path_number(day: int, month_num: int, year_be: int) -> int:
    digits = f"{day:02d}{month_num:02d}{year_be}"
    total = sum(int(d) for d in digits)
    return reduce_number(total)

def birth_day_energy(day: int) -> int:
    return reduce_number(day)

def safe_get(dictionary: dict, key, default):
    return dictionary[key] if key in dictionary else default

def paragraph(lines):
    if isinstance(lines, list):
        return " ".join([x.strip() for x in lines if x.strip()])
    return str(lines)

def verify_code(code_input: str):
    code = (code_input or "").strip().upper()
    if not code:
        return False
    return code in MANUAL_CODES

def push_to_google_sheet(payload: dict):
    try:
        requests.post(GOOGLE_SCRIPT_URL, json=payload, timeout=15)
    except Exception:
        pass

def make_profile(th_core, en_core, th_shadow, en_shadow, th_love, en_love, th_career, en_career, th_money, en_money, th_wound, en_wound, th_gift, en_gift, th_lesson, en_lesson, th_next, en_next, th_warning, en_warning, th_heal, en_heal):
    return {
        "core": {"th": th_core, "en": en_core},
        "shadow": {"th": th_shadow, "en": en_shadow},
        "love": {"th": th_love, "en": en_love},
        "career": {"th": th_career, "en": en_career},
        "money": {"th": th_money, "en": en_money},
        "wound": {"th": th_wound, "en": en_wound},
        "gift": {"th": th_gift, "en": en_gift},
        "lesson": {"th": th_lesson, "en": en_lesson},
        "next_step": {"th": th_next, "en": en_next},
        "warning": {"th": th_warning, "en": en_warning},
        "healing": {"th": th_heal, "en": en_heal},
    }

# -----------------------------
# Month / category config
# -----------------------------
month_options = [
    {"th": "มกราคม", "en": "January", "num": 1},
    {"th": "กุมภาพันธ์", "en": "February", "num": 2},
    {"th": "มีนาคม", "en": "March", "num": 3},
    {"th": "เมษายน", "en": "April", "num": 4},
    {"th": "พฤษภาคม", "en": "May", "num": 5},
    {"th": "มิถุนายน", "en": "June", "num": 6},
    {"th": "กรกฎาคม", "en": "July", "num": 7},
    {"th": "สิงหาคม", "en": "August", "num": 8},
    {"th": "กันยายน", "en": "September", "num": 9},
    {"th": "ตุลาคม", "en": "October", "num": 10},
    {"th": "พฤศจิกายน", "en": "November", "num": 11},
    {"th": "ธันวาคม", "en": "December", "num": 12},
]

categories = [
    {"key": "love", "th": "ความรักและความสัมพันธ์", "en": "Love & Relationships"},
    {"key": "career", "th": "การงานและเส้นทางชีวิต", "en": "Career & Life Path"},
    {"key": "money", "th": "โชคลาภและกระแสการเงิน", "en": "Luck & Financial Flow"}
]

month_energy_meanings = {
    1: {"th": "พลังของการเริ่มต้นและความชัดเจน", "en": "the energy of beginnings and clarity"},
    2: {"th": "พลังของความสัมพันธ์และความอ่อนโยน", "en": "the energy of connection and gentleness"},
    3: {"th": "พลังของการสื่อสารและความคิดสร้างสรรค์", "en": "the energy of communication and creativity"},
    4: {"th": "พลังของความมั่นคงและการวางรากฐาน", "en": "the energy of stability and foundation-building"},
    5: {"th": "พลังของการเปลี่ยนแปลงและอิสรภาพ", "en": "the energy of change and freedom"},
    6: {"th": "พลังของความรัก การดูแล และการเยียวยา", "en": "the energy of love, care, and healing"},
    7: {"th": "พลังของการค้นหาความหมายภายใน", "en": "the energy of inner searching and meaning"},
    8: {"th": "พลังของความสำเร็จและการสร้างสิ่งจับต้องได้", "en": "the energy of grounded success and building tangible results"},
    9: {"th": "พลังของการให้ การปล่อยวาง และการเข้าใจชีวิต", "en": "the energy of giving, release, and understanding life"},
    10: {"th": "พลังของจุดเปลี่ยนและการเปิดวงจรใหม่", "en": "the energy of turning points and new cycles"},
    11: {"th": "พลังของญาณรู้และการตื่นรู้ภายใน", "en": "the energy of intuition and inner awakening"},
    12: {"th": "พลังของการปิดวงจรเก่าเพื่อเตรียมสู่การเริ่มต้นใหม่", "en": "the energy of closing old cycles to prepare for a new beginning"}
}

# -----------------------------
# Phase 2 content library
# -----------------------------
PROFILE_LIBRARY = {
    1: make_profile(
        ["คุณมีพลังของผู้เริ่มต้นและผู้เปิดทาง ชีวิตของคุณมักไม่สบายใจเมื่อถูกบังคับให้อยู่ในกรอบที่ไม่ใช่ตัวเอง",
         "หัวใจของคุณต้องการอิสระในการตัดสินใจ และต้องการรู้สึกว่าชีวิตกำลังเดินไปในทิศทางที่ตัวเองเลือก"],
        ["You carry the energy of an initiator and path opener. Your soul does not feel at ease when it is trapped in a life that does not reflect who you are.",
         "At your core, you need freedom in decision-making and a sense that your life is moving in a direction you truly chose."],
        ["เมื่อพลังตก คุณอาจกดดันตัวเองเกินไป รีบเกินไป หรือรู้สึกว่าต้องแข็งแรงตลอดเวลา",
         "บทเรียนสำคัญคือการนำพาชีวิตโดยไม่ต้องต่อสู้กับทุกอย่างตลอดเวลา"],
        ["When your energy is low, you may pressure yourself too much, rush life, or feel you must always stay strong.",
         "A key lesson is learning to lead without turning everything into a battle."],
        ["ในความรัก คุณต้องการความสัมพันธ์ที่เคารพตัวตน ไม่ใช่ความสัมพันธ์ที่ทำให้คุณต้องหายไปเพื่อเอาใจอีกฝ่าย",
         "คุณรักได้จริง แต่หัวใจคุณจะปิดทันทีเมื่อรู้สึกว่าถูกควบคุม"],
        ["In love, you need a relationship that respects your identity rather than one that asks you to disappear to please the other person.",
         "You can love deeply, but your heart closes quickly when it feels controlled."],
        ["งานที่เหมาะกับคุณคือสิ่งที่ได้เริ่ม ได้ตัดสินใจ และได้สร้างบางอย่างด้วยวิธีของตัวเอง",
         "คุณมักเติบโตเมื่อกล้ารับบทนำ ไม่ใช่เมื่อซ่อนความสามารถไว้ข้างหลัง"],
        ["Work suits you best when you can initiate, decide, and build in your own way.",
         "You thrive when you are willing to step into leadership instead of hiding your capability."],
        ["การเงินของคุณดีขึ้นเมื่อคุณเชื่อในคุณค่าของตัวเองและกล้าตั้งราคากับสิ่งที่ทำ",
         "เมื่อคุณลังเลในคุณค่า เงินมักสะท้อนความลังเลนั้นกลับมา"],
        ["Your financial flow improves when you believe in your own value and dare to price what you create.",
         "When you doubt your worth, money tends to mirror that hesitation."],
        ["บาดแผลลึกของคุณคือความรู้สึกว่าต้องพิสูจน์ตัวเองตลอดเวลาเพื่อให้คนยอมรับ",
         "ลึกลงไป คุณอาจกลัวว่าถ้าไม่เก่งพอหรือไม่ชนะ คุณจะไม่มีที่ยืน"],
        ["Your deep wound is the feeling that you must constantly prove yourself in order to be accepted.",
         "Deep down, you may fear that if you are not capable enough or successful enough, you will lose your place."],
        ["ของขวัญของคุณคือพลังในการเริ่มต้นสิ่งใหม่และพาคนอื่นกล้าขยับตาม",
         "คุณมีแรงผลักดันภายในที่ช่วยเปิดทางแม้ในช่วงที่ชีวิตยังไม่ชัด"],
        ["Your gift is the power to initiate and help others move forward with courage.",
         "You carry an inner drive that opens new paths even when life still feels unclear."],
        ["บทเรียนของคุณคือการเป็นผู้นำโดยไม่ต้องเอาชนะทุกอย่าง",
         "เมื่อคุณยอมผ่อนแรงลง พลังแท้ของคุณจะสง่างามขึ้น"],
        ["Your lesson is to lead without turning life into constant conquest.",
         "When you soften the pressure, your true power becomes more graceful."],
        ["เริ่มจากตัดสินใจเรื่องเล็ก ๆ ให้ชัด และหยุดรอให้ทุกอย่างพร้อมก่อน",
         "พลังของคุณจะเปิดเมื่อคุณกล้าก้าวก่อนความมั่นใจจะมาครบ"],
        ["Start by making clear decisions in small things and stop waiting for perfect readiness.",
         "Your energy opens when you dare to move before confidence feels complete."],
        ["ระวังการใช้ความสำเร็จเป็นตัววัดคุณค่าหัวใจตัวเอง",
         "ถ้าคุณแข็งเกินไป คุณอาจชนะโลกแต่ห่างจากตัวเองมากขึ้น"],
        ["Be careful not to measure your worth only through success.",
         "If you become too hard, you may win in the world while drifting further from yourself."],
        ["คุณไม่ได้เกิดมาเพื่อเดินตามทุกคน คุณเกิดมาเพื่อจำเสียงของตัวเองให้ได้อีกครั้ง"],
        ["You were not born to follow every path around you. You were born to remember your own voice."]
    ),
    2: make_profile(
        ["คุณมีพลังของผู้ประสานใจ รับรู้อารมณ์ละเอียด และมักเข้าใจสิ่งที่คนอื่นไม่ได้พูดออกมาตรง ๆ",
         "หัวใจของคุณเติบโตเมื่ออยู่ในพื้นที่ที่อ่อนโยน จริงใจ และปลอดภัยพอให้เป็นตัวเอง"],
        ["You carry the energy of a harmonizer. You sense subtle emotions and often understand what others do not say directly.",
         "Your heart grows in spaces that feel gentle, sincere, and safe enough for your true self."],
        ["เมื่อพลังตก คุณอาจเก็บความรู้สึกตัวเองไว้เพราะกลัวความขัดแย้ง",
         "คุณอาจรับพลังคนอื่นมาหนักเกินไปจนลืมฟังหัวใจตัวเอง"],
        ["When your energy is low, you may suppress your own feelings because you fear conflict.",
         "You may carry too much of other people’s emotions and stop hearing your own heart."],
        ["ความรักของคุณต้องการความมั่นคงทางใจและการสื่อสารที่นุ่มนวล",
         "คุณไม่ได้ต้องการแค่คนรัก แต่ต้องการคนที่เห็นความละเอียดอ่อนของคุณอย่างจริงใจ"],
        ["Your love life needs emotional safety and soft, honest communication.",
         "You are not just seeking a partner—you are seeking someone who truly sees your sensitivity."],
        ["คุณเหมาะกับงานที่ใช้การประสานคน ดูแลความสัมพันธ์ รับฟัง หรือสร้างบรรยากาศที่ทำให้คนสบายใจ",
         "พรสวรรค์ของคุณคือการเชื่อมโยงมากกว่าการแข่งขัน"],
        ["You do well in work that involves connection, care, listening, or creating an environment where people feel safe.",
         "Your gift lies more in connecting than competing."],
        ["การเงินของคุณดีขึ้นเมื่อคุณหยุดมองว่าความอ่อนโยนไม่มีมูลค่า",
         "คุณสามารถสร้างเงินได้จากการช่วยให้คนรู้สึกดีขึ้นหรือเข้าใจตัวเองมากขึ้น"],
        ["Your money grows when you stop assuming that softness has no value.",
         "You can create income through helping people feel better or understand themselves more deeply."],
        ["บาดแผลของคุณคือความรู้สึกว่าถ้าพูดความจริงออกไป จะทำให้คนไม่พอใจหรือจากไป",
         "จึงมีหลายครั้งที่คุณเลือกเงียบแทนการซื่อสัตย์กับตัวเอง"],
        ["Your wound is the feeling that if you speak your truth, people may become upset or leave.",
         "So there are many times you choose silence over honesty with yourself."],
        ["ของขวัญของคุณคือการรับรู้ใจคนอย่างลึกและเชื่อมบรรยากาศให้กลับมาสงบ",
         "คุณสามารถเป็นสะพานระหว่างความรู้สึกที่แตกแยกได้"],
        ["Your gift is the ability to feel people deeply and restore emotional harmony.",
         "You can become a bridge where feelings have been fragmented."],
        ["บทเรียนของคุณคือการอ่อนโยนกับคนอื่นโดยไม่ทอดทิ้งตัวเอง",
         "ความสัมพันธ์ที่ดีไม่ได้เกิดจากการยอมตลอด แต่เกิดจากความจริงที่อ่อนโยน"],
        ["Your lesson is to stay gentle with others without abandoning yourself.",
         "A healthy relationship is not built on endless yielding, but on gentle truth."],
        ["เริ่มต้นจากพูดความต้องการของตัวเองทีละนิด แม้จะยังกลัวอยู่",
         "ยิ่งคุณให้พื้นที่หัวใจตัวเองมากเท่าไร พลังชีวิตคุณจะยิ่งนิ่งขึ้น"],
        ["Start by expressing your needs little by little, even if fear is still present.",
         "The more space you give your own heart, the steadier your energy becomes."],
        ["ระวังการเป็นคนรองรับทุกอย่างจนไม่มีใครรู้เลยว่าคุณเจ็บตรงไหน",
         "ถ้าคุณเงียบนานเกินไป ความสัมพันธ์จะบิดไปจากความจริง"],
        ["Be careful not to become everyone’s emotional container while no one knows where you hurt.",
         "If you stay silent too long, relationships begin to drift away from truth."],
        ["ความอ่อนไหวของคุณไม่ใช่จุดอ่อน แต่มันคือภาษาละเอียดของจิตวิญญาณ"],
        ["Your sensitivity is not a weakness. It is one of the subtle languages of the soul."]
    ),
    3: make_profile(
        ["คุณมีพลังของการสื่อสาร ความคิดสร้างสรรค์ และการทำให้พลังภายในถูกถ่ายทอดออกมาเป็นคำพูดหรือผลงาน",
         "ชีวิตของคุณมักเปิดทางเมื่อคุณยอมให้ตัวเองถูกมองเห็น"],
        ["You carry the energy of expression, creativity, and turning inner energy into words, art, or communication.",
         "Life opens for you when you allow yourself to be seen."],
        ["เมื่อพลังตก คุณอาจใช้ความสดใสกลบความจริงในใจ หรือกลัวว่าถ้าพูดจริงแล้วคนจะไม่รับ",
         "บทเรียนคือการสื่อสารจากแก่นแท้ ไม่ใช่จากการพยายามทำให้ทุกคนพอใจ"],
        ["When your energy drops, you may use brightness to cover what is really happening inside or fear that honesty will not be accepted.",
         "Your lesson is to express from truth rather than from the need to please everyone."],
        ["ในความรัก คุณต้องการความสนุก การสื่อสาร และการเชื่อมโยงที่มีชีวิตชีวา",
         "แต่ลึก ๆ แล้วคุณต้องการคนที่รับฟังโลกภายในของคุณด้วย ไม่ใช่เห็นแค่ภาพภายนอก"],
        ["In love, you need playfulness, communication, and a lively sense of connection.",
         "But underneath that, you also need someone who listens to your inner world, not just your outer sparkle."],
        ["คุณเหมาะกับงานสื่อสาร คอนเทนต์ การพูด การสอน การขายเชิงความรู้ หรือการสร้างแรงบันดาลใจ",
         "พรสวรรค์ของคุณคือการทำให้สิ่งที่จับต้องยากกลายเป็นสิ่งที่คนรู้สึกได้"],
        ["You suit communication, content, speaking, teaching, value-based selling, and inspiration-led work.",
         "Your gift is making intangible things feel real and emotionally accessible."],
        ["การเงินของคุณดีเมื่อคุณกล้าใช้เสียงของตัวเองและทำสิ่งที่มีเอกลักษณ์",
         "รายได้มักเชื่อมกับความสามารถในการดึงดูดคนผ่านเสน่ห์และการสื่อสาร"],
        ["Your financial flow improves when you dare to use your voice and create through your own uniqueness.",
         "Income often connects to your ability to attract people through communication and personal magnetism."],
        ["บาดแผลของคุณคือความกลัวว่าถ้าคนเห็นตัวจริงแล้ว เขาอาจไม่ชอบ",
         "จึงมีช่วงที่คุณแสดงด้านสว่างแต่ซ่อนด้านลึกไว้มากเกินไป"],
        ["Your wound is the fear that if people see the real you, they may not like what they find.",
         "So there are times when you show your sparkle but hide your depth too much."],
        ["ของขวัญของคุณคือการทำให้คนรู้สึกมีชีวิตและเข้าใจสิ่งที่ยากด้วยหัวใจที่เบาลง",
         "คุณเปลี่ยนบรรยากาศและเปลี่ยนความรู้สึกคนได้ผ่านคำพูด"],
        ["Your gift is helping people feel alive again and understand difficult things through lighter, heartfelt expression.",
         "You change atmosphere and emotion through the power of words."],
        ["บทเรียนของคุณคือการใช้เสียงเพื่อเปิดเผย ไม่ใช่เพื่อปกปิด",
         "เมื่อคุณพูดจากแก่นแท้ เสน่ห์ของคุณจะมีพลังมากกว่าการพยายามดูดี"],
        ["Your lesson is to use your voice to reveal, not to hide.",
         "When you speak from truth, your magnetism becomes more powerful than trying to appear perfect."],
        ["เริ่มสื่อสารสิ่งที่คุณรู้สึกจริงในแบบของตัวเอง แม้ยังไม่สมบูรณ์",
         "พลังของคุณจะชัดขึ้นทันทีเมื่อหยุดเล่นบทที่ไม่ใช่ตัวเอง"],
        ["Start expressing what you truly feel in your own way, even before it feels perfect.",
         "Your power becomes clearer the moment you stop performing a version of yourself that is not real."],
        ["ระวังการทำทุกอย่างให้ดูเบาและสนุกจนหัวใจลึก ๆ ไม่เคยถูกได้ยิน",
         "ถ้าคุณหนีความจริงนานเกินไป ความสดใสจะกลายเป็นเกราะแทนแสง"],
        ["Be careful not to make everything look light and playful until your deeper heart is never heard.",
         "If you avoid truth for too long, brightness becomes armor instead of light."],
        ["เสียงของคุณไม่ได้มีไว้เพื่อทำให้คนพอใจอย่างเดียว แต่มันมีไว้เพื่อปลดล็อกบางอย่างในใจคนด้วย"],
        ["Your voice is not only here to please people. It is here to unlock something in them too."]
    ),
    4: make_profile(
        ["คุณมีพลังของผู้สร้างรากฐาน ชีวิตของคุณเด่นเรื่องความรับผิดชอบ ความจริงจัง และการทำสิ่งเล็กให้กลายเป็นความมั่นคง",
         "คุณรู้สึกปลอดภัยเมื่อทุกอย่างมีโครงสร้างที่ชัดเจน"],
        ["You carry builder energy. Your life highlights responsibility, seriousness, and the ability to turn small actions into real stability.",
         "You feel safest when life has clear structure."],
        ["เมื่อพลังตก คุณอาจแบกเยอะเกินไป กดดันตัวเอง และยึดกับวิธีเดิมจนชีวิตไม่ไหล",
         "บทเรียนสำคัญคือการสร้างโดยไม่แข็งทื่อ"],
        ["When your energy is low, you may over-carry, over-pressure yourself, and cling to old methods until life feels blocked.",
         "Your key lesson is to build without becoming rigid."],
        ["ในความรัก คุณต้องการความชัดเจน ความมั่นคง และความไว้ใจที่พิสูจน์ได้จริง",
         "คุณเปิดใจช้า แต่ถ้าเชื่อใจแล้วจะจริงจังมาก"],
        ["In love, you need clarity, stability, and trust that can be felt in action.",
         "You open slowly, but once you trust, you become deeply committed."],
        ["คุณเหมาะกับงานระบบ งานวางแผน งานจัดการ หรือธุรกิจที่ต้องสร้างฐานให้มั่นคง",
         "ความสำเร็จของคุณมักมาแบบค่อยเป็นค่อยไปแต่ยั่งยืน"],
        ["You suit systems, planning, management, and businesses that require a strong foundation.",
         "Your success often builds slowly but lasts."],
        ["การเงินของคุณขึ้นกับวินัย การจัดระบบ และการตัดสินใจระยะยาว",
         "คุณมีศักยภาพสร้างความมั่นคงสูง ถ้าไม่กลัวการเติบโตที่ค่อยเป็นค่อยไป"],
        ["Your finances depend on discipline, systems, and long-term decision-making.",
         "You have strong potential for lasting stability if you stop underestimating slow growth."],
        ["บาดแผลของคุณคือความรู้สึกว่าถ้าปล่อยมือหรือผ่อนแรง ทุกอย่างจะพัง",
         "จึงมีหลายครั้งที่คุณเลือกแบกมากกว่าขอความช่วยเหลือ"],
        ["Your wound is the fear that if you loosen your grip, everything will collapse.",
         "So there are many times you choose to carry more instead of asking for help."],
        ["ของขวัญของคุณคือการสร้างสิ่งที่ยืนระยะได้จริง ไม่ใช่แค่สวยชั่วคราว",
         "คุณมีพลังเปลี่ยนความวุ่นวายให้กลายเป็นระบบที่คนพึ่งพาได้"],
        ["Your gift is building things that can last, not just look good for a moment.",
         "You can transform chaos into structure that people can rely on."],
        ["บทเรียนของคุณคือการเชื่อว่าความมั่นคงไม่จำเป็นต้องมาจากการเกร็งตลอดเวลา",
         "เมื่อคุณยืดหยุ่นมากขึ้น ชีวิตจะไหลไปข้างหน้าได้ดีกว่าเดิม"],
        ["Your lesson is learning that stability does not require constant tightening and control.",
         "As you become more flexible, life moves forward more naturally."],
        ["เริ่มจากวางระบบที่ช่วยคุณ ไม่ใช่ระบบที่กดคุณ",
         "ให้ตัวเองมีพื้นที่พักโดยไม่มองว่ามันคือความล้มเหลว"],
        ["Start building systems that support you, not systems that imprison you.",
         "Give yourself room to rest without labeling it as failure."],
        ["ระวังการติดกับโครงสร้างเดิมจนพลาดโอกาสใหม่ที่เหมาะกว่า",
         "ถ้าคุณแข็งกับตัวเองเกินไป ความมั่นคงจะค่อย ๆ กลายเป็นภาระ"],
        ["Be careful not to cling so tightly to old structures that you miss better opportunities.",
         "If you become too hard on yourself, stability slowly turns into burden."],
        ["คุณไม่ได้ช้า คุณกำลังสร้างสิ่งที่อยู่ได้นานกว่า"],
        ["You are not slow. You are building something designed to last."]
    ),
    5: make_profile(
        ["คุณมีพลังของการเปลี่ยนแปลง อิสรภาพ และการเรียนรู้จากประสบการณ์ตรง",
         "ชีวิตของคุณมักเติบโตเมื่อได้ขยับ เดินทาง ทดลอง และปล่อยให้ตัวเองมีพื้นที่"],
        ["You carry the energy of change, freedom, and learning through direct experience.",
         "Your life expands through movement, exploration, experimentation, and spaciousness."],
        ["เมื่อพลังตก คุณอาจรู้สึกเบื่อง่าย กระจัดกระจาย หรือหนีความรู้สึกลึกด้วยการหาสิ่งใหม่ตลอดเวลา",
         "บทเรียนคือการรักษาอิสรภาพโดยไม่หนีจากตัวเอง"],
        ["When your energy is low, you may become restless, scattered, or avoid deeper emotions by constantly chasing something new.",
         "Your lesson is to stay free without running from yourself."],
        ["ในความรัก คุณต้องการพื้นที่ ความสดใหม่ และคนที่ไม่ทำให้คุณรู้สึกติดกับ",
         "แต่หัวใจคุณก็ยังต้องการความจริงใจ ไม่ใช่แค่ความตื่นเต้นชั่วคราว"],
        ["In love, you need space, freshness, and a partner who does not make you feel trapped.",
         "Yet your heart still needs sincerity, not just temporary excitement."],
        ["คุณเหมาะกับงานที่มีความยืดหยุ่น การสื่อสาร การตลาด การเดินทาง หรือสิ่งที่ได้ลองหลายบทบาท",
         "คุณเติบโตเมื่อมีพื้นที่ให้พลังชีวิตได้ไหล"],
        ["You suit flexible work, communication, marketing, travel, and roles that allow variety.",
         "You thrive when your life-force is allowed to move."],
        ["การเงินของคุณมักขึ้นลงตามจังหวะชีวิต แต่ถ้าคุณสร้างระบบรองรับอิสรภาพได้ เงินจะไหลดีมาก",
         "คุณมีพลังดึงดูดโอกาส แต่ต้องระวังการใช้จ่ายตามอารมณ์"],
        ["Your finances may fluctuate with your life rhythm, but when you build systems that support your freedom, money can flow well.",
         "You attract opportunities, but emotional spending needs care."],
        ["บาดแผลของคุณคือความกลัวว่าถ้าหยุดนิ่งหรือถูกผูกมัด คุณจะเสียตัวเองไป",
         "จึงมีบางช่วงที่คุณเลือกหนีมากกว่าหยุดฟังว่าหัวใจต้องการอะไรจริง"],
        ["Your wound is the fear that if you stay still or become bound, you will lose yourself.",
         "So there are seasons when you choose escape instead of pausing to hear what your heart truly needs."],
        ["ของขวัญของคุณคือการพาคนอื่นเห็นความเป็นไปได้ใหม่และกล้าขยับจากสิ่งเดิม",
         "คุณนำพลังชีวิต ความสด และความกล้าเข้ามาในพื้นที่ที่นิ่งจนเกินไป"],
        ["Your gift is helping people see new possibilities and move beyond stagnant patterns.",
         "You bring life-force, freshness, and courage into spaces that have become too still."],
        ["บทเรียนของคุณคือการมีอิสระโดยไม่ทำให้ชีวิตกระจัดกระจาย",
         "เมื่อคุณอยู่กับตัวเองได้โดยไม่ต้องวิ่งหนี พลังของคุณจะทรงพลังกว่าเดิมมาก"],
        ["Your lesson is learning how to stay free without scattering your life-force.",
         "When you can remain with yourself without running, your energy becomes far more powerful."],
        ["เริ่มจากเลือกอิสระที่มีโครง ไม่ใช่แค่เลือกสิ่งที่ตื่นเต้น",
         "จัดระบบเล็ก ๆ ให้รองรับความเปลี่ยนแปลง แล้วคุณจะไปได้ไกลกว่าเดิม"],
        ["Start choosing freedom with structure, not only what feels exciting in the moment.",
         "Build small systems that support change, and you will go much farther."],
        ["ระวังการเปลี่ยนทุกอย่างเพียงเพราะรู้สึกอึดอัดชั่วคราว",
         "ถ้าคุณหนีความรู้สึกมากเกินไป คุณจะไม่เห็นบทเรียนที่ชีวิตกำลังให้"],
        ["Be careful not to change everything just because a temporary discomfort appears.",
         "If you run from feeling too quickly, you may miss the lesson life is trying to show you."],
        ["อิสรภาพที่แท้จริง ไม่ใช่การหนีทุกอย่าง แต่มันคือการอยู่กับตัวเองได้โดยไม่ติดกรง"],
        ["True freedom is not escaping everything. It is being able to stay with yourself without living in a cage."]
    ),
    6: make_profile(
        ["คุณมีพลังของผู้ดูแล ผู้เยียวยา และผู้สร้างพื้นที่ปลอดภัยให้คนอื่น",
         "หัวใจของคุณมีความรัก ความรับผิดชอบ และความต้องการทำสิ่งที่มีคุณค่าต่อผู้คน"],
        ["You carry the energy of the nurturer, healer, and one who creates emotional safety for others.",
         "Your heart is rooted in love, responsibility, and doing something meaningful for people."],
        ["เมื่อพลังตก คุณอาจให้มากเกินไป แบกคนอื่นเกินจำเป็น หรือรู้สึกผิดง่ายเมื่อไม่ได้ช่วยทุกคน",
         "บทเรียนคือการดูแลคนอื่นโดยไม่ละทิ้งตัวเอง"],
        ["When your energy drops, you may over-give, over-carry, or feel guilty when you cannot save everyone.",
         "Your lesson is to care for others without abandoning yourself."],
        ["ในความรัก คุณต้องการความอบอุ่น ความมั่นคง และความสัมพันธ์ที่ให้ความรู้สึกเหมือนบ้าน",
         "คุณรักลึกและทุ่มเท แต่ต้องระวังการเป็นคนเยียวยาแทนที่จะเป็นคนรัก"],
        ["In love, you need warmth, stability, and a bond that feels like home.",
         "You love deeply and generously, but be careful not to become the healer instead of the partner."],
        ["คุณเหมาะกับงานดูแล บริการ ให้คำแนะนำ ความงาม สุขภาวะ หรือสิ่งที่ช่วยยกระดับชีวิตคนอื่น",
         "พรสวรรค์ของคุณคือการทำให้คนรู้สึกว่าตัวเองมีค่า"],
        ["You suit care work, service, guidance, beauty, wellbeing, and anything that helps people feel better or live better.",
         "Your gift is helping people feel valued."],
        ["เงินของคุณมักมาเมื่อคุณให้คุณค่ากับสิ่งที่คุณมอบ ไม่ใช่แค่ทำไปเพราะใจดี",
         "คุณต้องเรียนรู้ว่าความสามารถในการดูแลและเยียวยาก็มีมูลค่าทางการเงิน"],
        ["Money tends to come when you value what you offer instead of giving endlessly just because you care.",
         "Your care and healing ability also hold financial value."],
        ["บาดแผลของคุณคือความรู้สึกว่าตัวเองจะมีค่าก็ต่อเมื่อกำลังดูแลหรือช่วยใครบางคน",
         "จึงมีช่วงที่คุณยอมเหนื่อยเกินไปเพื่อรักษาความสัมพันธ์หรือบทบาทบางอย่างไว้"],
        ["Your wound is the feeling that you are only valuable when you are taking care of someone.",
         "So there are seasons when you exhaust yourself to keep certain relationships or roles alive."],
        ["ของขวัญของคุณคือการสร้างพื้นที่ที่คนรู้สึกอบอุ่น ปลอดภัย และกล้ากลับมาเป็นตัวเอง",
         "พลังของคุณเยียวยาได้แม้บางครั้งยังไม่ได้พูดอะไรออกไปมาก"],
        ["Your gift is creating spaces where people feel warm, safe, and able to return to themselves.",
         "Your energy can heal even before many words are spoken."],
        ["บทเรียนของคุณคือการรักคนอื่นโดยไม่ใช้หัวใจตัวเองเป็นเชื้อเพลิงตลอดเวลา",
         "การดูแลที่สมดุลจะมีพลังมากกว่าการเสียสละจนหมดแรง"],
        ["Your lesson is learning to love others without making your own heart the constant fuel source.",
         "Balanced care is more powerful than self-sacrifice that leaves you empty."],
        ["เริ่มตั้งขอบเขตเล็ก ๆ กับสิ่งที่ทำให้คุณเหนื่อยซ้ำ",
         "ยิ่งคุณเคารพพลังตัวเองมากเท่าไร คนที่ใช่จะยิ่งเคารพคุณมากขึ้น"],
        ["Start setting small boundaries around what repeatedly drains you.",
         "The more you honor your energy, the more the right people will honor you too."],
        ["ระวังการให้เกินกว่าที่อีกฝ่ายร้องขอแล้วคาดหวังว่าจะถูกเห็นคุณค่าเอง",
         "ถ้าคุณลืมตัวเองนานเกินไป ความรักจะเริ่มปนกับความเหนื่อย"],
        ["Be careful not to give more than was asked and quietly expect others to notice your worth.",
         "If you forget yourself for too long, love becomes mixed with exhaustion."],
        ["การรักคนอื่นไม่จำเป็นต้องแลกกับการทิ้งตัวเองไว้ข้างหลัง"],
        ["Loving others does not require leaving yourself behind."]
    ),
    7: make_profile(
        ["คุณมีพลังของนักค้นหาความจริง ชีวิตของคุณมักไม่พอใจกับคำตอบผิวเผิน เพราะหัวใจต้องการเข้าใจสิ่งต่าง ๆ ให้ถึงแก่น",
         "คุณเชื่อมต่อกับโลกภายในได้ลึก และมักมีสัญชาตญาณที่ชัดกว่าที่ตัวเองยอมรับ"],
        ["You carry the energy of a truth seeker. Surface-level answers rarely satisfy you because your heart wants to understand life at its root.",
         "You are deeply connected to your inner world and often possess stronger intuition than you openly admit."],
        ["เมื่อพลังตก คุณอาจถอยห่าง เก็บตัว คิดวน หรือรู้สึกว่าไม่มีใครเข้าใจสิ่งที่อยู่ข้างใน",
         "บทเรียนสำคัญคือการใช้ความลึกเพื่อเปิดประตู ไม่ใช่สร้างกำแพง"],
        ["When your energy drops, you may withdraw, overthink, or feel that no one truly understands what lives inside you.",
         "A core lesson is to use depth as a doorway rather than as a wall."],
        ["ในความรัก คุณไม่ได้ต้องการเพียงความสัมพันธ์ แต่ต้องการ connection ที่จริง ลึก และซื่อสัตย์",
         "คุณอาจดูนิ่งหรือเปิดยาก แต่ความจริงคือคุณให้ความสำคัญกับความจริงใจมากกว่าความหวือหวา"],
        ["In love, you are not seeking just a relationship—you are seeking real, deep, and honest connection.",
         "You may seem reserved or hard to access, but the truth is you value sincerity more than spectacle."],
        ["คุณเหมาะกับงานที่ได้คิด วิเคราะห์ เขียน สอน วิจัย หรือถ่ายทอดสิ่งลึกให้คนเข้าใจง่ายขึ้น",
         "คุณเติบโตได้มากเมื่อทำงานที่เชื่อมโลกภายในกับคุณค่าที่ส่งต่อออกไปภายนอก"],
        ["You are suited to work involving analysis, writing, teaching, research, or translating depth into something others can understand.",
         "You grow most when your work bridges inner truth with outer contribution."],
        ["การเงินของคุณดีขึ้นเมื่อคุณหยุดแยกเรื่องจิตวิญญาณออกจากคุณค่าในโลกจริง",
         "เมื่อสิ่งที่คุณทำมีความหมายและมีโครงสร้าง เงินจะเริ่มไหลแบบมั่นคงขึ้น"],
        ["Your finances improve when you stop separating spirituality from real-world value.",
         "When your work carries meaning and structure, money begins to flow more steadily."],
        ["บาดแผลของคุณคือความรู้สึกว่าไม่มีใครเข้าใจสิ่งลึก ๆ ในตัวคุณจริง",
         "จึงมีหลายครั้งที่คุณปิดตัวเองก่อนที่จะถูกมองข้ามหรือเข้าใจผิด"],
        ["Your wound is the feeling that no one truly understands the deeper layers of you.",
         "So many times you protect yourself by closing off before you can be misunderstood or overlooked."],
        ["ของขวัญของคุณคือการมองทะลุสิ่งที่ซ่อนอยู่และตั้งคำถามกับสิ่งที่คนอื่นยอมรับแบบไม่คิด",
         "คุณมีแสงของผู้เห็นความจริง แม้ในพื้นที่ที่คลุมเครือ"],
        ["Your gift is seeing through what is hidden and questioning what others accept without thought.",
         "You carry the light of truth-seeing even in unclear spaces."],
        ["บทเรียนของคุณคือการใช้ความลึกเพื่อเชื่อม ไม่ใช่ใช้เพื่อแยกตัวออกจากโลก",
         "เมื่อคุณแบ่งปันสิ่งที่เห็นอย่างอ่อนโยน ความจริงของคุณจะกลายเป็นประโยชน์ต่อผู้คน"],
        ["Your lesson is to use depth to connect rather than to isolate yourself from the world.",
         "When you share what you see with gentleness, your truth becomes medicine for others."],
        ["เริ่มจากปล่อยให้คนที่ใช่เข้าถึงคุณทีละชั้น แทนที่จะปิดหมดตั้งแต่ต้น",
         "และให้สิ่งที่คุณรู้ลึก ๆ ถูกแปลออกมาเป็นงานหรือคำที่ส่งต่อได้จริง"],
        ["Start by letting the right people reach you layer by layer rather than closing all the doors at once.",
         "And allow what you know deeply to become work or words that can truly be shared."],
        ["ระวังการใช้ความลึกเป็นข้ออ้างในการไม่เชื่อมต่อกับชีวิตจริง",
         "ถ้าคุณอยู่แต่ในหัวตัวเองนานเกินไป ความจริงจะไม่เปลี่ยนอะไรเลย"],
        ["Be careful not to use depth as an excuse to disconnect from real life.",
         "If you remain only inside your mind for too long, truth changes nothing."],
        ["ความลึกของคุณไม่ได้ทำให้คุณยากเกินจะรัก มันแค่หมายความว่าหัวใจคุณต้องการความจริงมากกว่าคนทั่วไป"],
        ["Your depth does not make you too difficult to love. It simply means your heart requires more truth than most."]
    ),
    8: make_profile(
        ["คุณมีพลังของการบริหาร ความสำเร็จ และการทำให้สิ่งที่มองเห็นในหัวกลายเป็นผลลัพธ์ที่จับต้องได้",
         "ชีวิตของคุณมีศักยภาพสูงในเรื่องการสร้างอิทธิพล ความมั่นคง และพลังในโลกจริง"],
        ["You carry the energy of leadership, achievement, and turning vision into tangible results.",
         "Your life holds strong potential around influence, stability, and worldly power."],
        ["เมื่อพลังตก คุณอาจกดดันตัวเองหนัก วัดคุณค่าจากความสำเร็จ หรือกลัวการล้มเหลวจนไม่กล้าผ่อน",
         "บทเรียนสำคัญคือการมีอำนาจโดยไม่กลายเป็นนักสู้ที่ไม่มีวันพัก"],
        ["When your energy is low, you may pressure yourself harshly, measure your worth by success, or fear failure so much that you never fully rest.",
         "Your lesson is to hold power without becoming a warrior who never stops fighting."],
        ["ในความรัก คุณต้องการคนที่เคารพพลังและความทะเยอทะยานของคุณ ไม่ใช่ทำให้คุณรู้สึกผิดที่จริงจังกับชีวิต",
         "หัวใจคุณต้องการความซื่อสัตย์และความมั่นคงพอ ๆ กับความสำเร็จ"],
        ["In love, you need someone who respects your power and ambition rather than making you feel guilty for taking life seriously.",
         "Your heart needs honesty and stability just as much as success."],
        ["คุณเหมาะกับงานบริหาร ธุรกิจ การเงิน การสร้างแบรนด์ หรือบทบาทที่ต้องตัดสินใจและรับผิดชอบภาพใหญ่",
         "คุณมีศักยภาพเป็นผู้นำสิ่งที่สร้างความมั่นคงให้ตัวเองและคนอื่น"],
        ["You suit business, management, finance, branding, and roles that require decision-making and big-picture responsibility.",
         "You have the potential to lead something that creates stability for both you and others."],
        ["การเงินเป็นหนึ่งในสนามพลังสำคัญของคุณ ยิ่งคุณจัดระบบและกล้ายืนในคุณค่าของตัวเอง เงินยิ่งตอบสนอง",
         "คุณไม่ได้เกิดมาเพื่อเล็กกับเรื่องความอุดมสมบูรณ์"],
        ["Money is one of your major energetic arenas. The more you build structure and stand in your value, the more finances respond.",
         "You were not born to stay small around abundance."],
        ["บาดแผลของคุณคือการเชื่อว่าคุณจะปลอดภัยก็ต่อเมื่อทุกอย่างอยู่ภายใต้การควบคุม",
         "จึงมีหลายช่วงที่คุณยอมแบกมากกว่าปล่อยให้ใครเห็นความเปราะบาง"],
        ["Your wound is the belief that you are safe only when everything is under control.",
         "So there are many times you choose to carry more rather than let anyone see your vulnerability."],
        ["ของขวัญของคุณคือพลังในการทำสิ่งใหญ่ให้เกิดขึ้นจริงและพาคนอื่นมองเห็นศักยภาพของตัวเอง",
         "คุณมีความสามารถในการเปลี่ยนแรงกดดันให้เป็นโครงสร้างแห่งความสำเร็จ"],
        ["Your gift is the power to bring large visions into reality and help others recognize their own potential.",
         "You can transform pressure into structures of achievement."],
        ["บทเรียนของคุณคือการเรียนรู้ว่าอำนาจที่แท้จริงไม่จำเป็นต้องมาพร้อมความแข็งตลอดเวลา",
         "เมื่อคุณยอมให้หัวใจเข้ามาอยู่ในความสำเร็จ ชีวิตจะสมบูรณ์ขึ้นมาก"],
        ["Your lesson is learning that true power does not require hardness at all times.",
         "When you allow your heart into your success, life becomes far more complete."],
        ["เริ่มจัดระบบความสำเร็จให้มีพื้นที่พัก พื้นที่รัก และพื้นที่เป็นมนุษย์",
         "ยิ่งคุณสร้างจากคุณค่าจริง ไม่ใช่แค่แรงพิสูจน์ เงินจะยิ่งนิ่งขึ้น"],
        ["Start building success with room for rest, love, and humanity.",
         "The more you create from real value instead of pure proving energy, the steadier money becomes."],
        ["ระวังการทำทุกอย่างให้ใหญ่จนหัวใจไม่เหลือพื้นที่หายใจ",
         "ถ้าคุณชนะทุกอย่างแต่เสียตัวเองไป คุณจะยังรู้สึกขาดอยู่ดี"],
        ["Be careful not to make everything so large that your heart no longer has room to breathe.",
         "If you win everything but lose yourself, a sense of lack will remain."],
        ["ความสำเร็จที่แท้จริง ไม่ใช่การพิสูจน์ว่าคุณเก่งพอ แต่มันคือการสร้างชีวิตที่ไม่ต้องหักหลังหัวใจตัวเอง"],
        ["True success is not proving you are enough. It is building a life that does not betray your own heart."]
    ),
    9: make_profile(
        ["คุณมีพลังของผู้ให้ เมตตา เข้าใจมนุษย์ และมีสายเชื่อมกับบทเรียนเรื่องการปล่อยวาง",
         "หัวใจของคุณมักรู้สึกถึงความทุกข์ของผู้คนและต้องการทำบางอย่างที่มีความหมาย"],
        ["You carry compassionate, humanitarian energy and are deeply linked to lessons of release and meaning.",
         "Your heart often feels the suffering of others and wants to do something that matters."],
        ["เมื่อพลังตก คุณอาจแบกอดีต แบกคนอื่น หรือจมกับความผิดหวังที่ยังไม่ปิดวงจร",
         "บทเรียนสำคัญคือการให้โดยไม่ทำให้ตัวเองสูญหาย"],
        ["When your energy is low, you may carry the past, carry other people, or remain entangled in disappointments that never fully closed.",
         "Your lesson is to give without disappearing."],
        ["ในความรัก คุณต้องการความหมาย ความเข้าใจ และความสัมพันธ์ที่ไม่ตื้น",
         "แต่คุณต้องระวังความเมตตาที่ทำให้ยอมทนกับสิ่งที่ควรปล่อย"],
        ["In love, you seek meaning, emotional understanding, and depth.",
         "But you must watch for compassion becoming the reason you stay in what should already be released."],
        ["คุณเหมาะกับงานเยียวยา สอน ช่วยเหลือ สร้างแรงบันดาลใจ หรือสิ่งที่ส่งผลต่อผู้คนในวงกว้าง",
         "ชีวิตคุณเด่นเมื่อสิ่งที่ทำมีคุณค่าต่อมากกว่าตัวเอง"],
        ["You suit healing, teaching, helping, inspiring, or work that impacts people on a larger scale.",
         "Your life becomes powerful when what you do serves more than just yourself."],
        ["การเงินของคุณมั่นคงขึ้นเมื่อคุณเลิกคิดว่าจิตวิญญาณกับความอุดมสมบูรณ์ไปด้วยกันไม่ได้",
         "คุณทำเงินได้ดีเมื่อสิ่งที่ทำมีหัวใจและมีขอบเขตที่ชัด"],
        ["Your finances become steadier when you stop believing spirituality and abundance cannot coexist.",
         "You do well financially when your work has heart and clear boundaries."],
        ["บาดแผลของคุณคือการติดอยู่กับสิ่งที่หมดเวลาแล้วเพราะยังรักหรือยังรู้สึกผูกพัน",
         "จึงมีหลายช่วงที่คุณยอมเจ็บนานกว่าที่ควรเพราะไม่อยากปล่อยมือ"],
        ["Your wound is staying attached to what has already ended because love or emotional connection still remains.",
         "So there are times you hurt longer than necessary because letting go feels like betrayal."],
        ["ของขวัญของคุณคือหัวใจที่มองเห็นมนุษย์อย่างลึกและสามารถเปลี่ยนความเจ็บให้กลายเป็นความหมาย",
         "คุณมีพลังส่งต่อบางสิ่งที่เยียวยาใจคนหมู่มากได้"],
        ["Your gift is a heart that sees humanity deeply and can turn pain into meaning.",
         "You hold the ability to offer something that heals many people at once."],
        ["บทเรียนของคุณคือการปล่อยวางโดยไม่ต้องหยุดรัก",
         "เมื่อคุณรู้ว่าการปล่อยมือไม่ใช่การทรยศหัวใจ คุณจะเบาขึ้นมาก"],
        ["Your lesson is learning to release without needing to stop loving.",
         "When you understand that letting go is not a betrayal of the heart, you become much lighter."],
        ["เริ่มปิดวงจรที่ค้างทีละเรื่อง ไม่ว่าจะเป็นคน ความหวัง หรือเรื่องในใจที่ค้างมานาน",
         "พลังของคุณจะกลับมาเมื่อคุณไม่แบกสิ่งที่หมดเวลาแล้ว"],
        ["Begin closing unfinished cycles one by one—whether they are people, hopes, or old emotional stories.",
         "Your energy returns when you stop carrying what has already expired."],
        ["ระวังการใช้เมตตาเป็นข้ออ้างในการอยู่ต่อในสิ่งที่ทำร้ายคุณ",
         "ถ้าคุณไม่ยอมปล่อย วงจรเดิมจะกลับมาทดสอบซ้ำอีก"],
        ["Be careful not to use compassion as a reason to stay in what harms you.",
         "If you refuse to release, the old cycle will return for another lesson."],
        ["สิ่งที่คุณต้องปล่อย ไม่ได้แปลว่าคุณรักน้อยลง แต่มันแปลว่าคุณเริ่มรักตัวเองด้วย"],
        ["What you release does not mean you love less. It means you are finally including yourself in that love."]
    ),
    11: make_profile(
        ["คุณมีพลังของผู้ตื่นรู้ ญาณรู้ และการรับรู้สิ่งที่ลึกกว่าระดับผิว",
         "ชีวิตของคุณมักมีช่วงที่ดูเหมือนแรงเกินไปหรืออ่อนไหวเกินไป เพราะคุณรับคลื่นได้มากกว่าคนทั่วไป"],
        ["You carry awakened energy, heightened intuition, and the ability to sense what lies beyond the surface.",
         "Your life may often feel intense or overly sensitive because you receive more than most people do."],
        ["เมื่อพลังตก คุณอาจสับสนในสิ่งที่ตัวเองรับรู้ รู้สึกเหนื่อยง่าย หรือแยกไม่ออกว่าอะไรเป็นของตัวเองอะไรเป็นของคนอื่น",
         "บทเรียนของคุณคือการฝังแสงลงบนพื้นดิน ไม่ใช่ลอยอยู่กับความรู้สึกอย่างเดียว"],
        ["When your energy drops, you may doubt what you sense, feel easily drained, or struggle to separate your energy from others.",
         "Your lesson is to ground your light instead of floating only in feeling."],
        ["ในความรัก คุณต้องการความเชื่อมโยงระดับวิญญาณ แต่ก็ต้องการคนที่มั่นคงพอจะอยู่กับความลึกของคุณได้",
         "คุณไม่เหมาะกับความสัมพันธ์ที่เล่นเกมหรือไม่ชัดเจน"],
        ["In love, you seek soul-level connection, but you also need someone stable enough to meet your depth.",
         "You are not built for games or emotional vagueness."],
        ["คุณเหมาะกับงานที่ผสานจิตวิญญาณกับการสื่อสาร การสอน การเยียวยา หรือการสร้างแรงบันดาลใจ",
         "ชีวิตคุณจะเด่นเมื่อสิ่งที่คุณรับรู้ถูกแปลออกมาเป็นประโยชน์ต่อผู้คน"],
        ["You suit work that bridges spirituality with communication, teaching, healing, or inspiration.",
         "Your life path becomes powerful when what you sense is translated into something useful for others."],
        ["การเงินของคุณดีขึ้นเมื่อคุณหยุดลดทอนของขวัญตัวเอง",
         "สิ่งที่คุณมองว่าเป็นเรื่องลึกหรือธรรมดาสำหรับคุณ อาจเป็นสิ่งล้ำค่าสำหรับคนอื่น"],
        ["Your finances improve when you stop minimizing your gifts.",
         "What feels normal or deeply personal to you may actually be profoundly valuable to others."],
        ["บาดแผลของคุณคือความรู้สึกว่าโลกนี้อาจไม่เข้าใจความไวและความลึกของคุณ",
         "จึงมีบางช่วงที่คุณสงสัยตัวเอง ทั้งที่จริงคุณรับรู้อะไรได้มากกว่าที่คิด"],
        ["Your wound is the feeling that this world may not understand your sensitivity and depth.",
         "So there are times you doubt yourself even though you perceive far more than you realize."],
        ["ของขวัญของคุณคือการเห็นสัญญาณ เชื่อมสิ่งที่มองไม่เห็น และแปลมันออกมาให้ผู้คนเข้าใจได้",
         "คุณมีแสงของผู้ปลุกให้คนอื่นเริ่มตื่นในแบบของตัวเอง"],
        ["Your gift is perceiving signals, bridging the unseen, and translating it into something others can understand.",
         "You carry the light of an awakener who helps others begin to wake in their own way."],
        ["บทเรียนของคุณคือการทำให้สิ่งที่ลึกและละเอียดมีรากอยู่ในชีวิตจริง",
         "เมื่อคุณฝังแสงลงกับโครงสร้าง พลังของคุณจะเปลี่ยนชีวิตคนได้จริง"],
        ["Your lesson is grounding the subtle and the profound into real life.",
         "When you anchor your light in structure, your energy can truly transform lives."],
        ["เริ่มเชื่อสิ่งที่คุณรับรู้มากขึ้น แต่ให้มันมีพื้นที่ลงมือจริงควบคู่ไปด้วย",
         "สิ่งที่คุณเห็นจะมีพลังมากขึ้นเมื่อถูกจัดเป็นภาษา งาน หรือระบบที่ส่งต่อได้"],
        ["Start trusting what you sense more, but give it real-world channels of expression.",
         "What you perceive becomes more powerful when it is shaped into language, work, or systems that can be shared."],
        ["ระวังการเปิดรับทุกอย่างจนตัวเองพร่าและหมดแรง",
         "ถ้าคุณไม่แยกพลังตัวเองออกจากสิ่งรอบข้าง คุณจะเหนื่อยจนลืมว่าของขวัญตัวเองคืออะไร"],
        ["Be careful not to open yourself to everything until your energy becomes blurred and depleted.",
         "If you do not separate your own energy from what surrounds you, exhaustion can make you forget your gift."],
        ["คุณไม่ได้แปลกเกินไป คุณแค่รับแสงได้มากเกินกว่าที่โลกทั่วไปสอนให้เข้าใจ"],
        ["You are not too strange. You simply receive more light than the ordinary world knows how to explain."]
    ),
    22: make_profile(
        ["คุณมีพลังของผู้สร้างสิ่งใหญ่ให้เป็นจริง เห็นภาพกว้างและมีศักยภาพสร้างผลกระทบที่ยาวไกล",
         "คุณไม่ได้มีพลังแค่ฝัน แต่มีพลังทำให้สิ่งนั้นลงสู่โลกจริง"],
        ["You carry the energy of the master builder—someone who can see the bigger vision and create long-range impact.",
         "Your power is not just in dreaming, but in bringing that dream into reality."],
        ["เมื่อพลังตก คุณอาจรู้สึกหนักกับภาระ รู้สึกว่าต้องแบกอะไรใหญ่เกินไป หรือกลัวความรับผิดชอบในศักยภาพตัวเอง",
         "บทเรียนสำคัญคือการสร้างใหญ่โดยไม่แบกทุกอย่างคนเดียว"],
        ["When your energy drops, you may feel overwhelmed by responsibility or afraid of the scale of your own potential.",
         "Your lesson is to build big without carrying everything alone."],
        ["ในความรัก คุณต้องการคนที่เดินเติบโตไปด้วยกัน ไม่ใช่ความสัมพันธ์ที่ดึงคุณออกจากภารกิจชีวิต",
         "คุณรักจริงจังและมองไกล จึงต้องการความสัมพันธ์ที่มีรากฐาน"],
        ["In love, you need someone who can grow alongside you rather than pull you away from your mission.",
         "You love seriously and think long-term, so relationships need foundation."],
        ["คุณเหมาะกับการสร้างธุรกิจ ระบบ แพลตฟอร์ม ทีม หรือสิ่งที่ส่งผลต่อผู้คนจำนวนมาก",
         "คุณมีพลังทำวิสัยทัศน์ให้เป็นสิ่งจับต้องได้ ถ้ากล้าค่อย ๆ วางโครงอย่างมีวินัย"],
        ["You suit building businesses, systems, platforms, teams, or anything that serves many people.",
         "You can turn vision into form when you commit to structure and long-term discipline."],
        ["การเงินของคุณมีศักยภาพสูงมากเมื่อคุณทำสิ่งที่ใหญ่พอจะรับพลังคุณได้",
         "คุณไม่ได้เกิดมาเพื่อแค่พออยู่ แต่เพื่อสร้างสิ่งที่มั่นคงและส่งต่อได้"],
        ["Your financial potential is high when you engage in work big enough to hold your energy.",
         "You were not born only to survive—you were born to build something strong and transmissible."],
        ["บาดแผลของคุณคือความรู้สึกว่าภารกิจที่อยู่ในใจมันใหญ่เกินไปสำหรับชีวิตจริง",
         "จึงมีบางช่วงที่คุณหนีศักยภาพตัวเองด้วยการถอยไปทำแค่สิ่งเล็ก ๆ ที่ปลอดภัยกว่า"],
        ["Your wound is the feeling that the mission inside you is too large for ordinary life to hold.",
         "So there are times you avoid your potential by shrinking into what feels safer and smaller."],
        ["ของขวัญของคุณคือการเห็นทั้งภาพใหญ่และภาพลงมือจริงในเวลาเดียวกัน",
         "คุณสามารถสร้างสิ่งที่ไม่ใช่แค่สำเร็จ แต่ส่งผลยาวไกลต่อผู้คนจำนวนมาก"],
        ["Your gift is seeing both the larger vision and the practical steps at the same time.",
         "You can build things that are not only successful, but deeply impactful for many people."],
        ["บทเรียนของคุณคือการยอมรับว่าไม่จำเป็นต้องสร้างทุกอย่างคนเดียวเพื่อให้มันยิ่งใหญ่",
         "เมื่อคุณเปิดรับโครงสร้าง ทีม และจังหวะที่เหมาะ ภารกิจของคุณจะไปได้ไกลขึ้น"],
        ["Your lesson is accepting that you do not need to build everything alone for it to matter.",
         "When you allow structure, support, and timing, your mission can travel much farther."],
        ["เริ่มแบ่งวิสัยทัศน์ใหญ่ออกเป็นก้าวที่ทำจริงได้ทีละส่วน",
         "สิ่งที่ยิ่งใหญ่ที่สุดจะเกิดขึ้นเมื่อคุณหยุดมองว่ามันต้องเสร็จทั้งหมดในครั้งเดียว"],
        ["Start breaking your larger vision into steps that can truly be built.",
         "The greatest work emerges when you stop believing it must all be completed at once."],
        ["ระวังการผลักตัวเองด้วยมาตรฐานที่หนักจนหมดแรงก่อนสิ่งใหญ่จะเป็นรูปเป็นร่าง",
         "ถ้าคุณไม่เคารพจังหวะของตัวเอง ความฝันใหญ่จะกลายเป็นภาระ"],
        ["Be careful not to drive yourself with such heavy standards that you burn out before the vision takes form.",
         "If you do not honor your own timing, the great dream becomes a burden."],
        ["อย่ากลัวศักยภาพของตัวเอง เพราะสิ่งที่ดูใหญ่ในใจคุณ อาจเป็นเหตุผลที่คุณมาเกิด"],
        ["Do not fear your own potential. What feels huge inside you may be one of the reasons you came here."]
    ),
    33: make_profile(
        ["คุณมีพลังของครูผู้เยียวยา เมตตา ลึก ซื่อสัตย์กับหัวใจ และมีแรงผลักดันที่จะส่งบางอย่างที่ช่วยผู้คนได้จริง",
         "พลังของคุณไม่ใช่แค่เข้าใจความเจ็บปวด แต่สามารถแปรมันเป็นแสงให้คนอื่นได้"],
        ["You carry the energy of the healing teacher—compassionate, deep, heart-led, and moved to offer something genuinely helpful to people.",
         "Your gift is not only understanding pain, but turning it into light for others."],
        ["เมื่อพลังตก คุณอาจแบกความทุกข์คนอื่นมากไป คาดหวังกับตัวเองสูง และลืมว่าแม้ผู้เยียวยาก็ต้องได้รับการเยียวยา",
         "บทเรียนคือการรับใช้โดยไม่สูญเสียหัวใจตัวเอง"],
        ["When your energy drops, you may carry too much of others’ pain, hold impossible standards for yourself, and forget that healers also need healing.",
         "Your lesson is to serve without losing your own heart."],
        ["ในความรัก คุณต้องการความสัมพันธ์ที่อบอุ่น ลึก และช่วยให้ทั้งสองคนเติบโต",
         "แต่คุณต้องระวังบทบาทผู้ช่วยชีวิตที่ทำให้หัวใจเหนื่อย"],
        ["In love, you seek warmth, emotional depth, and a bond that helps both people grow.",
         "But you must watch for the savior role that exhausts the heart."],
        ["คุณเหมาะกับงานสอน เยียวยา โค้ช สื่อสารจากหัวใจ หรือธุรกิจที่สร้างการเปลี่ยนแปลงกับชีวิตคน",
         "ความสำเร็จของคุณมาเมื่อภารกิจและการลงมือจริงเดินไปด้วยกัน"],
        ["You suit teaching, healing, coaching, heart-led communication, or work that genuinely transforms lives.",
         "Your success comes when mission and practical action walk together."],
        ["การเงินของคุณไม่ควรถูกตัดออกจากภารกิจ คุณสามารถได้รับอย่างงดงามจากสิ่งที่ช่วยผู้คน",
         "คุณไม่ได้จำเป็นต้องเลือกระหว่างหัวใจกับความอุดมสมบูรณ์"],
        ["Your finances do not need to be separated from your mission. You can receive beautifully through work that helps people.",
         "You do not have to choose between heart and abundance."],
        ["บาดแผลของคุณคือความรู้สึกว่าตัวเองต้องแบกรับหรือเยียวยาทุกอย่างให้คนอื่นถึงจะมีคุณค่า",
         "จึงมีช่วงที่คุณเหนื่อยลึกโดยที่คนรอบข้างอาจไม่เห็นด้วยซ้ำ"],
        ["Your wound is the feeling that you must carry or heal everything for others in order to have value.",
         "So there are times you become deeply exhausted in ways people around you may not even notice."],
        ["ของขวัญของคุณคือการเปลี่ยนความเจ็บให้กลายเป็นปัญญาและส่งต่อแสงด้วยหัวใจจริง",
         "คุณมีพลังปลอบ ประคอง และเปิดประตูให้คนกลับมารักตัวเองได้"],
        ["Your gift is turning pain into wisdom and transmitting light through a sincere heart.",
         "You can comfort, hold, and open the door for people to love themselves again."],
        ["บทเรียนของคุณคือการรับใช้โดยไม่ใช้ชีวิตตัวเองเป็นเครื่องเผาไหม้",
         "เมื่อคุณเคารพพลังตัวเอง งานเยียวยาของคุณจะทรงพลังกว่าเดิมมาก"],
        ["Your lesson is learning to serve without using your own life-force as fuel to burn through.",
         "When you honor your own energy, your healing work becomes far more powerful."],
        ["เริ่มแยกให้ออกว่าอะไรคือการให้ด้วยหัวใจ และอะไรคือการให้เพราะกลัวจะไม่มีคุณค่า",
         "พลังของคุณจะไหลงดงามขึ้นเมื่อการดูแลเริ่มรวมตัวคุณเข้าไปด้วย"],
        ["Begin noticing the difference between giving from the heart and giving because you fear losing your worth.",
         "Your energy flows more beautifully when your care begins to include yourself."],
        ["ระวังการช่วยคนจนหลุดจากแกนตัวเอง",
         "ถ้าคุณไม่ดูแลแสงของตัวเองก่อน วันหนึ่งคุณจะเหลือแต่บทบาท แต่ไม่เหลือหัวใจ"],
        ["Be careful not to help others so much that you lose your own center.",
         "If you do not tend to your own light first, one day you may be left with only the role and not the heart."],
        ["การเป็นแสงให้คนอื่น ไม่จำเป็นต้องแผดเผาตัวเองจนหมดแรง"],
        ["Being a light for others does not require burning yourself out."]
    ),
}

BIRTH_DAY_LIBRARY = {
    1: {"th": "วันเกิดของคุณเติมพลังความกล้าและความเป็นตัวของตัวเอง", "en": "Your birth day amplifies courage and self-led energy."},
    2: {"th": "วันเกิดของคุณเติมพลังความอ่อนโยนและการรับรู้อารมณ์", "en": "Your birth day amplifies gentleness and emotional sensitivity."},
    3: {"th": "วันเกิดของคุณเติมพลังการสื่อสาร ความคิดสร้างสรรค์ และเสน่ห์ตามธรรมชาติ", "en": "Your birth day amplifies expression, creativity, and natural charm."},
    4: {"th": "วันเกิดของคุณเติมพลังความมั่นคง ความรับผิดชอบ และความจริงจัง", "en": "Your birth day amplifies stability, responsibility, and grounded focus."},
    5: {"th": "วันเกิดของคุณเติมพลังการเปลี่ยนแปลง ความคล่องตัว และอิสรภาพ", "en": "Your birth day amplifies change, adaptability, and freedom."},
    6: {"th": "วันเกิดของคุณเติมพลังการดูแล การเยียวยา และความรักที่ลึก", "en": "Your birth day amplifies care, healing, and deep love."},
    7: {"th": "วันเกิดของคุณเติมพลังการค้นหาความหมายและโลกภายในที่ลึก", "en": "Your birth day amplifies introspection and the search for deeper meaning."},
    8: {"th": "วันเกิดของคุณเติมพลังความสำเร็จ อำนาจภายใน และการสร้างผลลัพธ์", "en": "Your birth day amplifies achievement, inner authority, and tangible results."},
    9: {"th": "วันเกิดของคุณเติมพลังเมตตา การเข้าใจมนุษย์ และการปล่อยวาง", "en": "Your birth day amplifies compassion, understanding, and release."},
    11: {"th": "วันเกิดของคุณเติมพลังญาณรู้และความไวต่อสัญญาณชีวิต", "en": "Your birth day amplifies intuition and sensitivity to life signals."},
    22: {"th": "วันเกิดของคุณเติมพลังผู้สร้างและความสามารถในการทำสิ่งใหญ่ให้เป็นจริง", "en": "Your birth day amplifies builder energy and the ability to manifest larger visions."},
    33: {"th": "วันเกิดของคุณเติมพลังครูผู้เยียวยาและหัวใจแห่งการรับใช้", "en": "Your birth day amplifies the healing teacher archetype and heartfelt service."},
}

QUESTION_SIGNALS = {
    "love": {
        "th": ["รัก", "แฟน", "คนคุย", "เลิก", "นอกใจ", "ความสัมพันธ์", "คู่", "คิดถึง", "กลับมา", "เจ็บใจ"],
        "en": ["love", "relationship", "partner", "breakup", "heart", "ex", "romance", "separation"]
    },
    "career": {
        "th": ["งาน", "อาชีพ", "อนาคต", "เปลี่ยนงาน", "เป้าหมาย", "หมดไฟ", "เหนื่อย", "เส้นทาง", "ธุรกิจ", "คอนเทนต์"],
        "en": ["work", "career", "job", "future", "business", "purpose", "burnout", "path", "content"]
    },
    "money": {
        "th": ["เงิน", "หนี้", "รายได้", "การเงิน", "โชค", "ขาย", "ลูกค้า", "ติดขัด", "หมุนเงิน"],
        "en": ["money", "debt", "income", "finance", "cash", "clients", "sales", "blocked"]
    },
    "emotion": {
        "th": ["หลงทาง", "เหนื่อย", "สับสน", "กลัว", "กังวล", "เศร้า", "ติดขัด", "โดดเดี่ยว"],
        "en": ["lost", "tired", "confused", "afraid", "worry", "sad", "alone", "stuck"]
    }
}

# -----------------------------
# Content helpers
# -----------------------------
def detect_question_signal(question_text: str):
    text = (question_text or "").lower().strip()
    scores = {"love": 0, "career": 0, "money": 0, "emotion": 0}
    for signal_key, lang_map in QUESTION_SIGNALS.items():
        for kw in lang_map["th"] + lang_map["en"]:
            if kw.lower() in text:
                scores[signal_key] += 1
    return max(scores, key=scores.get) if max(scores.values()) > 0 else None

def get_profile(life_number: int):
    return safe_get(PROFILE_LIBRARY, life_number, PROFILE_LIBRARY[7])

def life_intro(life_number: int, birth_energy: int, month_num: int, lang: str):
    profile = get_profile(life_number)
    core_text = paragraph(profile["core"][lang])
    birth_text = safe_get(BIRTH_DAY_LIBRARY, birth_energy, BIRTH_DAY_LIBRARY[7])[lang]
    month_text = safe_get(month_energy_meanings, month_num, month_energy_meanings[7])[lang]
    if lang == "th":
        return f"{core_text} {birth_text} และพลังเดือนเกิดของคุณยังสะท้อนถึง{month_text} จึงทำให้เส้นทางชีวิตของคุณมีทั้งความลึก ความหมาย และบทเรียนที่เชื่อมกับการเติบโตภายใน"
    return f"{core_text} {birth_text} Your birth month also reflects {month_text}, which adds inner depth, meaning, and soul-level growth to your life path."

def category_reflection(category_key: str, life_number: int, lang: str):
    profile = get_profile(life_number)
    if category_key == "love":
        return paragraph(profile["love"][lang])
    if category_key == "career":
        return paragraph(profile["career"][lang])
    return paragraph(profile["money"][lang])

def current_focus_block(category_key: str, question_signal: str, life_number: int, lang: str):
    if lang == "th":
        base_map = {
            "love": "ช่วงนี้หัวใจของคุณกำลังสอนให้แยกความรักออกจากความกลัวที่จะสูญเสีย",
            "career": "ช่วงนี้ชีวิตกำลังกดให้คุณมองเส้นทางงานใหม่อย่างจริงจังมากขึ้น",
            "money": "ช่วงนี้กระแสการเงินกำลังชี้ให้คุณเห็นความสัมพันธ์ระหว่างคุณค่าตัวเองกับการรับความอุดมสมบูรณ์"
        }
        signal_map = {
            "emotion": "และจากสิ่งที่คุณพิมพ์เข้ามา ข้างในคุณกำลังต้องการความชัดเจน ความเบาใจ และการกลับมายืนอยู่กับตัวเองอีกครั้ง",
            "love": "คำถามของคุณยังสะท้อนว่าความสัมพันธ์นี้แตะบางแผลลึกที่กำลังรอการเข้าใจอย่างแท้จริง",
            "career": "คำถามของคุณสะท้อนว่าชีวิตกำลังบอกให้คุณหยุดฝืนกับเส้นทางที่ไม่สอดคล้องแล้ว",
            "money": "คำถามของคุณสะท้อนว่าประเด็นเรื่องเงินตอนนี้ไม่ได้มีแค่เรื่องตัวเลข แต่เชื่อมกับความมั่นคงทางใจและความรู้สึกมีคุณค่า"
        }
    else:
        base_map = {
            "love": "At this stage, your heart is learning to separate love from the fear of losing.",
            "career": "Right now, life is pushing you to look at your work path more honestly and more seriously.",
            "money": "At this stage, your financial flow is revealing the connection between self-worth and receiving abundance."
        }
        signal_map = {
            "emotion": "From what you wrote, there is a clear need for inner clarity, emotional relief, and a return to your own center.",
            "love": "Your question also suggests that this relationship is touching a deeper wound waiting to be understood.",
            "career": "Your question reflects a moment where life is asking you to stop forcing a path that no longer aligns.",
            "money": "Your question suggests that money right now is not only about numbers, but also about emotional safety and worth."
        }
    text = base_map.get(category_key, base_map["career"])
    if question_signal in signal_map:
        text += " " + signal_map[question_signal]
    if life_number in (7, 11, 33):
        text += " " + ("นี่ไม่ใช่สัญญาณว่าคุณพัง แต่คือสัญญาณว่าคุณกำลังตื่นลึกขึ้น" if lang == "th" else "This is not a sign that you are broken. It may be a sign that you are awakening more deeply.")
    return text

def generate_free_reflection(name: str, category_key: str, day_num: int, month_num: int, year_num: int, question_text: str, lang: str):
    life_num = life_path_number(day_num, month_num, year_num)
    birth_energy = birth_day_energy(day_num)
    q_signal = detect_question_signal(question_text)
    title = f"🔮 ผลสะท้อนพลังงานเบื้องต้น: คุณ {name}" if lang == "th" else f"🔮 Your Initial Energy Reflection: {name}"
    return {
        "title": title,
        "life_number": life_num,
        "birth_energy": birth_energy,
        "intro": life_intro(life_num, birth_energy, month_num, lang),
        "category_text": category_reflection(category_key, life_num, lang),
        "focus_text": current_focus_block(category_key, q_signal, life_num, lang),
        "question_signal": q_signal
    }

def generate_premium_reflection(name: str, category_key: str, day_num: int, month_num: int, year_num: int, question_text: str, lang: str):
    life_num = life_path_number(day_num, month_num, year_num)
    birth_energy = birth_day_energy(day_num)
    profile = get_profile(life_num)
    if lang == "th":
        premium_title = f"✨ พิมพ์เขียวพลังงานเชิงลึกของคุณ {name}"
        soul_text = (
            f"{name} คุณไม่ได้มาถึงจุดนี้โดยบังเอิญ "
            f"เลขเส้นทางชีวิต {life_num} ของคุณสะท้อนว่าชีวิตกำลังสอนให้คุณกลับมาใช้พลังแท้ของตัวเองอย่างมีสติ "
            f"ขณะเดียวกันเลขวันเกิด {birth_energy} ก็เติมโทนเฉพาะตัวให้คุณมีวิธีแสดงพลังชีวิตออกมาในแบบของตัวเอง "
            f"นี่คือช่วงที่ชีวิตไม่ได้ต้องการให้คุณเก่งขึ้นอย่างเดียว แต่ต้องการให้คุณจริงกับตัวเองมากขึ้นด้วย"
        )
    else:
        premium_title = f"✨ Your Deep Energy Blueprint: {name}"
        soul_text = (
            f"{name}, you did not arrive at this point by accident. "
            f"Your Life Path {life_num} suggests that life is asking you to return to your real power with greater awareness. "
            f"Your Birth Day Energy {birth_energy} adds its own signature to how that power wants to be expressed. "
            f"This is not only a season of becoming stronger—it is a season of becoming more honest with yourself."
        )
    return {
        "premium_title": premium_title,
        "soul_text": soul_text,
        "shadow": paragraph(profile["shadow"][lang]),
        "wound": paragraph(profile["wound"][lang]),
        "gift": paragraph(profile["gift"][lang]),
        "lesson": paragraph(profile["lesson"][lang]),
        "next_step": paragraph(profile["next_step"][lang]),
        "warning": paragraph(profile["warning"][lang]),
        "healing": paragraph(profile["healing"][lang]),
        "unlock_note": (
            "หากข้อความนี้สะท้อนชีวิตคุณจริง คุณสามารถใช้ผลลัพธ์นี้เป็นสะพานต่อไปยัง eBook หรือการอ่านส่วนตัวเชิงลึกได้"
            if lang == "th" else
            "If this resonates deeply, you can use this result as a bridge into your eBook or a deeper personal reading."
        )
    }

# -----------------------------
# Header
# -----------------------------
st.markdown(
f"""
<div class="hero-header-box">
<div class="top-floating-lang">
<a href="?lang=th" class="lang-chip {'active' if st.session_state.lang == 'th' else ''}">TH</a>
<a href="?lang=en" class="lang-chip {'active' if st.session_state.lang == 'en' else ''}">EN</a>
</div>
<div class="hero-title-wrap" style="margin-bottom:0;">
<div class="hero-brand" style="margin-bottom:0;">🔮 LUMINA SOUL</div>
</div>
</div>
""",
unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="hero-subtitle" style="margin-top:8px; margin-bottom:8px;">
        {tr("พื้นที่สะท้อนชีวิต | ถอดรหัสลับพลังงานวันเกิด", "A space for reflection | Decode your birth energy")}
    </div>
    """,
    unsafe_allow_html=True
)

st.write("---")

st.markdown(
    f"""
    <div class="hero-card">
        <p class='center-text' style='font-size:1.05rem; margin-bottom:8px;'>
        {tr(
            "ยินดีต้อนรับสู่พื้นที่แห่งการตื่นรู้และเยียวยาใจ ผ่านสัญญาณจากชีวิตและรหัสลับวันเกิด เพื่อช่วยให้คุณเข้าใจตัวเองลึกขึ้น",
            "Welcome to a space of awakening and healing through life signals and birth-energy decoding—created to help you understand yourself more deeply."
        )}
        </p>
        <p class='center-text soft-note' style='margin-bottom:0;'>
        {tr(
            "นี่ไม่ใช่คำทำนายอนาคต แต่คือการสะท้อนพลังงานชีวิตในช่วงเวลานี้",
            "This is not fortune telling. It is an energetic reflection of your life in this moment."
        )}
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="glow-box">
        <p style="margin:0; color:#3576c5 !important; font-weight:600;">
        {tr(
            "✨ บางคำตอบในชีวิต อาจเริ่มต้นจากการเข้าใจพลังงานของตัวเอง",
            "✨ Some of life’s answers may begin with understanding your own energy"
        )}
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(tr("### 🔯 ทำไมหลายคนถึงเริ่มจากการถอดรหัสพลังงานชีวิต", "### 🔯 Why many people begin with decoding their life energy"))

c1, c2, c3 = st.columns(3)
with c1:
    st.markdown(f"""
        <div class="stat-card">
            <div style="font-size:1.15rem; font-weight:700; color:#8e24aa;">{tr("⭐️เข้าใจตัวเอง", "Know Yourself")}</div>
            <div class="soft-note">{tr("เห็นจุดแข็ง จุดเปลี่ยน และบทเรียนที่กำลังเกิดขึ้น", "See your strengths, turning points, and the lessons unfolding in your life")}</div>
        </div>
    """, unsafe_allow_html=True)
with c2:
    st.markdown(f"""
        <div class="stat-card">
            <div style="font-size:1.15rem; font-weight:700; color:#8e24aa;">{tr("⭐️สะท้อนชีวิต", "Reflect on Life")}</div>
            <div class="soft-note">{tr("ช่วยมองความรัก งาน และการเงินในมุมที่ลึกขึ้น", "Gain deeper insight into love, career, and financial flow")}</div>
        </div>
    """, unsafe_allow_html=True)
with c3:
    st.markdown(f"""
        <div class="stat-card">
            <div style="font-size:1.15rem; font-weight:700; color:#8e24aa;">{tr("⭐️ต่อยอดได้จริง", "Take It Further")}</div>
            <div class="soft-note">{tr("หากรู้สึกว่าตรง คุณสามารถปลดล็อคคำอ่านฉบับเต็มได้ทันที", "If it resonates, you can unlock the full reading immediately")}</div>
        </div>
    """, unsafe_allow_html=True)

# -----------------------------
# Form
# -----------------------------
month_display_list = [m["th"] if st.session_state.lang == "th" else m["en"] for m in month_options]
category_display_list = [c["th"] if st.session_state.lang == "th" else c["en"] for c in categories]

with st.form("lumina_form_phase2"):
    name = st.text_input(tr("ชื่อ-นามสกุล", "Full Name"))
    contact = st.text_input(
        tr(
            "ID Line (เพื่อรับผลสะท้อนพลังงานและสิทธิ์อ่านเชิงลึก)",
            "Line ID (to receive your reflection and deeper reading access)"
        )
    )
    col1, col2, col3 = st.columns(3)
    with col1:
        birth_day = st.number_input(tr("วันที่เกิด", "Birth Day"), min_value=1, max_value=31, value=1, step=1)
    with col2:
        birth_month_index = st.selectbox(
            tr("เดือนเกิด", "Birth Month"),
            range(len(month_options)),
            format_func=lambda i: month_display_list[i]
        )
    with col3:
        birth_year = st.number_input(
            tr("ปี พ.ศ. เกิด", "Birth Year (B.E.)"),
            min_value=2450,
            max_value=2600,
            value=2535,
            step=1
        )

    category_index = st.selectbox(
        tr("ด้านที่คุณต้องการรับพลังงานนำทางในวันนี้:", "Which area would you like energetic guidance for today?"),
        range(len(categories)),
        format_func=lambda i: category_display_list[i]
    )

    st.markdown(f"**{tr('⭐️ เรื่องที่คุณกังวลใจที่สุดในตอนนี้คืออะไร?', '⭐️ What is your biggest concern right now?')}**")
    question = st.text_area(
        "",
        placeholder=tr("แชร์รายละเอียดเรื่องที่ติดค้างในใจแบบสั้น ๆ", "Share a short description of what has been on your mind"),
        height=120
    )

    submitted = st.form_submit_button(tr("🔮 ถอดรหัสพลังงานของฉัน", "🔮 Decode My Energy"))

# -----------------------------
# Processing
# -----------------------------
if submitted:
    name_clean = name.strip()
    contact_clean = contact.strip()
    question_clean = question.strip()

    if len(name_clean) < 2:
        st.error(tr("กรุณากรอกชื่อ-นามสกุลให้ครบถ้วน", "Please enter your full name."))
    elif len(contact_clean) < 3:
        st.error(tr("กรุณากรอก ID Line ให้ถูกต้อง", "Please enter a valid Line ID."))
    elif len(question_clean) < 5:
        st.error(tr("กรุณาพิมพ์เรื่องที่กังวลใจสั้น ๆ เพื่อให้คำสะท้อนเหมาะกับคุณมากขึ้น", "Please share a short concern so your reflection can feel more personalized."))
    else:
        selected_month = month_options[birth_month_index]
        month_num = selected_month["num"]
        selected_category = categories[category_index]

        free_result = generate_free_reflection(
            name_clean,
            selected_category["key"],
            int(birth_day),
            month_num,
            int(birth_year),
            question_clean,
            st.session_state.lang
        )

        premium_result = generate_premium_reflection(
            name_clean,
            selected_category["key"],
            int(birth_day),
            month_num,
            int(birth_year),
            question_clean,
            st.session_state.lang
        )

        st.session_state.latest_result = {
            "name": name_clean,
            "contact": contact_clean,
            "question": question_clean,
            "category_key": selected_category["key"],
            "category_label_th": selected_category["th"],
            "category_label_en": selected_category["en"],
            "birth_day": int(birth_day),
            "birth_month_num": month_num,
            "birth_month_th": selected_month["th"],
            "birth_month_en": selected_month["en"],
            "birth_year": int(birth_year),
            "free": free_result,
            "premium": premium_result
        }

        push_to_google_sheet({
            "name": name_clean,
            "line_id": contact_clean,
            "birth_day": int(birth_day),
            "birth_month": selected_month["th"],
            "birth_month_en": selected_month["en"],
            "birth_year_be": int(birth_year),
            "life_path_number": free_result["life_number"],
            "birth_day_energy": free_result["birth_energy"],
            "category": selected_category["th"],
            "category_en": selected_category["en"],
            "question": question_clean,
            "free_intro": free_result["intro"],
            "free_category_text": free_result["category_text"],
            "free_focus_text": free_result["focus_text"],
            "premium_shadow": premium_result["shadow"],
            "premium_wound": premium_result["wound"],
            "premium_gift": premium_result["gift"],
            "premium_lesson": premium_result["lesson"],
            "premium_next_step": premium_result["next_step"],
            "premium_warning": premium_result["warning"],
            "premium_soul_text": premium_result["soul_text"],
            "premium_healing": premium_result["healing"],
            "language": st.session_state.lang,
            "source": "website_form_phase2",
            "submitted_at": str(datetime.now())
        })

        st.session_state.premium_unlocked = False
        st.session_state.used_code = ""
        st.balloons()

# -----------------------------
# Result rendering
# -----------------------------
if st.session_state.latest_result:
    data = st.session_state.latest_result
    free_result = data["free"]
    premium_result = data["premium"]

    st.write("---")
    st.success(free_result["title"])

    st.markdown(f"""
        <div class="result-card">
            <h4 style="color:#7b1fa2; margin-top:0;">{tr("🔢 เลขพลังงานของคุณ", "🔢 Your Energy Numbers")}</h4>
            <p><b>{tr("เลขเส้นทางชีวิต:", "Life Path Number:")}</b> {free_result["life_number"]}</p>
            <p><b>{tr("เลขพลังงานวันเกิด:", "Birth Day Energy:")}</b> {free_result["birth_energy"]}</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="mini-card">
            <h4 style="color:#8e24aa; margin-top:0;">{tr("🌙 พลังแกนกลางของคุณ", "🌙 Your Core Energy")}</h4>
            <p>{free_result["intro"]}</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="result-card">
            <h4 style="color:#ad1457; margin-top:0;">{tr("🔮 คำสะท้อนในด้านที่คุณเลือก", "🔮 Reflection for your chosen area")}</h4>
            <p>{free_result["category_text"]}</p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
        <div class="mini-card">
            <h4 style="color:#8e24aa; margin-top:0;">{tr("🪄 สิ่งที่ชีวิตกำลังบอกคุณตอนนี้", "🪄 What life may be showing you right now")}</h4>
            <p>{free_result["focus_text"]}</p>
        </div>
    """, unsafe_allow_html=True)

    if not st.session_state.premium_unlocked:
        lock_text_th = "สิ่งที่คุณเพิ่งอ่าน…เป็นเพียงชั้นแรกของพลังงานชีวิตคุณ ลึกลงไปกว่านั้น ยังมีความจริงบางอย่างที่รอการถูกเปิดเผย"
        lock_text_en = "What you have just read is only the first layer of your life energy. Deeper than this, there is a truth still waiting to be revealed."
        st.markdown(f"""
            <div class="lock-card">
                <h4 style="color:#8e24aa; margin-top:0;">🔒 {tr("คำอ่านฉบับลึกยังไม่ถูกเปิด", "Your deeper reading is still locked")}</h4>
                <p>{tr(lock_text_th, lock_text_en)}</p>
                <p>{tr("หากคุณได้รับ Soul Code จาก eBook หรือ LINE แล้ว สามารถใส่รหัสด้านล่างเพื่อปลดล็อคคำอ่านฉบับเต็มได้ทันที",
                         "If you already received a Soul Code from your eBook or LINE, enter it below to unlock your full reading.")}</p>
            </div>
        """, unsafe_allow_html=True)

        code_input = st.text_input(tr("✨ ใส่ Soul Code ของคุณ", "✨ Enter your Soul Code"))

        if st.button(tr("🔓 ปลดล็อคคำอ่านฉบับเต็ม", "🔓 Unlock Full Reading")):
            if verify_code(code_input):
                st.session_state.premium_unlocked = True
                st.session_state.used_code = code_input.strip().upper()
                st.rerun()
            else:
                st.error(tr(
                    "รหัสไม่ถูกต้อง หรือยังไม่ได้เปิดสิทธิ์ กรุณาตรวจสอบอีกครั้ง หรือทัก LINE เพื่อรับรหัส",
                    "The code is invalid or has not been activated yet. Please check again or contact LINE to receive your code."
                ))

        st.markdown(f"""
            <div class="premium-btn">
                <a href="{LINE_LINK}" target="_blank">
                    ✳️👉 {tr("รับ Soul Code ผ่าน LINE", "Get your Soul Code via LINE")}
                </a>
            </div>
        """, unsafe_allow_html=True)

    if st.session_state.premium_unlocked:
        st.markdown(f"""
            <div class="result-card">
                <h4 style="color:#7b1fa2; margin-top:0;">{premium_result["premium_title"]}</h4>
                <p>{premium_result["soul_text"]}</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="mini-card">
                <h4 style="color:#8e24aa; margin-top:0;">{tr("🌑 เงาพลังงานและบทเรียนลึก", "🌑 Shadow Pattern & Deeper Lesson")}</h4>
                <p>{premium_result["shadow"]}</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="mini-card">
                <h4 style="color:#8e24aa; margin-top:0;">{tr("🩹 บาดแผลที่ชีวิตกำลังชี้ให้เห็น", "🩹 The Wound Life May Be Revealing")}</h4>
                <p>{premium_result["wound"]}</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="mini-card">
                <h4 style="color:#8e24aa; margin-top:0;">{tr("💎 ของขวัญที่ซ่อนอยู่ในตัวคุณ", "💎 The Gift Hidden Within You")}</h4>
                <p>{premium_result["gift"]}</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="mini-card">
                <h4 style="color:#8e24aa; margin-top:0;">{tr("📖 บทเรียนที่ชีวิตกำลังสอน", "📖 The Lesson Life Is Teaching You")}</h4>
                <p>{premium_result["lesson"]}</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="mini-card">
                <h4 style="color:#8e24aa; margin-top:0;">{tr("🪄 แนวทางที่ควรโฟกัสต่อ", "🪄 Your Next Focus")}</h4>
                <p>{premium_result["next_step"]}</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="mini-card">
                <h4 style="color:#8e24aa; margin-top:0;">{tr("⚠️ สิ่งที่ควรระวัง", "⚠️ What to Be Careful With")}</h4>
                <p>{premium_result["warning"]}</p>
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="mini-card">
                <h4 style="color:#6a1b9a; margin-top:0;">{tr("✨ ข้อความจาก Lumina Soul", "✨ A Message from Lumina Soul")}</h4>
                <p>{premium_result["healing"]}</p>
            </div>
        """, unsafe_allow_html=True)

        st.info("💡 " + premium_result["unlock_note"])

        st.markdown(f"""
            <div class="cta-note">
            {tr(
                "หากคำอ่านนี้สะท้อนชีวิตคุณจริง ขั้นต่อไปคือ eBook หรือการอ่านเชิงลึกส่วนตัว เพื่อเชื่อมสิ่งที่คุณรู้สึกเข้ากับเส้นทางชีวิตจริง",
                "If this reading deeply resonates, your next step is the eBook or a personalized deep reading to connect what you feel with your real life path."
            )}
            </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
            <div class="premium-btn">
                <a href="{LINE_LINK}" target="_blank">
                    ✳️👉 {tr("คุยกับที่ปรึกษา LUMINA SOUL", "Talk to a LUMINA SOUL guide")}
                </a>
            </div>
        """, unsafe_allow_html=True)

# -----------------------------
# Footer
# -----------------------------
st.write("---")
st.markdown(
    f"<p style='text-align: center; font-size: 0.82rem; color: #888;'>© 2026 LUMINA SOUL | {tr('พื้นที่สะท้อนชีวิตและการตื่นรู้', 'A space for reflection and awakening')}</p>",
    unsafe_allow_html=True
)
''')

path = Path("/mnt/data/app_phase2.py")
path.write_text(app_code, encoding="utf-8")
print(str(path))
