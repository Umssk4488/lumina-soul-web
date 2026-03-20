import streamlit as st
import requests
from datetime import datetime

# -----------------------------
# Page config
# -----------------------------
st.set_page_config(
    page_title="LUMINA SOUL",
    page_icon="🔮",
    layout="centered"
)
st.image("banner.jpg.png", use_container_width=True)

# -----------------------------
# Language state
# -----------------------------
if "lang" not in st.session_state:
    st.session_state.lang = "th"


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

    .result-card, .mini-card, .stat-card, .review-card {
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

@media (prefers-color-scheme: dark) {
    html, body, .stApp {
        color: #2f1f38 !important;
        background-color: transparent !important;
    }

    p, span, div, label, li, small {
        color: #2f1f38 !important;
    }

    .result-card, .mini-card, .stat-card, .review-card, .hero-card, .glow-box {
        color: #2f1f38 !important;
        background: rgba(255,255,255,0.88) !important;
    }

    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea textarea,
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: rgba(255,255,255,0.95) !important;
        color: #2f1f38 !important;
        -webkit-text-fill-color: #2f1f38 !important;
    }

    input::placeholder,
    textarea::placeholder {
        color: #8d7b9a !important;
        -webkit-text-fill-color: #8d7b9a !important;
    }
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# Google Sheets endpoint
# -----------------------------
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbztgbRuGYMGMC41V8QHgNl2wnNTgJ5ZhRckVoiUXpVNTkSA-U75MFg-GRZNiCiIjrQeGg/exec"

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


# -----------------------------
# Thai-English content
# -----------------------------
life_path_meanings = {
    1: {
        "th": "คุณมีพลังของผู้เริ่มต้น กล้าตัดสินใจ ชอบสร้างเส้นทางของตัวเอง และไม่เหมาะกับการใช้ชีวิตแบบที่ต้องกดตัวตนไว้ตลอดเวลา",
        "en": "You carry the energy of an initiator. You are courageous, decisive, and naturally drawn to create your own path instead of shrinking yourself to fit into someone else’s."
    },
    2: {
        "th": "คุณมีพลังของผู้ประสานใจ ลึกซึ้ง อ่อนโยน รับความรู้สึกคนอื่นได้ดี และมีพรสวรรค์ในการเชื่อมโยงหัวใจผู้คน",
        "en": "You hold the energy of a harmonizer—sensitive, gentle, and deeply attuned to the emotions of others, with a natural gift for connecting hearts."
    },
    3: {
        "th": "คุณมีพลังแห่งการสื่อสาร ความคิดสร้างสรรค์ และเสน่ห์ตามธรรมชาติ เมื่อคุณกล้าแสดงออก โลกจะเริ่มตอบรับคุณชัดขึ้น",
        "en": "You carry the energy of expression, creativity, and natural charm. When you allow yourself to be seen and heard, life responds more clearly."
    },
    4: {
        "th": "คุณมีพลังแห่งความมั่นคง เป็นคนสร้างรากฐาน เก่งเรื่องระบบ ความรับผิดชอบ และการเปลี่ยนสิ่งเล็ก ๆ ให้กลายเป็นความมั่นคงระยะยาว",
        "en": "You embody stability and grounded strength. You are gifted at building systems, taking responsibility, and turning small consistent actions into long-term security."
    },
    5: {
        "th": "คุณมีพลังแห่งอิสรภาพ การเปลี่ยนแปลง การเดินทาง และการเรียนรู้ผ่านประสบการณ์ตรง ชีวิตของคุณจะเติบโตมากเมื่อไม่ฝืนตัวเอง",
        "en": "You carry the energy of freedom, change, movement, and experience. Your life expands most when you stop forcing yourself into what no longer fits."
    },
    6: {
        "th": "คุณมีพลังของผู้ดูแลและผู้เยียวยา หัวใจของคุณมีพลังในการโอบอุ้มคนอื่น แต่บทเรียนสำคัญคืออย่าลืมดูแลหัวใจตัวเองด้วย",
        "en": "You hold the energy of a nurturer and healer. Your heart has the power to care deeply for others, but your lesson is to remember your own heart too."
    },
    7: {
        "th": "คุณมีพลังของนักค้นหาความจริง ชอบตั้งคำถาม ชอบเข้าใจชีวิตในระดับลึก และมักมีสายเชื่อมต่อกับโลกภายในอย่างชัดเจน",
        "en": "You carry the energy of a truth seeker. You are drawn to deeper questions, inner meaning, and often have a strong connection to your inner world."
    },
    8: {
        "th": "คุณมีพลังด้านการบริหาร การเงิน ความสำเร็จ และการทำสิ่งใหญ่ให้เกิดขึ้นจริง หากใช้พลังอย่างสมดุล คุณมีศักยภาพสร้างความมั่นคงสูงมาก",
        "en": "You carry strong energy for leadership, finance, achievement, and bringing big visions into reality. In balance, you can create solid success and lasting stability."
    },
    9: {
        "th": "คุณมีพลังของผู้ให้ เมตตา เข้าใจมนุษย์ และมักมีบทบาทเกี่ยวข้องกับการช่วยเหลือหรือส่งต่อบางอย่างที่มีความหมายต่อผู้อื่น",
        "en": "You embody compassion, generosity, and humanitarian energy. You are often connected to helping others or offering something deeply meaningful."
    },
    11: {
        "th": "คุณมีพลังของผู้ตื่นรู้ สัญชาตญาณแรง รับรู้อะไรลึกกว่าคนทั่วไป และมีศักยภาพเป็นแสงนำทางให้ผู้คนรอบตัว",
        "en": "You carry awakened energy with strong intuition. You often sense things beyond the surface and may serve as a guiding light for others."
    },
    22: {
        "th": "คุณมีพลังของผู้สร้างสิ่งใหญ่ให้เป็นจริง มองภาพกว้างได้ดี และมีศักยภาพเปลี่ยนวิสัยทัศน์ให้เป็นสิ่งที่จับต้องได้",
        "en": "You hold the energy of a master builder—someone who can turn large visions into tangible reality and create impact on a wider scale."
    },
    33: {
        "th": "คุณมีพลังของครูผู้เยียวยา เปี่ยมเมตตา อ่อนโยน และมีภารกิจในการส่งต่อความรัก ความเข้าใจ และแสงสว่างให้ผู้อื่น",
        "en": "You carry the energy of a healing teacher—compassionate, gentle, and deeply aligned with sharing love, wisdom, and light with others."
    }
}

birth_day_meanings = {
    1: {
        "th": "วันเกิดของคุณสะท้อนพลังนักบุกเบิก คุณมักไม่ชอบเดินตามกรอบเดิม และมีแรงขับภายในที่ชัดเจน",
        "en": "Your birth day reflects pioneering energy. You do not naturally enjoy staying inside old frameworks, and you carry strong internal drive."
    },
    2: {
        "th": "วันเกิดของคุณสะท้อนพลังความอ่อนโยน การรับรู้ และความสามารถในการเข้าใจความละเอียดอ่อนของผู้คน",
        "en": "Your birth day reflects gentleness, emotional awareness, and a natural ability to understand the subtle feelings of others."
    },
    3: {
        "th": "วันเกิดของคุณสะท้อนพลังความสดใส ความคิดสร้างสรรค์ และคำพูดที่มีอิทธิพลต่อความรู้สึกของคนรอบตัว",
        "en": "Your birth day reflects brightness, creativity, and words that can influence the emotions of those around you."
    },
    4: {
        "th": "วันเกิดของคุณสะท้อนพลังความมั่นคง ความรับผิดชอบ และความจริงจังต่อสิ่งที่คุณให้คุณค่า",
        "en": "Your birth day reflects stability, responsibility, and sincere commitment to what matters most to you."
    },
    5: {
        "th": "วันเกิดของคุณสะท้อนพลังการเปลี่ยนแปลง การเรียนรู้ ความคล่องตัว และความกล้าลองเส้นทางใหม่",
        "en": "Your birth day reflects change, learning, adaptability, and the courage to explore new directions."
    },
    6: {
        "th": "วันเกิดของคุณสะท้อนพลังผู้ดูแล ผู้เยียวยา และหัวใจที่ให้ความสำคัญกับความรักและความสัมพันธ์",
        "en": "Your birth day reflects the energy of care, healing, and a heart that values love and relationships deeply."
    },
    7: {
        "th": "วันเกิดของคุณสะท้อนพลังนักสังเกต นักค้นหาความหมาย และคนที่มีโลกภายในลึกกว่าที่คนอื่นมองเห็น",
        "en": "Your birth day reflects the energy of observation, inner meaning, and a rich inner world that others may not fully see."
    },
    8: {
        "th": "วันเกิดของคุณสะท้อนพลังความมุ่งมั่น อำนาจภายใน และศักยภาพในการสร้างผลลัพธ์ที่จับต้องได้",
        "en": "Your birth day reflects determination, inner authority, and the ability to create concrete results."
    },
    9: {
        "th": "วันเกิดของคุณสะท้อนพลังแห่งเมตตา ความเข้าใจมนุษย์ และการเรียนรู้เรื่องการปล่อยวาง",
        "en": "Your birth day reflects compassion, understanding of humanity, and important lessons around letting go."
    },
    11: {
        "th": "วันเกิดของคุณสะท้อนพลังญาณรู้ ความละเอียดทางพลังงาน และการเชื่อมต่อกับสิ่งที่มองไม่เห็น",
        "en": "Your birth day reflects intuitive knowing, energetic sensitivity, and connection to what cannot always be seen."
    },
    22: {
        "th": "วันเกิดของคุณสะท้อนพลังผู้สร้างสิ่งใหญ่ มีศักยภาพทำสิ่งที่ส่งผลต่อผู้คนจำนวนมาก",
        "en": "Your birth day reflects builder energy with the potential to create something meaningful for many people."
    },
    33: {
        "th": "วันเกิดของคุณสะท้อนพลังแห่งการเยียวยา การสอน และการรับใช้ด้วยหัวใจ",
        "en": "Your birth day reflects healing, teaching, and heartfelt service."
    }
}

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

month_energy_meanings = {
    1: {"th": "พลังของการเริ่มต้นและความชัดเจน", "en": "the energy of beginnings and clarity"},
    2: {"th": "พลังของความสัมพันธ์และความอ่อนโยน", "en": "the energy of connection and gentleness"},
    3: {"th": "พลังของการสื่อสารและความคิดสร้างสรรค์", "en": "the energy of communication and creativity"},
    4: {"th": "พลังของความมั่นคงและการวางรากฐาน", "en": "the energy of stability and foundation-building"},
    5: {"th": "พลังของการเปลี่ยนแปลงและอิสรภาพ", "en": "the energy of change and freedom"},
    6: {"th": "พลังของความรัก การดูแล และการเยียวยา", "en": "the energy of love, care, and healing"},
    7: {"th": "พลังของการค้นหาความหมายภายใน", "en": "the energy of inner searching and meaning"},
    8: {"th": "พลังของความสำเร็จและการผลักดันเป้าหมาย", "en": "the energy of achievement and forward momentum"},
    9: {"th": "พลังของการให้ การปล่อยวาง และการเข้าใจชีวิต", "en": "the energy of giving, release, and understanding life"},
    10: {"th": "พลังของจุดเปลี่ยนและการเปิดวงจรใหม่", "en": "the energy of turning points and new cycles"},
    11: {"th": "พลังของญาณรู้และการตื่นรู้ภายใน", "en": "the energy of intuition and inner awakening"},
    12: {"th": "พลังของการปิดวงจรเก่าเพื่อเตรียมสู่การเริ่มต้นใหม่", "en": "the energy of closing old cycles to prepare for a new beginning"}
}

categories = [
    {"key": "love", "th": "ความรักและความสัมพันธ์", "en": "Love & Relationships"},
    {"key": "career", "th": "การงานและเส้นทางชีวิต", "en": "Career & Life Path"},
    {"key": "money", "th": "โชคลาภและกระแสการเงิน", "en": "Luck & Financial Flow"}
]

category_advice = {
    "love": {
        "th": "นี่คือคำสะท้อนพลังงานเบื้องต้น หากอยากอ่านลึกเฉพาะความสัมพันธ์ของคุณแบบเจาะรายละเอียด สามารถทักเข้ามาได้",
        "en": "This is an initial energetic reflection. If you would like a deeper reading focused specifically on your relationships, you can reach out for a more personalized session."
    },
    "career": {
        "th": "นี่คือคำสะท้อนเบื้องต้นของเส้นทางชีวิต หากต้องการอ่านลึกเรื่องงานและจังหวะชีวิตเฉพาะตัว สามารถทักเข้ามาได้",
        "en": "This is an initial reflection of your life path. If you would like a deeper reading about career and personal timing, you can contact us for a personalized session."
    },
    "money": {
        "th": "นี่คือคำสะท้อนเบื้องต้นของกระแสการเงิน หากต้องการอ่านลึกเฉพาะตัวเรื่องเงินและโอกาส สามารถทักเข้ามาได้",
        "en": "This is an initial reflection of your financial flow. If you would like a deeper reading about money, opportunities, and personal timing, you can reach out for a personalized session."
    }
}

# -----------------------------
# Generate content
# -----------------------------
def generate_main_result(category_key: str, life_number: int, birth_energy: int, question_text: str, lang: str) -> str:
    if category_key == "love":
        if life_number in [2, 6, 9, 11, 33]:
            return (
                "พลังความรักของคุณเป็นพลังที่ลึกและจริงใจมาก คุณไม่ได้ต้องการแค่ความสัมพันธ์ แต่ต้องการความเชื่อมโยงที่สัมผัสถึงหัวใจจริง ๆ ช่วงนี้บทเรียนสำคัญคือการแยกให้ออกว่าอะไรคือความรัก และอะไรคือการยอมทนเพราะกลัวเสียใครบางคนไป"
                if lang == "th" else
                "Your love energy is deep, sincere, and emotionally real. You are not looking for just any relationship—you are seeking true heart-level connection. Your current lesson is learning to tell the difference between real love and staying because you fear losing someone."
            )
        elif life_number in [1, 5, 8, 22]:
            return (
                "ความรักของคุณมักเชื่อมโยงกับบทเรียนเรื่องคุณค่าในตัวเองและขอบเขตที่ชัดเจน คุณมีเสน่ห์และแรงดึงดูดสูง แต่หัวใจจะสงบได้จริงเมื่อคุณเลือกคนที่เคารพตัวตนของคุณ ไม่ใช่คนที่ทำให้คุณต้องเล็กลง"
                if lang == "th" else
                "Your love path is closely tied to self-worth and healthy boundaries. You carry strong magnetism, but your heart finds peace only when you choose someone who respects who you truly are rather than someone who makes you shrink."
            )
        return (
            "หัวใจของคุณกำลังเรียนรู้บางอย่างผ่านความสัมพันธ์ที่ผ่านมา สิ่งที่เกิดขึ้นไม่ได้มาเพื่อทำร้ายคุณ แต่มาเพื่อสอนให้คุณกลับมาเข้าใจความต้องการที่แท้จริงของหัวใจ และเปิดพื้นที่ให้ความสัมพันธ์ที่เหมาะสมกว่าเข้ามา"
            if lang == "th" else
            "Your heart is learning something important through past relationships. What happened was not here only to hurt you—it was here to teach you about your true emotional needs and make space for a healthier connection."
        )

    if category_key == "career":
        if life_number in [1, 4, 8, 22]:
            return (
                "เส้นทางการงานของคุณไม่ได้ธรรมดา คุณมีพลังในการสร้างบางอย่างให้เกิดขึ้นจริง ช่วงนี้อาจเหมือนถูกกดดันหรือถูกบีบให้ตัดสินใจ แต่แท้จริงแล้วชีวิตกำลังผลักคุณออกจากทางเดิม เพื่อพาไปสู่บทบาทที่ใหญ่และชัดเจนกว่าเดิม"
                if lang == "th" else
                "Your career path is not ordinary. You carry the energy to build something real. This period may feel pressuring or demanding, but life may actually be pushing you out of an old path and toward a bigger, clearer role."
            )
        elif life_number in [3, 5, 7, 11]:
            return (
                "เส้นทางชีวิตของคุณเด่นเรื่องการค้นหา การสื่อสาร และการใช้ตัวตนที่แท้จริงเป็นเครื่องนำทาง งานที่เหมาะกับคุณคือสิ่งที่ทำแล้วใจไม่ฝืน และยิ่งคุณฟังสัญญาณจากข้างในมากเท่าไร เส้นทางจะยิ่งเปิดชัดขึ้น"
                if lang == "th" else
                "Your life path stands out through exploration, expression, and following your authentic self. The right work for you is work that does not feel like inner resistance. The more you trust your inner signals, the clearer your path becomes."
            )
        return (
            "การงานในช่วงนี้อาจดูเหมือนยังไม่ชัด แต่จริง ๆ แล้วคุณกำลังอยู่ในช่วงจัดระเบียบชีวิตใหม่ เพื่อให้สิ่งที่สอดคล้องกับหัวใจมากกว่าเดิมเข้ามาแทนที่ ชีวิตไม่ได้พาคุณหลงทาง มันกำลังพาคุณกลับเข้าหาตัวเอง"
            if lang == "th" else
            "Work may feel uncertain right now, but you may actually be in a period of realignment. Life is not leading you away from yourself—it may be guiding you back to what feels more aligned and true."
        )

    if life_number in [8, 4, 22]:
        return (
            "พลังการเงินของคุณมีศักยภาพสูงมาก แต่จะเปิดเต็มที่เมื่อคุณจัดระบบความคิดและการตัดสินใจให้ชัดขึ้น เงินของคุณไม่ได้มาเพราะโชคอย่างเดียว แต่มาจากความสามารถในการสร้างมูลค่าและยืนระยะ"
            if lang == "th" else
            "Your financial energy has strong potential, but it opens most fully when your thinking and decisions become more structured and clear. Your prosperity is not based on luck alone—it grows through value creation and consistency."
        )
    elif life_number in [5, 3, 1]:
        return (
            "กระแสการเงินของคุณสัมพันธ์กับความกล้าลอง ความคิดสร้างสรรค์ และการขยับตัว หากช่วงนี้เงินนิ่งหรือช้า อาจไม่ใช่เพราะคุณไม่มีโชค แต่เป็นเพราะคุณกำลังต้องเปลี่ยนวิธีคิดหรือวิธีเปิดรับโอกาสใหม่"
            if lang == "th" else
            "Your financial flow is connected to courage, creativity, and movement. If money feels slow right now, it may not mean you lack luck—it may mean a new mindset or a new way of receiving opportunities is needed."
        )
    return (
        "การเงินของคุณเชื่อมโยงกับพลังใจอย่างมาก เมื่อใจแบกความกังวลมากเกินไป กระแสทรัพย์จะติดขัดง่าย ช่วงนี้จึงเป็นจังหวะสำคัญในการเคลียร์ความกลัว ความไม่มั่นใจ และกลับมาเชื่อในคุณค่าของตัวเองอีกครั้ง"
        if lang == "th" else
        "Your financial flow is deeply connected to your emotional state. When your heart carries too much fear or pressure, abundance can feel blocked. This may be an important time to release doubt and reconnect with your true worth."
    )


def generate_soul_message(name: str, category_label: str, life_number: int, birth_energy: int, month_num: int, lang: str) -> str:
    month_energy = month_energy_meanings.get(
        month_num,
        {"th": "พลังเฉพาะของช่วงเวลาที่คุณเกิด", "en": "a unique energy connected to the time you were born"}
    )

    if lang == "th":
        return f"""
{name} เป็นคนที่มีพลังภายในเฉพาะตัว และไม่ได้เดินทางมาถึงจุดนี้โดยบังเอิญ

เลขเส้นทางชีวิตของคุณสะท้อนว่า ชีวิตกำลังสอนให้คุณกลับมาใช้พลังแท้ของตัวเองอย่างมีสติ
ขณะที่พลังวันเกิดของคุณบอกว่า ลึกลงไปแล้วคุณมีศักยภาพบางอย่างที่พร้อมเติบโต หากคุณเลิกสงสัยในคุณค่าของตัวเอง

พลังเดือนเกิดของคุณยังสะท้อนถึง{month_energy["th"]}
จึงเป็นไปได้ว่า ชีวิตของคุณไม่ได้มาเพื่ออยู่แบบเดิมไปเรื่อย ๆ
แต่มาเพื่อเรียนรู้ เติบโต และค่อย ๆ เข้าใกล้เส้นทางที่สอดคล้องกับจิตวิญญาณมากขึ้น

นี่คือการอ่านพลังงานเบื้องต้นเท่านั้น
หากต้องการอ่านเชิงลึกแบบเฉพาะตัวในเรื่อง{category_label} สามารถทักมาพูดคุยต่อได้
""".strip()

    return f"""
{name} carries a unique inner energy and did not arrive at this point by accident.

Your life path number suggests that life is teaching you to return to your true power with more awareness.
Your birth-day energy also suggests that deep within you, there is a part of you ready to grow once you stop doubting your own worth.

Your birth month reflects {month_energy["en"]}.
Because of this, your life may not be meant to remain the same forever.
It may be calling you to learn, evolve, and move closer to a path that feels more aligned with your soul.

This is only a first energetic reflection.
If you would like a deeper personalized reading in the area of {category_label}, you are welcome to reach out.
""".strip()


def build_premium_reading(category_key: str, life_number: int, lang: str) -> dict:
    if lang == "th":
        strengths = {
            "love": "คุณมีพลังรักที่ลึก ซื่อสัตย์ และรับรู้อารมณ์คนอื่นได้ดี จุดเด่นของคุณคือการเชื่อมโยงหัวใจคนได้จริง",
            "career": "คุณมีพลังในการสร้างเส้นทางของตัวเอง และมีศักยภาพเติบโตมากเมื่อได้ทำสิ่งที่สอดคล้องกับตัวตนจริง",
            "money": "คุณมีพลังสร้างมูลค่าได้ดี หากจัดระบบความคิด การตัดสินใจ และความเชื่อเรื่องคุณค่าในตัวเองให้ชัด"
        }
        next_steps = {
            "love": "โฟกัสที่การตั้งขอบเขตและถามตัวเองให้ชัดว่าความรักแบบไหนที่ดีต่อใจคุณจริง",
            "career": "สังเกตว่างานแบบไหนที่ทำแล้วใจไม่ฝืน เพราะนั่นคือสัญญาณของเส้นทางที่ใช่กว่าเดิม",
            "money": "เริ่มจัดระบบการเงินและเปิดรับวิธีสร้างรายได้ใหม่ โดยไม่ดูถูกคุณค่าของตัวเอง"
        }
        cautions = {
            "love": "ระวังการยอมทนเพียงเพราะกลัวเสียใครไป",
            "career": "ระวังอยู่ในเส้นทางเดิมเพียงเพราะความคุ้นเคย",
            "money": "ระวังการตัดสินตัวเองจากรายได้ระยะสั้น"
        }
    else:
        strengths = {
            "love": "You carry deep, sincere love energy and a real ability to connect with people at heart level.",
            "career": "You have strong potential to create your own path and grow when your work aligns with your authentic self.",
            "money": "You have solid value-creation energy when your thinking, structure, and self-worth become clearer."
        }
        next_steps = {
            "love": "Focus on boundaries and get clearer about the kind of love that is truly healthy for you.",
            "career": "Notice which kind of work feels aligned rather than forced. That often points toward your true path.",
            "money": "Start creating better financial structure and open yourself to new ways of receiving income."
        }
        cautions = {
            "love": "Be careful not to stay only because you fear losing someone.",
            "career": "Be careful not to remain in an old path just because it feels familiar.",
            "money": "Be careful not to measure your worth by short-term financial fluctuations."
        }

    return {
        "strength": strengths.get(category_key, ""),
        "next_step": next_steps.get(category_key, ""),
        "caution": cautions.get(category_key, "")
    }


# -----------------------------
# Header with language switch
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
            "ยินดีต้อนรับสู่พื้นที่แห่งการตื่นรู้และเยียวยาใจ ผ่านสัญญาณจาก Oversoul และรหัสลับวันเกิด เพื่อปลดล็อกศักยภาพในตัวคุณ",
            "Welcome to a space of awakening and healing through Oversoul guidance and birth-energy decoding to help unlock your inner potential."
        )}
        </p>
        <p class='center-text soft-note' style='margin-bottom:0;'>
        {tr(
            "บางคำตอบในชีวิต อาจเริ่มต้นจากการเข้าใจพลังงานของตัวเอง",
            "Some of life’s answers may begin with understanding your own energy."
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
            "✨ รหัสลับจิตวิญญาณ... เมื่อคุณเริ่มเข้าใจพลังงานตัวเอง ประตูสู่ความเป็นไปได้ใหม่ ๆ จะเปิดออก",
            "✨ Soul codes... when you begin to understand your own energy, new doors of possibility begin to open."
        )}
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Trust section
# -----------------------------
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
            <div class="soft-note">{tr("หากรู้สึกว่าตรง คุณสามารถอ่านเชิงลึกต่อได้ทันที", "If it resonates, you can continue with a deeper personalized reading")}</div>
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

st.markdown(tr("### 🔮 ตัวอย่างสิ่งที่คุณอาจค้นพบ", "### 🔮 Examples of what you may discover"))
st.markdown(
    f"""
    <div class="mini-card">
    • {tr("ทำไมบางความสัมพันธ์ถึงเกิดซ้ำในชีวิต", "Why some relationship patterns keep repeating")}<br>
    • {tr("ทำไมช่วงนี้งานหรือการเงินถึงติดบางจุด", "Why work or money may feel blocked right now")}<br>
    • {tr("พลังหลักที่ซ่อนอยู่ในตัวคุณ", "The core energy hidden within you")}<br>
    • {tr("เส้นทางชีวิตที่กำลังเรียกให้คุณเปลี่ยนแปลง", "The life path calling you toward change")}
    </div>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# Form
# -----------------------------
month_display_list = [m["th"] if st.session_state.lang == "th" else m["en"] for m in month_options]
category_display_list = [c["th"] if st.session_state.lang == "th" else c["en"] for c in categories]

with st.form("lumina_single_page_form"):
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
        placeholder=tr(
            "แชร์รายละเอียดเรื่องที่ติดค้างในใจแบบสั้น ๆ",
            "Share a short description of what has been on your mind"
        ),
        height=120
    )

    submitted = st.form_submit_button(tr("🔮 ถอดรหัสพันธสัญญาจิตวิญญาณ", "🔮 Decode My Soul Contract"))

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
        birth_month_th = selected_month["th"]
        birth_month_en = selected_month["en"]

        selected_category = categories[category_index]
        category_key = selected_category["key"]
        category_label_th = selected_category["th"]
        category_label_en = selected_category["en"]

        day_num = int(birth_day)
        year_num = int(birth_year)

        life_number = life_path_number(day_num, month_num, year_num)
        birth_energy = birth_day_energy(day_num)

        life_meaning = life_path_meanings.get(
            life_number,
            {
                "th": "คุณมีพลังเฉพาะตัวที่น่าสนใจ และกำลังอยู่ในช่วงเรียนรู้พลังแท้ของตัวเอง",
                "en": "You carry a unique energy and may currently be in a phase of learning how to reconnect with your truest self."
            }
        )[st.session_state.lang]

        birth_meaning = birth_day_meanings.get(
            birth_energy,
            {
                "th": "วันเกิดของคุณสะท้อนพลังเฉพาะตัวที่ควรค่าแก่การทำความเข้าใจ",
                "en": "Your birth day reflects a unique energy that is worth exploring more deeply."
            }
        )[st.session_state.lang]

        main_result = generate_main_result(category_key, life_number, birth_energy, question_clean, st.session_state.lang)
        soul_message = generate_soul_message(
            name_clean,
            category_label_th if st.session_state.lang == "th" else category_label_en,
            life_number,
            birth_energy,
            month_num,
            st.session_state.lang
        )
        advice = category_advice.get(
            category_key,
            {
                "th": "หากอยากอ่านลึกเฉพาะตัว สามารถทักเข้ามาได้",
                "en": "If you would like a deeper personalized reading, feel free to reach out."
            }
        )[st.session_state.lang]

        premium = build_premium_reading(category_key, life_number, st.session_state.lang)
        strength = premium["strength"]
        next_step_text = premium["next_step"]
        caution = premium["caution"]

        birthdate_text_th = f"{day_num} {birth_month_th} {year_num}"
        birthdate_text_en = f"{day_num} {birth_month_en} {year_num}"

        try:
            requests.post(
                GOOGLE_SCRIPT_URL,
                json={
                    "name": name_clean,
                    "line_id": contact_clean,
                    "birthdate": birthdate_text_th,
                    "birthdate_en": birthdate_text_en,
                    "birth_day": day_num,
                    "birth_month": birth_month_th,
                    "birth_month_en": birth_month_en,
                    "birth_year_be": year_num,
                    "life_path_number": life_number,
                    "birth_day_energy": birth_energy,
                    "category": category_label_th,
                    "category_en": category_label_en,
                    "question": question_clean,
                    "result": main_result,
                    "life_meaning": life_meaning,
                    "birth_meaning": birth_meaning,
                    "soul_message": soul_message,
                    "advice": advice,
                    "strength": strength,
                    "next_step": next_step_text,
                    "caution": caution,
                    "language": st.session_state.lang,
                    "source": "website_form",
                    "submitted_at": str(datetime.now())
                },
                timeout=15
            )
        except Exception:
            pass

        st.balloons()
        st.write("---")
        st.success(
            tr(
                f"### 🌟 ผลสะท้อนพลังงานเบื้องต้น: คุณ {name_clean}",
                f"### 🌟 Your Initial Energy Reflection: {name_clean}"
            )
        )

        st.markdown(
            f"""
            <div class="result-card">
                <h4 style="color:#7b1fa2; margin-top:0;">{tr("🔢 เลขพลังงานของคุณ", "🔢 Your Energy Numbers")}</h4>
                <p><b>{tr("เลขเส้นทางชีวิต:", "Life Path Number:")}</b> {life_number}</p>
                <p><b>{tr("เลขพลังงานวันเกิด:", "Birth Day Energy:")}</b> {birth_energy}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="mini-card">
                <h4 style="color:#8e24aa; margin-top:0;">{tr("🌙 ความหมายพลังชีวิต", "🌙 Life Path Meaning")}</h4>
                <p>{life_meaning}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="mini-card">
                <h4 style="color:#8e24aa; margin-top:0;">{tr("💎 พลังงานจากวันเกิด", "💎 Birth Day Energy")}</h4>
                <p>{birth_meaning}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="result-card">
                <h4 style="color:#ad1457; margin-top:0;">
                    {tr("🔮 คำสะท้อนในด้าน", "🔮 Reflection for ")}
                    {category_label_th if st.session_state.lang == "th" else category_label_en}
                </h4>
                <p>{main_result}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="mini-card">
                <h4 style="color:#8e24aa; margin-top:0;">{tr("🌟 จุดเด่นพลังงานของคุณ", "🌟 Your Energy Strength")}</h4>
                <p>{strength}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="mini-card">
                <h4 style="color:#8e24aa; margin-top:0;">{tr("🪄 แนวทางที่ควรโฟกัสต่อ", "🪄 Your Next Focus")}</h4>
                <p>{next_step_text}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
            <div class="mini-card">
                <h4 style="color:#8e24aa; margin-top:0;">{tr("⚠️ สิ่งที่ควรระวัง", "⚠️ What to Be Careful With")}</h4>
                <p>{caution}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.info(f"💡 {advice}")

        st.markdown(
            f"""
            <div class="mini-card">
                <h4 style="color:#6a1b9a; margin-top:0;">{tr("✨ ข้อความจาก Lumina Soul", "✨ A Message from Lumina Soul")}</h4>
                <p>{soul_message}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
<div class="cta-note">
{tr(
"หากบางส่วนของข้อความนี้สะท้อนชีวิตคุณจริง คุณสามารถพูดคุยต่อเพื่อรับการอ่านเชิงลึกแบบเฉพาะตัวได้",
"If part of this message resonates with your life, you can continue with a deeper personalized reading"
)}
</div>
""",
            unsafe_allow_html=True
        )

        st.markdown(
            f"""
<div class="premium-btn">
    <a href="https://lin.ee/jmI4z6G" target="_blank">
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
