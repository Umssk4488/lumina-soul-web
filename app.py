
import streamlit as st
import requests
from datetime import datetime

st.set_page_config(page_title="LUMINA SOUL", page_icon="🔮", layout="centered")

if "lang" not in st.session_state:
    st.session_state.lang = "th"
if "premium_unlocked" not in st.session_state:
    st.session_state.premium_unlocked = False
if "latest_result" not in st.session_state:
    st.session_state.latest_result = {}
if "used_code" not in st.session_state:
    st.session_state.used_code = ""

def tr(th_text: str, en_text: str) -> str:
    return th_text if st.session_state.lang == "th" else en_text

query_params = st.query_params
if "lang" in query_params:
    qp_lang = str(query_params["lang"]).lower()
    if qp_lang in ["th", "en"]:
        st.session_state.lang = qp_lang

st.markdown("""
<style>
html, body, [class*="css"] { color: #2f1f38 !important; }
.stApp { background-image: linear-gradient(135deg, #fdfcfb 0%, #e7d7fb 38%, #fdfbfb 68%, #fff2ec 100%); color: #2f1f38 !important; }
p, span, div, label, li, small { color: #2f1f38 !important; }
h1, h2, h3, h4, h5, h6 { margin: 0 !important; }
div.stButton > button:first-child, div[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(to right, #ba68c8 0%, #f06292 100%) !important; color: white !important;
    border: none !important; border-radius: 25px !important; padding: 0.78rem 1.3rem !important;
    font-weight: 700 !important; font-size: 1.02rem !important; transition: 0.25s all ease !important;
    box-shadow: 0 6px 18px rgba(186, 104, 200, 0.28) !important; width: 100% !important; margin-top: 10px !important;
}
div.stButton > button:first-child:hover, div[data-testid="stFormSubmitButton"] > button:hover {
    transform: translateY(-2px); box-shadow: 0 8px 22px rgba(186, 104, 200, 0.38); color: white !important;
}
.stTextInput > div > div > input, .stNumberInput > div > div > input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div {
    border-radius: 14px !important; border: 1px solid #d9cfe6 !important; background-color: rgba(255,255,255,0.94) !important;
    color: #2f1f38 !important; -webkit-text-fill-color: #2f1f38 !important;
}
input::placeholder, textarea::placeholder { color: #8d7b9a !important; opacity: 1 !important; -webkit-text-fill-color: #8d7b9a !important; }
label, .stMarkdown, .stTextInput label, .stNumberInput label, .stSelectbox label, .stTextArea label { color: #4a3557 !important; }
div[data-baseweb="select"] * { color: #2f1f38 !important; }
.stAlert { border-radius: 14px !important; border: none !important; }
.hero-header-box { position: relative; }
.hero-title-wrap { text-align: left; margin-top: 6px; margin-bottom: 12px; }
.hero-brand { font-size: 3.0rem; font-weight: 800; line-height: 1.02; color: #3f234f !important; letter-spacing: -1px; margin-bottom: 10px; }
.hero-subtitle { font-size: 2.0rem; font-weight: 700; line-height: 1.22; color: #3f234f !important; }
.top-floating-lang { position: absolute; top: -33px; right: 0; z-index: 10; display: flex; gap: 8px; }
.lang-chip { display: inline-flex; align-items: center; justify-content: center; min-width: 38px; height: 28px; padding: 0 10px; border-radius: 999px; background: rgba(255,255,255,0.88); color: #6e4a7d !important; text-decoration: none !important; font-size: 12px; font-weight: 700; border: 1px solid rgba(186, 104, 200, 0.18); box-shadow: 0 4px 14px rgba(186, 104, 200, 0.12); backdrop-filter: blur(8px); transition: all 0.22s ease; }
.lang-chip:hover { background: rgba(255,255,255,0.98); transform: translateY(-1px); box-shadow: 0 6px 18px rgba(186, 104, 200, 0.18); }
.lang-chip.active { background: linear-gradient(to right, #ba68c8, #f06292); color: white !important; border: none; box-shadow: 0 0 12px rgba(186, 104, 200, 0.35); }
.hero-card { background: rgba(255,255,255,0.58) !important; backdrop-filter: blur(6px); padding: 20px 18px !important; border-radius: 24px !important; box-shadow: 0 8px 24px rgba(126, 87, 194, 0.10) !important; margin-top: 10px !important; margin-bottom: 16px !important; }
.glow-box { background: linear-gradient(135deg, rgba(214,228,255,0.95), rgba(234,223,255,0.95)) !important; border-radius: 18px !important; padding: 18px !important; box-shadow: 0 6px 20px rgba(126, 87, 194, 0.10) !important; margin-top: 8px !important; margin-bottom: 18px !important; }
.result-card { background: rgba(255,255,255,0.85) !important; padding: 22px !important; border-radius: 20px !important; box-shadow: 0 10px 28px rgba(126, 87, 194, 0.12) !important; margin-top: 10px !important; margin-bottom: 12px !important; color: #2f1f38 !important; }
.mini-card { background: rgba(255,255,255,0.80) !important; padding: 16px !important; border-radius: 18px !important; box-shadow: 0 4px 16px rgba(126, 87, 194, 0.10) !important; margin-bottom: 12px !important; color: #2f1f38 !important; }
.stat-card { background: rgba(255,255,255,0.78) !important; padding: 14px 12px !important; border-radius: 18px !important; text-align: center !important; box-shadow: 0 4px 14px rgba(126, 87, 194, 0.08) !important; margin-bottom: 10px !important; min-height: 120px; }
.lock-card { background: linear-gradient(135deg, rgba(255,255,255,0.84), rgba(246,235,255,0.95)) !important; padding: 20px !important; border-radius: 22px !important; box-shadow: 0 10px 28px rgba(126, 87, 194, 0.12) !important; border: 1px solid rgba(186, 104, 200, 0.18) !important; margin-top: 16px !important; margin-bottom: 16px !important; }
.center-text { text-align: center !important; color: #5a3d5c !important; }
.soft-note { color: #6b5876 !important; font-size: 0.95rem !important; }
.cta-note { text-align: center; color: #6e4a7d !important; font-size: 0.95rem; margin-top: 6px; margin-bottom: 8px; }
.premium-btn a { display: block; text-align: center; padding: 14px 18px; border-radius: 999px; font-weight: 600; font-size: 14px; background: linear-gradient(135deg, #ff4d8d, #7b61ff); color: white !important; box-shadow: 0 8px 20px rgba(123, 97, 255, 0.3); text-decoration: none; transition: all 0.25s ease; }
.premium-btn a:hover { transform: translateY(-2px) scale(1.02); box-shadow: 0 12px 28px rgba(123, 97, 255, 0.4); }
hr { border: none !important; border-top: 1px solid rgba(126, 87, 194, 0.15) !important; }
* { -webkit-text-fill-color: inherit; }
</style>
""", unsafe_allow_html=True)

GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbztgbRuGYMGMC41V8QHgNl2wnNTgJ5ZhRckVoiUXpVNTkSA-U75MFg-GRZNiCiIjrQeGg/exec"
LINE_LINK = "https://lin.ee/uDDXuWN"
MANUAL_CODES = {"SOUL111": {}, "AWAKE222": {}, "LUMINA333": {}, "OVERSOUL777": {}}

def push_to_google_sheet(payload: dict):
    try:
        requests.post(GOOGLE_SCRIPT_URL, json=payload, timeout=15)
    except Exception:
        pass

month_options = [
    {"th":"มกราคม","en":"January","num":1},{"th":"กุมภาพันธ์","en":"February","num":2},{"th":"มีนาคม","en":"March","num":3},
    {"th":"เมษายน","en":"April","num":4},{"th":"พฤษภาคม","en":"May","num":5},{"th":"มิถุนายน","en":"June","num":6},
    {"th":"กรกฎาคม","en":"July","num":7},{"th":"สิงหาคม","en":"August","num":8},{"th":"กันยายน","en":"September","num":9},
    {"th":"ตุลาคม","en":"October","num":10},{"th":"พฤศจิกายน","en":"November","num":11},{"th":"ธันวาคม","en":"December","num":12},
]
categories = [
    {"key":"love","th":"ความรักและความสัมพันธ์","en":"Love & Relationships"},
    {"key":"career","th":"การงานและเส้นทางชีวิต","en":"Career & Life Path"},
    {"key":"money","th":"โชคลาภและกระแสการเงิน","en":"Luck & Financial Flow"},
]
month_energy_meanings = {
    1: {"th":"พลังของการเริ่มต้นและความชัดเจน","en":"the energy of beginnings and clarity"},
    2: {"th":"พลังของความสัมพันธ์และความอ่อนโยน","en":"the energy of connection and gentleness"},
    3: {"th":"พลังของการสื่อสารและความคิดสร้างสรรค์","en":"the energy of communication and creativity"},
    4: {"th":"พลังของความมั่นคงและการวางรากฐาน","en":"the energy of stability and foundation-building"},
    5: {"th":"พลังของการเปลี่ยนแปลงและอิสรภาพ","en":"the energy of change and freedom"},
    6: {"th":"พลังของความรัก การดูแล และการเยียวยา","en":"the energy of love, care, and healing"},
    7: {"th":"พลังของการค้นหาความหมายภายใน","en":"the energy of inner searching and meaning"},
    8: {"th":"พลังของความสำเร็จและการสร้างสิ่งจับต้องได้","en":"the energy of grounded success and building tangible results"},
    9: {"th":"พลังของการให้ การปล่อยวาง และการเข้าใจชีวิต","en":"the energy of giving, release, and understanding life"},
    10: {"th":"พลังของจุดเปลี่ยนและการเปิดวงจรใหม่","en":"the energy of turning points and new cycles"},
    11: {"th":"พลังของญาณรู้และการตื่นรู้ภายใน","en":"the energy of intuition and inner awakening"},
    12: {"th":"พลังของการปิดวงจรเก่าเพื่อเตรียมสู่การเริ่มต้นใหม่","en":"the energy of closing old cycles to prepare for a new beginning"},
}
BIRTH_DAY_LIBRARY = {1:{"th":"วันเกิดของคุณเติมพลังความกล้าและความเป็นตัวของตัวเอง","en":"Your birth day amplifies courage and self-led energy."},
2:{"th":"วันเกิดของคุณเติมพลังความอ่อนโยนและการรับรู้อารมณ์","en":"Your birth day amplifies gentleness and emotional sensitivity."},
3:{"th":"วันเกิดของคุณเติมพลังการสื่อสาร ความคิดสร้างสรรค์ และเสน่ห์ตามธรรมชาติ","en":"Your birth day amplifies expression, creativity, and natural charm."},
4:{"th":"วันเกิดของคุณเติมพลังความมั่นคง ความรับผิดชอบ และความจริงจัง","en":"Your birth day amplifies stability, responsibility, and grounded focus."},
5:{"th":"วันเกิดของคุณเติมพลังการเปลี่ยนแปลง ความคล่องตัว และอิสรภาพ","en":"Your birth day amplifies change, adaptability, and freedom."},
6:{"th":"วันเกิดของคุณเติมพลังการดูแล การเยียวยา และความรักที่ลึก","en":"Your birth day amplifies care, healing, and deep love."},
7:{"th":"วันเกิดของคุณเติมพลังการค้นหาความหมายและโลกภายในที่ลึก","en":"Your birth day amplifies introspection and the search for deeper meaning."},
8:{"th":"วันเกิดของคุณเติมพลังความสำเร็จ อำนาจภายใน และการสร้างผลลัพธ์","en":"Your birth day amplifies achievement, inner authority, and tangible results."},
9:{"th":"วันเกิดของคุณเติมพลังเมตตา การเข้าใจมนุษย์ และการปล่อยวาง","en":"Your birth day amplifies compassion, understanding, and release."},
11:{"th":"วันเกิดของคุณเติมพลังญาณรู้และความไวต่อสัญญาณชีวิต","en":"Your birth day amplifies intuition and sensitivity to life signals."},
22:{"th":"วันเกิดของคุณเติมพลังผู้สร้างและความสามารถในการทำสิ่งใหญ่ให้เป็นจริง","en":"Your birth day amplifies builder energy and the ability to manifest larger visions."},
33:{"th":"วันเกิดของคุณเติมพลังครูผู้เยียวยาและหัวใจแห่งการรับใช้","en":"Your birth day amplifies the healing teacher archetype and heartfelt service."}}

QUESTION_SIGNALS = {
    "love": {"th": ["รัก","แฟน","คนคุย","เลิก","นอกใจ","ความสัมพันธ์","คู่","คิดถึง","กลับมา","เจ็บใจ"], "en": ["love","relationship","partner","breakup","heart","ex","romance","separation"]},
    "career": {"th": ["งาน","อาชีพ","อนาคต","เปลี่ยนงาน","เป้าหมาย","หมดไฟ","เหนื่อย","เส้นทาง","ธุรกิจ","คอนเทนต์"], "en": ["work","career","job","future","business","purpose","burnout","path","content"]},
    "money": {"th": ["เงิน","หนี้","รายได้","การเงิน","โชค","ขาย","ลูกค้า","ติดขัด","หมุนเงิน"], "en": ["money","debt","income","finance","cash","clients","sales","blocked"]},
    "emotion": {"th": ["หลงทาง","เหนื่อย","สับสน","กลัว","กังวล","เศร้า","ติดขัด","โดดเดี่ยว"], "en": ["lost","tired","confused","afraid","worry","sad","alone","stuck"]},
}

PROFILE_TEXTS = {
    1: {
        "core": ("คุณมีพลังของผู้เริ่มต้นและผู้เปิดทาง หัวใจของคุณต้องการอิสระในการเลือกเส้นทางชีวิตของตัวเอง","You carry the energy of an initiator and path opener. At your core, you need freedom to choose your own direction."),
        "shadow": ("เมื่อพลังตก คุณอาจกดดันตัวเองเกินไปและรู้สึกว่าต้องเก่งตลอดเวลา","When your energy drops, you may pressure yourself too much and feel that you must always stay strong."),
        "love": ("ในความรัก คุณต้องการความสัมพันธ์ที่เคารพตัวตน ไม่ใช่ความสัมพันธ์ที่บังคับให้คุณหายไป","In love, you need a relationship that respects your identity, not one that asks you to disappear."),
        "career": ("คุณเหมาะกับงานที่ได้ริเริ่ม ตัดสินใจ และสร้างสิ่งใหม่ด้วยวิธีของตัวเอง","You thrive in work where you can initiate, decide, and build in your own way."),
        "money": ("การเงินของคุณดีขึ้นเมื่อคุณเชื่อในคุณค่าของตัวเองและกล้าตั้งราคากับสิ่งที่ทำ","Your finances improve when you believe in your own value and dare to price what you create."),
        "wound": ("บาดแผลลึกของคุณคือความรู้สึกว่าต้องพิสูจน์ตัวเองตลอดเวลา","Your deeper wound is the feeling that you must constantly prove yourself."),
        "gift": ("ของขวัญของคุณคือพลังในการเริ่มต้นสิ่งใหม่และพาคนอื่นกล้าขยับตาม","Your gift is the power to begin something new and help others move with courage."),
        "lesson": ("บทเรียนของคุณคือการเป็นผู้นำโดยไม่ต้องเปลี่ยนทุกอย่างให้กลายเป็นการต่อสู้","Your lesson is learning to lead without turning everything into a battle."),
        "next_step": ("เริ่มจากตัดสินใจเรื่องเล็ก ๆ ให้ชัด และหยุดรอให้ทุกอย่างพร้อมก่อน","Start by making small clear decisions and stop waiting for perfect readiness."),
        "warning": ("ระวังการใช้ความสำเร็จเป็นตัววัดคุณค่าของหัวใจตัวเอง","Be careful not to use success as the only measure of your worth."),
        "healing": ("คุณไม่ได้เกิดมาเพื่อเดินตามทุกคน คุณเกิดมาเพื่อจำเสียงของตัวเองให้ได้อีกครั้ง","You were not born to follow every path around you. You were born to remember your own voice."),
    },
    2: {
        "core": ("คุณมีพลังของผู้ประสานใจ ลึกซึ้ง อ่อนโยน และรับรู้อารมณ์ได้ละเอียด","You carry harmonizer energy—sensitive, gentle, and emotionally perceptive."),
        "shadow": ("เมื่อพลังตก คุณอาจเก็บความรู้สึกตัวเองไว้เพราะกลัวความขัดแย้ง","When your energy is low, you may hide your feelings because you fear conflict."),
        "love": ("ความรักของคุณต้องการความมั่นคงทางใจและการสื่อสารที่นุ่มนวล","Your love life needs emotional safety and gentle communication."),
        "career": ("คุณเหมาะกับงานที่ใช้การเชื่อมโยง ดูแล รับฟัง หรือสร้างบรรยากาศที่คนสบายใจ","You suit work involving connection, care, listening, or creating emotional ease."),
        "money": ("การเงินดีขึ้นเมื่อคุณหยุดมองว่าความอ่อนโยนไม่มีมูลค่า","Money improves when you stop believing softness has no value."),
        "wound": ("บาดแผลของคุณคือความกลัวว่าถ้าพูดความจริงออกไป คนจะไม่พอใจหรือจากไป","Your wound is the fear that speaking your truth may upset people or make them leave."),
        "gift": ("ของขวัญของคุณคือการรับรู้ใจคนอย่างลึกและทำให้บรรยากาศกลับมาสงบ","Your gift is feeling people deeply and restoring emotional harmony."),
        "lesson": ("บทเรียนของคุณคือการอ่อนโยนกับคนอื่นโดยไม่ทอดทิ้งตัวเอง","Your lesson is to stay gentle with others without abandoning yourself."),
        "next_step": ("เริ่มจากพูดความต้องการของตัวเองทีละนิด แม้จะยังกลัวอยู่","Start expressing your needs little by little, even if fear is still there."),
        "warning": ("ระวังการเป็นคนรองรับทุกอย่างจนไม่มีใครรู้เลยว่าคุณเจ็บตรงไหน","Be careful not to hold everything for everyone until no one knows where you hurt."),
        "healing": ("ความอ่อนไหวของคุณไม่ใช่จุดอ่อน แต่มันคือภาษาละเอียดของจิตวิญญาณ","Your sensitivity is not a weakness. It is one of the subtle languages of the soul."),
    },
    3: {
        "core": ("คุณมีพลังแห่งการสื่อสาร ความคิดสร้างสรรค์ และเสน่ห์ตามธรรมชาติ","You carry the energy of expression, creativity, and natural charm."),
        "shadow": ("เมื่อพลังตก คุณอาจใช้ความสดใสกลบความจริงในใจ","When your energy drops, you may use brightness to hide what is really inside."),
        "love": ("ในความรัก คุณต้องการความสนุก การสื่อสาร และคนที่รับฟังโลกภายในของคุณ","In love, you need liveliness, communication, and someone who listens to your inner world."),
        "career": ("คุณเหมาะกับงานสื่อสาร คอนเทนต์ การพูด การสอน และการสร้างแรงบันดาลใจ","You thrive in communication, content, speaking, teaching, and inspiration-led work."),
        "money": ("การเงินดีขึ้นเมื่อคุณกล้าใช้เสียงของตัวเองและสร้างสิ่งที่มีเอกลักษณ์","Money improves when you dare to use your voice and create from your uniqueness."),
        "wound": ("บาดแผลของคุณคือความกลัวว่าถ้าคนเห็นตัวจริงแล้ว เขาอาจไม่ชอบ","Your wound is the fear that if people see the real you, they may not like it."),
        "gift": ("ของขวัญของคุณคือการทำให้สิ่งยากกลายเป็นสิ่งที่คนรู้สึกและเข้าใจได้","Your gift is making difficult things feel understandable and alive."),
        "lesson": ("บทเรียนของคุณคือการใช้เสียงเพื่อเปิดเผย ไม่ใช่เพื่อปกปิด","Your lesson is using your voice to reveal rather than hide."),
        "next_step": ("เริ่มสื่อสารสิ่งที่คุณรู้สึกจริง แม้ยังไม่สมบูรณ์","Start expressing what you truly feel, even before it feels perfect."),
        "warning": ("ระวังการทำทุกอย่างให้ดูเบาจนหัวใจลึก ๆ ไม่เคยถูกได้ยิน","Be careful not to make everything look light until your deeper heart is never heard."),
        "healing": ("เสียงของคุณไม่ได้มีไว้เพื่อทำให้คนพอใจอย่างเดียว แต่มันมีไว้เพื่อปลดล็อกบางอย่างในใจคนด้วย","Your voice is not here only to please. It is here to unlock something in people too."),
    },
    4: {
        "core": ("คุณมีพลังแห่งความมั่นคง ความรับผิดชอบ และการสร้างรากฐานที่อยู่ได้นาน","You carry the energy of stability, responsibility, and lasting foundations."),
        "shadow": ("เมื่อพลังตก คุณอาจแบกเยอะเกินไปและยึดกับวิธีเดิมจนชีวิตไม่ไหล","When your energy drops, you may over-carry and cling to old methods until life feels blocked."),
        "love": ("ในความรัก คุณต้องการความชัดเจน ความมั่นคง และความไว้ใจที่พิสูจน์ได้จริง","In love, you need clarity, stability, and trust shown through action."),
        "career": ("คุณเหมาะกับงานระบบ งานวางแผน งานจัดการ หรือสิ่งที่ต้องสร้างฐานให้มั่นคง","You suit systems, planning, management, and anything that needs a strong foundation."),
        "money": ("การเงินของคุณขึ้นกับวินัย การจัดระบบ และการตัดสินใจระยะยาว","Your finances depend on discipline, structure, and long-term choices."),
        "wound": ("บาดแผลของคุณคือความรู้สึกว่าถ้าปล่อยมือ ทุกอย่างจะพัง","Your wound is the feeling that if you loosen your grip, everything will fall apart."),
        "gift": ("ของขวัญของคุณคือการเปลี่ยนความวุ่นวายให้กลายเป็นระบบที่พึ่งพาได้","Your gift is turning chaos into structure people can rely on."),
        "lesson": ("บทเรียนของคุณคือการสร้างโดยไม่ต้องแข็งทื่อกับชีวิต","Your lesson is learning to build without becoming rigid."),
        "next_step": ("เริ่มวางระบบที่ช่วยคุณ ไม่ใช่ระบบที่กดคุณ","Start building systems that support you, not systems that trap you."),
        "warning": ("ระวังการติดกับโครงสร้างเดิมจนพลาดโอกาสใหม่ที่เหมาะกว่า","Be careful not to cling so tightly to old structures that you miss better opportunities."),
        "healing": ("คุณไม่ได้ช้า คุณกำลังสร้างสิ่งที่อยู่ได้นานกว่า","You are not slow. You are building something meant to last."),
    },
    5: {
        "core": ("คุณมีพลังแห่งอิสรภาพ การเปลี่ยนแปลง และการเรียนรู้ผ่านประสบการณ์ตรง","You carry the energy of freedom, change, and learning through direct experience."),
        "shadow": ("เมื่อพลังตก คุณอาจกระจัดกระจายหรือหนีความรู้สึกลึกด้วยการหาสิ่งใหม่ตลอดเวลา","When your energy is low, you may scatter yourself or avoid deeper feeling by constantly chasing something new."),
        "love": ("ในความรัก คุณต้องการพื้นที่ ความสดใหม่ และคนที่ไม่ทำให้คุณรู้สึกติดกับ","In love, you need space, freshness, and a partner who does not make you feel trapped."),
        "career": ("คุณเหมาะกับงานยืดหยุ่น การสื่อสาร การตลาด การเดินทาง หรือบทบาทที่เปลี่ยนแปลงได้","You suit flexible work, communication, marketing, travel, and roles that allow movement."),
        "money": ("การเงินของคุณดีขึ้นเมื่อคุณสร้างระบบที่รองรับอิสรภาพได้จริง","Your finances improve when you build systems that truly support your freedom."),
        "wound": ("บาดแผลของคุณคือความกลัวว่าถ้าหยุดนิ่งหรือถูกผูกมัด คุณจะเสียตัวเองไป","Your wound is the fear that if you stay still or become tied down, you will lose yourself."),
        "gift": ("ของขวัญของคุณคือการพาคนอื่นเห็นความเป็นไปได้ใหม่และกล้าขยับออกจากสิ่งเดิม","Your gift is helping others see new possibilities and move beyond old patterns."),
        "lesson": ("บทเรียนของคุณคือการมีอิสระโดยไม่ทำให้ชีวิตกระจัดกระจาย","Your lesson is learning to be free without scattering your life-force."),
        "next_step": ("เริ่มเลือกอิสระที่มีโครง ไม่ใช่แค่เลือกสิ่งที่ตื่นเต้น","Start choosing freedom with structure, not only what feels exciting."),
        "warning": ("ระวังการเปลี่ยนทุกอย่างเพียงเพราะรู้สึกอึดอัดชั่วคราว","Be careful not to change everything just because a temporary discomfort appears."),
        "healing": ("อิสรภาพที่แท้จริง ไม่ใช่การหนีทุกอย่าง แต่มันคือการอยู่กับตัวเองได้โดยไม่ติดกรง","True freedom is not escaping everything. It is being able to stay with yourself without living in a cage."),
    },
    6: {
        "core": ("คุณมีพลังของผู้ดูแล ผู้เยียวยา และผู้สร้างพื้นที่ปลอดภัยให้คนอื่น","You carry the energy of the nurturer, healer, and one who creates emotional safety for others."),
        "shadow": ("เมื่อพลังตก คุณอาจให้มากเกินไปหรือรู้สึกผิดง่ายเมื่อไม่ได้ช่วยทุกคน","When your energy drops, you may over-give or feel guilty when you cannot help everyone."),
        "love": ("ในความรัก คุณต้องการความอบอุ่น ความมั่นคง และความสัมพันธ์ที่ให้ความรู้สึกเหมือนบ้าน","In love, you need warmth, stability, and a bond that feels like home."),
        "career": ("คุณเหมาะกับงานดูแล ให้คำแนะนำ ความงาม สุขภาวะ หรือสิ่งที่ช่วยยกระดับชีวิตคนอื่น","You suit care work, guidance, beauty, wellbeing, and anything that helps people live better."),
        "money": ("การเงินดีขึ้นเมื่อคุณให้คุณค่ากับสิ่งที่คุณมอบ ไม่ใช่แค่ทำไปเพราะใจดี","Money improves when you value what you offer instead of giving endlessly just because you care."),
        "wound": ("บาดแผลของคุณคือความรู้สึกว่าตัวเองจะมีค่าก็ต่อเมื่อกำลังดูแลหรือช่วยใครบางคน","Your wound is the feeling that you are valuable only when you are taking care of someone."),
        "gift": ("ของขวัญของคุณคือการสร้างพื้นที่ที่คนรู้สึกอบอุ่น ปลอดภัย และกล้ากลับมาเป็นตัวเอง","Your gift is creating spaces where people feel warm, safe, and able to return to themselves."),
        "lesson": ("บทเรียนของคุณคือการดูแลคนอื่นโดยไม่ละทิ้งตัวเอง","Your lesson is to care for others without abandoning yourself."),
        "next_step": ("เริ่มตั้งขอบเขตเล็ก ๆ กับสิ่งที่ทำให้คุณเหนื่อยซ้ำ","Start setting small boundaries around what repeatedly drains you."),
        "warning": ("ระวังการให้เกินกว่าที่อีกฝ่ายร้องขอแล้วคาดหวังว่าจะถูกเห็นคุณค่าเอง","Be careful not to over-give and silently expect your worth to be recognized."),
        "healing": ("การรักคนอื่นไม่จำเป็นต้องแลกกับการทิ้งตัวเองไว้ข้างหลัง","Loving others does not require leaving yourself behind."),
    },
    7: {
        "core": ("คุณมีพลังของนักค้นหาความจริง ชีวิตของคุณไม่พอใจกับคำตอบผิวเผิน คุณเชื่อมต่อกับโลกภายในได้ลึก","You carry the energy of a truth seeker. Surface answers rarely satisfy you, and you are deeply connected to your inner world."),
        "shadow": ("เมื่อพลังตก คุณอาจถอยห่าง เก็บตัว คิดวน หรือรู้สึกว่าไม่มีใครเข้าใจสิ่งที่อยู่ข้างใน","When your energy drops, you may withdraw, overthink, or feel that no one truly understands what lives inside you."),
        "love": ("ในความรัก คุณไม่ได้ต้องการเพียงความสัมพันธ์ แต่ต้องการ connection ที่จริง ลึก และซื่อสัตย์","In love, you are not seeking just a relationship—you are seeking real, deep, and honest connection."),
        "career": ("คุณเหมาะกับงานที่ได้คิด วิเคราะห์ เขียน สอน วิจัย หรือถ่ายทอดสิ่งลึกให้คนเข้าใจง่ายขึ้น","You suit work involving analysis, writing, teaching, research, or translating depth into something others can understand."),
        "money": ("การเงินของคุณดีขึ้นเมื่อคุณหยุดแยกเรื่องจิตวิญญาณออกจากคุณค่าในโลกจริง","Your finances improve when you stop separating spirituality from real-world value."),
        "wound": ("บาดแผลของคุณคือความรู้สึกว่าไม่มีใครเข้าใจสิ่งลึก ๆ ในตัวคุณจริง","Your wound is the feeling that no one truly understands the deeper layers of you."),
        "gift": ("ของขวัญของคุณคือการมองทะลุสิ่งที่ซ่อนอยู่และตั้งคำถามกับสิ่งที่คนอื่นยอมรับแบบไม่คิด","Your gift is seeing through what is hidden and questioning what others accept without thought."),
        "lesson": ("บทเรียนของคุณคือการใช้ความลึกเพื่อเชื่อม ไม่ใช่ใช้เพื่อแยกตัวออกจากโลก","Your lesson is to use depth to connect rather than isolate yourself from the world."),
        "next_step": ("เริ่มจากปล่อยให้คนที่ใช่เข้าถึงคุณทีละชั้น และให้สิ่งที่คุณรู้ลึก ๆ ถูกแปลออกมาเป็นงานหรือคำที่ส่งต่อได้","Start by letting the right people reach you layer by layer, and let what you know deeply become shareable work or words."),
        "warning": ("ระวังการใช้ความลึกเป็นข้ออ้างในการไม่เชื่อมต่อกับชีวิตจริง","Be careful not to use depth as an excuse to disconnect from real life."),
        "healing": ("ความลึกของคุณไม่ได้ทำให้คุณยากเกินจะรัก มันแค่หมายความว่าหัวใจคุณต้องการความจริงมากกว่าคนทั่วไป","Your depth does not make you too difficult to love. It simply means your heart requires more truth than most."),
    },
    8: {
        "core": ("คุณมีพลังของการบริหาร ความสำเร็จ และการทำให้สิ่งที่มองเห็นในหัวกลายเป็นผลลัพธ์ที่จับต้องได้","You carry the energy of leadership, achievement, and turning vision into tangible results."),
        "shadow": ("เมื่อพลังตก คุณอาจกดดันตัวเองหนัก วัดคุณค่าจากความสำเร็จ หรือกลัวการล้มเหลวจนไม่กล้าผ่อน","When your energy is low, you may pressure yourself harshly, measure your worth by success, or fear failure so much that you never fully rest."),
        "love": ("ในความรัก คุณต้องการคนที่เคารพพลังและความทะเยอทะยานของคุณ","In love, you need someone who respects your power and ambition."),
        "career": ("คุณเหมาะกับงานบริหาร ธุรกิจ การเงิน การสร้างแบรนด์ หรือบทบาทที่ต้องตัดสินใจและรับผิดชอบภาพใหญ่","You suit business, management, finance, branding, and big-picture decision-making roles."),
        "money": ("การเงินของคุณตอบสนองเมื่อคุณจัดระบบและกล้ายืนในคุณค่าของตัวเอง","Money responds when you build structure and stand in your value."),
        "wound": ("บาดแผลของคุณคือการเชื่อว่าคุณจะปลอดภัยก็ต่อเมื่อทุกอย่างอยู่ภายใต้การควบคุม","Your wound is the belief that you are safe only when everything is under control."),
        "gift": ("ของขวัญของคุณคือพลังในการทำสิ่งใหญ่ให้เกิดขึ้นจริงและพาคนอื่นมองเห็นศักยภาพของตัวเอง","Your gift is the power to bring large visions into reality and help others see their potential."),
        "lesson": ("บทเรียนของคุณคือการเรียนรู้ว่าอำนาจที่แท้จริงไม่จำเป็นต้องมาพร้อมความแข็งตลอดเวลา","Your lesson is learning that true power does not require hardness at all times."),
        "next_step": ("เริ่มจัดระบบความสำเร็จให้มีพื้นที่พัก พื้นที่รัก และพื้นที่เป็นมนุษย์","Start building success with room for rest, love, and humanity."),
        "warning": ("ระวังการทำทุกอย่างให้ใหญ่จนหัวใจไม่เหลือพื้นที่หายใจ","Be careful not to make everything so large that your heart no longer has room to breathe."),
        "healing": ("ความสำเร็จที่แท้จริง ไม่ใช่การพิสูจน์ว่าคุณเก่งพอ แต่มันคือการสร้างชีวิตที่ไม่ต้องหักหลังหัวใจตัวเอง","True success is not proving you are enough. It is building a life that does not betray your own heart."),
    },
    9: {
        "core": ("คุณมีพลังของผู้ให้ เมตตา เข้าใจมนุษย์ และมีสายเชื่อมกับบทเรียนเรื่องการปล่อยวาง","You carry compassionate, humanitarian energy and are deeply linked to lessons of release and meaning."),
        "shadow": ("เมื่อพลังตก คุณอาจแบกอดีต แบกคนอื่น หรือจมกับความผิดหวังที่ยังไม่ปิดวงจร","When your energy is low, you may carry the past, carry other people, or remain entangled in disappointments that never fully closed."),
        "love": ("ในความรัก คุณต้องการความหมาย ความเข้าใจ และความสัมพันธ์ที่ไม่ตื้น","In love, you seek meaning, emotional understanding, and depth."),
        "career": ("คุณเหมาะกับงานเยียวยา สอน ช่วยเหลือ สร้างแรงบันดาลใจ หรือสิ่งที่ส่งผลต่อผู้คนในวงกว้าง","You suit healing, teaching, helping, inspiring, or work that impacts people on a larger scale."),
        "money": ("การเงินของคุณมั่นคงขึ้นเมื่อคุณเลิกคิดว่าจิตวิญญาณกับความอุดมสมบูรณ์ไปด้วยกันไม่ได้","Your finances become steadier when you stop believing spirituality and abundance cannot coexist."),
        "wound": ("บาดแผลของคุณคือการติดอยู่กับสิ่งที่หมดเวลาแล้วเพราะยังรักหรือยังรู้สึกผูกพัน","Your wound is staying attached to what has already ended because love or emotional attachment still remains."),
        "gift": ("ของขวัญของคุณคือหัวใจที่มองเห็นมนุษย์อย่างลึกและสามารถเปลี่ยนความเจ็บให้กลายเป็นความหมาย","Your gift is a heart that sees humanity deeply and can turn pain into meaning."),
        "lesson": ("บทเรียนของคุณคือการปล่อยวางโดยไม่ต้องหยุดรัก","Your lesson is learning to release without needing to stop loving."),
        "next_step": ("เริ่มปิดวงจรที่ค้างทีละเรื่อง ไม่ว่าจะเป็นคน ความหวัง หรือเรื่องในใจที่ค้างมานาน","Begin closing unfinished cycles one by one—whether they are people, hopes, or old emotional stories."),
        "warning": ("ระวังการใช้เมตตาเป็นข้ออ้างในการอยู่ต่อในสิ่งที่ทำร้ายคุณ","Be careful not to use compassion as a reason to stay in what harms you."),
        "healing": ("สิ่งที่คุณต้องปล่อย ไม่ได้แปลว่าคุณรักน้อยลง แต่มันแปลว่าคุณเริ่มรักตัวเองด้วย","What you release does not mean you love less. It means you are finally including yourself in that love."),
    },
    11: {
        "core": ("คุณมีพลังของผู้ตื่นรู้ ญาณรู้ และการรับรู้สิ่งที่ลึกกว่าระดับผิว","You carry awakened energy, heightened intuition, and the ability to sense what lies beyond the surface."),
        "shadow": ("เมื่อพลังตก คุณอาจสับสนในสิ่งที่ตัวเองรับรู้ รู้สึกเหนื่อยง่าย หรือแยกไม่ออกว่าอะไรเป็นของตัวเองอะไรเป็นของคนอื่น","When your energy drops, you may doubt what you sense, feel easily drained, or struggle to separate your energy from others."),
        "love": ("ในความรัก คุณต้องการความเชื่อมโยงระดับวิญญาณ แต่ก็ต้องการคนที่มั่นคงพอจะอยู่กับความลึกของคุณได้","In love, you seek soul-level connection, but you also need someone stable enough to meet your depth."),
        "career": ("คุณเหมาะกับงานที่ผสานจิตวิญญาณกับการสื่อสาร การสอน การเยียวยา หรือการสร้างแรงบันดาลใจ","You suit work that bridges spirituality with communication, teaching, healing, or inspiration."),
        "money": ("การเงินของคุณดีขึ้นเมื่อคุณหยุดลดทอนของขวัญตัวเอง","Your finances improve when you stop minimizing your gifts."),
        "wound": ("บาดแผลของคุณคือความรู้สึกว่าโลกนี้อาจไม่เข้าใจความไวและความลึกของคุณ","Your wound is the feeling that this world may not understand your sensitivity and depth."),
        "gift": ("ของขวัญของคุณคือการเห็นสัญญาณ เชื่อมสิ่งที่มองไม่เห็น และแปลมันออกมาให้ผู้คนเข้าใจได้","Your gift is perceiving signals, bridging the unseen, and translating it into something others can understand."),
        "lesson": ("บทเรียนของคุณคือการทำให้สิ่งที่ลึกและละเอียดมีรากอยู่ในชีวิตจริง","Your lesson is grounding the subtle and profound into real life."),
        "next_step": ("เริ่มเชื่อสิ่งที่คุณรับรู้มากขึ้น แต่ให้มันมีพื้นที่ลงมือจริงควบคู่ไปด้วย","Start trusting what you sense more, but give it real-world channels of expression."),
        "warning": ("ระวังการเปิดรับทุกอย่างจนตัวเองพร่าและหมดแรง","Be careful not to open yourself to everything until your energy becomes blurred and depleted."),
        "healing": ("คุณไม่ได้แปลกเกินไป คุณแค่รับแสงได้มากเกินกว่าที่โลกทั่วไปสอนให้เข้าใจ","You are not too strange. You simply receive more light than the ordinary world knows how to explain."),
    },
    22: {
        "core": ("คุณมีพลังของผู้สร้างสิ่งใหญ่ให้เป็นจริง เห็นภาพกว้างและมีศักยภาพสร้างผลกระทบที่ยาวไกล","You carry the energy of the master builder—seeing a bigger vision and creating long-range impact."),
        "shadow": ("เมื่อพลังตก คุณอาจรู้สึกหนักกับภาระ หรือกลัวความรับผิดชอบในศักยภาพตัวเอง","When your energy drops, you may feel overwhelmed by responsibility or afraid of your own potential."),
        "love": ("ในความรัก คุณต้องการคนที่เดินเติบโตไปด้วยกัน ไม่ใช่ดึงคุณออกจากภารกิจชีวิต","In love, you need someone who grows with you rather than pulling you away from your mission."),
        "career": ("คุณเหมาะกับการสร้างธุรกิจ ระบบ แพลตฟอร์ม หรือสิ่งที่ส่งผลต่อผู้คนจำนวนมาก","You suit building businesses, systems, platforms, or anything that serves many people."),
        "money": ("การเงินของคุณมีศักยภาพสูงมากเมื่อคุณทำสิ่งที่ใหญ่พอจะรับพลังคุณได้","Your financial potential is high when you do work big enough to hold your energy."),
        "wound": ("บาดแผลของคุณคือความรู้สึกว่าภารกิจในใจมันใหญ่เกินไปสำหรับชีวิตจริง","Your wound is the feeling that the mission inside you is too large for ordinary life to hold."),
        "gift": ("ของขวัญของคุณคือการเห็นทั้งภาพใหญ่และภาพลงมือจริงในเวลาเดียวกัน","Your gift is seeing both the larger vision and the practical steps at the same time."),
        "lesson": ("บทเรียนของคุณคือการสร้างใหญ่โดยไม่แบกทุกอย่างคนเดียว","Your lesson is to build big without carrying everything alone."),
        "next_step": ("เริ่มแบ่งวิสัยทัศน์ใหญ่ออกเป็นก้าวที่ทำจริงได้ทีละส่วน","Start breaking the larger vision into practical steps that can really be built."),
        "warning": ("ระวังการผลักตัวเองด้วยมาตรฐานที่หนักจนหมดแรงก่อนสิ่งใหญ่จะเป็นรูปเป็นร่าง","Be careful not to drive yourself so hard that you burn out before the vision takes shape."),
        "healing": ("อย่ากลัวศักยภาพของตัวเอง เพราะสิ่งที่ดูใหญ่ในใจคุณ อาจเป็นเหตุผลที่คุณมาเกิด","Do not fear your own potential. What feels huge inside you may be one of the reasons you came here."),
    },
    33: {
        "core": ("คุณมีพลังของครูผู้เยียวยา เมตตา ลึก ซื่อสัตย์กับหัวใจ และมีแรงผลักดันที่จะส่งบางอย่างที่ช่วยผู้คนได้จริง","You carry the energy of the healing teacher—compassionate, deep, and moved to offer something genuinely helpful."),
        "shadow": ("เมื่อพลังตก คุณอาจแบกความทุกข์คนอื่นมากไป คาดหวังกับตัวเองสูง และลืมว่าแม้ผู้เยียวยาก็ต้องได้รับการเยียวยา","When your energy drops, you may carry too much of others' pain and forget that healers need healing too."),
        "love": ("ในความรัก คุณต้องการความสัมพันธ์ที่อบอุ่น ลึก และช่วยให้ทั้งสองคนเติบโต","In love, you seek warmth, emotional depth, and a bond that helps both people grow."),
        "career": ("คุณเหมาะกับงานสอน เยียวยา โค้ช สื่อสารจากหัวใจ หรือการทำงานที่เปลี่ยนชีวิตคนจริง","You suit teaching, healing, coaching, heart-led communication, or work that genuinely transforms lives."),
        "money": ("การเงินของคุณไม่ควรถูกตัดออกจากภารกิจ คุณสามารถได้รับอย่างงดงามจากสิ่งที่ช่วยผู้คน","Your finances do not need to be separated from your mission. You can receive beautifully through work that helps people."),
        "wound": ("บาดแผลของคุณคือความรู้สึกว่าตัวเองต้องแบกรับหรือเยียวยาทุกอย่างให้คนอื่นถึงจะมีคุณค่า","Your wound is the feeling that you must carry or heal everything for others in order to have value."),
        "gift": ("ของขวัญของคุณคือการเปลี่ยนความเจ็บให้กลายเป็นปัญญาและส่งต่อแสงด้วยหัวใจจริง","Your gift is turning pain into wisdom and transmitting light through a sincere heart."),
        "lesson": ("บทเรียนของคุณคือการรับใช้โดยไม่ใช้ชีวิตตัวเองเป็นเครื่องเผาไหม้","Your lesson is learning to serve without using your own life-force as fuel."),
        "next_step": ("เริ่มแยกให้ออกว่าอะไรคือการให้ด้วยหัวใจ และอะไรคือการให้เพราะกลัวจะไม่มีคุณค่า","Begin noticing the difference between giving from the heart and giving from fear of losing worth."),
        "warning": ("ระวังการช่วยคนจนหลุดจากแกนตัวเอง","Be careful not to help others so much that you lose your own center."),
        "healing": ("การเป็นแสงให้คนอื่น ไม่จำเป็นต้องแผดเผาตัวเองจนหมดแรง","Being a light for others does not require burning yourself out."),
    },
}

def get_profile(life_number: int):
    return PROFILE_TEXTS.get(life_number, PROFILE_TEXTS[7])

def detect_question_signal(question_text: str):
    text = (question_text or "").lower().strip()
    scores = {"love": 0, "career": 0, "money": 0, "emotion": 0}
    for signal_key, lang_map in QUESTION_SIGNALS.items():
        for kw in lang_map["th"] + lang_map["en"]:
            if kw.lower() in text:
                scores[signal_key] += 1
    max_score = max(scores.values())
    return max(scores, key=scores.get) if max_score > 0 else None

def get_text(profile, key, lang):
    th, en = profile[key]
    return th if lang == "th" else en

def life_intro(life_number: int, birth_energy: int, month_num: int, lang: str):
    profile = get_profile(life_number)
    core_text = get_text(profile, "core", lang)
    birth_text = BIRTH_DAY_LIBRARY.get(birth_energy, BIRTH_DAY_LIBRARY[7])[lang]
    month_text = month_energy_meanings.get(month_num, month_energy_meanings[7])[lang]
    if lang == "th":
        return f"{core_text} {birth_text} และพลังเดือนเกิดของคุณยังสะท้อนถึง{month_text} จึงทำให้เส้นทางชีวิตของคุณมีทั้งความลึก ความหมาย และบทเรียนที่เชื่อมกับการเติบโตภายใน"
    return f"{core_text} {birth_text} Your birth month also reflects {month_text}, which adds inner depth, meaning, and soul-level growth to your life path."

def category_reflection(category_key: str, life_number: int, lang: str):
    profile = get_profile(life_number)
    if category_key == "love":
        return get_text(profile, "love", lang)
    if category_key == "career":
        return get_text(profile, "career", lang)
    return get_text(profile, "money", lang)

def current_focus_block(category_key: str, question_signal: str, life_number: int, lang: str):
    if lang == "th":
        base_map = {
            "love": "ช่วงนี้หัวใจของคุณกำลังสอนให้แยกความรักออกจากความกลัวที่จะสูญเสีย",
            "career": "ช่วงนี้ชีวิตกำลังกดให้คุณมองเส้นทางงานใหม่อย่างจริงจังมากขึ้น",
            "money": "ช่วงนี้กระแสการเงินกำลังชี้ให้คุณเห็นความสัมพันธ์ระหว่างคุณค่าตัวเองกับการรับความอุดมสมบูรณ์",
        }
        signal_map = {
            "emotion": "และจากสิ่งที่คุณพิมพ์เข้ามา ข้างในคุณกำลังต้องการความชัดเจน ความเบาใจ และการกลับมายืนอยู่กับตัวเองอีกครั้ง",
            "love": "คำถามของคุณยังสะท้อนว่าความสัมพันธ์นี้แตะบางแผลลึกที่กำลังรอการเข้าใจอย่างแท้จริง",
            "career": "คำถามของคุณสะท้อนว่าชีวิตกำลังบอกให้คุณหยุดฝืนกับเส้นทางที่ไม่สอดคล้องแล้ว",
            "money": "คำถามของคุณสะท้อนว่าประเด็นเรื่องเงินตอนนี้ไม่ได้มีแค่เรื่องตัวเลข แต่เชื่อมกับความมั่นคงทางใจและความรู้สึกมีคุณค่า",
        }
    else:
        base_map = {
            "love": "At this stage, your heart is learning to separate love from the fear of losing.",
            "career": "Right now, life is pushing you to look at your work path more honestly and more seriously.",
            "money": "At this stage, your financial flow is revealing the connection between self-worth and receiving abundance.",
        }
        signal_map = {
            "emotion": "From what you wrote, there is a clear need for inner clarity, emotional relief, and a return to your own center.",
            "love": "Your question also suggests that this relationship is touching a deeper wound waiting to be understood.",
            "career": "Your question reflects a moment where life is asking you to stop forcing a path that no longer aligns.",
            "money": "Your question suggests that money right now is not only about numbers, but also about emotional safety and worth.",
        }
    text = base_map.get(category_key, base_map["career"])
    if question_signal in signal_map:
        text += " " + signal_map[question_signal]
    if life_number in (7, 11, 33):
        text += " " + ("นี่ไม่ใช่สัญญาณว่าคุณพัง แต่คือสัญญาณว่าคุณกำลังตื่นลึกขึ้น" if lang == "th" else "This is not a sign that you are broken. It may be a sign that you are awakening more deeply.")
    return text

def generate_free_reflection(name, category_key, day_num, month_num, year_num, question_text, lang):
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
    }

def generate_premium_reflection(name, day_num, month_num, year_num, lang):
    life_num = life_path_number(day_num, month_num, year_num)
    birth_energy = birth_day_energy(day_num)
    profile = get_profile(life_num)
    if lang == "th":
        premium_title = f"✨ พิมพ์เขียวพลังงานเชิงลึกของคุณ {name}"
        soul_text = f"{name} คุณไม่ได้มาถึงจุดนี้โดยบังเอิญ เลขเส้นทางชีวิต {life_num} ของคุณสะท้อนว่าชีวิตกำลังสอนให้คุณกลับมาใช้พลังแท้ของตัวเองอย่างมีสติ ขณะเดียวกันเลขวันเกิด {birth_energy} ก็เติมโทนเฉพาะตัวให้คุณมีวิธีแสดงพลังชีวิตออกมาในแบบของตัวเอง"
        unlock_note = "หากข้อความนี้สะท้อนชีวิตคุณจริง คุณสามารถใช้ผลลัพธ์นี้เป็นสะพานต่อไปยัง eBook หรือการอ่านส่วนตัวเชิงลึกได้"
    else:
        premium_title = f"✨ Your Deep Energy Blueprint: {name}"
        soul_text = f"{name}, you did not arrive at this point by accident. Your Life Path {life_num} suggests that life is asking you to return to your real power with greater awareness. Your Birth Day Energy {birth_energy} adds its own signature to how that power wants to be expressed."
        unlock_note = "If this resonates deeply, you can use this result as a bridge into your eBook or a deeper personal reading."
    return {
        "premium_title": premium_title,
        "soul_text": soul_text,
        "shadow": get_text(profile, "shadow", lang),
        "wound": get_text(profile, "wound", lang),
        "gift": get_text(profile, "gift", lang),
        "lesson": get_text(profile, "lesson", lang),
        "next_step": get_text(profile, "next_step", lang),
        "warning": get_text(profile, "warning", lang),
        "healing": get_text(profile, "healing", lang),
        "unlock_note": unlock_note,
    }

st.markdown(f"""
<div class="hero-header-box">
<div class="top-floating-lang">
<a href="?lang=th" class="lang-chip {'active' if st.session_state.lang == 'th' else ''}">TH</a>
<a href="?lang=en" class="lang-chip {'active' if st.session_state.lang == 'en' else ''}">EN</a>
</div>
<div class="hero-title-wrap" style="margin-bottom:0;">
<div class="hero-brand" style="margin-bottom:0;">🔮 LUMINA SOUL</div>
</div>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""<div class="hero-subtitle" style="margin-top:8px; margin-bottom:8px;">{tr("พื้นที่สะท้อนชีวิต | ถอดรหัสลับพลังงานวันเกิด", "A space for reflection | Decode your birth energy")}</div>""", unsafe_allow_html=True)
st.write("---")
st.markdown(f"""
<div class="hero-card">
<p class='center-text' style='font-size:1.05rem; margin-bottom:8px;'>{tr("ยินดีต้อนรับสู่พื้นที่แห่งการตื่นรู้และเยียวยาใจ ผ่านสัญญาณจากชีวิตและรหัสลับวันเกิด เพื่อช่วยให้คุณเข้าใจตัวเองลึกขึ้น", "Welcome to a space of awakening and healing through life signals and birth-energy decoding—created to help you understand yourself more deeply.")}</p>
<p class='center-text soft-note' style='margin-bottom:0;'>{tr("นี่ไม่ใช่คำทำนายอนาคต แต่คือการสะท้อนพลังงานชีวิตในช่วงเวลานี้", "This is not fortune telling. It is an energetic reflection of your life in this moment.")}</p>
</div>
""", unsafe_allow_html=True)

st.markdown(f"""<div class="glow-box"><p style="margin:0; color:#3576c5 !important; font-weight:600;">{tr("✨ บางคำตอบในชีวิต อาจเริ่มต้นจากการเข้าใจพลังงานของตัวเอง", "✨ Some of life’s answers may begin with understanding your own energy")}</p></div>""", unsafe_allow_html=True)

month_display_list = [m["th"] if st.session_state.lang == "th" else m["en"] for m in month_options]
category_display_list = [c["th"] if st.session_state.lang == "th" else c["en"] for c in categories]

with st.form("lumina_form_phase2"):
    name = st.text_input(tr("ชื่อ-นามสกุล", "Full Name"))
    contact = st.text_input(tr("ID Line (เพื่อรับผลสะท้อนพลังงานและสิทธิ์อ่านเชิงลึก)", "Line ID (to receive your reflection and deeper reading access)"))
    col1, col2, col3 = st.columns(3)
    with col1:
        birth_day = st.number_input(tr("วันที่เกิด", "Birth Day"), min_value=1, max_value=31, value=1, step=1)
    with col2:
        birth_month_index = st.selectbox(tr("เดือนเกิด", "Birth Month"), range(len(month_options)), format_func=lambda i: month_display_list[i])
    with col3:
        birth_year = st.number_input(tr("ปี พ.ศ. เกิด", "Birth Year (B.E.)"), min_value=2450, max_value=2600, value=2535, step=1)

    category_index = st.selectbox(tr("ด้านที่คุณต้องการรับพลังงานนำทางในวันนี้:", "Which area would you like energetic guidance for today?"), range(len(categories)), format_func=lambda i: category_display_list[i])
    st.markdown(f"**{tr('⭐️ เรื่องที่คุณกังวลใจที่สุดในตอนนี้คืออะไร?', '⭐️ What is your biggest concern right now?')}**")
    question = st.text_area("", placeholder=tr("แชร์รายละเอียดเรื่องที่ติดค้างในใจแบบสั้น ๆ", "Share a short description of what has been on your mind"), height=120)
    submitted = st.form_submit_button(tr("🔮 ถอดรหัสพลังงานของฉัน", "🔮 Decode My Energy"))

if submitted:
    name_clean, contact_clean, question_clean = name.strip(), contact.strip(), question.strip()
    if len(name_clean) < 2:
        st.error(tr("กรุณากรอกชื่อ-นามสกุลให้ครบถ้วน", "Please enter your full name."))
    elif len(contact_clean) < 3:
        st.error(tr("กรุณากรอก ID Line ให้ถูกต้อง", "Please enter a valid Line ID."))
    elif len(question_clean) < 5:
        st.error(tr("กรุณาพิมพ์เรื่องที่กังวลใจสั้น ๆ เพื่อให้คำสะท้อนเหมาะกับคุณมากขึ้น", "Please share a short concern so your reflection can feel more personalized."))
    else:
        selected_month = month_options[birth_month_index]
        selected_category = categories[category_index]
        free_result = generate_free_reflection(name_clean, selected_category["key"], int(birth_day), selected_month["num"], int(birth_year), question_clean, st.session_state.lang)
        premium_result = generate_premium_reflection(name_clean, int(birth_day), selected_month["num"], int(birth_year), st.session_state.lang)
        st.session_state.latest_result = {
            "name": name_clean, "contact": contact_clean, "question": question_clean,
            "category_key": selected_category["key"], "category_label_th": selected_category["th"], "category_label_en": selected_category["en"],
            "birth_day": int(birth_day), "birth_month_num": selected_month["num"], "birth_month_th": selected_month["th"], "birth_month_en": selected_month["en"],
            "birth_year": int(birth_year), "free": free_result, "premium": premium_result,
        }
        push_to_google_sheet({
            "name": name_clean, "line_id": contact_clean, "birth_day": int(birth_day), "birth_month": selected_month["th"], "birth_month_en": selected_month["en"],
            "birth_year_be": int(birth_year), "life_path_number": free_result["life_number"], "birth_day_energy": free_result["birth_energy"],
            "category": selected_category["th"], "category_en": selected_category["en"], "question": question_clean,
            "free_intro": free_result["intro"], "free_category_text": free_result["category_text"], "free_focus_text": free_result["focus_text"],
            "premium_shadow": premium_result["shadow"], "premium_wound": premium_result["wound"], "premium_gift": premium_result["gift"],
            "premium_lesson": premium_result["lesson"], "premium_next_step": premium_result["next_step"], "premium_warning": premium_result["warning"],
            "premium_soul_text": premium_result["soul_text"], "premium_healing": premium_result["healing"], "language": st.session_state.lang,
            "source": "website_form_phase2", "submitted_at": str(datetime.now()),
        })
        st.session_state.premium_unlocked = False
        st.session_state.used_code = ""
        st.balloons()

if st.session_state.latest_result:
    data = st.session_state.latest_result
    free_result = data["free"]
    premium_result = data["premium"]
    st.write("---")
    st.success(free_result["title"])
    st.markdown(f"""<div class="result-card"><h4 style="color:#7b1fa2; margin-top:0;">{tr("🔢 เลขพลังงานของคุณ", "🔢 Your Energy Numbers")}</h4><p><b>{tr("เลขเส้นทางชีวิต:", "Life Path Number:")}</b> {free_result["life_number"]}</p><p><b>{tr("เลขพลังงานวันเกิด:", "Birth Day Energy:")}</b> {free_result["birth_energy"]}</p></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="mini-card"><h4 style="color:#8e24aa; margin-top:0;">{tr("🌙 พลังแกนกลางของคุณ", "🌙 Your Core Energy")}</h4><p>{free_result["intro"]}</p></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="result-card"><h4 style="color:#ad1457; margin-top:0;">{tr("🔮 คำสะท้อนในด้านที่คุณเลือก", "🔮 Reflection for your chosen area")}</h4><p>{free_result["category_text"]}</p></div>""", unsafe_allow_html=True)
    st.markdown(f"""<div class="mini-card"><h4 style="color:#8e24aa; margin-top:0;">{tr("🪄 สิ่งที่ชีวิตกำลังบอกคุณตอนนี้", "🪄 What life may be showing you right now")}</h4><p>{free_result["focus_text"]}</p></div>""", unsafe_allow_html=True)

    if not st.session_state.premium_unlocked:
        lock_text_th = "สิ่งที่คุณเพิ่งอ่าน…เป็นเพียงชั้นแรกของพลังงานชีวิตคุณ ลึกลงไปกว่านั้น ยังมีความจริงบางอย่างที่รอการถูกเปิดเผย"
        lock_text_en = "What you have just read is only the first layer of your life energy. Deeper than this, there is a truth still waiting to be revealed."
        st.markdown(f"""<div class="lock-card"><h4 style="color:#8e24aa; margin-top:0;">🔒 {tr("คำอ่านฉบับลึกยังไม่ถูกเปิด", "Your deeper reading is still locked")}</h4><p>{tr(lock_text_th, lock_text_en)}</p><p>{tr("หากคุณได้รับ Soul Code จาก eBook หรือ LINE แล้ว สามารถใส่รหัสด้านล่างเพื่อปลดล็อคคำอ่านฉบับเต็มได้ทันที", "If you already received a Soul Code from your eBook or LINE, enter it below to unlock your full reading.")}</p></div>""", unsafe_allow_html=True)
        code_input = st.text_input(tr("✨ ใส่ Soul Code ของคุณ", "✨ Enter your Soul Code"))
        if st.button(tr("🔓 ปลดล็อคคำอ่านฉบับเต็ม", "🔓 Unlock Full Reading")):
            if verify_code(code_input):
                st.session_state.premium_unlocked = True
                st.session_state.used_code = code_input.strip().upper()
                st.rerun()
            else:
                st.error(tr("รหัสไม่ถูกต้อง หรือยังไม่ได้เปิดสิทธิ์ กรุณาตรวจสอบอีกครั้ง หรือทัก LINE เพื่อรับรหัส", "The code is invalid or has not been activated yet. Please check again or contact LINE to receive your code."))
        st.markdown(f"""<div class="premium-btn"><a href="{LINE_LINK}" target="_blank">✳️👉 {tr("รับ Soul Code ผ่าน LINE", "Get your Soul Code via LINE")}</a></div>""", unsafe_allow_html=True)

    if st.session_state.premium_unlocked:
        st.markdown(f"""<div class="result-card"><h4 style="color:#7b1fa2; margin-top:0;">{premium_result["premium_title"]}</h4><p>{premium_result["soul_text"]}</p></div>""", unsafe_allow_html=True)
        sections = [
            (tr("🌑 เงาพลังงานและบทเรียนลึก", "🌑 Shadow Pattern & Deeper Lesson"), premium_result["shadow"]),
            (tr("🩹 บาดแผลที่ชีวิตกำลังชี้ให้เห็น", "🩹 The Wound Life May Be Revealing"), premium_result["wound"]),
            (tr("💎 ของขวัญที่ซ่อนอยู่ในตัวคุณ", "💎 The Gift Hidden Within You"), premium_result["gift"]),
            (tr("📖 บทเรียนที่ชีวิตกำลังสอน", "📖 The Lesson Life Is Teaching You"), premium_result["lesson"]),
            (tr("🪄 แนวทางที่ควรโฟกัสต่อ", "🪄 Your Next Focus"), premium_result["next_step"]),
            (tr("⚠️ สิ่งที่ควรระวัง", "⚠️ What to Be Careful With"), premium_result["warning"]),
            (tr("✨ ข้อความจาก Lumina Soul", "✨ A Message from Lumina Soul"), premium_result["healing"]),
        ]
        for title, content in sections:
            st.markdown(f"""<div class="mini-card"><h4 style="color:#8e24aa; margin-top:0;">{title}</h4><p>{content}</p></div>""", unsafe_allow_html=True)
        st.info("💡 " + premium_result["unlock_note"])
        st.markdown(f"""<div class="cta-note">{tr("หากคำอ่านนี้สะท้อนชีวิตคุณจริง ขั้นต่อไปคือ eBook หรือการอ่านเชิงลึกส่วนตัว เพื่อเชื่อมสิ่งที่คุณรู้สึกเข้ากับเส้นทางชีวิตจริง", "If this reading deeply resonates, your next step is the eBook or a personalized deep reading to connect what you feel with your real life path.")}</div>""", unsafe_allow_html=True)
        st.markdown(f"""<div class="premium-btn"><a href="{LINE_LINK}" target="_blank">✳️👉 {tr("คุยกับที่ปรึกษา LUMINA SOUL", "Talk to a LUMINA SOUL guide")}</a></div>""", unsafe_allow_html=True)

st.write("---")
st.markdown(f"<p style='text-align: center; font-size: 0.82rem; color: #888;'>© 2026 LUMINA SOUL | {tr('พื้นที่สะท้อนชีวิตและการตื่นรู้', 'A space for reflection and awakening')}</p>", unsafe_allow_html=True)
