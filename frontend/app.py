import streamlit as st
import requests
import os

BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Sales Forecast",
    page_icon="📈",
    layout="centered",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

/* ── Reset & root ── */
:root {
    --bg:        #0a0a0f;
    --surface:   #111118;
    --card:      #16161f;
    --border:    #2a2a3a;
    --accent:    #ff6b35;
    --accent2:   #ffb800;
    --text:      #e8e8f0;
    --muted:     #6b6b80;
    --success:   #00e5a0;
    --font-head: 'Syne', sans-serif;
    --font-mono: 'DM Mono', monospace;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg) !important;
    color: var(--text) !important;
}

[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(ellipse 80% 40% at 50% -10%, rgba(255,107,53,.18) 0%, transparent 65%),
        radial-gradient(ellipse 60% 30% at 80% 80%,  rgba(255,184,0,.10)  0%, transparent 60%),
        var(--bg) !important;
}

[data-testid="stHeader"]          { background: transparent !important; }
[data-testid="stToolbar"]         { display: none; }
.block-container {
    max-width: 760px !important;
    padding: 3rem 2rem 6rem !important;
}

/* ── Hero heading ── */
.hero {
    text-align: center;
    padding: 2.5rem 0 2rem;
    margin-bottom: 2rem;
}
.hero-eyebrow {
    font-family: var(--font-mono);
    font-size: .72rem;
    letter-spacing: .25em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: .75rem;
}
.hero h1 {
    font-family: var(--font-head) !important;
    font-size: clamp(2.4rem, 6vw, 3.6rem) !important;
    font-weight: 800 !important;
    line-height: 1.05 !important;
    color: var(--text) !important;
    margin: 0 !important;
    padding: 0 !important;
}
.hero h1 span {
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-family: var(--font-mono);
    font-size: .82rem;
    color: var(--muted);
    margin-top: .9rem;
}

/* ── Section cards ── */
.section-card {
    background: var(--card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 1.6rem 1.8rem 1.4rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
}
.section-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    opacity: .6;
}
.section-label {
    font-family: var(--font-mono);
    font-size: .65rem;
    letter-spacing: .2em;
    text-transform: uppercase;
    color: var(--accent);
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: .5rem;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── Streamlit widget resets ── */
label, .stSelectbox label, .stNumberInput label, .stDateInput label {
    font-family: var(--font-head) !important;
    font-size: .78rem !important;
    font-weight: 600 !important;
    letter-spacing: .04em !important;
    color: var(--muted) !important;
    text-transform: uppercase !important;
    margin-bottom: .25rem !important;
}

/* inputs */
input[type="number"],
input[type="text"],
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div,
[data-testid="stDateInput"] input {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text) !important;
    font-family: var(--font-mono) !important;
    font-size: .92rem !important;
    transition: border-color .2s !important;
}
input:focus, div[data-baseweb="select"]:focus-within > div {
    border-color: var(--accent) !important;
    box-shadow: 0 0 0 3px rgba(255,107,53,.15) !important;
}

/* dropdown menu */
[data-baseweb="popover"] [role="listbox"] {
    background: #1c1c28 !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
}
[data-baseweb="popover"] [role="option"] {
    font-family: var(--font-mono) !important;
    font-size: .88rem !important;
    color: var(--text) !important;
}
[data-baseweb="popover"] [role="option"]:hover,
[data-baseweb="popover"] [aria-selected="true"] {
    background: rgba(255,107,53,.15) !important;
    color: var(--accent) !important;
}

/* number input arrows */
button[aria-label="increment"], button[aria-label="decrement"],
button[kind="secondary"] {
    background: var(--surface) !important;
    border: 1px solid var(--border) !important;
    color: var(--muted) !important;
    border-radius: 8px !important;
}

/* ── CTA Button ── */
.stButton > button {
    width: 100% !important;
    margin-top: .5rem !important;
    padding: 1rem 2rem !important;
    background: linear-gradient(135deg, var(--accent) 0%, var(--accent2) 100%) !important;
    color: #0a0a0f !important;
    font-family: var(--font-head) !important;
    font-size: 1rem !important;
    font-weight: 800 !important;
    letter-spacing: .06em !important;
    text-transform: uppercase !important;
    border: none !important;
    border-radius: 12px !important;
    cursor: pointer !important;
    transition: opacity .2s, transform .15s !important;
    box-shadow: 0 8px 30px rgba(255,107,53,.35) !important;
}
.stButton > button:hover {
    opacity: .9 !important;
    transform: translateY(-2px) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Success / Error banners ── */
[data-testid="stAlert"] {
    border-radius: 12px !important;
    border: none !important;
    font-family: var(--font-mono) !important;
}
div[data-baseweb="notification"][kind="positive"] {
    background: rgba(0,229,160,.1) !important;
    border-left: 3px solid var(--success) !important;
}
div[data-baseweb="notification"][kind="negative"] {
    background: rgba(255,107,53,.1) !important;
    border-left: 3px solid var(--accent) !important;
}

/* ── Result display ── */
.result-box {
    background: linear-gradient(135deg, rgba(255,107,53,.08), rgba(255,184,0,.08));
    border: 1px solid rgba(255,107,53,.3);
    border-radius: 16px;
    padding: 2rem;
    text-align: center;
    margin-top: 1.2rem;
}
.result-label {
    font-family: var(--font-mono);
    font-size: .68rem;
    letter-spacing: .22em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: .5rem;
}
.result-value {
    font-family: var(--font-head);
    font-size: 3rem;
    font-weight: 800;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

/* ── Divider ── */
hr { border-color: var(--border) !important; margin: 1.6rem 0 !important; }

/* ── Scrollbar ── */
::-webkit-scrollbar       { width: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">↗ Predictive Analytics</div>
    <h1>Sales<br><span>Forecast</span></h1>
    <div class="hero-sub">Enter store parameters to predict daily revenue</div>
</div>
""", unsafe_allow_html=True)

# ── Section 1 — Store Identity ────────────────────────────────────────────────
st.markdown('<div class="section-card"><div class="section-label">01 &nbsp; Store Identity</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1:
    store = st.number_input("Store ID", min_value=1, value=1000, step=1)
with col2:
    day_of_week = st.number_input("Day of Week", min_value=1, step=1, max_value=7)

col3, col4 = st.columns(2)
with col3:
    store_type = st.selectbox("Store Type", ["a", "b", "c", "d"])
with col4:
    assortment = st.selectbox("Assortment", ["a", "b", "c"])

st.markdown('</div>', unsafe_allow_html=True)

# ── Section 2 — Date & Status ─────────────────────────────────────────────────
st.markdown('<div class="section-card"><div class="section-label">02 &nbsp; Date & Status</div>', unsafe_allow_html=True)

col5, col6 = st.columns(2)
with col5:
    date = st.date_input("Date")
    date_str = date.strftime("%Y-%m-%d")
with col6:
    open_status = st.selectbox("Open", ["Yes", "No"])
    open_value = 1 if open_status == "Yes" else 0

col7, col8 = st.columns(2)
with col7:
    state_holiday = st.selectbox("State Holiday", ["0", "a", "b", "c"])
with col8:
    school_holiday = st.selectbox("School Holiday", ["Yes", "no"])
    school_holiday_value = 1 if school_holiday == "Yes" else 0

st.markdown('</div>', unsafe_allow_html=True)

# ── Section 3 — Promotions ────────────────────────────────────────────────────
st.markdown('<div class="section-card"><div class="section-label">03 &nbsp; Promotions</div>', unsafe_allow_html=True)

col9, col10 = st.columns(2)
with col9:
    promo = st.selectbox("Promo", ['Yes', 'No'])
    promo_value = 1 if promo == 'Yes' else 0
with col10:
    promo2 = st.selectbox("Promo 2", ['Yes', 'No'])
    promo2_value = 1 if promo2 == 'Yes' else 0

col11, col12, col13 = st.columns(3)
with col11:
    promo2_since_week = st.number_input("Promo 2 Since Week", min_value=1, step=1, max_value=50)
with col12:
    promo2_since_year = st.number_input("Promo 2 Since Year", min_value=2009, step=1, max_value=2015)
with col13:
    promo_interval = st.selectbox("Promo Interval", ['Jan,Apr,Jul,Oct', 'Feb,May,Aug,Nov', 'Mar,Jun,Sept,Dec'])

st.markdown('</div>', unsafe_allow_html=True)

# ── Section 4 — Competition ───────────────────────────────────────────────────
st.markdown('<div class="section-card"><div class="section-label">04 &nbsp; Competition</div>', unsafe_allow_html=True)

col14, col15, col16 = st.columns(3)
with col14:
    competition_distance = st.number_input("Competition Distance", min_value=0, step=1, max_value=100000)
with col15:
    competition_open_since_month = st.number_input("Comp. Open Since Month", min_value=1, step=1, max_value=12)
with col16:
    competition_open_since_year = st.number_input("Comp. Open Since Year", min_value=1900, step=1, max_value=2016)

st.markdown('</div>', unsafe_allow_html=True)

# ── CTA ───────────────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

if st.button("⚡ Run Forecast"):
    try:
        payload = {
            "Store": store,
            "DayOfWeek": day_of_week,
            "Date": date_str,
            "Open": open_value,
            "Promo": promo_value,
            "StateHoliday": state_holiday,
            "SchoolHoliday": school_holiday_value,
            "StoreType": store_type,
            "Assortment": assortment,
            "CompetitionDistance": competition_distance,
            "CompetitionOpenSinceMonth": competition_open_since_month,
            "CompetitionOpenSinceYear": competition_open_since_year,
            "Promo2": promo2_value,
            "Promo2SinceWeek": promo2_since_week,
            "Promo2SinceYear": promo2_since_year,
            "PromoInterval": promo_interval
        }

        with st.spinner("Waking up backend & forecasting..."):
            response = requests.post(
                f"{BACKEND_URL}/predict",
                json=payload,
                timeout=60
            )

        if response.status_code != 200:
            st.error(f"Backend error {response.status_code}: {response.text}")
        else:
            predicted = response.json()["predicted_sales"]

            st.markdown(f"""
            <div class="result-box">
                <div class="result-label">Predicted Sales</div>
                <div class="result-value">{predicted:.2f}</div>
            </div>
            """, unsafe_allow_html=True)

    except requests.exceptions.Timeout:
        st.error("Request timed out. The backend is waking up — please try again in 30 seconds.")
    except requests.exceptions.ConnectionError:
        st.error(f"Cannot connect to backend at {BACKEND_URL}. Check that the Render service is running.")
    except Exception as e:
        st.error(f"Error: {e}")