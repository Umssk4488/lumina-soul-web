from textwrap import dedent

code = dedent(r'''
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
# Content library
# -----------------------------
PROFILE_LIBRARY = {
    1: {
        "core": {
            "th": [
                "คุณมีพลังของผู้เริ่มต้นและผู้เปิดทาง ชีวิตของคุณมักไม่สบายใจเมื่อถูกบังคับให้อยู่ในกรอบที่ไม่ใช่ตัวเอง",
                "หัวใจของคุณต้องการอิสระในการตัดสินใจ และต้องการรู้สึกว่าชีวิตกำลังเดินไปในทิศทางที่ตัวเองเลือก"
            ],
            "en": [
                "You carry the energy of an initiator and path opener. Your soul does not feel at ease when it is trapped in a life that does not reflect who you are.",
                "At your core, you need freedom in decision-making and a sense that your life is moving in a direction you truly chose."
            ]
        },
        "shadow": {
            "th": [
                "เมื่อพลังคุณตก คุณอาจกลายเป็นคนกดดันตัวเองเกินไป รีบเกินไป หรือรู้สึกว่าต้องแข็งแรงตลอดเวลา",
                "บทเรียนสำคัญคือการนำพาชีวิตโดยไม่ต้องต่อสู้กับทุกอย่างตลอดเวลา"
            ],
            "en": [
                "When your energy is low, you may pressure yourself too much, rush life, or feel you must always stay strong.",
                "A key lesson is learning to lead without turning everything into a battle."
            ]
        },
        "love": {
            "th": [
                "ในความรัก คุณต้องการความสัมพันธ์ที่เคารพตัวตน ไม่ใช่ความสัมพันธ์ที่ทำให้คุณต้องหายไปเพื่อเอาใจอีกฝ่าย",
                "คุณรักได้จริง แต่หัวใจคุณจะปิดทันทีเมื่อรู้สึกว่าถูกควบคุม"
            ],
            "en": [
                "In love, you need a relationship that respects your identity rather than one that asks you to disappear to please the other person.",
                "You can love deeply, but your heart closes quickly when it feels controlled."
            ]
        },
        "career": {
            "th": [
                "งานที่เหมาะกับคุณคือสิ่งที่ได้เริ่ม ได้ตัดสินใจ และได้สร้างบางอย่างด้วยวิธีของตัวเอง",
                "คุณมักเติบโตเมื่อกล้ารับบทนำ ไม่ใช่เมื่อซ่อนความสามารถไว้ข้างหลัง"
            ],
            "en": [
                "Work suits you best when you can initiate, decide, and build in your own way.",
                "You thrive when you are willing to step into leadership instead of hiding your capability."
            ]
        },
        "money": {
            "th": [
                "การเงินของคุณดีขึ้นเมื่อคุณเชื่อในคุณค่าของตัวเองและกล้าตั้งราคากับสิ่งที่ทำ",
                "เมื่อคุณลังเลในคุณค่า เงินมักสะท้อนความลังเลนั้นกลับมา"
            ],
            "en": [
                "Your financial flow improves when you believe in your own value and dare to price what you create.",
                "When you doubt your worth, money tends to mirror that hesitation."
            ]
        },
        "healing": {
            "th": ["คุณไม่ได้เกิดมาเพื่อเดินตามทุกคน คุณเกิดมาเพื่อจำเสียงของตัวเองให้ได้อีกครั้ง"],
            "en": ["You were not born to follow every path around you. You were born to remember your own voice."]
        }
    },
    2: {
        "core": {
            "th": [
                "คุณมีพลังของผู้ประสานใจ รับรู้อารมณ์ละเอียด และมักเข้าใจสิ่งที่คนอื่นไม่ได้พูดออกมาตรง ๆ",
                "หัวใจของคุณเติบโตเมื่ออยู่ในพื้นที่ที่อ่อนโยน จริงใจ และปลอดภัยพอให้เป็นตัวเอง"
            ],
            "en": [
                "You carry the energy of a harmonizer. You sense subtle emotions and often understand what others do not say directly.",
                "Your heart grows in spaces that feel gentle, sincere, and safe enough for your true self."
            ]
        },
        "shadow": {
            "th": [
                "เมื่อพลังตก คุณอาจกลัวความขัดแย้งจนเก็บความรู้สึกตัวเองไว้ หรือรับพลังคนอื่นมาหนักเกินไป",
                "บทเรียนของคุณคือการอ่อนโยนกับคนอื่นโดยไม่ทอดทิ้งหัวใจตัวเอง"
            ],
            "en": [
                "When your energy is low, you may avoid conflict so much that you suppress your own feelings or carry too much of other people’s energy.",
                "Your lesson is to remain gentle with others without abandoning your own heart."
            ]
        },
        "love": {
            "th": [
                "ความรักของคุณต้องการความมั่นคงทางใจและการสื่อสารที่นุ่มนวล",
                "คุณไม่ได้ต้องการแค่คนรัก แต่ต้องการคนที่เห็นความละเอียดอ่อนของคุณอย่างจริงใจ"
            ],
            "en": [
                "Your love life needs emotional safety and soft, honest communication.",
                "You are not just seeking a partner—you are seeking someone who truly sees your sensitivity."
            ]
        },
        "career": {
            "th": [
                "คุณเหมาะกับงานที่ใช้การประสานคน ดูแลความสัมพันธ์ รับฟัง หรือสร้างบรรยากาศที่ทำให้คนสบายใจ",
                "พรสวรรค์ของคุณคือการเชื่อมโยงมากกว่าการแข่งขัน"
            ],
            "en": [
                "You do well in work that involves connection, care, listening, or creating an environment where people feel safe.",
                "Your gift lies more in connecting than competing."
            ]
        },
        "money": {
            "th": [
                "การเงินของคุณดีขึ้นเมื่อคุณหยุดมองว่าความอ่อนโยนไม่มีมูลค่า",
                "คุณสามารถสร้างเงินได้จากการช่วยให้คนรู้สึกดีขึ้นหรือเข้าใจตัวเองมากขึ้น"
            ],
            "en": [
                "Your money grows when you stop assuming that softness has no value.",
                "You can create income through helping people feel better or understand themselves more deeply."
            ]
        },
        "healing": {
            "th": ["ความอ่อนไหวของคุณไม่ใช่จุดอ่อน แต่มันคือภาษาละเอียดของจิตวิญญาณ"],
            "en": ["Your sensitivity is not a weakness. It is one of the subtle languages of the soul."]
        }
    },
    3: {
        "core": {
            "th": [
                "คุณมีพลังของการสื่อสาร ความคิดสร้างสรรค์ และการทำให้พลังภายในถูกถ่ายทอดออกมาเป็นคำพูดหรือผลงาน",
                "ชีวิตของคุณมักเปิดทางเมื่อคุณยอมให้ตัวเองถูกมองเห็น"
            ],
            "en": [
                "You carry the energy of expression, creativity, and turning inner energy into words, art, or communication.",
                "Life opens for you when you allow yourself to be seen."
            ]
        },
        "shadow": {
            "th": [
                "เมื่อพลังตก คุณอาจใช้ความสดใสกลบความจริงในใจ หรือกลัวว่าถ้าพูดจริงแล้วคนจะไม่รับ",
                "บทเรียนคือการสื่อสารจากแก่นแท้ ไม่ใช่จากการพยายามทำให้ทุกคนพอใจ"
            ],
            "en": [
                "When your energy drops, you may use brightness to cover what is really happening inside or fear that honesty will not be accepted.",
                "Your lesson is to express from truth rather than from the need to please everyone."
            ]
        },
        "love": {
            "th": [
                "ในความรัก คุณต้องการความสนุก การสื่อสาร และการเชื่อมโยงที่มีชีวิตชีวา",
                "แต่ลึก ๆ แล้วคุณต้องการคนที่รับฟังโลกภายในของคุณด้วย ไม่ใช่เห็นแค่ภาพภายนอก"
            ],
            "en": [
                "In love, you need playfulness, communication, and a lively sense of connection.",
                "But underneath that, you also need someone who listens to your inner world, not just your outer sparkle."
            ]
        },
        "career": {
            "th": [
                "คุณเหมาะกับงานสื่อสาร คอนเทนต์ การพูด การสอน การขายเชิงความรู้ หรือการสร้างแรงบันดาลใจ",
                "พรสวรรค์ของคุณคือการทำให้สิ่งที่จับต้องยากกลายเป็นสิ่งที่คนรู้สึกได้"
            ],
            "en": [
                "You suit communication, content, speaking, teaching, value-based selling, and inspiration-led work.",
                "Your gift is making intangible things feel real and emotionally accessible."
            ]
        },
        "money": {
            "th": [
                "การเงินของคุณดีเมื่อคุณกล้าใช้เสียงของตัวเองและทำสิ่งที่มีเอกลักษณ์",
                "รายได้มักเชื่อมกับความสามารถในการดึงดูดคนผ่านเสน่ห์และการสื่อสาร"
            ],
            "en": [
                "Your financial flow improves when you dare to use your voice and create through your own uniqueness.",
                "Income often connects to your ability to attract people through communication and personal magnetism."
            ]
        },
        "healing": {
            "th": ["เสียงของคุณไม่ได้มีไว้เพื่อทำให้คนพอใจอย่างเดียว แต่มันมีไว้เพื่อปลดล็อกบางอย่างในใจคนด้วย"],
            "en": ["Your voice is not only here to please people. It is here to unlock something in them too."]
        }
    },
    4: {
        "core": {
            "th": [
                "คุณมีพลังของผู้สร้างรากฐาน ชีวิตของคุณเด่นเรื่องความรับผิดชอบ ความจริงจัง และการทำสิ่งเล็กให้กลายเป็นความมั่นคง",
                "คุณรู้สึกปลอดภัยเมื่อทุกอย่างมีโครงสร้างที่ชัดเจน"
            ],
            "en": [
                "You carry builder energy. Your life highlights responsibility, seriousness, and the ability to turn small actions into real stability.",
                "You feel safest when life has clear structure."
            ]
        },
        "shadow": {
            "th": [
                "เมื่อพลังตก คุณอาจแบกเยอะเกินไป กดดันตัวเอง และยึดกับวิธีเดิมจนชีวิตไม่ไหล",
                "บทเรียนสำคัญคือการสร้างโดยไม่แข็งทื่อ"
            ],
            "en": [
                "When your energy is low, you may over-carry, over-pressure yourself, and cling to old methods until life feels blocked.",
                "Your key lesson is to build without becoming rigid."
            ]
        },
        "love": {
            "th": [
                "ในความรัก คุณต้องการความชัดเจน ความมั่นคง และความไว้ใจที่พิสูจน์ได้จริง",
                "คุณเปิดใจช้า แต่ถ้าเชื่อใจแล้วจะจริงจังมาก"
            ],
            "en": [
                "In love, you need clarity, stability, and trust that can be felt in action.",
                "You open slowly, but once you trust, you become deeply committed."
            ]
        },
        "career": {
            "th": [
                "คุณเหมาะกับงานระบบ งานวางแผน งานจัดการ หรือธุรกิจที่ต้องสร้างฐานให้มั่นคง",
                "ความสำเร็จของคุณมักมาแบบค่อยเป็นค่อยไปแต่ยั่งยืน"
            ],
            "en": [
                "You suit systems, planning, management, and businesses that require a strong foundation.",
                "Your success often builds slowly but lasts."
            ]
        },
        "money": {
            "th": [
                "การเงินของคุณขึ้นกับวินัย การจัดระบบ และการตัดสินใจระยะยาว",
                "คุณมีศักยภาพสร้างความมั่นคงสูง ถ้าไม่กลัวการเติบโตที่ค่อยเป็นค่อยไป"
            ],
            "en": [
                "Your finances depend on discipline, systems, and long-term decision-making.",
                "You have strong potential for lasting stability if you stop underestimating slow growth."
            ]
        },
        "healing": {
            "th": ["คุณไม่ได้ช้า คุณกำลังสร้างสิ่งที่อยู่ได้นานกว่า"],
            "en": ["You are not slow. You are building something designed to last."]
        }
    },
    5: {
        "core": {
            "th": [
                "คุณมีพลังของการเปลี่ยนแปลง อิสรภาพ และการเรียนรู้จากประสบการณ์ตรง",
                "ชีวิตของคุณมักเติบโตเมื่อได้ขยับ เดินทาง ทดลอง และปล่อยให้ตัวเองมีพื้นที่"
            ],
            "en": [
                "You carry the energy of change, freedom, and learning through direct experience.",
                "Your life expands through movement, exploration, experimentation, and spaciousness."
            ]
        },
        "shadow": {
            "th": [
                "เมื่อพลังตก คุณอาจรู้สึกเบื่อง่าย กระจัดกระจาย หรือหนีความรู้สึกลึกด้วยการหาสิ่งใหม่ตลอดเวลา",
                "บทเรียนคือการรักษาอิสรภาพโดยไม่หนีจากตัวเอง"
            ],
            "en": [
                "When your energy is low, you may become restless, scattered, or avoid deeper emotions by constantly chasing something new.",
                "Your lesson is to stay free without running from yourself."
            ]
        },
        "love": {
            "th": [
                "ในความรัก คุณต้องการพื้นที่ ความสดใหม่ และคนที่ไม่ทำให้คุณรู้สึกติดกับ",
                "แต่หัวใจคุณก็ยังต้องการความจริงใจ ไม่ใช่แค่ความตื่นเต้นชั่วคราว"
            ],
            "en": [
                "In love, you need space, freshness, and a partner who does not make you feel trapped.",
                "Yet your heart still needs sincerity, not just temporary excitement."
            ]
        },
        "career": {
            "th": [
                "คุณเหมาะกับงานที่มีความยืดหยุ่น การสื่อสาร การตลาด การเดินทาง หรือสิ่งที่ได้ลองหลายบทบาท",
                "คุณเติบโตเมื่อมีพื้นที่ให้พลังชีวิตได้ไหล"
            ],
            "en": [
                "You suit flexible work, communication, marketing, travel, and roles that allow variety.",
                "You thrive when your life-force is allowed to move."
            ]
        },
        "money": {
            "th": [
                "การเงินของคุณมักขึ้นลงตามจังหวะชีวิต แต่ถ้าคุณสร้างระบบรองรับอิสรภาพได้ เงินจะไหลดีมาก",
                "คุณมีพลังดึงดูดโอกาส แต่ต้องระวังการใช้จ่ายตามอารมณ์"
            ],
            "en": [
                "Your finances may fluctuate with your life rhythm, but when you build systems that support your freedom, money can flow well.",
                "You attract opportunities, but emotional spending needs care."
            ]
        },
        "healing": {
            "th": ["อิสรภาพที่แท้จริง ไม่ใช่การหนีทุกอย่าง แต่มันคือการอยู่กับตัวเองได้โดยไม่ติดกรง"],
            "en": ["True freedom is not escaping everything. It is being able to stay with yourself without living in a cage."]
        }
    },
    6: {
        "core": {
            "th": [
                "คุณมีพลังของผู้ดูแล ผู้เยียวยา และผู้สร้างพื้นที่ปลอดภัยให้คนอื่น",
                "หัวใจของคุณมีความรัก ความรับผิดชอบ และความต้องการทำสิ่งที่มีคุณค่าต่อผู้คน"
            ],
            "en": [
                "You carry the energy of the nurturer, healer, and one who creates emotional safety for others.",
                "Your heart is rooted in love, responsibility, and doing something meaningful for people."
            ]
        },
        "shadow": {
            "th": [
                "เมื่อพลังตก คุณอาจให้มากเกินไป แบกคนอื่นเกินจำเป็น หรือรู้สึกผิดง่ายเมื่อไม่ได้ช่วยทุกคน",
                "บทเรียนคือการดูแลคนอื่นโดยไม่ละทิ้งตัวเอง"
            ],
            "en": [
                "When your energy drops, you may over-give, over-carry, or feel guilty when you cannot save everyone.",
                "Your lesson is to care for others without abandoning yourself."
            ]
        },
        "love": {
            "th": [
                "ในความรัก คุณต้องการความอบอุ่น ความมั่นคง และความสัมพันธ์ที่ให้ความรู้สึกเหมือนบ้าน",
                "คุณรักลึกและทุ่มเท แต่ต้องระวังการเป็นคนเยียวยาแทนที่จะเป็นคนรัก"
            ],
            "en": [
                "In love, you need warmth, stability, and a bond that feels like home.",
                "You love deeply and generously, but be careful not to become the healer instead of the partner."
            ]
        },
        "career": {
            "th": [
                "คุณเหมาะกับงานดูแล บริการ ให้คำแนะนำ ความงาม สุขภาวะ หรือสิ่งที่ช่วยยกระดับชีวิตคนอื่น",
                "พรสวรรค์ของคุณคือการทำให้คนรู้สึกว่าตัวเองมีค่า"
            ],
            "en": [
                "You suit care work, service, guidance, beauty, wellbeing, and anything that helps people feel better or live better.",
                "Your gift is helping people feel valued."
            ]
        },
        "money": {
            "th": [
                "เงินของคุณมักมาเมื่อคุณให้คุณค่ากับสิ่งที่คุณมอบ ไม่ใช่แค่ทำไปเพราะใจดี",
                "คุณต้องเรียนรู้ว่าความสามารถในการดูแลและเยียวยาก็มีมูลค่าทางการเงิน"
            ],
            "en": [
                "Money tends to come when you value what you offer instead of giving endlessly just because you care.",
                "Your care and healing ability also hold financial value."
            ]
        },
        "healing": {
            "th": ["การรักคนอื่นไม่จำเป็นต้องแลกกับการทิ้งตัวเองไว้ข้างหลัง"],
            "en": ["Loving others does not require leaving yourself behind."]
        }
    },
    7: {
        "core": {
            "th": [
                "คุณมีพลังของนักค้นหาความจริง ชีวิตของคุณมักไม่พอใจกับคำตอบผิวเผิน เพราะหัวใจต้องการเข้าใจสิ่งต่าง ๆ ให้ถึงแก่น",
                "คุณเชื่อมต่อกับโลกภายในได้ลึก และมักมีสัญชาตญาณที่ชัดกว่าที่ตัวเองยอมรับ"
            ],
            "en": [
                "You carry the energy of a truth seeker. Surface-level answers rarely satisfy you because your heart wants to understand life at its root.",
                "You are deeply connected to your inner world and often possess stronger intuition than you openly admit."
            ]
        },
        "shadow": {
            "th": [
                "เมื่อพลังตก คุณอาจถอยห่าง เก็บตัว คิดวน หรือรู้สึกว่าไม่มีใครเข้าใจสิ่งที่อยู่ข้างใน",
                "บทเรียนสำคัญคือการใช้ความลึกเพื่อเปิดประตู ไม่ใช่สร้างกำแพง"
            ],
            "en": [
                "When your energy drops, you may withdraw, overthink, or feel that no one truly understands what lives inside you.",
                "A core lesson is to use depth as a doorway rather than as a wall."
            ]
        },
        "love": {
            "th": [
                "ในความรัก คุณไม่ได้ต้องการเพียงความสัมพันธ์ แต่ต้องการ connection ที่จริง ลึก และซื่อสัตย์",
                "คุณอาจดูนิ่งหรือเปิดยาก แต่ความจริงคือคุณให้ความสำคัญกับความจริงใจมากกว่าความหวือหวา"
            ],
            "en": [
                "In love, you are not seeking just a relationship—you are seeking real, deep, and honest connection.",
                "You may seem reserved or hard to access, but the truth is you value sincerity more than spectacle."
            ]
        },
        "career": {
            "th": [
                "คุณเหมาะกับงานที่ได้คิด วิเคราะห์ เขียน สอน วิจัย หรือถ่ายทอดสิ่งลึกให้คนเข้าใจง่ายขึ้น",
                "คุณเติบโตได้มากเมื่อทำงานที่เชื่อมโลกภายในกับคุณค่าที่ส่งต่อออกไปภายนอก"
            ],
            "en": [
                "You are suited to work involving analysis, writing, teaching, research, or translating depth into something others can understand.",
                "You grow most when your work bridges inner truth with outer contribution."
            ]
        },
        "money": {
            "th": [
                "การเงินของคุณดีขึ้นเมื่อคุณหยุดแยกเรื่องจิตวิญญาณออกจากคุณค่าในโลกจริง",
                "เมื่อสิ่งที่คุณทำมีความหมายและมีโครงสร้าง เงินจะเริ่มไหลแบบมั่นคงขึ้น"
            ],
            "en": [
                "Your finances improve when you stop separating spirituality from real-world value.",
                "When your work carries meaning and structure, money begins to flow more steadily."
            ]
        },
        "healing": {
            "th": ["ความลึกของคุณไม่ได้ทำให้คุณยากเกินจะรัก มันแค่หมายความว่าหัวใจคุณต้องการความจริงมากกว่าคนทั่วไป"],
            "en": ["Your depth does not make you too difficult to love. It simply means your heart requires more truth than most."]
        }
    },
    8: {
        "core": {
            "th": [
                "คุณมีพลังของการบริหาร ความสำเร็จ และการทำให้สิ่งที่มองเห็นในหัวกลายเป็นผลลัพธ์ที่จับต้องได้",
                "ชีวิตของคุณมีศักยภาพสูงในเรื่องการสร้างอิทธิพล ความมั่นคง และพลังในโลกจริง"
            ],
            "en": [
                "You carry the energy of leadership, achievement, and turning vision into tangible results.",
                "Your life holds strong potential around influence, stability, and worldly power."
            ]
        },
        "shadow": {
            "th": [
                "เมื่อพลังตก คุณอาจกดดันตัวเองหนัก วัดคุณค่าจากความสำเร็จ หรือกลัวการล้มเหลวจนไม่กล้าผ่อน",
                "บทเรียนสำคัญคือการมีอำนาจโดยไม่กลายเป็นนักสู้ที่ไม่มีวันพัก"
            ],
            "en": [
                "When your energy is low, you may pressure yourself harshly, measure your worth by success, or fear failure so much that you never fully rest.",
                "Your lesson is to hold power without becoming a warrior who never stops fighting."
            ]
        },
        "love": {
            "th": [
                "ในความรัก คุณต้องการคนที่เคารพพลังและความทะเยอทะยานของคุณ ไม่ใช่ทำให้คุณรู้สึกผิดที่จริงจังกับชีวิต",
                "หัวใจคุณต้องการความซื่อสัตย์และความมั่นคงพอ ๆ กับความสำเร็จ"
            ],
            "en": [
                "In love, you need someone who respects your power and ambition rather than making you feel guilty for taking life seriously.",
                "Your heart needs honesty and stability just as much as success."
            ]
        },
        "career": {
            "th": [
                "คุณเหมาะกับงานบริหาร ธุรกิจ การเงิน การสร้างแบรนด์ หรือบทบาทที่ต้องตัดสินใจและรับผิดชอบภาพใหญ่",
                "คุณมีศักยภาพเป็นผู้นำสิ่งที่สร้างความมั่นคงให้ตัวเองและคนอื่น"
            ],
            "en": [
                "You suit business, management, finance, branding, and roles that require decision-making and big-picture responsibility.",
                "You have the potential to lead something that creates stability for both you and others."
            ]
        },
        "money": {
            "th": [
                "การเงินเป็นหนึ่งในสนามพลังสำคัญของคุณ ยิ่งคุณจัดระบบและกล้ายืนในคุณค่าของตัวเอง เงินยิ่งตอบสนอง",
                "คุณไม่ได้เกิดมาเพื่อเล็กกับเรื่องความอุดมสมบูรณ์"
            ],
            "en": [
                "Money is one of your major energetic arenas. The more you build structure and stand in your value, the more finances respond.",
                "You were not born to stay small around abundance."
            ]
        },
        "healing": {
            "th": ["ความสำเร็จที่แท้จริง ไม่ใช่การพิสูจน์ว่าคุณเก่งพอ แต่มันคือการสร้างชีวิตที่ไม่ต้องหักหลังหัวใจตัวเอง"],
            "en": ["True success is not proving you are enough. It is building a life that does not betray your own heart."]
        }
    },
    9: {
        "core": {
            "th": [
                "คุณมีพลังของผู้ให้ เมตตา เข้าใจมนุษย์ และมีสายเชื่อมกับบทเรียนเรื่องการปล่อยวาง",
                "หัวใจของคุณมักรู้สึกถึงความทุกข์ของผู้คนและต้องการทำบางอย่างที่มีความหมาย"
            ],
            "en": [
                "You carry compassionate, humanitarian energy and are deeply linked to lessons of release and meaning.",
                "Your heart often feels the suffering of others and wants to do something that matters."
            ]
        },
        "shadow": {
            "th": [
                "เมื่อพลังตก คุณอาจแบกอดีต แบกคนอื่น หรือจมกับความผิดหวังที่ยังไม่ปิดวงจร",
                "บทเรียนสำคัญคือการให้โดยไม่ทำให้ตัวเองสูญหาย"
            ],
            "en": [
                "When your energy is low, you may carry the past, carry other people, or remain entangled in disappointments that never fully closed.",
                "Your lesson is to give without disappearing."
            ]
        },
        "love": {
            "th": [
                "ในความรัก คุณต้องการความหมาย ความเข้าใจ และความสัมพันธ์ที่ไม่ตื้น",
                "แต่คุณต้องระวังความเมตตาที่ทำให้ยอมทนกับสิ่งที่ควรปล่อย"
            ],
            "en": [
                "In love, you seek meaning, emotional understanding, and depth.",
                "But you must watch for compassion becoming the reason you stay in what should already be released."
            ]
        },
        "career": {
            "th": [
                "คุณเหมาะกับงานเยียวยา สอน ช่วยเหลือ สร้างแรงบันดาลใจ หรือสิ่งที่ส่งผลต่อผู้คนในวงกว้าง",
                "ชีวิตคุณเด่นเมื่อสิ่งที่ทำมีคุณค่าต่อมากกว่าตัวเอง"
            ],
            "en": [
                "You suit healing, teaching, helping, inspiring, or work that impacts people on a larger scale.",
                "Your life becomes powerful when what you do serves more than just yourself."
            ]
        },
        "money": {
            "th": [
                "การเงินของคุณมั่นคงขึ้นเมื่อคุณเลิกคิดว่าจิตวิญญาณกับความอุดมสมบูรณ์ไปด้วยกันไม่ได้",
                "คุณทำเงินได้ดีเมื่อสิ่งที่ทำมีหัวใจและมีขอบเขตที่ชัด"
            ],
            "en": [
                "Your finances become steadier when you stop believing spirituality and abundance cannot coexist.",
                "You do well financially when your work has heart and clear boundaries."
            ]
        },
        "healing": {
            "th": ["สิ่งที่คุณต้องปล่อย ไม่ได้แปลว่าคุณรักน้อยลง แต่มันแปลว่าคุณเริ่มรักตัวเองด้วย"],
            "en": ["What you release does not mean you love less. It means you are finally including yourself in that love."]
        }
    },
    11: {
        "core": {
            "th": [
                "คุณมีพลังของผู้ตื่นรู้ ญาณรู้ และการรับรู้สิ่งที่ลึกกว่าระดับผิว",
                "ชีวิตของคุณมักมีช่วงที่ดูเหมือนแรงเกินไปหรืออ่อนไหวเกินไป เพราะคุณรับคลื่นได้มากกว่าคนทั่วไป"
            ],
            "en": [
                "You carry awakened energy, heightened intuition, and the ability to sense what lies beyond the surface.",
                "Your life may often feel intense or overly sensitive because you receive more than most people do."
            ]
        },
        "shadow": {
            "th": [
                "เมื่อพลังตก คุณอาจสับสนในสิ่งที่ตัวเองรับรู้ รู้สึกเหนื่อยง่าย หรือแยกไม่ออกว่าอะไรเป็นของตัวเองอะไรเป็นของคนอื่น",
                "บทเรียนของคุณคือการฝังแสงลงบนพื้นดิน ไม่ใช่ลอยอยู่กับความรู้สึกอย่างเดียว"
            ],
            "en": [
                "When your energy drops, you may doubt what you sense, feel easily drained, or struggle to separate your energy from others.",
                "Your lesson is to ground your light instead of floating only in feeling."
            ]
        },
        "love": {
            "th": [
                "ในความรัก คุณต้องการความเชื่อมโยงระดับวิญญาณ แต่ก็ต้องการคนที่มั่นคงพอจะอยู่กับความลึกของคุณได้",
                "คุณไม่เหมาะกับความสัมพันธ์ที่เล่นเกมหรือไม่ชัดเจน"
            ],
            "en": [
                "In love, you seek soul-level connection, but you also need someone stable enough to meet your depth.",
                "You are not built for games or emotional vagueness."
            ]
        },
        "career": {
            "th": [
                "คุณเหมาะกับงานที่ผสานจิตวิญญาณกับการสื่อสาร การสอน การเยียวยา หรือการสร้างแรงบันดาลใจ",
                "ชีวิตคุณจะเด่นเมื่อสิ่งที่คุณรับรู้ถูกแปลออกมาเป็นประโยชน์ต่อผู้คน"
            ],
            "en": [
                "You suit work that bridges spirituality with communication, teaching, healing, or inspiration.",
                "Your life path becomes powerful when what you sense is translated into something useful for others."
            ]
        },
        "money": {
            "th": [
                "การเงินของคุณดีขึ้นเมื่อคุณหยุดลดทอนของขวัญตัวเอง",
                "สิ่งที่คุณมองว่าเป็นเรื่องลึกหรือธรรมดาสำหรับคุณ อาจเป็นสิ่งล้ำค่าสำหรับคนอื่น"
            ],
            "en": [
                "Your finances improve when you stop minimizing your gifts.",
                "What feels normal or deeply personal to you may actually be profoundly valuable to others."
            ]
        },
        "healing": {
            "th": ["คุณไม่ได้แปลกเกินไป คุณแค่รับแสงได้มากเกินกว่าที่โลกทั่วไปสอนให้เข้าใจ"],
            "en": ["You are not too strange. You simply receive more light than the ordinary world knows how to explain."]
        }
    },
    22: {
        "core": {
            "th": [
                "คุณมีพลังของผู้สร้างสิ่งใหญ่ให้เป็นจริง เห็นภาพกว้างและมีศักยภาพสร้างผลกระทบที่ยาวไกล",
                "คุณไม่ได้มีพลังแค่ฝัน แต่มีพลังทำให้สิ่งนั้นลงสู่โลกจริง"
            ],
            "en": [
                "You carry the energy of the master builder—someone who can see the bigger vision and create long-range impact.",
                "Your power is not just in dreaming, but in bringing that dream into reality."
            ]
        },
        "shadow": {
            "th": [
                "เมื่อพลังตก คุณอาจรู้สึกหนักกับภาระ รู้สึกว่าต้องแบกอะไรใหญ่เกินไป หรือกลัวความรับผิดชอบในศักยภาพตัวเอง",
                "บทเรียนสำคัญคือการสร้างใหญ่โดยไม่แบกทุกอย่างคนเดียว"
            ],
            "en": [
                "When your energy drops, you may feel overwhelmed by responsibility or afraid of the scale of your own potential.",
                "Your lesson is to build big without carrying everything alone."
            ]
        },
        "love": {
            "th": [
                "ในความรัก คุณต้องการคนที่เดินเติบโตไปด้วยกัน ไม่ใช่ความสัมพันธ์ที่ดึงคุณออกจากภารกิจชีวิต",
                "คุณรักจริงจังและมองไกล จึงต้องการความสัมพันธ์ที่มีรากฐาน"
            ],
            "en": [
                "In love, you need someone who can grow alongside you rather than pull you away from your mission.",
                "You love seriously and think long-term, so relationships need foundation."
            ]
        },
        "career": {
            "th": [
                "คุณเหมาะกับการสร้างธุรกิจ ระบบ แพลตฟอร์ม ทีม หรือสิ่งที่ส่งผลต่อผู้คนจำนวนมาก",
                "คุณมีพลังทำวิสัยทัศน์ให้เป็นสิ่งจับต้องได้ ถ้ากล้าค่อย ๆ วางโครงอย่างมีวินัย"
            ],
            "en": [
                "You suit building businesses, systems, platforms, teams, or anything that serves many people.",
                "You can turn vision into form when you commit to structure and long-term discipline."
            ]
        },
        "money": {
            "th": [
                "การเงินของคุณมีศักยภาพสูงมากเมื่อคุณทำสิ่งที่ใหญ่พอจะรับพลังคุณได้",
                "คุณไม่ได้เกิดมาเพื่อแค่พออยู่ แต่เพื่อสร้างสิ่งที่มั่นคงและส่งต่อได้"
            ],
            "en": [
                "Your financial potential is high when you engage in work big enough to hold your energy.",
                "You were not born only to survive—you were born to build something strong and transmissible."
            ]
        },
        "healing": {
            "th": ["อย่ากลัวศักยภาพของตัวเอง เพราะสิ่งที่ดูใหญ่ในใจคุณ อาจเป็นเหตุผลที่คุณมาเกิด"],
            "en": ["Do not fear your own potential. What feels huge inside you may be one of the reasons you came here."]
        }
    },
    33: {
        "core": {
            "th": [
                "คุณมีพลังของครูผู้เยียวยา เมตตา ลึก ซื่อสัตย์กับหัวใจ และมีแรงผลักดันที่จะส่งบางอย่างที่ช่วยผู้คนได้จริง",
                "พลังของคุณไม่ใช่แค่เข้าใจความเจ็บปวด แต่สามารถแปรมันเป็นแสงให้คนอื่นได้"
            ],
            "en": [
                "You carry the energy of the healing teacher—compassionate, deep, heart-led, and moved to offer something genuinely helpful to people.",
                "Your gift is not only understanding pain, but turning it into light for others."
            ]
        },
        "shadow": {
            "th": [
                "เมื่อพลังตก คุณอาจแบกความทุกข์คนอื่นมากไป คาดหวังกับตัวเองสูง และลืมว่าแม้ผู้เยียวยาก็ต้องได้รับการเยียวยา",
                "บทเรียนคือการรับใช้โดยไม่สูญเสียหัวใจตัวเอง"
            ],
            "en": [
                "When your energy drops, you may carry too much of others’ pain, hold impossible standards for yourself, and forget that healers also need healing.",
                "Your lesson is to serve without losing your own heart."
            ]
        },
        "love": {
            "th": [
                "ในความรัก คุณต้องการความสัมพันธ์ที่อบอุ่น ลึก และช่วยให้ทั้งสองคนเติบโต",
                "แต่คุณต้องระวังบทบาทผู้ช่วยชีวิตที่ทำให้หัวใจเหนื่อย"
            ],
            "en": [
                "In love, you seek warmth, emotional depth, and a bond that helps both people grow.",
                "But you must watch for the savior role that exhausts the heart."
            ]
        },
        "career": {
            "th": [
                "คุณเหมาะกับงานสอน เยียวยา โค้ช สื่อสารจากหัวใจ หรือธุรกิจที่สร้างการเปลี่ยนแปลงกับชีวิตคน",
                "ความสำเร็จของคุณมาเมื่อภารกิจและการลงมือจริงเดินไปด้วยกัน"
            ],
            "en": [
                "You suit teaching, healing, coaching, heart-led communication, or work that genuinely transforms lives.",
                "Your success comes when mission and practical action walk together."
            ]
        },
        "money": {
            "th": [
                "การเงินของคุณไม่ควรถูกตัดออกจากภารกิจ คุณสามารถได้รับอย่างงดงามจากสิ่งที่ช่วยผู้คน",
                "คุณไม่ได้จำเป็นต้องเลือกระหว่างหัวใจกับความอุดมสมบูรณ์"
            ],
            "en": [
                "Your finances do not need to be separated from your mission. You can receive beautifully through work that helps people.",
                "You do not have to choose between heart and abundance."
            ]
        },
        "healing": {
            "th": ["การเป็นแสงให้คนอื่น ไม่จำเป็นต้องแผดเผาตัวเองจนหมดแรง"],
            "en": ["Being a light for others does not require burning yourself out."]
        }
    }
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


def shadow_reflection(life_number: int, lang: str):
    profile = get_profile(life_number)
    return paragraph(profile["shadow"][lang])


def healing_message(life_number: int, lang: str):
    profile = get_profile(life_number)
    return paragraph(profile["healing"][lang])


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

    result = {
        "title": title,
        "life_number": life_num,
        "birth_energy": birth_energy,
        "intro": life_intro(life_num, birth_energy, month_num, lang),
        "category_text": category_reflection(category_key, life_num, lang),
        "focus_text": current_focus_block(category_key, q_signal, life_num, lang),
        "question_signal": q_signal
    }
    return result


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
        next_steps = {
            "love": "ลองถามตัวเองให้ชัดว่า ความรักแบบไหนที่ทำให้ใจคุณขยาย ไม่ใช่หดเล็กลง และอย่าด่วนกลับไปหาสิ่งเดิมเพียงเพราะมันคุ้น",
            "career": "จัดโครงสิ่งที่คุณทำให้ชัดขึ้นทีละขั้น เลือกสิ่งที่ใช่จริงก่อน แล้วค่อยให้พลังของคุณขยายตามนั้น",
            "money": "เริ่มมองเงินเป็นพลังตอบรับคุณค่า ไม่ใช่ตัวตัดสินคุณค่า เมื่อคุณกล้ายืนในสิ่งที่มีจริง กระแสรับจะชัดขึ้น"
        }
        caution_map = {
            "love": "ระวังการตีความความผูกพันเป็นความรัก หากสิ่งนั้นทำให้คุณเสียพลังซ้ำ ๆ",
            "career": "ระวังการรอให้พร้อมจนเกินไป เพราะบางเส้นทางจะชัดขึ้นก็ต่อเมื่อเริ่มเดิน",
            "money": "ระวังการกดราคาตัวเอง หรือทำทุกอย่างฟรีจนพลังชีวิตอ่อนแรง"
        }
        unlock_note = "หากข้อความนี้สะท้อนชีวิตคุณจริง คุณสามารถใช้ผลลัพธ์นี้เป็นสะพานต่อไปยัง eBook หรือการอ่านส่วนตัวเชิงลึกได้"
    else:
        premium_title = f"✨ Your Deep Energy Blueprint: {name}"
        soul_text = (
            f"{name}, you did not arrive at this point by accident. "
            f"Your Life Path {life_num} suggests that life is asking you to return to your real power with greater awareness. "
            f"Your Birth Day Energy {birth_energy} adds its own signature to how that power wants to be expressed. "
            f"This is not only a season of becoming stronger—it is a season of becoming more honest with yourself."
        )
        next_steps = {
            "love": "Ask yourself what kind of love makes your heart expand rather than shrink. Do not return to what is familiar if it repeatedly costs you your energy.",
            "career": "Create clearer structure around what you are building. Choose what is truly aligned first, then let your energy expand from there.",
            "money": "Start seeing money as feedback to value rather than as proof of value. When you stand in what is real, receiving becomes clearer."
        }
        caution_map = {
            "love": "Be careful not to mistake attachment for love if it keeps draining your energy.",
            "career": "Be careful not to wait for total readiness; some paths become clear only after you begin walking them.",
            "money": "Be careful not to underprice yourself or give everything away until your life-force weakens."
        }
        unlock_note = "If this resonates deeply, you can use this result as a bridge into your eBook or a deeper personal reading."

    return {
        "premium_title": premium_title,
        "shadow": paragraph(profile["shadow"][lang]),
        "soul_text": soul_text,
        "healing": paragraph(profile["healing"][lang]),
        "next_step": next_steps.get(category_key, next_steps["career"]),
        "caution": caution_map.get(category_key, caution_map["career"]),
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
    contact = st.text_input(tr("ID Line (เพื่อรับสิทธิ์ปลดล็อค)", "Line ID (for unlock access)"), value=LINE_ID)

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
            "premium_next_step": premium_result["next_step"],
            "premium_caution": premium_result["caution"],
            "language": st.session_state.lang,
            "source": "website_form_v2",
            "submitted_at": str(datetime.now())
        })

        st.session_state.premium_unlocked = False
        st.session_state.used_code = ""

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
                    "สิ่งที่คุณอ่านไป คือเพียงชั้นแรกของพลังงานชีวิตคุณเท่านั้น ลึกลงไปกว่านั้น ยังมีเงา บทเรียน จุดระวัง และข้อความเฉพาะตัวที่ยังไม่ได้ถูกเปิดออก",
                    "What you have read so far is only the first layer of your energetic blueprint. Deeper beneath it, there are shadow patterns, lessons, cautions, and a more personal soul message still waiting to be revealed."
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
                <p>{premium_result["caution"]}</p>
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
''')

path = "/mnt/data/app.py"
with open(path, "w", encoding="utf-8") as f:
    f.write(code)

print(path)
