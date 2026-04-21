import streamlit as st
import requests
from datetime import datetime
import base64
from pathlib import Path

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

if "latest_soul_key" not in st.session_state:
    st.session_state.latest_soul_key = ""

if "page" not in st.session_state:
    st.session_state.page = "main"

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

if "page" in query_params:
    qp_page = str(query_params["page"]).lower()
    if qp_page in ["main", "ebook"]:
        st.session_state.page = qp_page


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
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 10px;
    text-align: center;
    padding: 16px 18px;
    border-radius: 999px;
    font-weight: 700;
    font-size: 15px;
    background: linear-gradient(135deg, #f7a8cf, #c9b5ff 58%, #aebeff);
    color: white !important;
    box-shadow: 0 8px 22px rgba(180, 140, 255, 0.22);
    text-decoration: none;
    transition: all 0.22s ease;
}
.premium-btn a img {
    width: 22px;
    height: 22px;
    display: inline-block;
}

.premium-btn a:hover {
    transform: translateY(-1px);
    box-shadow: 0 12px 24px rgba(180, 140, 255, 0.28);
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

.nav-shell {
    display:flex;
    align-items:center;
    justify-content:space-between;
    gap:14px;
    margin-bottom: 10px;
}
.brand-mini {
    font-size: 0.82rem;
    letter-spacing: 2.6px;
    color:#7b6590 !important;
    font-weight:700;
}
.top-actions {
    display:flex;
    align-items:center;
    gap:10px;
    flex-wrap:nowrap;
    justify-content:flex-end;
}
.top-link-chip {
    display:inline-flex;
    align-items:center;
    justify-content:center;
    min-height: 36px;
    padding: 0 15px;
    border-radius: 999px;
    text-decoration:none !important;
    font-size: 12px;
    font-weight:700;
    box-shadow: 0 6px 18px rgba(186, 104, 200, 0.12);
    white-space:nowrap;
}
.top-link-chip.line {
    background: linear-gradient(135deg, #22c55e, #06c755);
    color:#fff !important;
    border:none;
    box-shadow: 0 8px 22px rgba(34,197,94,0.25);
}
.lang-group {
    display:inline-flex;
    align-items:center;
    background: rgba(255,255,255,0.88);
    border:1px solid rgba(186,104,200,0.18);
    border-radius:999px;
    padding:4px;
    gap:4px;
    box-shadow: 0 6px 18px rgba(186, 104, 200, 0.10);
}
.lang-pill {
    display:inline-flex;
    align-items:center;
    justify-content:center;
    min-width:36px;
    height:28px;
    padding:0 10px;
    border-radius:999px;
    text-decoration:none !important;
    color:#6f4a80 !important;
    font-size:11px;
    font-weight:800;
}
.lang-pill.active {
    background: linear-gradient(135deg, #ba68c8, #f06292);
    color:#fff !important;
    box-shadow: 0 6px 14px rgba(186,104,200,0.24);
}
.hero-orb-wrap {
    display:flex;
    justify-content:center;
    margin-top: 18px;
    margin-bottom: 12px;
}
.hero-orb {
    width: 122px;
    height: 122px;
    border-radius: 50%;
    display:flex;
    align-items:center;
    justify-content:center;
    background: radial-gradient(circle at center, rgba(255,255,255,0.98) 0%, rgba(235,214,255,0.96) 42%, rgba(216,189,247,0.78) 65%, rgba(216,189,247,0.18) 100%);
    box-shadow: 0 16px 42px rgba(174, 128, 220, 0.22);
}
.hero-orb-inner {
    width:58px;
    height:58px;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size: 30px;
    background: linear-gradient(135deg, #f5d0fe, #d8b4fe 55%, #c4b5fd);
    box-shadow: inset 0 2px 6px rgba(255,255,255,0.9), 0 10px 28px rgba(163, 108, 210, 0.28);
}
.hero-kicker {
    text-align:center;
    letter-spacing: 5px;
    font-size: 0.88rem;
    color:#8c77a0 !important;
    margin-bottom: 14px;
}
.hero-title-center {
    text-align:center;
    font-size: 4rem;
    line-height: 1.03;
    font-weight: 900;
    color:#3f234f !important;
    margin-bottom: 10px;
}
.hero-sub-center {
    text-align:center;
    font-size: 2rem;
    line-height: 1.18;
    font-weight: 800;
    color:#4a2e60 !important;
    margin-bottom: 8px;
}
.hero-meta {
    text-align:center;
    color:#6d597d !important;
    font-size: 1.02rem;
    margin-bottom: 24px;
}
.section-kicker {
    text-align:center;
    color:#8d6ca1 !important;
    font-size:0.95rem;
    letter-spacing: 3px;
    margin: 12px 0 14px 0;
}
.feature-grid {
    display:grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 10px;
    margin-bottom: 16px;
}
.feature-card {
    background: rgba(255,255,255,0.82);
    border: 1px solid rgba(223,208,237,0.95);
    border-radius: 18px;
    padding: 14px 14px;
    box-shadow: 0 6px 18px rgba(126, 87, 194, 0.08);
    min-height: 104px;
    display:flex;
    gap:12px;
    align-items:flex-start;
}
.feature-icon {
    width: 42px;
    height: 42px;
    border-radius: 14px;
    background: linear-gradient(135deg, #f5d5ef, #f6e6fb);
    display:flex;
    align-items:center;
    justify-content:center;
    font-size: 20px;
    flex-shrink:0;
}
.feature-title {
    font-size: 1.02rem;
    font-weight: 800;
    color:#44245b !important;
    line-height:1.22;
    margin-bottom: 3px;
}
.feature-text {
    font-size: 0.90rem;
    color:#65556f !important;
    line-height:1.35;
}
.form-shell {
    background: rgba(255,255,255,0.70) !important;
    border: 1px solid rgba(216, 201, 231, 0.95);
    border-radius: 24px !important;
    padding: 22px 18px 10px 18px !important;
    box-shadow: 0 12px 30px rgba(126, 87, 194, 0.10) !important;
    margin-top: 8px !important;
    margin-bottom: 8px !important;
}
.ebook-hero-card {
    background: linear-gradient(180deg, rgba(255,255,255,0.84), rgba(255,250,242,0.92));
    border: 1px solid rgba(224, 210, 190, 0.95);
    border-radius: 26px;
    padding: 22px 18px;
    box-shadow: 0 14px 28px rgba(196, 164, 112, 0.18);
}
.ebook-cover {
    width: min(280px, 78vw);
    border-radius: 18px;
    box-shadow: 0 18px 42px rgba(170, 138, 72, 0.24);
    display:block;
    margin: 0 auto 18px auto;
}
.ebook-title {
    text-align:center;
    font-size: 2rem;
    font-weight: 900;
    line-height:1.15;
    color:#6a4b18 !important;
    margin-bottom: 8px;
}
.ebook-sub {
    text-align:center;
    font-size: 1rem;
    color:#7a6440 !important;
    margin-bottom: 14px;
}
.ebook-list-card {
    background: rgba(255,255,255,0.88);
    border: 1px solid rgba(225, 213, 192, 0.96);
    border-radius: 18px;
    padding: 14px 14px;
    margin-bottom: 10px;
}
.ebook-mini-item {
    display:flex;
    gap:10px;
    align-items:flex-start;
    padding: 10px 0;
    border-bottom: 1px solid rgba(193, 174, 139, 0.24);
}
.ebook-mini-item:last-child { border-bottom:none; }
.cta-button-row {
    display:flex;
    gap:10px;
    flex-wrap:wrap;
    justify-content:center;
    margin-top: 12px;
}
.center-button-link {
    display:inline-flex;
    align-items:center;
    justify-content:center;
    min-height: 46px;
    border-radius: 999px;
    padding: 0 20px;
    text-decoration:none !important;
    font-weight:700;
}
.center-button-link.soft {
    background: rgba(255,255,255,0.84);
    color:#6f4a80 !important;
    border:1px solid rgba(186,104,200,0.18);
}
.center-button-link.line {
    background: linear-gradient(135deg, #22c55e, #06c755);
    color:#fff !important;
    border:none;
}
.result-next-card {
    background: linear-gradient(180deg, rgba(255,255,255,0.82), rgba(255,250,244,0.92));
    border: 1px solid rgba(223, 208, 224, 0.96);
    border-radius: 22px;
    padding: 18px;
    box-shadow: 0 12px 26px rgba(126,87,194,0.10);
    margin-top: 18px;
}
@media (max-width: 768px) {
    .nav-shell { align-items:flex-start; }
    .top-actions { gap:6px; }
    .top-link-chip { min-height:32px; padding:0 12px; font-size:11px; }
    .lang-group { padding:3px; gap:3px; }
    .lang-pill { min-width:34px; height:26px; padding:0 8px; font-size:10px; }
    .hero-kicker { letter-spacing: 3.2px; font-size:0.72rem; }
    .hero-title-center { font-size: 2.7rem; }
    .hero-sub-center { font-size: 1.18rem; }
    .hero-meta { font-size: 0.94rem; margin-bottom:18px; }
    .feature-grid { gap:8px; }
    .feature-card { min-height: 90px; padding: 12px 12px; gap:10px; border-radius:16px; }
    .feature-icon { width:36px; height:36px; border-radius:12px; font-size:18px; }
    .feature-title { font-size: 0.92rem; }
    .feature-text { font-size: 0.80rem; }
    .form-shell { padding: 18px 14px 6px 14px !important; border-radius: 20px !important; }
    .ebook-title { font-size: 1.45rem; }
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Existing links provided by user
# -----------------------------
GOOGLE_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbztgbRuGYMGMC41V8QHgNl2wnNTgJ5ZhRckVoiUXpVNTkSA-U75MFg-GRZNiCiIjrQeGg/exec"
SOULCODES_API_URL = "https://script.google.com/macros/s/AKfycbyBHg-JhN2YMWfpvf8zk28Yvv7yOqtrL5mTOl41lNRmreUF8c76B_J2fEpxHaj_b8SELA/exec"
SOULPROFILES_API_URL = "https://script.google.com/macros/s/AKfycbxDoHX4soOKHxM2Jc7ajmCfkrDLhF1_ETDnXW7GgY1QBDsHDlXvbroSo5pfPKxReD_deg/exec"
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
def verify_code_via_api(code_input: str):
    code = (code_input or "").strip().upper()
    if not code:
        return {"success": False, "valid": False}

    try:
        response = requests.post(
            SOULCODES_API_URL,
            json={
                "action": "verify_code",
                "code": code
            },
            timeout=10
        )

        data = response.json()

        if data.get("success") and data.get("valid"):
            return {
                "success": True,
                "valid": True,
                "code": code
            }

        return {
            "success": True,
            "valid": False
        }

    except Exception:
        return {
            "success": False,
            "valid": False
        }


def mark_code_used_via_api(code_input: str):
    code = (code_input or "").strip().upper()
    if not code:
        return False

    try:
        response = requests.post(
            SOULCODES_API_URL,
            json={
                "action": "mark_used",
                "code": code
            },
            timeout=10
        )

        data = response.json()
        return bool(data.get("success"))

    except Exception:
        return False


def verify_profile_via_api(soul_key: str, birth_day: int, birth_month: int, birth_year: int):
    key = (soul_key or "").strip().upper()
    if not key:
        return {"success": False, "valid": False}

    try:
        response = requests.post(
            SOULPROFILES_API_URL,
            json={
                "action": "verify_profile",
                "soul_key": key,
                "birth_day": str(birth_day),
                "birth_month": str(birth_month),
                "birth_year": str(birth_year)
            },
            timeout=10
        )
        data = response.json()
        return {
            "success": bool(data.get("success")),
            "valid": bool(data.get("valid")),
            "soul_key": data.get("soul_key", key),
            "owner_name": data.get("owner_name", ""),
            "line_id": data.get("line_id", ""),
            "message": data.get("message", "")
        }
    except Exception:
        return {"success": False, "valid": False}


def log_profile_login_via_api(soul_key: str):
    key = (soul_key or "").strip().upper()
    if not key:
        return False

    try:
        response = requests.post(
            SOULPROFILES_API_URL,
            json={
                "action": "log_login",
                "soul_key": key
            },
            timeout=10
        )
        data = response.json()
        return bool(data.get("success"))
    except Exception:
        return False


def create_or_get_profile_via_api(owner_name: str, line_id: str, birth_day: int, birth_month: int, birth_year: int, note: str = ""):
    try:
        payload = {
            "action": "create_profile",
            "owner_name": (owner_name or "").strip(),
            "line_id": (line_id or "").strip(),
            "birth_day": str(birth_day),
            "birth_month": str(birth_month),
            "birth_year": str(birth_year),
            "note": note or ""
        }
        response = requests.post(SOULPROFILES_API_URL, json=payload, timeout=15)
        data = response.json()
        return {
            "success": bool(data.get("success")),
            "created": bool(data.get("created", False)),
            "soul_key": data.get("soul_key", ""),
            "owner_name": data.get("owner_name", ""),
            "line_id": data.get("line_id", ""),
            "message": data.get("message", "")
        }
    except Exception:
        return {"success": False, "soul_key": "", "message": "api_error"}

def push_to_google_sheet(payload: dict):
    try:
        requests.post(GOOGLE_SCRIPT_URL, json=payload, timeout=15)
    except Exception:
        pass


def get_page_link(page_name: str) -> str:
    return f"?lang={st.session_state.lang}&page={page_name}"


def get_cover_data_uri() -> str:
    return "data:image/webp;base64,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"


def render_ebook_page():
    st.markdown(
        f"""
        <div class="nav-shell">
            <div class="brand-mini">LUMINA SOUL</div>
            <div class="top-actions">
                <a href="{get_page_link('main')}" class="top-link-chip ebook">← {tr('กลับหน้าถอดรหัส', 'Back to decoder')}</a>
                <a href="{LINE_LINK}" target="_blank" class="top-link-chip line">💬 LINE</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="ebook-hero-card">
            <img src="{get_cover_data_uri()}" class="ebook-cover" alt="LUMINA SOUL eBook cover">
            <div class="ebook-title">{tr('จากจุดที่พัง... สู่พลังแห่งการตื่นรู้', 'From Collapse to Awakening')}</div>
            <div class="ebook-sub">{tr('คุณอาจไม่ได้พัง แต่คุณกำลังถูกปลุกให้กลับมาเป็นตัวเอง', 'You may not be broken. You may be awakening back to yourself.')}</div>
            <p class="center-text" style="margin-bottom:8px;">{tr('คู่มือปลอบใจในวันที่ไปต่อไม่ถูก เปลี่ยนความเจ็บปวดให้ค่อย ๆ กลายเป็นแสงสว่างในตัวคุณ', 'A gentle guide for the days you feel lost, helping pain slowly become light within you.')}</p>
            <p class="center-text soft-note" style="margin-bottom:18px;">{tr('หนังสือเล่มนี้ไม่ได้เร่งให้คุณเข้มแข็ง แต่พาคุณกลับไปเจอหัวใจที่คุณเคยทิ้งไว้', 'This book does not force you to be strong. It helps you return to the heart you left behind.')}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(tr('### ✨ เนื้อหาภายในเล่ม', '### ✨ What is inside this eBook'))
    ebook_items = [
        ("💔", tr("บทที่ 1: ในวันที่ชีวิตพัง... จนไปต่อไม่เป็น", "Chapter 1: When life falls apart and you do not know how to keep going"), tr("เข้าใจความรู้สึกที่เหมือนชีวิตหยุดอยู่กลางทาง", "Understand the feeling of being emotionally stuck in life.")),
        ("🌧️", tr("บทที่ 2: เมื่อน้ำตาคือการชำระล้าง", "Chapter 2: When tears become cleansing"), tr("อนุญาตให้ตัวเองอ่อนแออย่างปลอดภัย", "Give yourself permission to feel and soften safely.")),
        ("🔍", tr("บทที่ 3: ถอดรหัสบทเรียน ทำไมสิ่งนี้ถึงเกิดกับเรา?", "Chapter 3: Decoding the lesson — why did this happen?"), tr("มองความเจ็บเป็นภาษาหนึ่งของชีวิต", "See pain as one of life’s hidden languages.")),
        ("🌙", tr("บทที่ 4: การตื่นรู้แบบเข้าใจง่าย", "Chapter 4: Awakening made simple"), tr("ค่อย ๆ กลับมาเจอตัวเองอย่างไม่กดดัน", "Return to yourself gently, without pressure.")),
        ("🧠", tr("บทที่ 5: ดีท็อกซ์อารมณ์", "Chapter 5: Emotional detox"), tr("ปล่อยของเก่าที่ค้างอยู่ในใจมานาน", "Release what your heart has held for too long.")),
        ("🛡️", tr("บทที่ 6: สร้างเกราะป้องกันใจ", "Chapter 6: Building an inner shield"), tr("อยู่ในโลกที่วุ่นวายโดยไม่สูญเสียตัวเอง", "Stay in a noisy world without losing yourself.")),
        ("🌟", tr("บทที่ 7: จูนคลื่นพลังงานดึงดูดความโชคดี", "Chapter 7: Tuning your energy toward good fortune"), tr("เข้าใจพลังงานที่แท้จริงของคุณ", "Understand the energy that naturally supports you.")),
        ("🔄", tr("บทที่ 8: แผนฟื้นฟูจิตวิญญาณ 7 วัน", "Chapter 8: A 7-day soul reset"), tr("เริ่มต้นใหม่แบบมีขั้นตอน", "Begin again with a clear and gentle structure.")),
        ("💫", tr("บทที่ 9: ความสุขที่ไหลลื่นจากภายใน", "Chapter 9: Happiness flowing from within"), tr("ไม่ต้องรอโลกเปลี่ยนก่อนจึงค่อยหายใจได้", "Stop waiting for the world to change before you feel okay.")),
        ("✨", tr("บทที่ 10: แสงสว่างที่ไม่มีวันดับในใจคุณ", "Chapter 10: The light within you never goes out"), tr("จำได้อีกครั้งว่าคุณเป็นใคร", "Remember who you truly are.")),
    ]
    for icon, title, desc in ebook_items:
        st.markdown(
            f"""
            <div class="ebook-list-card">
                <div class="ebook-mini-item">
                    <div style="font-size:20px;">{icon}</div>
                    <div>
                        <div style="font-weight:800; color:#6a4b18 !important; margin-bottom:2px;">{title}</div>
                        <div class="soft-note" style="color:#7a6440 !important;">{desc}</div>
                    </div>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    st.markdown(
        f"""
        <div class="result-next-card" style="margin-bottom: 12px;">
            <h4 style="color:#8e24aa; margin-top:0; text-align:center;">{tr('ทำไมหนังสือเล่มนี้ถึงต่าง', 'Why this eBook feels different')}</h4>
            <p>{tr('ไม่ใช่หนังสือให้กำลังใจแบบกว้าง ๆ แต่เป็นหนังสือที่พูดในสิ่งที่หลายคนรู้สึกอยู่แต่ไม่เคยมีคำพูดให้มัน', 'This is not generic motivation. It gives language to what many people have felt but never fully named.')}</p>
            <p>{tr('เหมาะกับคนที่กำลังอยู่ในช่วงเปลี่ยนผ่าน อ่อนล้า สับสน หรืออยากกลับมารักตัวเองอย่างลึกและจริง', 'It is for people in transition, emotional fatigue, confusion, or anyone ready to return to self-love in a deeper and more honest way.')}</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="cta-button-row">
            <a href="{LINE_LINK}" target="_blank" class="center-button-link line">💬 {tr('สั่งซื้อผ่าน LINE', 'Order via LINE')}</a>
            <a href="{get_page_link('main')}" class="center-button-link soft">🔮 {tr('กลับไปถอดรหัสชีวิต', 'Back to life decoder')}</a>
        </div>
        <div class="cta-note">{tr('ชำระผ่าน PromptPay ทาง LINE | รับลิงก์และรายละเอียดการสั่งซื้อจากทีม LUMINA SOUL', 'Pay via PromptPay on LINE | Receive your ordering details from the LUMINA SOUL team')}</div>
        """,
        unsafe_allow_html=True
    )


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
    1: {
        "th": "คุณเคยรู้สึกว่าต้องเก่ง ต้องทำได้ ต้องพิสูจน์ตัวเองตลอดเวลา จนบางครั้งคุณไม่กล้าพัก เพราะลึก ๆ กลัวว่าถ้าหยุดเมื่อไหร่ คุณจะดูไม่มีค่า",
        "en": "You’ve felt like you always need to be strong, capable, and constantly proving yourself. Deep down, you fear that if you stop, you might lose your sense of worth."
    },
    2: {
        "th": "คุณมักเก็บความรู้สึกไว้ ไม่พูดในสิ่งที่ตัวเองต้องการจริง ๆ เพราะกลัวอีกฝ่ายจะไม่พอใจ จนสุดท้ายคุณกลายเป็นคนที่เข้าใจทุกคน…ยกเว้นตัวเอง",
        "en": "You tend to hold your feelings in and avoid expressing what you truly need, fearing others might be upset. In the end, you understand everyone—except yourself."
    },
    3: {
        "th": "คุณมีหลายอย่างในใจที่อยากพูด อยากเป็น แต่คุณมักเก็บมันไว้ เพราะกลัวว่าถ้าคนเห็นตัวจริงของคุณ เขาอาจจะไม่ยอมรับ",
        "en": "You have many thoughts and feelings you want to express, but you hold them back because you fear that if people see the real you, they may not accept you."
    },
    4: {
        "th": "คุณรู้สึกว่าตัวเองต้องควบคุมทุกอย่างให้ดี ต้องรับผิดชอบให้ได้ เพราะลึก ๆ กลัวว่าถ้าปล่อยเมื่อไหร่ ทุกอย่างจะพัง และคุณจะเป็นคนที่พลาด",
        "en": "You feel the need to control everything and stay responsible, because deep down you fear that if you let go, everything will fall apart—and it will be your fault."
    },
    5: {
        "th": "คุณเคยอยู่ในสิ่งที่ไม่ใช่ตัวเองมานาน ทั้งที่ลึก ๆ อยากออกมา แต่ก็ยังไม่กล้าพอที่จะปล่อย เพราะไม่รู้ว่าชีวิตใหม่จะไปทางไหน",
        "en": "You’ve stayed in situations that don’t truly fit you, even though you’ve wanted to leave. But you haven’t fully let go because you’re unsure where life will take you next."
    },
    6: {
        "th": "คุณให้คนอื่นมากจนกลายเป็นเรื่องปกติ จนสุดท้ายไม่มีใครรู้เลยว่าคุณก็เหนื่อย คุณก็ต้องการการดูแลเหมือนกัน",
        "en": "You give so much to others that it becomes normal, until no one realizes that you’re tired and need care too."
    },
    7: {
        "th": "คุณรู้สึกว่าคุณคิดไม่เหมือนคนอื่น และไม่มีใครเข้าใจคุณลึกจริง ๆ ทำให้หลายครั้งคุณเลือกอยู่เงียบ ๆ มากกว่าจะอธิบายตัวเอง",
        "en": "You feel like you think differently from others, and no one truly understands you. So many times, you choose silence instead of explaining yourself."
    },
    8: {
        "th": "คุณถูกบังคับให้เข้มแข็งเร็วกว่าที่ควร จนคุณชินกับการไม่แสดงความอ่อนแอ และลึก ๆ คุณก็ไม่รู้ว่าจะขอความช่วยเหลือยังไง",
        "en": "You had to become strong earlier than you should have, and now you’re used to hiding your vulnerability. Deep down, you don’t even know how to ask for help."
    },
    9: {
        "th": "คุณยังเก็บบางความสัมพันธ์หรือบางความรู้สึกไว้ในใจ ทั้งที่มันจบไปแล้ว เพราะคุณรักจริง และคุณไม่ได้ลืมง่ายเหมือนที่คนอื่นคิด",
        "en": "You still hold on to certain relationships or feelings, even though they’ve ended—because you truly loved, and you don’t forget easily like others think."
    },
    11: {
        "th": "คุณรับความรู้สึกและพลังของคนอื่นได้ลึกมาก จนบางครั้งคุณแยกไม่ออกว่าอะไรคือของคุณ อะไรคือของคนอื่น และมันทำให้คุณเหนื่อยโดยไม่รู้ตัว",
        "en": "You feel others’ emotions and energy deeply, to the point where you sometimes can’t tell what belongs to you and what belongs to others—and it drains you without you realizing it."
    },
    22: {
        "th": "คุณรู้สึกว่าตัวเองมีศักยภาพทำอะไรบางอย่างที่ใหญ่กว่าชีวิตปกติ แต่ในขณะเดียวกัน คุณก็กลัวว่าตัวเองจะทำไม่สำเร็จ จนกลายเป็นแรงกดดันที่คุณแบกไว้เงียบ ๆ",
        "en": "You feel that you’re meant for something bigger than an ordinary life, yet at the same time you fear you might not live up to it—creating a silent pressure you carry within."
    },
    33: {
        "th": "คุณมักเป็นคนที่อยากช่วยคนอื่นก่อนเสมอ จนบางครั้งคุณลืมตัวเองไป และลึก ๆ คุณอาจรู้สึกว่าคุณต้องมีประโยชน์ต่อคนอื่น ถึงจะมีคุณค่า",
        "en": "You often feel the need to help others first, sometimes forgetting yourself. Deep down, you may feel that you need to be useful to others in order to be worthy."
    }
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
    1: {
        "th": "เริ่มจากการเลือกสิ่งเล็ก ๆ ที่เป็นของคุณจริง ๆ ก่อน เช่น ตัดสินใจบางอย่างด้วยตัวเอง โดยไม่รอความเห็นจากใครทั้งหมด คุณไม่ต้องเปลี่ยนทั้งชีวิตวันนี้ แค่เริ่มกลับมาเลือกชีวิตของตัวเองทีละเรื่องก็พอ",
        "en": "Start by making small decisions that truly belong to you, without waiting for everyone’s approval. You don’t need to change your whole life today—just begin choosing your own path, one step at a time."
    },
    2: {
        "th": "ลองพูดสิ่งที่คุณรู้สึกจริงออกมา แม้มันจะไม่สมบูรณ์ หรือกลัวว่าจะทำให้อีกฝ่ายไม่พอใจ เพราะถ้าคุณไม่เริ่มพูด วันนี้คุณจะยังคงเป็นคนที่เข้าใจทุกคน…แต่ไม่มีใครเข้าใจคุณ",
        "en": "Start expressing what you truly feel, even if it’s not perfect or you fear upsetting someone. If you don’t begin now, you’ll remain the one who understands everyone—but no one understands you."
    },
    3: {
        "th": "เริ่มจากการพูดหรือเขียนสิ่งที่อยู่ในใจคุณออกมา โดยไม่ต้องรอให้มันสมบูรณ์ เพราะสิ่งที่คุณคิดว่าธรรมดา อาจเป็นสิ่งที่คนอื่นกำลังต้องการได้ยิน",
        "en": "Start by expressing what’s inside you—through speaking or writing—without waiting for perfection. What you think is ordinary may be exactly what someone else needs to hear."
    },
    4: {
        "th": "ลองหยุดแบกทุกอย่างไว้คนเดียว แล้วเริ่มแบ่งบางอย่างออกไปบ้าง ไม่ว่าจะเป็นงาน ความรับผิดชอบ หรือความคาดหวัง เพราะชีวิตคุณไม่ได้มีไว้เพื่อ “รับผิดชอบทุกอย่าง” คนเดียว",
        "en": "Stop carrying everything alone. Begin sharing responsibilities, tasks, or expectations. Your life is not meant to be something you handle entirely on your own."
    },
    5: {
        "th": "เริ่มถามตัวเองให้ชัดว่าอะไรคือสิ่งที่คุณ “อยากทำจริง” กับอะไรคือสิ่งที่คุณ “แค่ทน” แล้วค่อย ๆ ขยับออกจากสิ่งที่ไม่ใช่ทีละนิด คุณไม่ต้องหนีทันที แค่เริ่มขยับก็พอ",
        "en": "Ask yourself what you truly want and what you are only tolerating. Then slowly move away from what isn’t right. You don’t need to escape everything at once—just start shifting."
    },
    6: {
        "th": "ลองเริ่มดูแลตัวเองแบบเดียวกับที่คุณดูแลคนอื่น ตั้งขอบเขตเล็ก ๆ เช่น ไม่รับทุกอย่าง ไม่ตอบทุกคนทันที และให้เวลาตัวเองได้พักโดยไม่รู้สึกผิด",
        "en": "Start treating yourself the way you treat others. Set small boundaries—don’t accept everything, don’t respond to everyone immediately, and allow yourself to rest without guilt."
    },
    7: {
        "th": "เริ่มเปิดใจให้คนบางคนเข้ามาในโลกของคุณบ้าง ไม่ต้องทั้งหมด แค่คนที่คุณรู้สึกปลอดภัย เพราะคุณไม่จำเป็นต้องเข้าใจทุกอย่างคนเดียวตลอดไป",
        "en": "Start letting a few people into your world—just those you feel safe with. You don’t have to understand everything alone forever."
    },
    8: {
        "th": "ลองหยุดกดดันตัวเองให้ต้องสำเร็จตลอดเวลา แล้วเริ่มถามตัวเองว่า “ชีวิตแบบไหนที่คุณอยากใช้จริง ๆ” ไม่ใช่แค่ชีวิตที่ดูสำเร็จในสายตาคนอื่น",
        "en": "Stop pressuring yourself to succeed all the time. Ask yourself what kind of life you truly want—not just what looks successful to others."
    },
    9: {
        "th": "เริ่มยอมรับว่าสิ่งบางอย่างจบไปแล้ว และมันไม่ใช่ความผิดของคุณทั้งหมด คุณไม่จำเป็นต้องลืมทันที แต่คุณต้องเริ่มปล่อยทีละนิด เพื่อให้ชีวิตคุณเดินต่อได้",
        "en": "Start accepting that some things have ended—and it’s not entirely your fault. You don’t have to forget instantly, but you do need to begin letting go little by little so your life can move forward."
    },
    11: {
        "th": "เริ่มเชื่อสิ่งที่คุณรู้สึกข้างในมากขึ้น แต่ไม่ต้องเก็บไว้คนเดียว ลองแปลงมันออกมาเป็นคำพูด งาน หรือสิ่งที่คุณสร้าง เพราะสิ่งที่คุณรับรู้…มีค่ามากกว่าที่คุณคิด",
        "en": "Start trusting what you feel inside, but don’t keep it to yourself. Turn it into words, creations, or something you can share—because what you sense is more valuable than you realize."
    },
    22: {
        "th": "หยุดคิดใหญ่จนไม่กล้าเริ่ม แล้วเริ่มจากก้าวเล็ก ๆ ที่ทำได้จริงก่อน เพราะสิ่งใหญ่ที่คุณอยากสร้าง จะไม่มีวันเกิดขึ้น ถ้าคุณยังไม่เริ่มลงมือ",
        "en": "Stop overthinking the big vision and begin with small, real steps. The big thing you want to build will never exist if you don’t start taking action."
    },
    33: {
        "th": "เริ่มแยกให้ออกว่าอะไรคือการช่วยคนอื่นด้วยหัวใจ และอะไรคือการฝืนช่วยเพราะกลัวจะไม่มีคุณค่า เพราะคุณไม่จำเป็นต้องเหนื่อยเพื่อพิสูจน์ว่าคุณมีค่า",
        "en": "Start noticing the difference between helping from your heart and helping out of fear of losing your worth. You don’t have to exhaust yourself just to prove you matter."
    }
}
WARNING_TEXT = {
    1: {
        "th": "ระวังการพยายามพิสูจน์ตัวเองตลอดเวลา จนชีวิตกลายเป็นการแข่งขันที่ไม่มีวันจบ เพราะสุดท้าย…คุณจะเหนื่อยกับการเป็นคนที่ต้องเก่งตลอด โดยที่ไม่เคยได้เป็นตัวเองจริง ๆ",
        "en": "Be careful not to constantly prove yourself. Life can turn into an endless competition, leaving you exhausted from always needing to be strong—without ever being your true self."
    },
    2: {
        "th": "ระวังการเก็บทุกอย่างไว้ในใจ เพื่อรักษาความสัมพันธ์ เพราะวันหนึ่งคุณจะกลายเป็นคนที่เข้าใจทุกคน…แต่ไม่มีใครเข้าใจคุณเลย",
        "en": "Be careful not to keep everything inside just to maintain relationships. One day, you may become the one who understands everyone—but no one understands you."
    },
    3: {
        "th": "ระวังการทำเป็นโอเค ทำเป็นตลก หรือทำให้ทุกอย่างดูเบา จนไม่มีใครรู้ว่าจริง ๆ แล้วคุณกำลังรู้สึกอะไรอยู่ลึก ๆ",
        "en": "Be careful not to hide behind humor or pretend everything is okay. People may never realize what you truly feel deep inside."
    },
    4: {
        "th": "ระวังการแบกทุกอย่างไว้คนเดียว เพราะคุณจะกลายเป็นคนที่เหนื่อยที่สุด…โดยที่ไม่มีใครรู้ว่าคุณต้องการความช่วยเหลือ",
        "en": "Be careful not to carry everything alone. You may become the most exhausted person, while no one realizes you need help."
    },
    5: {
        "th": "ระวังการอยู่ในสิ่งที่ไม่ใช่นานเกินไป เพราะยิ่งคุณทนมากเท่าไหร่ คุณจะยิ่งลืมไปว่า ‘ชีวิตที่เป็นตัวเองจริง ๆ’ มันรู้สึกยังไง",
        "en": "Be careful not to stay too long in places that aren’t right for you. The longer you endure, the more you forget what it feels like to truly be yourself."
    },
    6: {
        "th": "ระวังการให้คนอื่นมากเกินไป จนวันหนึ่งคุณไม่เหลือพลังให้ตัวเอง และเริ่มรู้สึกว่าชีวิตคุณมีไว้เพื่อคนอื่นเท่านั้น",
        "en": "Be careful not to give too much to others. One day, you may have no energy left for yourself and feel like your life exists only for others."
    },
    7: {
        "th": "ระวังการถอยออกจากโลก เพราะคิดว่าไม่มีใครเข้าใจคุณ เพราะยิ่งคุณเงียบ คุณจะยิ่งโดดเดี่ยว และไม่มีใครเข้าถึงคุณได้จริง",
        "en": "Be careful not to withdraw from the world because you feel misunderstood. The more you stay silent, the more alone you become."
    },
    8: {
        "th": "ระวังการทำตัวให้แข็งแรงตลอดเวลา จนไม่มีใครกล้าเข้ามาดูแลคุณ เพราะทุกคนคิดว่าคุณไม่ต้องการใคร",
        "en": "Be careful not to appear strong all the time. People may assume you don’t need anyone, and no one will step in to support you."
    },
    9: {
        "th": "ระวังการยึดติดกับอดีตหรือคนที่จบไปแล้ว เพราะมันจะทำให้คุณไม่สามารถเปิดรับสิ่งใหม่ที่กำลังเข้ามาในชีวิตได้",
        "en": "Be careful not to stay attached to the past or people who are no longer in your life. It may block new opportunities from entering."
    },
    11: {
        "th": "ระวังการเปิดรับพลังหรือความรู้สึกของคนอื่นมากเกินไป จนคุณสับสนและหมดแรง โดยที่ไม่รู้ว่าอะไรคือของคุณจริง ๆ",
        "en": "Be careful not to absorb too much from others. It can leave you confused and drained, unable to tell what truly belongs to you."
    },
    22: {
        "th": "ระวังการกดดันตัวเองด้วยความคาดหวังที่สูงเกินไป จนคุณไม่กล้าเริ่ม เพราะกลัวว่าจะทำได้ไม่ดีพอ",
        "en": "Be careful not to pressure yourself with unrealistic expectations. You may end up not starting at all out of fear of not doing it perfectly."
    },
    33: {
        "th": "ระวังการช่วยคนอื่นจนลืมตัวเอง เพราะสุดท้ายคุณจะเป็นคนที่เหนื่อยที่สุด แต่ไม่มีใครรู้ว่าคุณกำลังหมดแรง",
        "en": "Be careful not to help others so much that you forget yourself. In the end, you may be the most exhausted person—and no one will even notice."
    }
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
# Page gate
# -----------------------------
if st.session_state.page == "ebook":
    render_ebook_page()
    st.write("---")
    st.markdown(
        f"<p style='text-align: center; font-size: 0.82rem; color: #888;'>© 2026 LUMINA SOUL | {tr('พื้นที่สะท้อนชีวิตและการตื่นรู้', 'A space for reflection and awakening')}</p>",
        unsafe_allow_html=True
    )
    st.stop()


# -----------------------------
# Header
# -----------------------------
st.markdown(
    f"""
    <div class="nav-shell">
        <div class="brand-mini">LUMINA SOUL</div>
        <div class="top-actions">
            <a href="{LINE_LINK}" target="_blank" class="top-link-chip line">💬 LINE</a>
            <div class="lang-group">
                <a href="?lang=th&page={st.session_state.page}" class="lang-pill {'active' if st.session_state.lang == 'th' else ''}">TH</a>
                <a href="?lang=en&page={st.session_state.page}" class="lang-pill {'active' if st.session_state.lang == 'en' else ''}">EN</a>
            </div>
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    <div class="hero-orb-wrap">
        <div class="hero-orb"><div class="hero-orb-inner">🔮</div></div>
    </div>
    <div class="hero-kicker">DECODE YOUR COSMIC BLUEPRINT</div>
    <div class="hero-title-center">{tr('พิมพ์เขียวชีวิต', 'LIFE BLUEPRINT')}</div>
    <div class="hero-sub-center">{tr('คุณเกิดมาทำอะไร? จักรวาลมีคำตอบ', 'Why were you born? The universe has answers')}</div>
    <div class="hero-meta">{tr('โหราศาสตร์ · พลังงาน · จิตวิญญาณ · การสะท้อนชีวิตเฉพาะคุณ', 'Astrology · Energy · Spiritual reflection · Personal life decoding')}</div>
    """,
    unsafe_allow_html=True
)

st.markdown(f"<div class='section-kicker'>{tr('สิ่งที่คุณจะค้นพบ', 'WHAT YOU WILL DISCOVER')}</div>", unsafe_allow_html=True)
feature_cards = [
    ("🪐", tr("ตัวตนจักรวาล", "Cosmic identity"), tr("ราศี พลังวันเกิด และภาพรวมพลังงาน", "Zodiac, birth energy, and your overall energetic profile")),
    ("🔮", tr("นิสัยลึกที่ซ่อนอยู่", "Hidden inner traits"), tr("ด้านในที่คนรอบตัวอาจไม่เคยรู้", "The inner side that others may not fully see")),
    ("💫", tr("รูปแบบอารมณ์", "Emotional pattern"), tr("เวลาคุณรู้สึกลึกจริง ๆ คุณเป็นแบบไหน", "How you tend to feel when emotions run deep")),
    ("🗝️", tr("สัญญาณจักรวาล", "Life signals"), tr("สิ่งที่ชีวิตกำลังพยายามบอกคุณอยู่", "What life may be trying to tell you right now")),
    ("🌌", tr("ภารกิจชีวิต", "Life mission"), tr("แนวทางที่พลังของคุณอยากพาไป", "The direction your energy wants to move toward")),
    ("💼", tr("งานและเส้นทางที่ใช่", "Career alignment"), tr("พลังที่เหมาะกับงานและการสร้างตัว", "The work energy that fits your real path")),
    ("🌑", tr("เงาชีวิตและบทเรียน", "Shadow and lessons"), tr("สิ่งที่คุณต้องก้าวผ่านเพื่อโตขึ้น", "The lesson life may be asking you to move through")),
    ("📅", tr("Timeline พลังงาน", "Energy timeline"), tr("ช่วงเวลาที่ควรฟังหัวใจตัวเองให้ชัด", "Periods when you should listen to yourself more clearly")),
]
feature_html = '<div class="feature-grid">'
for icon, title, desc in feature_cards:
    feature_html += f"<div class='feature-card'><div class='feature-icon'>{icon}</div><div><div class='feature-title'>{title}</div><div class='feature-text'>{desc}</div></div></div>"
feature_html += '</div>'
st.markdown(feature_html, unsafe_allow_html=True)


# -----------------------------
# Form
# -----------------------------
month_display_list = [m["th"] if st.session_state.lang == "th" else m["en"] for m in month_options]
category_display_list = [c["th"] if st.session_state.lang == "th" else c["en"] for c in categories]

st.markdown(f"<div class='section-kicker' style='margin-top:22px;'>{tr('เริ่มต้นการเดินทาง', 'BEGIN YOUR JOURNEY')}</div>", unsafe_allow_html=True)
st.markdown(f"<p class='center-text soft-note' style='margin-top:-6px; margin-bottom:12px;'>{tr('กรอกข้อมูลเพื่อเริ่มอ่านพิมพ์เขียวชีวิตของคุณ', 'Fill in your details to begin decoding your life blueprint')}</p>", unsafe_allow_html=True)
st.markdown("<div class='form-shell'>", unsafe_allow_html=True)

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

st.markdown("</div>", unsafe_allow_html=True)

st.markdown(
    f"""
    <div class="glow-box">
        <p style="margin:0; color:#3576c5 !important; font-weight:600; text-align:center;">
        {tr(
            '✨ บางคำตอบในชีวิต อาจเริ่มต้นจากการเข้าใจพลังงานของตัวเอง',
            '✨ Some answers in life may begin with understanding your own energy'
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

        with st.spinner(tr("กำลังถอดรหัสพลังงานของคุณ...", "Decoding your energy...")):
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
                <p>{tr("สิ่งที่คุณได้อ่านในตอนนี้ คือคำสะท้อนชั้นแรกของพลังงานชีวิตคุณ", "What you have read so far is only the first layer of your life energy.")}</p>
                <p>{tr("หากต้องการอ่านลึกต่อ คุณจะได้เห็นหัวข้อเหล่านี้แบบเฉพาะตัว:", "If you want to go deeper, these are the areas waiting to be revealed for you:")}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

        locked_items = [
            ("🌌", tr("ภารกิจชีวิต", "Life mission"), tr("แนวทางที่พลังของคุณอยากพาไป", "The deeper path your energy wants to move toward")),
            ("🔮", tr("นิสัยลึกที่ซ่อนอยู่", "Hidden inner traits"), tr("ด้านในที่คนรอบตัวอาจไม่เคยรู้", "The side of you others may never fully see")),
            ("🌑", tr("เงาชีวิตและบทเรียน", "Shadow and lessons"), tr("สิ่งที่คุณต้องก้าวผ่านเพื่อโตขึ้น", "What life is asking you to move through")),
            ("💼", tr("งานและเส้นทางที่ใช่", "Career alignment"), tr("พลังที่เหมาะกับงานและการสร้างตัว", "The work and direction that fit your energy")),
            ("💞", tr("ความรักและความสัมพันธ์", "Love and relationships"), tr("รูปแบบความรักที่สะท้อนหัวใจคุณ", "How your heart tends to love and attach")),
            ("💰", tr("กระแสการเงิน", "Financial flow"), tr("รูปแบบพลังงานด้านการรับและการสร้างคุณค่า", "How your energy relates to value and receiving")),
            ("📅", tr("Timeline พลังงาน", "Energy timeline"), tr("ช่วงเวลาที่ควรฟังหัวใจตัวเองให้ชัด", "When to listen to yourself more clearly")),
            ("🪄", tr("แนวทางต่อจากนี้", "Your next step"), tr("สิ่งที่ควรโฟกัสเพื่อให้ชีวิตขยับ", "What to focus on next so life can move")),
        ]
        lock_html = '<div class="feature-grid" style="margin-top:10px;">'
        for icon, title, desc in locked_items:
            lock_html += f"<div class='feature-card'><div class='feature-icon'>{icon}</div><div><div class='feature-title'>🔒 {title}</div><div class='feature-text'>{desc}</div></div></div>"
        lock_html += '</div>'
        st.markdown(lock_html, unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="result-next-card">
                <h4 style="color:#8e24aa; margin-top:0; text-align:center;">{tr('อยากอ่านพิมพ์เขียวชีวิตฉบับลึกไหม', 'Want your deeper life blueprint?')}</h4>
                <p class="center-text">{tr('หากคำอ่านนี้ตรงกับใจคุณ คำอ่านฉบับเต็มจะช่วยให้คุณเห็นทั้งแพทเทิร์นชีวิต จุดติดค้าง และทิศทางที่เหมาะกับพลังงานของคุณจริง ๆ', 'If this resonates, the full reading helps you see your deeper patterns, what still feels unresolved, and the direction that truly fits your energy.')}</p>
                <p class="center-text soft-note" style="margin-top:-6px;">{tr('คำอ่านเชิงลึกเฉพาะคุณ · ราคา 1,111 บาท · ติดต่อผ่าน LINE', 'Personal deep reading · 1,111 THB · contact via LINE')}</p>
                <div class="cta-button-row">
                    <a href="{LINE_LINK}" target="_blank" class="center-button-link line">💬 {tr('ติดต่อ LINE เพื่ออ่านลึก', 'Contact LINE for deep reading')}</a>
                </div>
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


if st.session_state.latest_result:
    st.markdown(
        f"""
        <div class="result-next-card">
            <h4 style="color:#8e24aa; margin-top:0; text-align:center;">📖 {tr('eBook สำหรับคนที่อยากค่อย ๆ กลับมาเจอตัวเอง', 'An eBook for gently returning to yourself')}</h4>
            <p class="center-text" style="margin-bottom:14px;">{tr('ถ้าคำอ่านนี้สะท้อนใจคุณจริง eBook ของ LUMINA SOUL จะช่วยโอบประคองหัวใจ และค่อย ๆ พาคุณผ่านช่วงชีวิตที่กำลังสั่นไหวอยู่ตอนนี้', 'If this reading resonates, the LUMINA SOUL eBook gently supports your heart and helps you move through the season you are in.')}</p>
            <img src="{get_cover_data_uri()}" class="ebook-cover" alt="LUMINA SOUL eBook cover" style="width:min(220px,70vw); margin-bottom:14px;">
            <div class="cta-button-row">
                <a href="{get_page_link('ebook')}" class="center-button-link soft">📖 {tr('ดูรายละเอียด eBook', 'See eBook details')}</a>
                <a href="{LINE_LINK}" target="_blank" class="center-button-link line">💬 {tr('สั่งซื้อผ่าน LINE', 'Order via LINE')}</a>
            </div>
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
