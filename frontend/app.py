import os
import streamlit as st
import requests
import json

# ─── Page Config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Student Performance Predictor",
    page_icon="🎓",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# ─── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

  html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
  }

  .stApp {
    background: #0d0f14;
    color: #e8e6e1;
  }

  /* ── Hero Header ── */
  .hero {
    text-align: center;
    padding: 3rem 1rem 2rem;
  }
  .hero-badge {
    display: inline-block;
    background: rgba(99, 217, 149, 0.12);
    color: #63d995;
    border: 1px solid rgba(99, 217, 149, 0.3);
    border-radius: 20px;
    padding: 4px 14px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    margin-bottom: 1rem;
  }
  .hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2rem, 5vw, 3.2rem);
    font-weight: 800;
    line-height: 1.1;
    color: #f0ede8;
    margin: 0 0 0.75rem;
  }
  .hero-title span {
    color: #63d995;
  }
  .hero-sub {
    font-size: 0.95rem;
    color: #7a7870;
    font-weight: 300;
    letter-spacing: 0.02em;
  }

  /* ── Card / Panel ── */
  .panel {
    background: #161920;
    border: 1px solid #1f2330;
    border-radius: 16px;
    padding: 2rem;
    margin: 1.5rem 0;
  }
  .panel-title {
    font-family: 'Syne', sans-serif;
    font-size: 0.78rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #63d995;
    margin-bottom: 1.4rem;
  }

  /* ── Sliders & Inputs ── */
  .stSlider > div > div > div > div {
    background: #63d995 !important;
  }
  .stSlider [data-testid="stThumbValue"] {
    color: #63d995;
  }
  label[data-testid="stWidgetLabel"] {
    font-size: 0.83rem !important;
    font-weight: 500 !important;
    color: #b0aca4 !important;
    letter-spacing: 0.03em;
  }

  /* ── Radio ── */
  .stRadio > label { display: none; }
  .stRadio [data-testid="stMarkdownContainer"] p {
    font-size: 0.83rem;
    color: #b0aca4;
    font-weight: 500;
    letter-spacing: 0.03em;
  }

  /* ── Button ── */
  .stButton > button {
    background: #63d995 !important;
    color: #0d0f14 !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.06em !important;
    text-transform: uppercase !important;
    padding: 0.7rem 2rem !important;
    width: 100%;
    transition: all 0.2s ease !important;
  }
  .stButton > button:hover {
    background: #7fe8ab !important;
    box-shadow: 0 0 24px rgba(99, 217, 149, 0.35) !important;
  }

  /* ── Result Cards ── */
  .result-pass {
    background: linear-gradient(135deg, rgba(99,217,149,0.10), rgba(99,217,149,0.04));
    border: 1px solid rgba(99,217,149,0.35);
    border-radius: 14px;
    padding: 1.8rem;
    text-align: center;
  }
  .result-fail {
    background: linear-gradient(135deg, rgba(255,99,99,0.10), rgba(255,99,99,0.04));
    border: 1px solid rgba(255,99,99,0.35);
    border-radius: 14px;
    padding: 1.8rem;
    text-align: center;
  }
  .result-verdict {
    font-family: 'Syne', sans-serif;
    font-size: 2.4rem;
    font-weight: 800;
    margin-bottom: 0.3rem;
  }
  .result-verdict.pass { color: #63d995; }
  .result-verdict.fail { color: #ff6363; }
  .result-label {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #7a7870;
  }

  /* ── Probability Bar ── */
  .prob-row {
    display: flex;
    align-items: center;
    gap: 0.75rem;
    margin: 0.6rem 0;
  }
  .prob-label {
    font-size: 0.78rem;
    font-weight: 500;
    color: #7a7870;
    width: 40px;
    text-align: right;
  }
  .prob-bar-wrap {
    flex: 1;
    background: #1f2330;
    border-radius: 6px;
    height: 8px;
    overflow: hidden;
  }
  .prob-bar-fill-pass {
    height: 100%;
    border-radius: 6px;
    background: linear-gradient(90deg, #63d995, #7fe8ab);
    transition: width 0.8s ease;
  }
  .prob-bar-fill-fail {
    height: 100%;
    border-radius: 6px;
    background: linear-gradient(90deg, #ff6363, #ff8a8a);
  }
  .prob-pct {
    font-family: 'Syne', sans-serif;
    font-size: 0.8rem;
    font-weight: 700;
    width: 42px;
    color: #e8e6e1;
  }

  /* ── Divider ── */
  hr { border-color: #1f2330 !important; }

  /* ── Error / Info ── */
  .stAlert { border-radius: 10px !important; }

  /* ── Footer ── */
  .footer {
    text-align: center;
    padding: 2rem 0 1rem;
    font-size: 0.73rem;
    color: #3a3830;
    letter-spacing: 0.05em;
  }
</style>
""", unsafe_allow_html=True)

# ─── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
  <div class="hero-badge">🎓 ML-Powered</div>
  <h1 class="hero-title">Student Performance<br><span>Predictor</span></h1>
  <p class="hero-sub">Logistic Regression · Pass / Fail Classification</p>
</div>
""", unsafe_allow_html=True)

# ─── API Config ────────────────────────────────────────────────────────────────
# Use Railway private networking for secure, fast backend communication.
# Allow overriding for local development via BACKEND_URL.
DEFAULT_BACKEND = os.getenv(
    "BACKEND_URL",
    "http://backend.railway.internal:8001"
)

API_URL = st.sidebar.text_input(
    "API Base URL",
    value=DEFAULT_BACKEND,
    help="Railway private networking URL for FastAPI backend (or override for local development)"
)

# ─── Input Panel ───────────────────────────────────────────────────────────────
st.markdown('<div class="panel"><div class="panel-title">📋 Student Profile</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    hours_studied = st.slider(
        "Hours Studied per Day",
        min_value=1.0, max_value=9.0,
        value=5.0, step=0.5,
        help="Range: 1–9 hours"
    )
    previous_scores = st.slider(
        "Previous Test Score",
        min_value=40.0, max_value=100.0,
        value=70.0, step=1.0,
        help="Range: 40–100"
    )
    sleep_hours = st.slider(
        "Sleep Hours per Night",
        min_value=4.0, max_value=9.0,
        value=7.0, step=0.5,
        help="Range: 4–9 hours"
    )

with col2:
    sample_papers = st.slider(
        "Sample Papers Practiced",
        min_value=0, max_value=9,
        value=3, step=1,
        help="Range: 0–9 papers"
    )
    st.markdown("**Extracurricular Activities**")
    extracurricular = st.radio(
        "Extracurricular Activities",
        options=["Yes", "No"],
        horizontal=True,
        label_visibility="collapsed"
    )

st.markdown('</div>', unsafe_allow_html=True)

# ─── Predict Button ────────────────────────────────────────────────────────────
predict_clicked = st.button("⚡ Predict Performance")

# ─── Prediction Logic ──────────────────────────────────────────────────────────
if predict_clicked:
    payload = {
        "hours_studied": hours_studied,
        "previous_scores": previous_scores,
        "extracurricular_activities": 1 if extracurricular == "Yes" else 0,
        "sleep_hours": sleep_hours,
        "sample_question_papers": sample_papers
    }

    with st.spinner("Running prediction..."):
        try:
            response = requests.post(f"{API_URL}/predict", json=payload, timeout=10)
            response.raise_for_status()
            result = response.json()

            verdict = result["prediction"]
            confidence = result["confidence_score"]
            pass_prob = result["pass_probability"]
            fail_prob = result["fail_probability"]

            # ── Result Card ──
            css_class = "result-pass" if verdict == "Pass" else "result-fail"
            verdict_class = "pass" if verdict == "Pass" else "fail"
            emoji = "✅" if verdict == "Pass" else "❌"

            st.markdown(f"""
            <div class="{css_class}">
              <div class="result-verdict {verdict_class}">{emoji} {verdict}</div>
              <div class="result-label">Confidence · {confidence:.1%}</div>
            </div>
            """, unsafe_allow_html=True)

            # ── Probability Breakdown ──
            st.markdown('<div class="panel"><div class="panel-title">📊 Probability Breakdown</div>', unsafe_allow_html=True)

            pass_pct = int(pass_prob * 100)
            fail_pct = int(fail_prob * 100)

            st.markdown(f"""
            <div class="prob-row">
              <div class="prob-label">Pass</div>
              <div class="prob-bar-wrap">
                <div class="prob-bar-fill-pass" style="width:{pass_pct}%"></div>
              </div>
              <div class="prob-pct">{pass_pct}%</div>
            </div>
            <div class="prob-row">
              <div class="prob-label">Fail</div>
              <div class="prob-bar-wrap">
                <div class="prob-bar-fill-fail" style="width:{fail_pct}%"></div>
              </div>
              <div class="prob-pct">{fail_pct}%</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('</div>', unsafe_allow_html=True)

            # ── Input Summary ──
            with st.expander("🔍 Input Summary"):
                st.json(payload)

        except requests.exceptions.ConnectionError:
            st.error(f"❌ Cannot connect to the API at `{API_URL}`. Make sure your FastAPI server is running.")
        except requests.exceptions.Timeout:
            st.error("⏱️ Request timed out. The server took too long to respond.")
        except requests.exceptions.HTTPError as e:
            try:
                detail = response.json().get("detail", str(e))
            except Exception:
                detail = str(e)
            st.error(f"⚠️ API Error: {detail}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")

# ─── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
  Powered by Logistic Regression · FastAPI · Streamlit
</div>
""", unsafe_allow_html=True)
