import streamlit as st
import requests
import time
from pathlib import Path

# =========================================================
# LUMINA SOUL — FINAL ONE-FILE APP
# Based on user's original Streamlit structure and pastel brand
# Adds:
# - Stronger landing headline
# - Feature cards before form
# - Loading experience
# - Free short reading result
# - Premium unlock preview + CTA
# - eBook sales section with cover image
# - Keeps LINE / Apps Script hooks ready
# =========================================================

st.set_page_config(page_title="LUMINA SOUL", page_icon="🔮", layout="centered")

# -----------------------------
# External endpoints / links
# -----------------------------
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbztgbRuGYMGMC41V8QHgNl2wnNTgJ5ZhRckVoiUXpVNTkSA-U75MFg-GRZNiCiIjrQeGg/exec"
LINE_LINK = "https://lin.ee/uDDXuWN"
LINE_ID = "@908bgzai"

# -----------------------------
# Session state
# -----------------------------
if "show_result" not in st.session_state:
    st.session_state.show_result = False
if "latest_result" not in st.session_state:
    st.session_state.latest_result = {}
if "active_tab" not in st.session_state:
    st.session_state.active_tab = "energy"
if "lang" not in st.session_state:
    st.session_state.lang = "th"

# -----------------------------
# Helpers
# -----------------------------
def tr(th: str, en: str) -> str:
    return th if st.session_state.lang == "th" else en


def safe_post(url: str, payload: dict):
    try:
        requests.post(url, json=payload, timeout=15)
    except Exception:
        pass


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


def zodiac_sign(day: int, month_num: int):
    signs = [
        ((1, 20), "มังกร", "Capricorn", "♑"),
        ((2, 19), "กุมภ์", "Aquarius", "♒"),
        ((3, 21), "มีน", "Pisces", "♓"),
        ((4, 20), "เมษ", "Aries", "♈"),
        ((5, 21), "พฤษภ", "Taurus", "♉"),
        ((6, 21), "เมถุน", "Gemini", "♊"),
        ((7, 23), "กรกฎ", "Cancer", "♋"),
        ((8, 23), "สิงห์", "Leo", "♌"),
        ((9, 23), "กันย์", "Virgo", "♍"),
        ((10, 23), "ตุล", "Libra", "♎"),
        ((11, 22), "พิจิก", "Scorpio", "♏"),
        ((12, 22), "ธนู", "Sagittarius", "♐"),
        ((12, 32), "มังกร", "Capricorn", "♑"),
    ]
    for (m, cutoff), th, en, sym in signs:
        if month_num < m:
            prev = signs[signs.index(((m, cutoff), th, en, sym)) - 1]
            return prev[1], prev[2], prev[3]
        if month_num == m:
            if day < cutoff:
                prev = signs[signs.index(((m, cutoff), th, en, sym)) - 1]
                return prev[1], prev[2], prev[3]
            return th, en, sym
    return "มังกร", "Capricorn", "♑"


CHINESE_ANIMALS = [
    "ลิง", "ไก่", "หมา", "หมู", "หนู", "วัว",
    "เสือ", "กระต่าย", "มังกร", "งู", "ม้า", "แพะ"
]


def chinese_zodiac(year_be: int):
    gregorian = year_be - 543
    return CHINESE_ANIMALS[gregorian % 12]


MONTHS = [
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


LIFE_PATH_LABELS = {
    1: ("ผู้บุกเบิก", "Pioneer"),
    2: ("ผู้ประสานใจ", "Peacemaker"),
    3: ("นักสร้างสรรค์", "Creator"),
    4: ("ผู้วางรากฐาน", "Builder"),
    5: ("นักเปลี่ยนแปลง", "Explorer"),
    6: ("ผู้เยียวยา", "Healer"),
    7: ("นักค้นหาความจริง", "Seeker"),
    8: ("ผู้สร้างความสำเร็จ", "Power Builder"),
    9: ("ผู้รับใช้มนุษยชาติ", "Humanitarian"),
    11: ("ผู้ส่องสว่าง", "Illuminator"),
    22: ("สถาปนิกวิสัยทัศน์", "Master Builder"),
    33: ("ครูแห่งหัวใจ", "Master Teacher"),
}

ENERGY_SUMMARIES = {
    1: "คุณมีพลังของการเริ่มต้น กล้าตัดสินใจ และไม่เหมาะกับชีวิตที่ต้องถูกกำหนดโดยคนอื่นตลอดเวลา",
    2: "คุณมีพลังของความอ่อนโยน รับรู้อารมณ์คนเก่ง และมักเป็นคนที่แอบแบกความรู้สึกไว้เงียบ ๆ",
    3: "คุณมีพลังของการสื่อสาร เสน่ห์ และความคิดสร้างสรรค์ แต่บางครั้งสิ่งที่อยู่ข้างในลึกกว่าที่คนเห็นมาก",
    4: "คุณมีพลังของความมั่นคง ความรับผิดชอบ และการสร้างฐานชีวิต แต่ก็มักแบกมากเกินไป",
    5: "คุณมีพลังของอิสรภาพ การเปลี่ยนแปลง และความกล้าลองสิ่งใหม่ แต่ไม่เหมาะกับชีวิตที่อึดอัดเกินไป",
    6: "คุณมีพลังของการดูแล ความรัก และการเยียวยา แต่ต้องระวังการให้คนอื่นจนลืมตัวเอง",
    7: "คุณมีพลังของความลึก การค้นหาความหมาย และโลกภายในที่ซับซ้อนกว่าที่คนรอบตัวเข้าใจ",
    8: "คุณมีพลังของความสำเร็จ การสร้างผลลัพธ์ และการรับผิดชอบภาพใหญ่ของชีวิต",
    9: "คุณมีพลังของหัวใจที่ลึก เมตตา และมักรักหรือผูกพันกับสิ่งที่สำคัญต่อใจอย่างจริงจัง",
    11: "คุณมีพลังของญาณรู้ ความไวต่อพลังงาน และการรับสัญญาณชีวิตได้เร็วกว่าคนทั่วไป",
    22: "คุณมีพลังของการสร้างสิ่งใหญ่ให้เกิดขึ้นจริง และมักมีบางอย่างในใจที่ใหญ่กว่าชีวิตธรรมดา",
    33: "คุณมีพลังของครูผู้เยียวยา หัวใจรับใช้ และการเปลี่ยนความเจ็บให้กลายเป็นประโยชน์ต่อผู้อื่น",
}

HIDDEN_SIDE = {
    1: "ลึก ๆ คุณไม่อยากแค่เก่ง แต่คุณอยากมีชีวิตที่ไม่ต้องฝืนตัวเอง",
    2: "ด้านในที่คนไม่ค่อยรู้คือคุณเองก็เหนื่อย และอยากถูกดูแลบ้างเหมือนกัน",
    3: "หลายครั้งคุณยิ้มง่ายหรือดูสว่าง แต่ความจริงในใจลึกกว่านั้นมาก",
    4: "สิ่งที่คนไม่ค่อยเห็นคือคุณมักกดดันตัวเองให้รับผิดชอบทุกอย่างอยู่เงียบ ๆ",
    5: "คุณดูเหมือนรับมือได้ แต่จริง ๆ คุณไวต่อความอึดอัดและเหนื่อยกับสิ่งเดิมง่ายมาก",
    6: "คุณอาจดูเหมือนคนพร้อมให้เสมอ แต่หัวใจคุณก็มีจุดที่ล้าจากการเป็นที่พึ่งให้ทุกคน",
    7: "คนส่วนใหญ่อาจไม่รู้ว่าคุณคิดลึกกว่าที่พูด และรู้สึกมากกว่าที่แสดงออก",
    8: "ภายนอกคุณอาจดูเอาอยู่ แต่ข้างในมีแรงกดดันที่ไม่ค่อยมีใครรู้",
    9: "คุณอาจดูเข้มแข็ง แต่หัวใจคุณจำสิ่งที่สำคัญได้ยาวนานกว่าที่คนอื่นคิด",
    11: "คุณอาจอธิบายตัวเองไม่หมด แต่หลายสิ่งในใจคุณรับรู้ได้ก่อนเหตุผลเสมอ",
    22: "หลายครั้งคุณรู้สึกว่าตัวเองควรทำบางอย่างที่ใหญ่กว่านี้ แต่ก็แบกความคาดหวังไว้เงียบ ๆ",
    33: "คุณอาจช่วยคนอื่นเก่งมาก แต่สิ่งที่คนไม่ค่อยรู้คือคุณก็ต้องการการปลอบโยนเหมือนกัน",
}

SIGNAL_HINTS = {
    1: "สัญญาณของคุณคือการถูกผลักให้ออกมาเลือกทางของตัวเองให้ชัดขึ้น",
    2: "สัญญาณของคุณคือการเรียนรู้ที่จะฟังใจตัวเองพอ ๆ กับที่ฟังคนอื่น",
    3: "สัญญาณของคุณคือการใช้เสียง ความคิด หรือสิ่งที่สร้างสรรค์เป็นประตูเปิดชีวิต",
    4: "สัญญาณของคุณคือการสร้างฐานชีวิตใหม่ที่มั่นคงกว่าเดิม แต่ไม่แข็งทื่อเกินไป",
    5: "สัญญาณของคุณคือการขยับออกจากสิ่งเดิมและกลับไปใช้ชีวิตที่เป็นตัวเองมากขึ้น",
    6: "สัญญาณของคุณคือการเรียนรู้ความรักที่ไม่ทิ้งตัวเองไว้ข้างหลัง",
    7: "สัญญาณของคุณคือการเปลี่ยนความลึกของตัวเองให้กลายเป็นปัญญาที่ใช้งานได้จริง",
    8: "สัญญาณของคุณคือการยืนในคุณค่าของตัวเองอย่างมั่นคงและสร้างบางอย่างที่จับต้องได้",
    9: "สัญญาณของคุณคือการปล่อยของเก่าบางอย่าง เพื่อให้พลังใหม่ไหลเข้ามา",
    11: "สัญญาณของคุณคือการเชื่อในสิ่งที่หัวใจรับรู้และแปลมันออกมาเป็นสิ่งที่มีคุณค่า",
    22: "สัญญาณของคุณคือการหยุดคิดใหญ่จนไม่เริ่ม และเริ่มลงมือกับภาพที่คุณเห็นในใจ",
    33: "สัญญาณของคุณคือการใช้หัวใจที่เยียวยาคนอื่นได้ โดยไม่เผาตัวเองจนหมดแรง",
}

MONTH_ENERGY = {
    1: "พลังเริ่มต้น", 2: "พลังความสัมพันธ์", 3: "พลังการสื่อสาร", 4: "พลังการวางรากฐาน",
    5: "พลังการเปลี่ยนแปลง", 6: "พลังความรักและการดูแล", 7: "พลังค้นหาความหมาย", 8: "พลังความสำเร็จ",
    9: "พลังการปล่อยวาง", 10: "พลังจุดเปลี่ยน", 11: "พลังญาณรู้", 12: "พลังปิดวงจรเก่า"
}

FEATURES = [
    ("🪐", "ตัวตนจักรวาล", "ราศี พลังวันเกิด และภาพรวมพลังงาน"),
    ("🔮", "นิสัยลึกที่ซ่อนอยู่", "ด้านในที่คนรอบตัวอาจไม่เคยรู้"),
    ("💫", "รูปแบบอารมณ์", "เวลาคุณรู้สึกลึกจริง ๆ คุณเป็นแบบไหน"),
    ("🗝️", "สัญญาณจักรวาล", "สิ่งที่ชีวิตกำลังพยายามบอกคุณอยู่"),
    ("🌌", "ภารกิจชีวิต", "แนวทางที่พลังของคุณอยากพาไป"),
    ("💼", "งานและเส้นทางที่ใช่", "พลังที่เหมาะกับการงานและการสร้างตัว"),
    ("🌑", "เงาชีวิตและบทเรียน", "สิ่งที่คุณต้องก้าวผ่านเพื่อโตขึ้น"),
    ("📅", "Timeline พลังงาน", "ช่วงเวลาที่ควรฟังหัวใจตัวเองให้ชัด"),
]

PREMIUM_ITEMS = [
    "🌌 ภารกิจจิตวิญญาณที่แท้จริง",
    "⚡ พลังพิเศษ 7 ด้านที่ติดตัวมาแต่เกิด",
    "💼 อาชีพ / ธุรกิจที่เหมาะกับพลังงานคุณ",
    "💰 รูปแบบการเงินและการรับทรัพย์",
    "💞 ความรัก ความสัมพันธ์ และคู่ที่เหมาะ",
    "🌑 เงาชีวิต บาดแผล และวิธีเอาชนะ",
    "📅 Timeline พลังงาน 1–3 ปี",
    "🔑 Action Plan ก้าวแรกที่ควรเริ่มในชีวิตนี้",
]

EBOOK_SELL_POINTS = [
    ("💔", "เข้าใจความเจ็บปวดและความสูญเสีย", "ทำไมบางช่วงของชีวิตจึงเหมือนพังไปทั้งใจ"),
    ("🌱", "เครื่องมือเปลี่ยนพลังงานภายใน", "ค่อย ๆ กลับมาเป็นตัวเองอีกครั้ง"),
    ("🔮", "ค้นพบตัวตนหลังพายุ", "เมื่อความเจ็บไม่ได้ทำลายคุณ แต่มาปลุกคุณ"),
    ("✨", "สร้างชีวิตที่ตรงกับจิตวิญญาณ", "ออกจากความฝืนและกลับไปสู่ความจริงของใจ"),
    ("🌟", "Affirmation และการเยียวยารายวัน", "ใช้ได้จริงในวันที่ใจยังเปราะบาง"),
]

TOC_COPY = [
    "บทที่ 1: ในวันที่ชีวิตพัง... จนไปต่อไม่เป็น",
    "บทที่ 2: เมื่อน้ำตาคือการชำระล้าง: อนุญาตให้ตัวเองอ่อนแอ",
    "บทที่ 3: ถอดรหัสบทเรียน: ทำไมสิ่งนี้ถึงเกิดกับเรา?",
    "บทที่ 4: การตื่นรู้แบบเข้าใจง่าย: ตื่นจากฝันร้ายมาเจอตัวเอง",
    "บทที่ 5: ดีท็อกซ์อารมณ์: ทิ้งขยะใจที่เก็บไว้มานาน",
    "บทที่ 6: สร้างเกราะป้องกันใจในโลกที่วุ่นวาย",
    "บทที่ 7: จูนคลื่นพลังงานดึงดูดความโชคดี",
    "บทที่ 8: แผนฟื้นฟูจิตวิญญาณ 7 วัน",
    "บทที่ 9: ความสุขที่ไหลลื่นจากภายใน",
    "บทที่ 10: แสงสว่างที่ไม่มีวันดับในใจคุณ",
]


def generate_reading(name: str, day: int, month_num: int, year_be: int, focus_area: str, note: str, place: str = ""):
    lp = life_path_number(day, month_num, year_be)
    birth_energy = birth_day_energy(day)
    z_th, z_en, z_sym = zodiac_sign(day, month_num)
    chinese = chinese_zodiac(year_be)
    lp_label_th, lp_label_en = LIFE_PATH_LABELS.get(lp, ("เส้นทางเฉพาะตัว", "Unique Path"))

    note_text = (note or "").strip()
    focus_text = (focus_area or "").strip()

    opening = (
        f"{name} เป็นคนที่มีพลังหลักแบบ {lp_label_th} และมีแกนชีวิตอยู่ที่{ENERGY_SUMMARIES.get(lp, '')} "
        f"ประกอบกับพลังวันเกิดเลข {birth_energy} และราศี{z_th} ทำให้ชีวิตของคุณไม่ได้เหมาะกับการใช้ชีวิตแบบฝืนตัวเองนาน ๆ"
    )

    if note_text:
        opening += f" ตอนนี้สิ่งที่คุณแบกอยู่ในใจสะท้อนชัดว่าเรื่อง '{note_text}' กำลังดึงพลังงานของคุณไปมากกว่าที่คนรอบตัวเห็น"

    hidden = HIDDEN_SIDE.get(lp, "ลึก ๆ แล้วคุณต้องการพื้นที่ที่คุณเป็นตัวเองได้จริง")
    signal = SIGNAL_HINTS.get(lp, "สัญญาณของคุณคือการกลับมาฟังหัวใจตัวเองให้ชัด")

    emotion = (
        f"เมื่อพลังตก คุณมีแนวโน้มจะ{'เก็บไว้คนเดียว' if lp in [2,6,7,9,11,33] else 'กดดันตัวเองเงียบ ๆ'} "
        f"และทำให้คนอื่นไม่เห็นว่าจริง ๆ แล้วคุณเหนื่อยแค่ไหน"
    )

    if focus_text:
        emotion += f" โดยเฉพาะในเรื่อง '{focus_text}' ชีวิตกำลังบอกให้คุณหยุดใช้วิธีเดิม แล้วเริ่มฟังความต้องการลึก ๆ ของตัวเองมากขึ้น"

    short_hint = (
        f"เดือนเกิดของคุณมีพลัง '{MONTH_ENERGY.get(month_num, 'พลังเฉพาะตัว')}' จึงยิ่งตอกย้ำว่าการเปลี่ยนชีวิตของคุณไม่ได้เริ่มจากการฝืน แต่เริ่มจากการเข้าใจตัวเองให้ชัด"
    )

    premium_tease = (
        "ยังมีพิมพ์เขียวอีกหลายชั้นที่ซ่อนอยู่ เช่น ภารกิจชีวิตจริง ความรัก งาน เงิน เงาชีวิต และ timeline พลังงานที่ละเอียดกว่านี้"
    )

    return {
        "name": name,
        "day": day,
        "month_num": month_num,
        "year_be": year_be,
        "month_name": MONTHS[month_num - 1]["th"],
        "place": place,
        "zodiac_th": z_th,
        "zodiac_en": z_en,
        "zodiac_sym": z_sym,
        "chinese": chinese,
        "life_path": lp,
        "life_path_label_th": lp_label_th,
        "life_path_label_en": lp_label_en,
        "birth_energy": birth_energy,
        "opening": opening,
        "hidden": hidden,
        "emotion": emotion,
        "signal": signal,
        "short_hint": short_hint,
        "premium_tease": premium_tease,
    }


def render_stat_card(icon: str, title: str, value: str, note: str = ""):
    st.markdown(
        f"""
        <div class="stat-card final-stat-card">
            <div class="stat-icon">{icon}</div>
            <div class="stat-title">{title}</div>
            <div class="stat-value">{value}</div>
            <div class="stat-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_feature_card(icon: str, title: str, sub: str):
    st.markdown(
        f"""
        <div class="feature-card">
            <div class="feature-icon">{icon}</div>
            <div class="feature-text-wrap">
                <div class="feature-title">{title}</div>
                <div class="feature-sub">{sub}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def get_image_path(candidates):
    for c in candidates:
        p = Path(c)
        if p.exists():
            return str(p)
    return None


query_params = st.query_params
if "lang" in query_params:
    qp = str(query_params["lang"]).lower()
    if qp in ["th", "en"]:
        st.session_state.lang = qp

# -----------------------------
# CSS
# -----------------------------
st.markdown(
    """
<style>
html, body, [class*="css"] {color:#2f1f38 !important;}
.stApp {
    background-image: linear-gradient(135deg, #fcf8ff 0%, #eadcf9 32%, #fdf8f7 68%, #fff3ea 100%);
    color:#2f1f38 !important;
}
section.main > div {padding-top: 1rem !important;}

p, span, div, label, li, small {color:#2f1f38 !important;}
h1, h2, h3, h4, h5, h6 {margin:0 !important; color:#392049 !important;}

a {text-decoration:none !important;}

div.stButton > button:first-child,
div[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(to right, #ba68c8 0%, #f06292 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 28px !important;
    padding: 0.82rem 1.3rem !important;
    font-weight: 700 !important;
    font-size: 1.02rem !important;
    transition: 0.25s all ease !important;
    box-shadow: 0 8px 22px rgba(186, 104, 200, 0.28) !important;
    width: 100% !important;
    margin-top: 10px !important;
}

div.stButton > button:first-child:hover,
div[data-testid="stFormSubmitButton"] > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 28px rgba(186, 104, 200, 0.36);
    color: white !important;
}

.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stTextArea textarea,
.stSelectbox div[data-baseweb="select"] > div {
    border-radius: 16px !important;
    border: 1px solid #d9cfe6 !important;
    background-color: rgba(255,255,255,0.94) !important;
    color: #2f1f38 !important;
    -webkit-text-fill-color: #2f1f38 !important;
}

input::placeholder, textarea::placeholder {
    color: #8d7b9a !important;
    opacity: 1 !important;
    -webkit-text-fill-color: #8d7b9a !important;
}

label, .stMarkdown, .stTextInput label, .stNumberInput label, .stSelectbox label, .stTextArea label {
    color: #4a3557 !important;
}

.stAlert, .stSuccess, .stInfo, .stWarning {border-radius:16px !important;}

.page-shell {max-width: 840px; margin: 0 auto;}

.topbar {
    display:flex; align-items:center; justify-content:space-between;
    gap:14px; margin-bottom:24px;
}
.brand-mini {
    font-size: 0.92rem; font-weight: 800; letter-spacing: 1px; color:#4a245f !important;
}
.topbar-actions {display:flex; gap:10px; align-items:center;}
.top-pill, .top-pill-line {
    display:inline-flex; align-items:center; justify-content:center; gap:7px;
    border-radius:999px; padding:10px 16px; font-weight:700; font-size:13px;
    box-shadow:0 6px 18px rgba(186, 104, 200, 0.12);
}
.top-pill {
    background: rgba(255,255,255,0.78); color:#6b3e81 !important; border:1px solid rgba(186,104,200,0.18);
}
.top-pill-line {
    background: linear-gradient(135deg,#06c755,#25d366); color:#fff !important; border:none;
    box-shadow:0 8px 22px rgba(6,199,85,0.26);
}

.hero-wrap {text-align:center; padding: 16px 6px 10px;}
.hero-orb {
    width:82px; height:82px; margin:0 auto 18px; border-radius:50%;
    background: radial-gradient(circle at center, rgba(255,255,255,0.95) 0%, rgba(241,228,255,0.95) 40%, rgba(204,166,237,0.8) 70%, rgba(204,166,237,0.12) 100%);
    display:flex; align-items:center; justify-content:center;
    box-shadow:0 0 26px rgba(190,130,255,0.35), 0 0 60px rgba(240,150,210,0.14);
    font-size:34px;
}
.eyebrow {
    font-size:12px; letter-spacing:4px; text-transform:uppercase; color:#8f70a4 !important; margin-bottom:10px;
}
.hero-title {
    font-size: clamp(2.1rem, 5vw, 3.4rem); font-weight: 900; line-height:1.03;
    color:#47225a !important; margin-bottom:10px;
}
.hero-subtitle {
    font-size: clamp(1.12rem, 2.7vw, 1.55rem); font-weight:700; color:#633b78 !important; margin-bottom:8px;
}
.hero-mini {
    color:#7b6888 !important; font-size:0.95rem; margin-bottom:22px;
}

.hero-card, .soft-card, .glow-box, .result-card, .mini-card, .lock-card, .ebook-card, .toc-card {
    background: rgba(255,255,255,0.62) !important;
    backdrop-filter: blur(10px);
    border:1px solid rgba(186,104,200,0.10) !important;
    border-radius: 24px !important;
    box-shadow: 0 10px 28px rgba(126, 87, 194, 0.10) !important;
}

.hero-card {padding:20px 18px !important; margin: 8px 0 18px 0 !important;}
.glow-box {padding:18px !important; margin: 12px 0 22px 0 !important;}
.result-card {padding:22px !important; margin: 12px 0 !important;}
.mini-card {padding:16px !important; margin-bottom: 12px !important;}
.lock-card {padding:22px !important; margin: 18px 0 !important;}
.ebook-card {padding:22px !important; margin: 18px 0 !important;}
.toc-card {padding:18px !important; margin-top: 12px !important;}

.section-kicker {
    text-align:center; font-size:12px; letter-spacing:3px; color:#9662ab !important; margin:12px 0 16px 0; text-transform:uppercase;
}
.section-title {
    text-align:center; font-size:1.65rem; font-weight:800; color:#4a245f !important; margin-bottom:8px !important;
}
.section-sub {
    text-align:center; color:#735f82 !important; font-size:0.98rem; margin-bottom:14px !important;
}

.feature-card {
    display:flex; gap:12px; align-items:flex-start; background:rgba(255,255,255,0.78);
    padding:16px; border-radius:18px; box-shadow:0 6px 18px rgba(126,87,194,0.08);
    min-height:110px; border:1px solid rgba(186,104,200,0.10);
}
.feature-icon {
    width:44px; height:44px; border-radius:14px; display:flex; align-items:center; justify-content:center;
    font-size:22px; background:linear-gradient(135deg, rgba(186,104,200,0.22), rgba(240,98,146,0.18));
    box-shadow:0 6px 16px rgba(186,104,200,0.10);
    flex-shrink:0;
}
.feature-title {font-size:1rem; font-weight:800; color:#4a245f !important; margin-bottom:5px;}
.feature-sub {font-size:0.92rem; color:#6f607c !important; line-height:1.5;}

.final-stat-card {
    background: rgba(255,255,255,0.82); border-radius:20px; padding:18px 14px; text-align:center;
    box-shadow:0 6px 18px rgba(126,87,194,0.08); min-height:144px;
}
.stat-icon {font-size:28px; margin-bottom:8px;}
.stat-title {font-size:12px; letter-spacing:1.3px; text-transform:uppercase; color:#9468a8 !important; margin-bottom:6px;}
.stat-value {font-size:1.05rem; font-weight:800; color:#4a245f !important; line-height:1.35;}
.stat-note {font-size:0.85rem; color:#6f607c !important; margin-top:6px; line-height:1.45;}

.insight-box {
    background:rgba(255,255,255,0.78); border-radius:18px; padding:16px; box-shadow:0 5px 16px rgba(126,87,194,0.07);
    border-left:4px solid rgba(186,104,200,0.35); height:100%;
}
.insight-label {font-size:12px; font-weight:800; color:#8a59a0 !important; margin-bottom:8px;}
.insight-text {font-size:0.98rem; line-height:1.7; color:#4e3f58 !important;}

.tab-note {
    background:rgba(255,255,255,0.82); border-radius:16px; padding:16px; margin-top:10px; box-shadow:0 4px 14px rgba(126,87,194,0.06);
}
.premium-item {
    background:rgba(255,255,255,0.76); border-radius:16px; padding:12px 14px; margin-bottom:8px;
    box-shadow:0 4px 14px rgba(126,87,194,0.06); color:#4d365c !important; font-weight:600;
}
.badge-row {
    display:flex; gap:8px; flex-wrap:wrap; justify-content:center; margin:14px 0 8px;
}
.soft-badge {
    background:rgba(255,255,255,0.82); border-radius:999px; padding:8px 12px; font-size:13px; color:#6a5776 !important;
    border:1px solid rgba(186,104,200,0.12);
}
.cta-box {
    background:linear-gradient(135deg, rgba(255,255,255,0.68), rgba(255,245,252,0.78));
    border-radius:20px; padding:18px; box-shadow:0 10px 28px rgba(126,87,194,0.10);
    text-align:center; margin-top:14px;
}
.line-big a {
    display:flex; align-items:center; justify-content:center; gap:10px;
    width:100%; padding:16px 18px; border-radius:999px; font-weight:800;
    font-size:1rem; background:linear-gradient(135deg,#00b900,#06c755); color:white !important;
    box-shadow:0 10px 24px rgba(6,199,85,0.24);
}
.link-soft a {
    display:inline-flex; align-items:center; justify-content:center; gap:8px; padding:10px 16px;
    border-radius:999px; background:rgba(255,255,255,0.8); color:#6a3d80 !important;
    border:1px solid rgba(186,104,200,0.14);
}

.loading-wrap {
    text-align:center; padding:32px 8px 10px;
}
.loading-orb {
    width:108px; height:108px; margin:0 auto 18px; border-radius:50%; background: radial-gradient(circle, #ffffff 0%, #f1e6ff 38%, #d4b5f8 70%, rgba(212,181,248,0.2) 100%);
    box-shadow:0 0 28px rgba(186,104,200,0.34), 0 0 64px rgba(240,98,146,0.10);
    display:flex; align-items:center; justify-content:center; font-size:42px;
}
.loading-title {font-size:1.28rem; font-weight:800; color:#4a245f !important; margin-bottom:8px;}
.loading-sub {color:#735f82 !important; line-height:1.7;}

.ebook-cover-wrap {text-align:center; margin: 14px 0 18px;}
.ebook-copy {font-size:1rem; line-height:1.9; color:#4f3f59 !important; text-align:left;}
.toc-item {
    padding:10px 0; border-bottom:1px solid rgba(133,105,150,0.20); color:#44334f !important; font-size:1rem;
}
.toc-item:last-child {border-bottom:none;}
.footer-note {text-align:center; color:#7a677f !important; font-size:12px; margin:26px 0 18px;}

@media (max-width: 768px) {
    .topbar {align-items:flex-start;}
    .topbar-actions {gap:8px;}
    .top-pill, .top-pill-line {padding:8px 12px; font-size:12px;}
    .hero-title {font-size: 2.35rem;}
    .hero-subtitle {font-size: 1.08rem;}
    .feature-card {min-height:96px;}
}
</style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Top navigation
# -----------------------------
st.markdown('<div class="page-shell">', unsafe_allow_html=True)
st.markdown(
    f"""
    <div class="topbar">
        <div class="brand-mini">🔮 LUMINA SOUL</div>
        <div class="topbar-actions">
            <a class="top-pill" href="#ebook-section">📖 eBook</a>
            <a class="top-pill-line" href="{LINE_LINK}" target="_blank">💬 LINE</a>
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# HERO
# -----------------------------
st.markdown(
    f"""
    <div class="hero-wrap">
        <div class="hero-orb">🔮</div>
        <div class="eyebrow">Decode Your Cosmic Blueprint</div>
        <div class="hero-title">พิมพ์เขียวชีวิต</div>
        <div class="hero-subtitle">คุณเกิดมาทำอะไร? จักรวาลมีคำตอบ</div>
        <div class="hero-mini">โหราศาสตร์ · พลังงาน · จิตวิญญาณ · การสะท้อนชีวิตเฉพาะคุณ</div>
    </div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# FEATURES
# -----------------------------
st.markdown('<div class="section-kicker">สิ่งที่คุณจะค้นพบ</div>', unsafe_allow_html=True)
feature_cols = st.columns(2)
for i, item in enumerate(FEATURES):
    with feature_cols[i % 2]:
        render_feature_card(*item)

# -----------------------------
# FORM
# -----------------------------
st.markdown('<div class="hero-card">', unsafe_allow_html=True)
st.markdown('<div class="section-title">เริ่มต้นการเดินทาง</div>', unsafe_allow_html=True)
st.markdown('<div class="section-sub">กรอกข้อมูลเพื่อเริ่มอ่านพิมพ์เขียวชีวิตของคุณ</div>', unsafe_allow_html=True)

with st.form("lumina_form", clear_on_submit=False):
    full_name = st.text_input(
        tr("ชื่อ-นามสกุล", "Full name"),
        placeholder=tr("ใช้ชื่อจริงหรือชื่อที่คุณอยากให้เรียก", "Use your real name or preferred name"),
    )

    c1, c2, c3 = st.columns([1, 1.25, 1])
    with c1:
        birth_day = st.number_input(tr("วันเกิด", "Day"), min_value=1, max_value=31, value=1, step=1)
    with c2:
        month_labels = [m["th"] if st.session_state.lang == "th" else m["en"] for m in MONTHS]
        month_index = st.selectbox(tr("เดือนเกิด", "Month"), range(12), format_func=lambda x: month_labels[x])
    with c3:
        birth_year = st.number_input(tr("ปี พ.ศ. เกิด", "Birth year (B.E.)"), min_value=2400, max_value=2600, value=2535, step=1)

    c4, c5 = st.columns(2)
    with c4:
        birth_time = st.text_input(tr("เวลาเกิด (ถ้าทราบ)", "Birth time (optional)"), placeholder="10:25")
    with c5:
        birth_place = st.text_input(tr("สถานที่เกิด (ถ้าทราบ)", "Birth place (optional)"), placeholder=tr("เช่น กรุงเทพ", "e.g. Bangkok"))

    focus_area = st.selectbox(
        tr("ด้านที่คุณอยากรับพลังงานมากที่สุดวันนี้", "Main focus area today"),
        [
            tr("ภาพรวมชีวิตทั้งหมด", "Overall life"),
            tr("ความรักและความสัมพันธ์", "Love & relationships"),
            tr("การงานและเส้นทางชีวิต", "Career & life path"),
            tr("โชคลาภและกระแสการเงิน", "Luck & financial flow"),
            tr("พลังใจและการเยียวยาภายใน", "Inner healing & emotional strength"),
        ],
    )

    note = st.text_area(
        tr("เรื่องที่คุณกังวลใจที่สุดตอนนี้คืออะไร?", "What is weighing on your heart most right now?"),
        placeholder=tr("เล่าแบบสั้น ๆ ก็พอ เช่น ความรัก งาน เงิน หรือความรู้สึกที่ติดอยู่ในใจ", "Share briefly: love, work, money, or what feels heavy inside"),
        height=110,
    )

    submitted = st.form_submit_button(tr("🔮 ถอดรหัสพลังงานของฉัน", "🔮 Decode my energy blueprint"))

st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="footer-note">ฟรี · ไม่ต้องสมัคร · ใช้เวลาไม่นาน · ถ้ารู้สึกเชื่อมโยง คุณสามารถปลดล็อกฉบับเต็มผ่าน LINE ได้ทันที</div>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# Submit flow
# -----------------------------
if submitted:
    st.session_state.show_result = False

    if not full_name.strip():
        st.warning(tr("กรุณากรอกชื่อก่อนนะ", "Please enter your name first."))
    else:
        with st.container():
            st.markdown('<div class="glow-box loading-wrap">', unsafe_allow_html=True)
            st.markdown('<div class="loading-orb">🔮</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="loading-title">{tr("กำลังอ่านพิมพ์เขียวจักรวาล", "Reading your cosmic blueprint")}</div>',
                unsafe_allow_html=True,
            )
            st.markdown(
                f'<div class="loading-sub">{tr("AI กำลังวิเคราะห์พลังงานวันเกิดของคุณ...<br>และเชื่อมโยงสิ่งที่หัวใจกำลังพยายามบอกอยู่", "AI is reading your birth energy...<br>and connecting with what your heart is trying to say")}</div>',
                unsafe_allow_html=True,
            )
            progress = st.progress(0)
            for pct in [10, 28, 46, 68, 86, 100]:
                time.sleep(0.18)
                progress.progress(pct)
            st.markdown('</div>', unsafe_allow_html=True)

        result = generate_reading(
            name=full_name.strip(),
            day=int(birth_day),
            month_num=MONTHS[month_index]["num"],
            year_be=int(birth_year),
            focus_area=focus_area,
            note=note,
            place=birth_place.strip(),
        )

        safe_post(
            GOOGLE_SCRIPT_URL,
            {
                "name": full_name.strip(),
                "birthdate": f"{int(birth_day):02d}/{MONTHS[month_index]['num']:02d}/{int(birth_year)}",
                "birthtime": birth_time.strip(),
                "location": birth_place.strip(),
                "focus_area": focus_area,
                "note": note,
                "life_path": result["life_path"],
                "zodiac": result["zodiac_th"],
                "reading_type": "free_blueprint_preview",
            },
        )

        st.session_state.latest_result = result
        st.session_state.show_result = True

# -----------------------------
# RESULT SECTION
# -----------------------------
if st.session_state.show_result and st.session_state.latest_result:
    r = st.session_state.latest_result

    st.markdown('<div class="result-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-kicker">ผลอ่านฟรีของคุณ</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="section-title">{r["name"]}</div>', unsafe_allow_html=True)
    place_line = f' · {r["place"]}' if r["place"] else ''
    st.markdown(
        f'<div class="section-sub">{r["day"]} {r["month_name"]} {r["year_be"]}{place_line}</div>',
        unsafe_allow_html=True,
    )

    s1, s2, s3 = st.columns(3)
    with s1:
        render_stat_card(r["zodiac_sym"], "ราศีสากล", f'{r["zodiac_th"]} · {r["zodiac_en"]}', "โหราศาสตร์สากล")
    with s2:
        render_stat_card("🔢", "Life Path", f'{r["life_path"]} · {r["life_path_label_th"]}', r["life_path_label_en"])
    with s3:
        render_stat_card("🐲", "นักษัตรจีน", r["chinese"], f'พลังวันเกิดเลข {r["birth_energy"]}')

    st.markdown('<div class="tab-note">', unsafe_allow_html=True)
    st.markdown(f'<div class="insight-label">ภาพรวมพลังงานของคุณ</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="insight-text">{r["opening"]}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-kicker">ด้านในที่คนมักไม่รู้</div>', unsafe_allow_html=True)
    i1, i2 = st.columns(2)
    with i1:
        st.markdown(
            f"""
            <div class="insight-box">
                <div class="insight-label">ตัวตนลึกที่ซ่อนอยู่</div>
                <div class="insight-text">{r['hidden']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with i2:
        st.markdown(
            f"""
            <div class="insight-box">
                <div class="insight-label">สัญญาณที่ชีวิตกำลังบอก</div>
                <div class="insight-text">{r['signal']}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    tabs = st.tabs([
        tr("🌌 พลังงาน", "🌌 Energy"),
        tr("🔮 นิสัยลึก", "🔮 Personality"),
        tr("💫 อารมณ์", "💫 Emotion"),
        tr("🗝️ สัญญาณ", "🗝️ Signal"),
    ])

    with tabs[0]:
        st.markdown('<div class="tab-note">', unsafe_allow_html=True)
        st.markdown(f'<div class="insight-text">{r["opening"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with tabs[1]:
        st.markdown('<div class="tab-note">', unsafe_allow_html=True)
        st.markdown(f'<div class="insight-text">{r["hidden"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with tabs[2]:
        st.markdown('<div class="tab-note">', unsafe_allow_html=True)
        st.markdown(f'<div class="insight-text">{r["emotion"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    with tabs[3]:
        st.markdown('<div class="tab-note">', unsafe_allow_html=True)
        st.markdown(f'<div class="insight-text">{r["signal"]}<br><br>{r["short_hint"]}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    # Premium Preview
    st.markdown('<div class="lock-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-kicker">พิมพ์เขียวชีวิตฉบับเต็ม — รอการปลดล็อก</div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">ปลดล็อกพิมพ์เขียวชีวิต 360°</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-sub">รายงานเชิงลึกเฉพาะคุณ ที่ช่วยให้เห็นทั้งภารกิจชีวิต ความรัก งาน เงิน และเงาชีวิตอย่างชัดเจนกว่าเดิม</div>',
        unsafe_allow_html=True,
    )

    prem_c1, prem_c2 = st.columns(2)
    for idx, item in enumerate(PREMIUM_ITEMS):
        with (prem_c1 if idx % 2 == 0 else prem_c2):
            st.markdown(f'<div class="premium-item">{item}</div>', unsafe_allow_html=True)

    st.markdown(
        f'<div class="tab-note"><div class="insight-text">{r["premium_tease"]}</div></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="badge-row">
            <div class="soft-badge">✍️ เขียนเฉพาะคุณ</div>
            <div class="soft-badge">📬 ส่งภายใน 7 วัน</div>
            <div class="soft-badge">💰 ราคา 1,111 ฿</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
        <div class="cta-box">
            <div class="section-sub" style="margin-bottom:10px !important;">ถ้าคุณอยากเห็นรายละเอียดฉบับเต็มแบบเจาะลึก สามารถปลดล็อกต่อผ่าน LINE ได้ทันที</div>
            <div class="line-big"><a href="{LINE_LINK}" target="_blank">💬 ทักสั่งซื้อใน LINE</a></div>
            <div class="footer-note" style="margin:12px 0 0 !important;">LINE ID: {LINE_ID} · ชำระผ่าน PromptPay</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# eBook section
# -----------------------------
st.markdown('<div id="ebook-section"></div>', unsafe_allow_html=True)
st.markdown('<div class="ebook-card">', unsafe_allow_html=True)
st.markdown('<div class="section-kicker">lumina soul ebook</div>', unsafe_allow_html=True)
st.markdown('<div class="section-title">จากจุดที่พัง… สู่พลังแห่งการตื่นรู้</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="section-sub">หนังสือสำหรับคนที่ไม่ได้อยากแค่ “ดีขึ้น” แต่กำลังอยาก “กลับมาเจอตัวเอง” หลังผ่านบางอย่างที่หนักเกินไป</div>',
    unsafe_allow_html=True,
)

cover_path = get_image_path([
    "/mnt/data/preview.webp",
    "preview.webp",
    "ebook-cover.webp",
    "cover.jpg",
    "cover.png",
])

if cover_path:
    st.markdown('<div class="ebook-cover-wrap">', unsafe_allow_html=True)
    st.image(cover_path, width=260)
    st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown(
        """
        <div class="ebook-cover-wrap">
            <div style="display:inline-block;padding:26px 30px;border-radius:22px;background:linear-gradient(145deg,#fff5d4,#f6e4a8,#e2c06f);box-shadow:0 12px 30px rgba(194,154,76,0.18);font-weight:800;color:#6e5325;">📖 eBook Cover</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown(
    """
    <div class="tab-note">
        <div class="ebook-copy">
            ในบางช่วงของชีวิต เราไม่ได้อ่อนแอ… แต่เรากำลังแบกบางอย่างที่หนักเกินไปคนเดียว<br><br>
            หนังสือเล่มนี้ไม่ได้สอนให้คุณ “เข้มแข็งขึ้น” แบบฝืน ๆ แต่มันจะพาคุณค่อย ๆ กลับไปเจอ
            ตัวตนที่คุณเคยทิ้งไว้ระหว่างความเจ็บ ความสูญเสีย และความสับสน<br><br>
            ถ้าหัวใจคุณเคยรู้สึกว่า “ไปต่อไม่ถูก” หนังสือเล่มนี้อาจเป็นพื้นที่ปลอดภัยที่ทำให้คุณเข้าใจตัวเองมากขึ้น
            และเปลี่ยนความเจ็บให้กลายเป็นแสงของตัวเองได้อีกครั้ง
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="section-kicker">เนื้อหาภายในเล่ม</div>', unsafe_allow_html=True)
for icon, title, sub in EBOOK_SELL_POINTS:
    st.markdown(
        f"""
        <div class="premium-item"><span style="font-size:19px;">{icon}</span> {title}<br><span style="font-size:13px;font-weight:400;color:#6b5b75 !important;">{sub}</span></div>
        """,
        unsafe_allow_html=True,
    )

st.markdown('<div class="toc-card">', unsafe_allow_html=True)
st.markdown('<div class="insight-label">สารบัญ</div>', unsafe_allow_html=True)
for item in TOC_COPY:
    st.markdown(f'<div class="toc-item">• {item}</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown(
    """
    <div class="tab-note">
        <div class="insight-label">ทำไมเล่มนี้ถึงต่าง</div>
        <div class="insight-text">
            ไม่ใช่หนังสือให้กำลังใจแบบกว้าง ๆ<br>
            ไม่ใช่คำสวย ๆ ที่อ่านแล้วลืม<br>
            แต่เป็นหนังสือที่พูดในสิ่งที่หลายคนรู้สึกอยู่…แต่ไม่เคยมีคำพูดให้มันจริง ๆ
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="cta-box">
        <div class="section-sub" style="margin-bottom:10px !important;">พร้อมเปลี่ยนจุดที่พัง ให้กลายเป็นพลังของคุณหรือยัง?</div>
        <div class="line-big"><a href="{LINE_LINK}" target="_blank">💬 สั่งซื้อ eBook ผ่าน LINE</a></div>
        <div class="footer-note" style="margin:12px 0 0 !important;">รับไฟล์หลังชำระเงิน · LINE ID: {LINE_ID}</div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------
# Footer
# -----------------------------
st.markdown(
    """
    <div class="footer-note">© 2026 LUMINA SOUL | พื้นที่สะท้อนชีวิตและเยียวยาหัวใจ</div>
    """,
    unsafe_allow_html=True,
)
st.markdown('</div>', unsafe_allow_html=True)
