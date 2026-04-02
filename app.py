import streamlit as st
import requests
from datetime import datetime

# =========================================================
# LUMINA SOUL — FULL APP.PY
# Copy-paste ready
# Keeps:
# - Google Sheets logging
# - LINE link
# - pastel premium spiritual brand
# - bilingual TH/EN
# Adds:
# - professional content structure
# - free reflection + locked premium section
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
# Existing links provided by user
# -----------------------------
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbztgbRuGYMGMC41V8QHgNl2wnNTgJ5ZhRckVoiUXpVNTkSA-U75MFg-GRZNiCiIjrQeGg/exec"
LINE_LINK = "https://lin.ee/uDDXuWN"
LINE_ID = "@908bgzai"

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
# Smaller libraries reused by all numbers
# -----------------------------
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
        "th": ["รัก", "แฟน", "คนคุย", "เลิก", "นอกใจ", "ความสัมพันธ์", "คู่", "คิดถึง", "เจ็บใจ", "กลับมา"],
        "en": ["love", "relationship", "partner", "breakup", "heart", "ex", "romance", "together", "separation"]
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
# Main content library (compact + scalable)
# -----------------------------
BASE_CORE = {
    1: {
        "th": "คุณเป็นคนที่ไม่ชอบให้ใครมากำหนดชีวิตแทน ลึก ๆ แล้วคุณอยากเลือกทางของตัวเองทั้งหมด แต่ที่ผ่านมา คุณอาจต้องฝืนอยู่ในสิ่งที่ไม่ใช่ตัวเองอยู่บ่อยครั้ง",
        "en": "You do not like other people deciding your life for you. Deep down, you want to choose your own path completely, but you may have often forced yourself to stay in places that do not truly fit you."
    },
    2: {
        "th": "คุณเป็นคนที่แคร์ความรู้สึกคนอื่นมาก และมักพยายามรักษาความสัมพันธ์ให้ราบรื่นเสมอ แต่หลายครั้งคุณกลับเก็บความรู้สึกตัวเองไว้ จนสุดท้ายคนอื่นไม่รู้เลยว่าจริง ๆ แล้วคุณรู้สึกยังไง",
        "en": "You care deeply about other people's feelings and often try to keep relationships peaceful. But many times, you hide your own feelings so well that others do not even know what you truly feel."
    },
    3: {
        "th": "คุณเป็นคนที่มีอะไรอยู่ในใจเยอะ คิดเยอะ รู้สึกเยอะ และมีมุมที่อยากสื่อสารออกไปมากกว่าที่คนเห็น แต่ที่ผ่านมา คุณอาจชินกับการเก็บบางอย่างไว้ เพราะกลัวว่าพูดไปแล้วคนจะไม่เข้าใจ",
        "en": "You hold a lot inside. You think deeply, feel deeply, and have more to express than people usually see. But you may have become used to holding parts of yourself back because you fear being misunderstood."
    },
    4: {
        "th": "คุณเป็นคนที่พยายามทำให้ชีวิตมั่นคงอยู่เสมอ และมักเป็นคนที่รับผิดชอบหลายอย่างมากกว่าที่คนอื่นรู้ ลึก ๆ แล้วคุณไม่ได้อยากแบกทุกอย่างคนเดียว แต่คุณมักรู้สึกว่าถ้าไม่ทำเอง ทุกอย่างอาจไม่เป็นอย่างที่ควร",
        "en": "You are someone who always tries to create stability in life and often carries more responsibility than people realize. Deep down, you do not truly want to carry everything alone, but you often feel that if you do not do it yourself, things may fall apart."
    },
    5: {
        "th": "คุณเป็นคนที่ต้องการอิสระ ต้องการพื้นที่ของตัวเอง และไม่ชอบรู้สึกว่าชีวิตถูกบีบจนหายใจไม่ออก แต่ที่ผ่านมา ชีวิตอาจพาคุณไปอยู่ในสถานการณ์ที่ต้องทน ต้องฝืน หรืออยู่ในสิ่งที่ไม่เป็นตัวเอง",
        "en": "You need freedom, space, and room to be yourself. You do not like feeling trapped or suffocated by life. But life may have often placed you in situations where you had to endure, force yourself, or stay in places that did not feel true to you."
    },
    6: {
        "th": "คุณเป็นคนที่ให้ความสำคัญกับคนที่รักมาก และมักทุ่มเทกับความสัมพันธ์หรือหน้าที่เกินกว่าที่คนอื่นเห็น ลึก ๆ แล้วคุณอยากให้ทุกอย่างอบอุ่นและลงตัว แต่บางครั้งคุณก็เผลอให้คนอื่นมากเกินไป จนตัวเองเริ่มเหนื่อยโดยไม่รู้ตัว",
        "en": "You place great importance on the people you love and often give more to relationships or responsibilities than others realize. Deep down, you want life to feel warm and harmonious. But sometimes you give so much that you begin to drain yourself without noticing."
    },
    7: {
        "th": "คุณเป็นคนที่คิดลึก รู้สึกลึก และมองเห็นอะไรบางอย่างที่คนอื่นอาจมองไม่เห็น คุณไม่ได้ต้องการแค่ใช้ชีวิตไปวัน ๆ แต่ต้องการเข้าใจว่าทั้งหมดนี้มีความหมายอะไร ลึก ๆ แล้วคุณอาจรู้สึกว่าตัวเองต่างจากคนอื่นอยู่เสมอ",
        "en": "You think deeply, feel deeply, and notice things that other people may not see. You are not someone who wants to simply drift through life. You want to understand what all of this truly means. Deep down, you may often feel different from others."
    },
    8: {
        "th": "คุณเป็นคนที่ดูเข้มแข็ง ดูเอาจริงเอาจัง และมักเป็นคนที่ผลักชีวิตให้เดินต่อ แม้ในวันที่เหนื่อยมาก ลึก ๆ แล้วคุณไม่ได้อยากแข็งแรงตลอดเวลา แต่ชีวิตมักสอนให้คุณต้องรับผิดชอบ ต้องเอาอยู่ และต้องไม่ล้มต่อหน้าคนอื่น",
        "en": "You come across as strong, serious, and often the one who keeps life moving forward even on exhausting days. Deep down, you do not always want to be strong, but life has often taught you to take responsibility, hold things together, and avoid falling apart in front of others."
    },
    9: {
        "th": "คุณเป็นคนที่มีหัวใจลึก มีความรู้สึกมาก และมักผูกพันกับสิ่งที่ตัวเองรักจริง คุณไม่ได้ลืมอะไรง่าย ๆ โดยเฉพาะเรื่องที่เคยสำคัญกับใจ ลึก ๆ แล้วคุณเป็นคนที่ทั้งรักเป็นและเจ็บเป็น จึงปล่อยบางอย่างยากกว่าที่คนอื่นคิด",
        "en": "You have a deep heart, strong emotions, and a powerful bond with what you truly love. You do not forget easily, especially when something once mattered to your heart. Deep down, you know how to love deeply and hurt deeply, which is why letting go can be harder for you than people realize."
    },
    11: {
        "th": "คุณเป็นคนที่รับรู้อะไรบางอย่างได้ไวและลึกกว่าคนทั่วไป บางครั้งคุณเองก็อธิบายไม่หมดว่าทำไมถึงรู้สึกแบบนั้น แต่หัวใจคุณมักจับบางอย่างได้ก่อนเสมอ ลึก ๆ แล้วคุณไม่ได้ต้องการชีวิตธรรมดา คุณต้องการชีวิตที่มีความหมายและมีบางอย่างเชื่อมถึงจิตวิญญาณจริง ๆ",
        "en": "You sense things faster and more deeply than most people. At times, even you may not be able to fully explain why you feel what you feel, but your heart often notices something first. Deep down, you are not seeking an ordinary life. You want a life that feels meaningful and spiritually real."
    },
    22: {
        "th": "คุณเป็นคนที่ไม่ได้คิดแค่เรื่องเล็ก ๆ ของตัวเอง แต่ลึก ๆ แล้วคุณมีภาพบางอย่างที่ใหญ่กว่านั้นอยู่ในใจ คุณอาจรู้สึกมาตลอดว่าตัวเองควรสร้างอะไรบางอย่างที่มีความหมายจริง แต่ในขณะเดียวกัน คุณก็แบกแรงกดดันของศักยภาพตัวเองไว้มากกว่าที่คนอื่นเห็น",
        "en": "You do not think only about small personal matters. Deep down, there is a much bigger vision living inside you. You may have always felt that you are meant to build something truly meaningful. At the same time, you carry more pressure around your own potential than others can see."
    },
    33: {
        "th": "คุณเป็นคนที่มีหัวใจของผู้เยียวยา และมักรู้สึกอยากช่วย อยากปลอบ หรืออยากทำอะไรบางอย่างที่มีประโยชน์ต่อชีวิตคนอื่น ลึก ๆ แล้วคุณไม่ได้อยากมีชีวิตที่ว่างเปล่า คุณอยากให้สิ่งที่คุณผ่านมามีความหมาย และเปลี่ยนเป็นบางอย่างที่ช่วยคนได้จริง",
        "en": "You carry the heart of a healer and often feel the urge to help, comfort, or offer something meaningful to others. Deep down, you do not want an empty life. You want what you have been through to mean something and to become something that can genuinely help people."
    }
}

BASE_SHADOW = {
    1: {"th": "เมื่อพลังตก คุณอาจกดดันตัวเองเกินไปและรู้สึกว่าต้องแข็งแรงตลอดเวลา", "en": "When your energy drops, you may pressure yourself too much and feel you must stay strong all the time."},
    2: {"th": "เมื่อพลังตก คุณอาจเก็บความรู้สึกตัวเองไว้และรับพลังคนอื่นมาหนักเกินไป", "en": "When your energy drops, you may hide your own feelings and carry too much of other people’s energy."},
    3: {"th": "เมื่อพลังตก คุณอาจใช้ความสดใสกลบความจริงในใจ หรือกลัวว่าถ้าพูดจริงแล้วคนจะไม่รับ", "en": "When your energy drops, you may use brightness to hide what is really happening inside or fear honesty will not be welcomed."},
    4: {"th": "เมื่อพลังตก คุณอาจแบกเยอะเกินไปและยึดกับวิธีเดิมจนชีวิตไม่ไหล", "en": "When your energy drops, you may over-carry and cling to old methods until life feels blocked."},
    5: {"th": "เมื่อพลังตก คุณอาจกระจัดกระจาย เบื่อง่าย หรือหนีความรู้สึกลึกด้วยการหาสิ่งใหม่ตลอดเวลา", "en": "When your energy drops, you may become scattered, restless, or use constant novelty to avoid deeper feelings."},
    6: {"th": "เมื่อพลังตก คุณอาจให้มากเกินไปและลืมดูแลหัวใจตัวเอง", "en": "When your energy drops, you may over-give and forget to care for your own heart."},
    7: {"th": "เมื่อพลังตก คุณอาจถอยห่าง เก็บตัว คิดวน และรู้สึกว่าไม่มีใครเข้าใจสิ่งที่อยู่ข้างใน", "en": "When your energy drops, you may withdraw, overthink, and feel that no one understands what is inside you."},
    8: {"th": "เมื่อพลังตก คุณอาจวัดคุณค่าจากความสำเร็จและกลัวการล้มเหลวจนไม่กล้าผ่อน", "en": "When your energy drops, you may measure your worth by success and fear failure so much that you cannot relax."},
    9: {"th": "เมื่อพลังตก คุณอาจแบกอดีต แบกคนอื่น หรือจมกับความผิดหวังที่ยังไม่ปิดวงจร", "en": "When your energy drops, you may carry the past, carry other people, or stay tangled in disappointments that never fully closed."},
    11: {"th": "เมื่อพลังตก คุณอาจสับสนในสิ่งที่ตัวเองรับรู้และแยกไม่ออกว่าอะไรเป็นพลังของตัวเองอะไรเป็นของคนอื่น", "en": "When your energy drops, you may doubt what you sense and struggle to tell your own energy from other people’s."},
    22: {"th": "เมื่อพลังตก คุณอาจรู้สึกหนักกับภาระและกลัวความรับผิดชอบในศักยภาพตัวเอง", "en": "When your energy drops, you may feel overwhelmed by responsibility and afraid of your own potential."},
    33: {"th": "เมื่อพลังตก คุณอาจแบกความทุกข์คนอื่นมากไปและลืมว่าผู้เยียวยาก็ต้องได้รับการเยียวยา", "en": "When your energy drops, you may carry too much of others’ pain and forget that healers need healing too."},
}

LOVE_TEXT = {
    1: {"th": "ในความรัก คุณต้องการคนที่เคารพตัวตน ไม่ใช่คนที่ทำให้คุณต้องเล็กลง", "en": "In love, you need someone who respects your identity rather than making you shrink."},
    2: {"th": "ในความรัก คุณต้องการความมั่นคงทางใจและคนที่เห็นความละเอียดอ่อนของคุณอย่างจริงใจ", "en": "In love, you need emotional safety and someone who truly sees your sensitivity."},
    3: {"th": "ในความรัก คุณต้องการการสื่อสารและความสดใส แต่ลึก ๆ ก็ต้องการคนที่ฟังโลกภายในของคุณด้วย", "en": "In love, you need communication and brightness, but deeply you also need someone who listens to your inner world."},
    4: {"th": "ในความรัก คุณต้องการความชัดเจน ความมั่นคง และความไว้ใจที่พิสูจน์ได้จริง", "en": "In love, you need clarity, stability, and trust that can be felt in action."},
    5: {"th": "ในความรัก คุณต้องการพื้นที่และความสดใหม่ แต่หัวใจก็ยังต้องการความจริงใจ ไม่ใช่แค่ความตื่นเต้น", "en": "In love, you need space and freshness, but your heart still needs sincerity rather than only excitement."},
    6: {"th": "ในความรัก คุณต้องการความอบอุ่นและความสัมพันธ์ที่ให้ความรู้สึกเหมือนบ้าน", "en": "In love, you need warmth and a bond that feels like home."},
    7: {"th": "ในความรัก คุณต้องการ connection ที่จริง ลึก และซื่อสัตย์ มากกว่าความหวือหวา", "en": "In love, you seek a connection that is real, deep, and honest more than dramatic."},
    8: {"th": "ในความรัก คุณต้องการคนที่เคารพพลังและความจริงจังของคุณ", "en": "In love, you need someone who respects your strength and seriousness."},
    9: {"th": "ในความรัก คุณต้องการความหมาย ความเข้าใจ และความสัมพันธ์ที่ไม่ตื้น", "en": "In love, you seek meaning, emotional understanding, and depth."},
    11: {"th": "ในความรัก คุณต้องการความเชื่อมโยงระดับวิญญาณและคนที่มั่นคงพอจะอยู่กับความลึกของคุณได้", "en": "In love, you seek soul-level connection and someone stable enough to meet your depth."},
    22: {"th": "ในความรัก คุณต้องการคนที่เดินเติบโตไปด้วยกันและไม่ดึงคุณออกจากภารกิจชีวิต", "en": "In love, you need someone who grows with you and does not pull you away from your mission."},
    33: {"th": "ในความรัก คุณต้องการความสัมพันธ์ที่อบอุ่น ลึก และช่วยให้ทั้งสองคนเติบโต", "en": "In love, you seek warmth, depth, and a relationship that helps both people grow."},
}

CAREER_TEXT = {
    1: {"th": "งานที่เหมาะกับคุณคือสิ่งที่ได้เริ่ม ได้ตัดสินใจ และได้สร้างบางอย่างด้วยวิธีของตัวเอง", "en": "Work suits you best when you can initiate, decide, and build in your own way."},
    2: {"th": "คุณเหมาะกับงานที่ใช้การประสานคน รับฟัง ดูแลความสัมพันธ์ และสร้างพื้นที่ปลอดภัย", "en": "You suit work that involves connection, listening, care, and creating safe spaces."},
    3: {"th": "คุณเหมาะกับงานสื่อสาร คอนเทนต์ การพูด การสอน หรือการสร้างแรงบันดาลใจ", "en": "You suit communication, content, speaking, teaching, and inspiration-led work."},
    4: {"th": "คุณเหมาะกับงานระบบ งานวางแผน งานจัดการ หรือธุรกิจที่ต้องสร้างฐานให้มั่นคง", "en": "You suit systems, planning, management, and businesses that require a strong foundation."},
    5: {"th": "คุณเหมาะกับงานที่ยืดหยุ่น การสื่อสาร การตลาด การเดินทาง หรือบทบาทที่มีความหลากหลาย", "en": "You suit flexible work, communication, marketing, travel, and varied roles."},
    6: {"th": "คุณเหมาะกับงานดูแล บริการ ให้คำแนะนำ สุขภาวะ หรือสิ่งที่ช่วยยกระดับชีวิตคนอื่น", "en": "You suit care work, service, guidance, wellbeing, and anything that improves people’s lives."},
    7: {"th": "คุณเหมาะกับงานที่ได้คิด วิเคราะห์ เขียน สอน วิจัย หรือถ่ายทอดสิ่งลึกให้คนเข้าใจง่ายขึ้น", "en": "You suit analysis, writing, teaching, research, or translating deep truths into something accessible."},
    8: {"th": "คุณเหมาะกับงานบริหาร ธุรกิจ การเงิน การสร้างแบรนด์ หรือบทบาทที่ต้องรับผิดชอบภาพใหญ่", "en": "You suit business, management, finance, branding, and big-picture responsibility."},
    9: {"th": "คุณเหมาะกับงานเยียวยา สอน ช่วยเหลือ สร้างแรงบันดาลใจ หรือสิ่งที่ส่งผลต่อผู้คนวงกว้าง", "en": "You suit healing, teaching, helping, inspiring, and work that impacts people more widely."},
    11: {"th": "คุณเหมาะกับงานที่ผสานจิตวิญญาณกับการสื่อสาร การสอน การเยียวยา หรือการสร้างแรงบันดาลใจ", "en": "You suit work that bridges spirituality with communication, teaching, healing, and inspiration."},
    22: {"th": "คุณเหมาะกับการสร้างธุรกิจ ระบบ แพลตฟอร์ม หรือสิ่งที่ส่งผลต่อผู้คนจำนวนมาก", "en": "You suit building businesses, systems, platforms, or anything that serves many people."},
    33: {"th": "คุณเหมาะกับงานสอน เยียวยา โค้ช สื่อสารจากหัวใจ หรือธุรกิจที่เปลี่ยนชีวิตคน", "en": "You suit teaching, healing, coaching, heart-led communication, and transformative work."},
}

MONEY_TEXT = {
    1: {"th": "การเงินของคุณดีขึ้นเมื่อคุณเชื่อในคุณค่าของตัวเองและกล้าตั้งราคากับสิ่งที่ทำ", "en": "Your financial flow improves when you believe in your value and dare to price what you create."},
    2: {"th": "การเงินของคุณดีขึ้นเมื่อคุณหยุดมองว่าความอ่อนโยนไม่มีมูลค่า", "en": "Your money improves when you stop assuming softness has no value."},
    3: {"th": "การเงินของคุณดีเมื่อคุณกล้าใช้เสียงของตัวเองและทำสิ่งที่มีเอกลักษณ์", "en": "Your finances improve when you use your voice and create through your uniqueness."},
    4: {"th": "การเงินของคุณขึ้นกับวินัย การจัดระบบ และการตัดสินใจระยะยาว", "en": "Your finances depend on discipline, structure, and long-term decision-making."},
    5: {"th": "การเงินของคุณดีขึ้นเมื่อคุณสร้างระบบรองรับอิสรภาพ ไม่ใช่ใช้ชีวิตตามอารมณ์อย่างเดียว", "en": "Your finances improve when you build systems to support freedom rather than living only by impulse."},
    6: {"th": "เงินของคุณมักมาเมื่อคุณให้คุณค่ากับสิ่งที่คุณมอบ ไม่ใช่ทำไปเพราะใจดีอย่างเดียว", "en": "Money tends to come when you value what you offer rather than giving endlessly just because you care."},
    7: {"th": "การเงินของคุณดีขึ้นเมื่อคุณหยุดแยกเรื่องจิตวิญญาณออกจากคุณค่าในโลกจริง", "en": "Your finances improve when you stop separating spirituality from real-world value."},
    8: {"th": "การเงินเป็นหนึ่งในสนามพลังสำคัญของคุณ ยิ่งคุณจัดระบบและยืนในคุณค่า เงินยิ่งตอบสนอง", "en": "Money is one of your major energetic arenas. The more you build structure and stand in your value, the more it responds."},
    9: {"th": "การเงินของคุณมั่นคงขึ้นเมื่อคุณเลิกคิดว่าจิตวิญญาณกับความอุดมสมบูรณ์ไปด้วยกันไม่ได้", "en": "Your finances steady when you stop believing spirituality and abundance cannot coexist."},
    11: {"th": "การเงินของคุณดีขึ้นเมื่อคุณหยุดลดทอนของขวัญตัวเอง", "en": "Your finances improve when you stop minimizing your gifts."},
    22: {"th": "การเงินของคุณมีศักยภาพสูงมากเมื่อคุณทำสิ่งที่ใหญ่พอจะรับพลังคุณได้", "en": "Your financial potential is high when you engage in work big enough to hold your energy."},
    33: {"th": "การเงินของคุณไม่ควรถูกตัดออกจากภารกิจ คุณสามารถได้รับอย่างงดงามจากสิ่งที่ช่วยผู้คน", "en": "Your finances do not need to be separated from your mission. You can receive beautifully through work that helps people."},
}

HEALING_TEXT = {
    1: {"th": "คุณไม่ได้เกิดมาเพื่อเดินตามทุกคน คุณเกิดมาเพื่อจำเสียงของตัวเองให้ได้อีกครั้ง", "en": "You were not born to follow every path around you. You were born to remember your own voice."},
    2: {"th": "ความอ่อนไหวของคุณไม่ใช่จุดอ่อน แต่มันคือภาษาละเอียดของจิตวิญญาณ", "en": "Your sensitivity is not a weakness. It is one of the subtle languages of the soul."},
    3: {"th": "เสียงของคุณไม่ได้มีไว้เพื่อทำให้คนพอใจอย่างเดียว แต่มันมีไว้เพื่อปลดล็อกบางอย่างในใจคนด้วย", "en": "Your voice is not only here to please people. It is here to unlock something in them too."},
    4: {"th": "คุณไม่ได้ช้า คุณกำลังสร้างสิ่งที่อยู่ได้นานกว่า", "en": "You are not slow. You are building something designed to last."},
    5: {"th": "อิสรภาพที่แท้จริง ไม่ใช่การหนีทุกอย่าง แต่มันคือการอยู่กับตัวเองได้โดยไม่ติดกรง", "en": "True freedom is not escaping everything. It is being able to stay with yourself without living in a cage."},
    6: {"th": "การรักคนอื่นไม่จำเป็นต้องแลกกับการทิ้งตัวเองไว้ข้างหลัง", "en": "Loving others does not require leaving yourself behind."},
    7: {"th": "ความลึกของคุณไม่ได้ทำให้คุณยากเกินจะรัก มันแค่หมายความว่าหัวใจคุณต้องการความจริงมากกว่าคนทั่วไป", "en": "Your depth does not make you too difficult to love. It simply means your heart requires more truth than most."},
    8: {"th": "ความสำเร็จที่แท้จริง ไม่ใช่การพิสูจน์ว่าคุณเก่งพอ แต่มันคือการสร้างชีวิตที่ไม่ต้องหักหลังหัวใจตัวเอง", "en": "True success is not proving you are enough. It is building a life that does not betray your own heart."},
    9: {"th": "สิ่งที่คุณต้องปล่อย ไม่ได้แปลว่าคุณรักน้อยลง แต่มันแปลว่าคุณเริ่มรักตัวเองด้วย", "en": "What you release does not mean you love less. It means you are finally including yourself in that love."},
    11: {"th": "คุณไม่ได้แปลกเกินไป คุณแค่รับแสงได้มากเกินกว่าที่โลกทั่วไปสอนให้เข้าใจ", "en": "You are not too strange. You simply receive more light than the ordinary world knows how to explain."},
    22: {"th": "อย่ากลัวศักยภาพของตัวเอง เพราะสิ่งที่ดูใหญ่ในใจคุณ อาจเป็นเหตุผลที่คุณมาเกิด", "en": "Do not fear your own potential. What feels huge inside you may be one of the reasons you came here."},
    33: {"th": "การเป็นแสงให้คนอื่น ไม่จำเป็นต้องแผดเผาตัวเองจนหมดแรง", "en": "Being a light for others does not require burning yourself out."},
}

WOUND_TEXT = {
    1: {"th": "บาดแผลลึกของคุณคือความรู้สึกว่าต้องพิสูจน์ตัวเองตลอดเวลา", "en": "Your deeper wound is the feeling that you must constantly prove yourself."},
    2: {"th": "บาดแผลของคุณคือความกลัวว่าถ้าพูดความจริงออกไป คนจะไม่พอใจหรือจากไป", "en": "Your wound is the fear that speaking your truth may upset people or make them leave."},
    3: {"th": "บาดแผลของคุณคือความกลัวว่าถ้าคนเห็นตัวจริงแล้ว เขาอาจไม่ชอบ", "en": "Your wound is the fear that if people see the real you, they may not like it."},
    4: {"th": "บาดแผลของคุณคือความรู้สึกว่าถ้าปล่อยมือ ทุกอย่างจะพัง", "en": "Your wound is the feeling that if you loosen your grip, everything will fall apart."},
    5: {"th": "บาดแผลของคุณคือความกลัวว่าถ้าหยุดนิ่งหรือถูกผูกมัด คุณจะเสียตัวเองไป", "en": "Your wound is the fear that if you stay still or become tied down, you will lose yourself."},
    6: {"th": "บาดแผลของคุณคือความรู้สึกว่าตัวเองจะมีค่าก็ต่อเมื่อกำลังดูแลหรือช่วยใครบางคน", "en": "Your wound is the feeling that you are valuable only when you are taking care of someone."},
    7: {"th": "บาดแผลของคุณคือความรู้สึกว่าไม่มีใครเข้าใจสิ่งลึก ๆ ในตัวคุณจริง", "en": "Your wound is the feeling that no one truly understands the deeper layers of you."},
    8: {"th": "บาดแผลของคุณคือการเชื่อว่าคุณจะปลอดภัยก็ต่อเมื่อทุกอย่างอยู่ภายใต้การควบคุม", "en": "Your wound is the belief that you are safe only when everything is under control."},
    9: {"th": "บาดแผลของคุณคือการติดอยู่กับสิ่งที่หมดเวลาแล้วเพราะยังรักหรือยังรู้สึกผูกพัน", "en": "Your wound is staying attached to what has already ended because love or emotional attachment still remains."},
    11: {"th": "บาดแผลของคุณคือความรู้สึกว่าโลกนี้อาจไม่เข้าใจความไวและความลึกของคุณ", "en": "Your wound is the feeling that this world may not understand your sensitivity and depth."},
    22: {"th": "บาดแผลของคุณคือความรู้สึกว่าภารกิจในใจมันใหญ่เกินไปสำหรับชีวิตจริง", "en": "Your wound is the feeling that the mission inside you is too large for ordinary life to hold."},
    33: {"th": "บาดแผลของคุณคือความรู้สึกว่าตัวเองต้องแบกรับหรือเยียวยาทุกอย่างให้คนอื่นถึงจะมีคุณค่า", "en": "Your wound is the feeling that you must carry or heal everything for others in order to have value."},
}

GIFT_TEXT = {
    1: {"th": "ของขวัญของคุณคือพลังในการเริ่มต้นสิ่งใหม่และพาคนอื่นกล้าขยับตาม", "en": "Your gift is the power to begin something new and help others move with courage."},
    2: {"th": "ของขวัญของคุณคือการรับรู้ใจคนอย่างลึกและทำให้บรรยากาศกลับมาสงบ", "en": "Your gift is feeling people deeply and restoring emotional harmony."},
    3: {"th": "ของขวัญของคุณคือการทำให้สิ่งยากกลายเป็นสิ่งที่คนรู้สึกและเข้าใจได้", "en": "Your gift is making difficult things feel understandable and alive."},
    4: {"th": "ของขวัญของคุณคือการเปลี่ยนความวุ่นวายให้กลายเป็นระบบที่พึ่งพาได้", "en": "Your gift is turning chaos into structure people can rely on."},
    5: {"th": "ของขวัญของคุณคือการพาคนอื่นเห็นความเป็นไปได้ใหม่และกล้าขยับออกจากสิ่งเดิม", "en": "Your gift is helping others see new possibilities and move beyond old patterns."},
    6: {"th": "ของขวัญของคุณคือการสร้างพื้นที่ที่คนรู้สึกอบอุ่น ปลอดภัย และกล้ากลับมาเป็นตัวเอง", "en": "Your gift is creating spaces where people feel warm, safe, and able to return to themselves."},
    7: {"th": "ของขวัญของคุณคือการมองทะลุสิ่งที่ซ่อนอยู่และตั้งคำถามกับสิ่งที่คนอื่นยอมรับแบบไม่คิด", "en": "Your gift is seeing through what is hidden and questioning what others accept without thought."},
    8: {"th": "ของขวัญของคุณคือพลังในการทำสิ่งใหญ่ให้เกิดขึ้นจริงและพาคนอื่นมองเห็นศักยภาพของตัวเอง", "en": "Your gift is the power to bring large visions into reality and help others recognize their own potential."},
    9: {"th": "ของขวัญของคุณคือหัวใจที่มองเห็นมนุษย์อย่างลึกและสามารถเปลี่ยนความเจ็บให้กลายเป็นความหมาย", "en": "Your gift is a heart that sees humanity deeply and can turn pain into meaning."},
    11: {"th": "ของขวัญของคุณคือการเห็นสัญญาณ เชื่อมสิ่งที่มองไม่เห็น และแปลมันออกมาให้ผู้คนเข้าใจได้", "en": "Your gift is perceiving signals, bridging the unseen, and translating it into something others can understand."},
    22: {"th": "ของขวัญของคุณคือการเห็นทั้งภาพใหญ่และภาพลงมือจริงในเวลาเดียวกัน", "en": "Your gift is seeing both the larger vision and the practical steps at the same time."},
    33: {"th": "ของขวัญของคุณคือการเปลี่ยนความเจ็บให้กลายเป็นปัญญาและส่งต่อแสงด้วยหัวใจจริง", "en": "Your gift is turning pain into wisdom and transmitting light through a sincere heart."},
}

LESSON_TEXT = {
    1: {"th": "บทเรียนของคุณคือการเป็นผู้นำโดยไม่ต้องเปลี่ยนทุกอย่างให้กลายเป็นการต่อสู้", "en": "Your lesson is learning to lead without turning everything into a battle."},
    2: {"th": "บทเรียนของคุณคือการอ่อนโยนกับคนอื่นโดยไม่ทอดทิ้งตัวเอง", "en": "Your lesson is to stay gentle with others without abandoning yourself."},
    3: {"th": "บทเรียนของคุณคือการใช้เสียงเพื่อเปิดเผย ไม่ใช่เพื่อปกปิด", "en": "Your lesson is using your voice to reveal rather than hide."},
    4: {"th": "บทเรียนของคุณคือการสร้างโดยไม่ต้องแข็งทื่อกับชีวิต", "en": "Your lesson is learning to build without becoming rigid."},
    5: {"th": "บทเรียนของคุณคือการมีอิสระโดยไม่ทำให้ชีวิตกระจัดกระจาย", "en": "Your lesson is learning to be free without scattering your life-force."},
    6: {"th": "บทเรียนของคุณคือการดูแลคนอื่นโดยไม่ละทิ้งตัวเอง", "en": "Your lesson is to care for others without abandoning yourself."},
    7: {"th": "บทเรียนของคุณคือการใช้ความลึกเพื่อเชื่อม ไม่ใช่ใช้เพื่อแยกตัวออกจากโลก", "en": "Your lesson is to use depth to connect rather than isolate yourself from the world."},
    8: {"th": "บทเรียนของคุณคือการเรียนรู้ว่าอำนาจที่แท้จริงไม่จำเป็นต้องมาพร้อมความแข็งตลอดเวลา", "en": "Your lesson is learning that true power does not require hardness at all times."},
    9: {"th": "บทเรียนของคุณคือการปล่อยวางโดยไม่ต้องหยุดรัก", "en": "Your lesson is learning to release without needing to stop loving."},
    11: {"th": "บทเรียนของคุณคือการทำให้สิ่งที่ลึกและละเอียดมีรากอยู่ในชีวิตจริง", "en": "Your lesson is grounding the subtle and profound into real life."},
    22: {"th": "บทเรียนของคุณคือการสร้างใหญ่โดยไม่แบกทุกอย่างคนเดียว", "en": "Your lesson is to build big without carrying everything alone."},
    33: {"th": "บทเรียนของคุณคือการรับใช้โดยไม่ใช้ชีวิตตัวเองเป็นเครื่องเผาไหม้", "en": "Your lesson is learning to serve without using your own life-force as fuel."},
}

NEXT_STEP_TEXT = {
    1: {"th": "เริ่มจากตัดสินใจเรื่องเล็ก ๆ ให้ชัด และหยุดรอให้ทุกอย่างพร้อมก่อน", "en": "Start by making small clear decisions and stop waiting for perfect readiness."},
    2: {"th": "เริ่มจากพูดความต้องการของตัวเองทีละนิด แม้จะยังกลัวอยู่", "en": "Start expressing your needs little by little, even if fear is still there."},
    3: {"th": "เริ่มสื่อสารสิ่งที่คุณรู้สึกจริง แม้ยังไม่สมบูรณ์", "en": "Start expressing what you truly feel, even before it feels perfect."},
    4: {"th": "เริ่มวางระบบที่ช่วยคุณ ไม่ใช่ระบบที่กดคุณ", "en": "Start building systems that support you, not systems that trap you."},
    5: {"th": "เริ่มเลือกอิสระที่มีโครง ไม่ใช่แค่เลือกสิ่งที่ตื่นเต้น", "en": "Start choosing freedom with structure, not only what feels exciting."},
    6: {"th": "เริ่มตั้งขอบเขตเล็ก ๆ กับสิ่งที่ทำให้คุณเหนื่อยซ้ำ", "en": "Start setting small boundaries around what repeatedly drains you."},
    7: {"th": "เริ่มจากปล่อยให้คนที่ใช่เข้าถึงคุณทีละชั้น และให้สิ่งที่คุณรู้ลึก ๆ ถูกแปลออกมาเป็นงานหรือคำที่ส่งต่อได้", "en": "Start by letting the right people reach you layer by layer, and let what you know deeply become shareable work or words."},
    8: {"th": "เริ่มจัดระบบความสำเร็จให้มีพื้นที่พัก พื้นที่รัก และพื้นที่เป็นมนุษย์", "en": "Start building success with room for rest, love, and humanity."},
    9: {"th": "เริ่มปิดวงจรที่ค้างทีละเรื่อง ไม่ว่าจะเป็นคน ความหวัง หรือเรื่องในใจที่ค้างมานาน", "en": "Begin closing unfinished cycles one by one—whether they are people, hopes, or old emotional stories."},
    11: {"th": "เริ่มเชื่อสิ่งที่คุณรับรู้มากขึ้น แต่ให้มันมีพื้นที่ลงมือจริงควบคู่ไปด้วย", "en": "Start trusting what you sense more, but give it real-world channels of expression."},
    22: {"th": "เริ่มแบ่งวิสัยทัศน์ใหญ่ออกเป็นก้าวที่ทำจริงได้ทีละส่วน", "en": "Start breaking the larger vision into practical steps that can really be built."},
    33: {"th": "เริ่มแยกให้ออกว่าอะไรคือการให้ด้วยหัวใจ และอะไรคือการให้เพราะกลัวจะไม่มีคุณค่า", "en": "Begin noticing the difference between giving from the heart and giving from fear of losing worth."},
}

WARNING_TEXT = {
    1: {"th": "ระวังการใช้ความสำเร็จเป็นตัววัดคุณค่าของหัวใจตัวเอง", "en": "Be careful not to use success as the only measure of your worth."},
    2: {"th": "ระวังการเป็นคนรองรับทุกอย่างจนไม่มีใครรู้เลยว่าคุณเจ็บตรงไหน", "en": "Be careful not to hold everything for everyone until no one knows where you hurt."},
    3: {"th": "ระวังการทำทุกอย่างให้ดูเบาจนหัวใจลึก ๆ ไม่เคยถูกได้ยิน", "en": "Be careful not to make everything look light until your deeper heart is never heard."},
    4: {"th": "ระวังการติดกับโครงสร้างเดิมจนพลาดโอกาสใหม่ที่เหมาะกว่า", "en": "Be careful not to cling so tightly to old structures that you miss better opportunities."},
    5: {"th": "ระวังการเปลี่ยนทุกอย่างเพียงเพราะรู้สึกอึดอัดชั่วคราว", "en": "Be careful not to change everything just because a temporary discomfort appears."},
    6: {"th": "ระวังการให้เกินกว่าที่อีกฝ่ายร้องขอแล้วคาดหวังว่าจะถูกเห็นคุณค่าเอง", "en": "Be careful not to over-give and silently expect your worth to be recognized."},
    7: {"th": "ระวังการใช้ความลึกเป็นข้ออ้างในการไม่เชื่อมต่อกับชีวิตจริง", "en": "Be careful not to use depth as an excuse to disconnect from real life."},
    8: {"th": "ระวังการทำทุกอย่างให้ใหญ่จนหัวใจไม่เหลือพื้นที่หายใจ", "en": "Be careful not to make everything so large that your heart no longer has room to breathe."},
    9: {"th": "ระวังการใช้เมตตาเป็นข้ออ้างในการอยู่ต่อในสิ่งที่ทำร้ายคุณ", "en": "Be careful not to use compassion as a reason to stay in what harms you."},
    11: {"th": "ระวังการเปิดรับทุกอย่างจนตัวเองพร่าและหมดแรง", "en": "Be careful not to open yourself to everything until your energy becomes blurred and depleted."},
    22: {"th": "ระวังการผลักตัวเองด้วยมาตรฐานที่หนักจนหมดแรงก่อนสิ่งใหญ่จะเป็นรูปเป็นร่าง", "en": "Be careful not to drive yourself so hard that you burn out before the vision takes shape."},
    33: {"th": "ระวังการช่วยคนจนหลุดจากแกนตัวเอง", "en": "Be careful not to help others so much that you lose your own center."},
}



def detect_question_signal(question_text: str):
    text = (question_text or "").lower().strip()
    scores = {"love": 0, "career": 0, "money": 0, "emotion": 0}
    for signal_key, lang_map in QUESTION_SIGNALS.items():
        for kw in lang_map["th"] + lang_map["en"]:
            if kw.lower() in text:
                scores[signal_key] += 1
    return max(scores, key=scores.get) if max(scores.values()) > 0 else None


def get_profile_text(life_number: int, section: str, lang: str):
    section_map = {
        "core": BASE_CORE,
        "shadow": BASE_SHADOW,
        "love": LOVE_TEXT,
        "career": CAREER_TEXT,
        "money": MONEY_TEXT,
        "healing": HEALING_TEXT,
        "wound": WOUND_TEXT,
        "gift": GIFT_TEXT,
        "lesson": LESSON_TEXT,
        "next_step": NEXT_STEP_TEXT,
        "warning": WARNING_TEXT,
    }
    library = section_map[section]
    return safe_get(library, life_number, library[7])[lang]


def life_intro(life_number: int, birth_energy: int, month_num: int, lang: str):
    core_text = get_profile_text(life_number, "core", lang)
    birth_text = safe_get(BIRTH_DAY_LIBRARY, birth_energy, BIRTH_DAY_LIBRARY[7])[lang]
    month_text = safe_get(month_energy_meanings, month_num, month_energy_meanings[7])[lang]
    if lang == "th":
        return f"{core_text} {birth_text} และพลังเดือนเกิดของคุณยังสะท้อนถึง{month_text} จึงทำให้เส้นทางชีวิตของคุณมีทั้งความลึก ความหมาย และบทเรียนที่เชื่อมกับการเติบโตภายใน"
    return f"{core_text} {birth_text} Your birth month also reflects {month_text}, which adds inner depth, meaning, and soul-level growth to your life path."


def category_reflection(category_key: str, life_number: int, lang: str):
    if category_key == "love":
        return get_profile_text(life_number, "love", lang)
    if category_key == "career":
        return get_profile_text(life_number, "career", lang)
    return get_profile_text(life_number, "money", lang)


def current_focus_block(category_key: str, question_signal: str, life_number: int, lang: str):
    if lang == "th":
        base_map = {
            "love": "ช่วงนี้หัวใจของคุณกำลังสอนให้แยกความรักออกจากความกลัวที่จะสูญเสีย",
            "career": "ช่วงนี้ชีวิตกำลังกดให้คุณมองเส้นทางงานใหม่อย่างจริงจังมากขึ้น",
            "money": "ช่วงนี้กระแสการเงินกำลังชี้ให้คุณเห็นความสัมพันธ์ระหว่างคุณค่าตัวเองกับการรับความอุดมสมบูรณ์"
        }
        signal_map = {
            "emotion": "และจากสิ่งที่คุณพิมพ์เข้ามา เห็นได้ว่าข้างในคุณกำลังอยู่ในจุดที่ต้องการความชัดเจน ความเบาใจ และการกลับมายืนอยู่กับตัวเองอีกครั้ง",
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
            "emotion": "From what you wrote, there is also a clear need for inner clarity, emotional relief, and a return to your own center.",
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

    title = (
        f"🔮 ผลสะท้อนพลังงานเบื้องต้น: คุณ {name}"
        if lang == "th" else
        f"🔮 Your Initial Energy Reflection: {name}"
    )

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

    if lang == "th":
        premium_title = f"✨ พิมพ์เขียวพลังงานเชิงลึกของคุณ {name}"
        soul_text = (
            f"{name} คุณไม่ได้มาถึงจุดนี้โดยบังเอิญ "
            f"เลขเส้นทางชีวิต {life_num} ของคุณสะท้อนว่าชีวิตกำลังสอนให้คุณกลับมาใช้พลังแท้ของตัวเองอย่างมีสติ "
            f"ขณะเดียวกันเลขวันเกิด {birth_energy} ก็เติมโทนเฉพาะตัวให้คุณมีวิธีแสดงพลังชีวิตออกมาในแบบของตัวเอง "
            f"นี่คือช่วงที่ชีวิตไม่ได้ต้องการให้คุณเก่งขึ้นอย่างเดียว แต่ต้องการให้คุณจริงกับตัวเองมากขึ้นด้วย"
        )
        unlock_note = "หากข้อความนี้สะท้อนชีวิตคุณจริง คุณสามารถใช้ผลลัพธ์นี้เป็นสะพานต่อไปยัง eBook หรือการอ่านส่วนตัวเชิงลึกได้"
    else:
        premium_title = f"✨ Your Deep Energy Blueprint: {name}"
        soul_text = (
            f"{name}, you did not arrive at this point by accident. "
            f"Your Life Path {life_num} suggests that life is asking you to return to your real power with greater awareness. "
            f"Your Birth Day Energy {birth_energy} adds its own signature to how that power wants to be expressed. "
            f"This is not only a season of becoming stronger—it is a season of becoming more honest with yourself."
        )
        unlock_note = "If this resonates deeply, you can use this result as a bridge into your eBook or a deeper personal reading."

    return {
        "premium_title": premium_title,
        "shadow": get_profile_text(life_num, "shadow", lang),
        "soul_text": soul_text,
        "wound": get_profile_text(life_num, "wound", lang),
        "gift": get_profile_text(life_num, "gift", lang),
        "lesson": get_profile_text(life_num, "lesson", lang),
        "next_step": get_profile_text(life_num, "next_step", lang),
        "warning": get_profile_text(life_num, "warning", lang),
        "healing": get_profile_text(life_num, "healing", lang),
        "unlock_note": unlock_note
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
        {tr("พื้นที่สะท้อนชีวิต | ถอดรหัสลับพลังงานวันเกิด",
             "A space for reflection | Decode your birth energy")}
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
    st.markdown(
        f"""
        <div class="stat-card">
            <div style="font-size:1.15rem; font-weight:700; color:#8e24aa;">{tr("⭐️เข้าใจตัวเอง", "Know Yourself")}</div>
            <div class="soft-note">{tr("เห็นจุดแข็ง จุดเปลี่ยน และบทเรียนที่กำลังเกิดขึ้น", "See your strengths, turning points, and the lessons unfolding in your life")}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
with c2:
    st.markdown(
        f"""
        <div class="stat-card">
            <div style="font-size:1.15rem; font-weight:700; color:#8e24aa;">{tr("⭐️สะท้อนชีวิต", "Reflect on Life")}</div>
            <div class="soft-note">{tr("ช่วยมองความรัก งาน และการเงินในมุมที่ลึกขึ้น", "Gain deeper insight into love, career, and financial flow")}</div>
        </div>
        """,
        unsafe_allow_html=True
    )
with c3:
    st.markdown(
        f"""
        <div class="stat-card">
            <div style="font-size:1.15rem; font-weight:700; color:#8e24aa;">{tr("⭐️ต่อยอดได้จริง", "Take It Further")}</div>
            <div class="soft-note">{tr("หากรู้สึกว่าตรง คุณสามารถปลดล็อคคำอ่านฉบับเต็มได้ทันที", "If it resonates, you can unlock the full reading immediately")}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

st.markdown(tr("### ☪️ รีวิวความรู้สึกจากผู้ที่เคยสะท้อนพลังงาน💫", "### ☪️ Reflections from people who resonated with their reading 💫"))

r1, r2 = st.columns(2)
with r1:
    st.markdown(
        f"""
        <div class="review-card">
            <div style="font-weight:700; color:#7b1fa2;">{tr("“อ่านแล้วเหมือนมีใครอธิบายชีวิตเราได้”", '"It felt like someone could finally explain my life."')}</div>
            <div class="soft-note">{tr("หลายอย่างตรงแบบรู้สึกได้ว่าไม่ใช่แค่คำทั่วไป", "So many parts felt deeply accurate—not like generic words at all")}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with r2:
    st.markdown(
        f"""
        <div class="review-card">
            <div style="font-weight:700; color:#7b1fa2;">{tr("“ช่วยให้เข้าใจช่วงชีวิตที่กำลังเปลี่ยน”", '"It helped me understand the phase of life I am moving through."')}</div>
            <div class="soft-note">{tr("ยิ่งอ่านยิ่งเห็นภาพว่าบางอย่างที่เกิดขึ้นมีเหตุผลของมัน", "The more I read, the more I could see that what was happening had meaning")}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------
# Form
# -----------------------------
month_display_list = [m["th"] if st.session_state.lang == "th" else m["en"] for m in month_options]
category_display_list = [c["th"] if st.session_state.lang == "th" else c["en"] for c in categories]

with st.form("lumina_form_v2"):
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
            "premium_soul_text": premium_result["soul_text"],
            "premium_wound": premium_result["wound"],
            "premium_gift": premium_result["gift"],
            "premium_lesson": premium_result["lesson"],
            "premium_next_step": premium_result["next_step"],
            "premium_warning": premium_result["warning"],
            "language": st.session_state.lang,
            "source": "website_form_v2",
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

    st.markdown(
        f"""
        <div class="result-card">
            <h4 style="color:#7b1fa2; margin-top:0;">{tr("🔢 เลขพลังงานของคุณ", "🔢 Your Energy Numbers")}</h4>
            <p><b>{tr("เลขเส้นทางชีวิต:", "Life Path Number:")}</b> {free_result["life_number"]}</p>
            <p><b>{tr("เลขพลังงานวันเกิด:", "Birth Day Energy:")}</b> {free_result["birth_energy"]}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="mini-card">
            <h4 style="color:#8e24aa; margin-top:0;">{tr("🌙 พลังแกนกลางของคุณ", "🌙 Your Core Energy")}</h4>
            <p>{free_result["intro"]}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="result-card">
            <h4 style="color:#ad1457; margin-top:0;">{tr("🔮 คำสะท้อนในด้านที่คุณเลือก", "🔮 Reflection for your chosen area")}</h4>
            <p>{free_result["category_text"]}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="mini-card">
            <h4 style="color:#8e24aa; margin-top:0;">{tr("🪄 สิ่งที่ชีวิตกำลังบอกคุณตอนนี้", "🪄 What life may be showing you right now")}</h4>
            <p>{free_result["focus_text"]}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if not st.session_state.premium_unlocked:
        st.markdown(
            f"""
            <div class="lock-card">
                <h4 style="color:#8e24aa; margin-top:0;">🔒 {tr("คำอ่านฉบับลึกยังไม่ถูกเปิด", "Your deeper reading is still locked")}</h4>
                <p>
                {tr(
                    "สิ่งที่คุณเพิ่งอ่าน…เป็นเพียงชั้นแรกของพลังงานชีวิตคุณ ลึกลงไปกว่านั้น ยังมีความจริงบางอย่างที่รอการถูกเปิดเผย",
                    "What you have just read is only the first layer of your life energy. Deeper than this, there is a truth still waiting to be revealed."
                )}
                </p>
                <p>
                {tr(
                    "หากคุณได้รับ Soul Code จาก eBook หรือ LINE แล้ว สามารถใส่รหัสด้านล่างเพื่อปลดล็อคคำอ่านฉบับเต็มได้ทันที",
                    "If you have already received a Soul Code from your eBook or LINE, enter it below to unlock your full reading."
                )}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )

        code_input = st.text_input(tr("✨ ใส่ Soul Code ของคุณ", "✨ Enter your Soul Code"))

        if st.button(tr("🔓 ปลดล็อคคำอ่านฉบับเต็ม", "🔓 Unlock Full Reading")):
            if verify_code(code_input):
                st.session_state.premium_unlocked = True
                st.session_state.used_code = code_input.strip().upper()
                st.rerun()
            else:
                st.error(
                    tr(
                        "รหัสไม่ถูกต้อง หรือยังไม่ได้เปิดสิทธิ์ กรุณาตรวจสอบอีกครั้ง หรือทัก LINE เพื่อรับรหัส",
                        "The code is invalid or has not been activated yet. Please check again or contact LINE to receive your code."
                    )
                )

        st.markdown(
            f"""
            <div class="premium-btn">
                <a href="{LINE_LINK}" target="_blank">
                    ✳️👉 {tr("รับ Soul Code ผ่าน LINE", "Get your Soul Code via LINE")}
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="cta-note">
            {tr("LINE ID ของเรา:", "Our LINE ID:")} <b>{LINE_ID}</b>
            </div>
            """,
            unsafe_allow_html=True
        )

    if st.session_state.premium_unlocked:
        st.markdown(
            f"""
            <div class="result-card">
                <h4 style="color:#7b1fa2; margin-top:0;">{premium_result["premium_title"]}</h4>
                <p>{premium_result["soul_text"]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="mini-card">
                <h4 style="color:#8e24aa; margin-top:0;">{tr("🌑 เงาพลังงานและบทเรียนลึก", "🌑 Shadow Pattern & Deeper Lesson")}</h4>
                <p>{premium_result["shadow"]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="mini-card">
                <h4 style="color:#8e24aa; margin-top:0;">{tr("🩹 บาดแผลที่ชีวิตกำลังชี้ให้เห็น", "🩹 The Wound Life May Be Revealing")}</h4>
                <p>{premium_result["wound"]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="mini-card">
                <h4 style="color:#8e24aa; margin-top:0;">{tr("💎 ของขวัญที่ซ่อนอยู่ในตัวคุณ", "💎 The Gift Hidden Within You")}</h4>
                <p>{premium_result["gift"]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="mini-card">
                <h4 style="color:#8e24aa; margin-top:0;">{tr("📖 บทเรียนที่ชีวิตกำลังสอน", "📖 The Lesson Life Is Teaching You")}</h4>
                <p>{premium_result["lesson"]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="mini-card">
                <h4 style="color:#8e24aa; margin-top:0;">{tr("🪄 แนวทางที่ควรโฟกัสต่อ", "🪄 Your Next Focus")}</h4>
                <p>{premium_result["next_step"]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="mini-card">
                <h4 style="color:#8e24aa; margin-top:0;">{tr("⚠️ สิ่งที่ควรระวัง", "⚠️ What to Be Careful With")}</h4>
                <p>{premium_result["warning"]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="mini-card">
                <h4 style="color:#6a1b9a; margin-top:0;">{tr("✨ ข้อความจาก Lumina Soul", "✨ A Message from Lumina Soul")}</h4>
                <p>{premium_result["healing"]}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.info("💡 " + premium_result["unlock_note"])

        st.markdown(
            f"""
            <div class="cta-note">
            {tr(
                "หากคำอ่านนี้สะท้อนชีวิตคุณจริง ขั้นต่อไปคือ eBook หรือการอ่านเชิงลึกส่วนตัว เพื่อเชื่อมสิ่งที่คุณรู้สึกเข้ากับเส้นทางชีวิตจริง",
                "If this reading deeply resonates, your next step is the eBook or a personalized deep reading to connect what you feel with your real life path."
            )}
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="premium-btn">
                <a href="{LINE_LINK}" target="_blank">
                    ✳️👉 {tr("คุยกับที่ปรึกษา LUMINA SOUL", "Talk to a LUMINA SOUL guide")}
                </a>
            </div>
            """,
            unsafe_allow_html=True
        )

# -----------------------------
# Footer
# -----------------------------
st.write("---")
st.markdown(
    f"<p style='text-align: center; font-size: 0.82rem; color: #888;'>© 2026 LUMINA SOUL | {tr('พื้นที่สะท้อนชีวิตและการตื่นรู้', 'A space for reflection and awakening')}</p>",
    unsafe_allow_html=True
)
