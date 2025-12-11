import streamlit as st
import time
import numpy as np
import pandas as pd
import altair as alt
import os
import hashlib
import sqlite3
from pathlib import Path
from datetime import datetime
import json
from io import BytesIO
try:
    from reportlab.lib.pagesizes import A4
    from reportlab.pdfgen import canvas
    from reportlab.lib.utils import simpleSplit  # for wrapping
except ImportError:
    A4 = None
    canvas = None
    simpleSplit = None


# ---------------------------------------------------------
# DESIGN SYSTEM – NeuroRisk AI
# ---------------------------------------------------------
PRIMARY_COLOR = "#06436D"
SECONDARY_COLOR = "#0B6AA4"
ACCENT_COLOR = "#F0F6FB"
SUCCESS_COLOR = "#10B981"
WARNING_COLOR = "#F59E0B"
DANGER_COLOR = "#EF4444"
TEXT_PRIMARY = "#1F2937"
TEXT_SECONDARY = "#6B7280"
TEXT_BUTTON = "#FFFFFF"  # White text for buttons
BACKGROUND_LIGHT = "#FFFFFF"
BACKGROUND_SUBTLE = "#F9FAFB"
BORDER_COLOR = "#E5E7EB"

# ---------------------------------------------------------
# Base Configuration & Branding
# ---------------------------------------------------------
st.set_page_config(
    page_title="NeuroRiskAI",
    page_icon="🧠",
    layout="centered"
)

st.markdown(
    f"""
    <style>
    /* Additional styles - does NOT override button styles */
    .neuro-card {{
        padding: 1rem 1.25rem;
        border-radius: 0.75rem;
        border: 1px solid #e5e7eb;
        background-color: #f9fafb;
        margin-bottom: 1rem;
    }}
    .neuro-phase-intro {{
        padding: 1.25rem 1.5rem;
        border-radius: 0.75rem;
        border: 1px solid #d1e3f0;
        background-color: #f2f7fb;
        margin-bottom: 1rem;
    }}
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# GLOBAL CSS – Professional B2C Design
# ---------------------------------------------------------
st.markdown(
    f"""
    <style>
    /* Force light theme regardless of device settings */
    :root {{
        color-scheme: light !important;
    }}
    html, body, .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stHeader"],
    [data-testid="stSidebar"],
    .main, .block-container {{
        background-color: #ffffff !important;
        color: {TEXT_PRIMARY} !important;
    }}
    @media (prefers-color-scheme: dark) {{
        :root {{ color-scheme: light !important; }}
        html, body, .stApp,
        [data-testid="stAppViewContainer"],
        [data-testid="stHeader"],
        [data-testid="stSidebar"],
        .main, .block-container {{
            background-color: #ffffff !important;
            color: {TEXT_PRIMARY} !important;
        }}
    }}

    /* ===== TYPOGRAPHY ===== */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    html, body, [class*="css"] {{
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
        color: {TEXT_PRIMARY};
    }}
    
    h1, h2, h3, h4, h5, h6 {{
        font-family: 'Inter', sans-serif;
        color: {PRIMARY_COLOR};
        font-weight: 700;
        letter-spacing: -0.02em;
    }}
    
    h1 {{ font-size: 2.5rem; line-height: 1.2; }}
    h2 {{ font-size: 1.875rem; line-height: 1.3; }}
    h3 {{ font-size: 1.5rem; line-height: 1.4; }}
    h4 {{ font-size: 0.8rem; line-height: 0.9; }}
    
    p, li {{ 
        color: {TEXT_SECONDARY}; 
        line-height: 1.6;
        font-size: 1rem;
    }}
 

    /* ===== LAYOUT CONTAINER ===== */
    .main .block-container {{
        max-width: 900px;
        padding: 2rem 1.5rem 4rem;
    }}
    
     /* ===== DECORATIVE CIRCLES (Brand Element) - MEHRERE KREISE ===== */
    .neuro-bg-circles {{
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        width: 100% !important;
        height: 100% !important;
        pointer-events: none !important;
        z-index: 0 !important;
        overflow: visible !important;
    }}
    
    /* Kreis 1: Oben links */
    .neuro-bg-circles::before {{
        content: '' !important;
        position: absolute !important;
        top: -250px !important;
        left: -500px !important;
        width: 400px !important;
        height: 400px !important;
        border-radius: 50% !important;
        border: 60px solid {PRIMARY_COLOR} !important;
        opacity: 1 !important;
        pointer-events: none !important;
    }}

 

    /* ===== CARDS ===== */
    .neuro-card {{
        background: {BACKGROUND_LIGHT};
        border: 1px solid {BORDER_COLOR};
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.25rem;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 1px 2px rgba(0,0,0,0.06);
        transition: box-shadow 0.2s ease, transform 0.2s ease;
    }}
    
    .neuro-card:hover {{
        box-shadow: 0 4px 12px rgba(6,67,109,0.08);
    }}
    
    .neuro-card h3 {{
        margin-top: 0;
        margin-bottom: 0.75rem;
        font-size: 1.25rem;
    }}
    
    .neuro-card p {{
        margin-bottom: 0;
    }}
    
    /* Hero Card */
    .neuro-hero {{
        background: linear-gradient(135deg, {ACCENT_COLOR} 0%, {BACKGROUND_LIGHT} 100%);
        border: 1px solid {PRIMARY_COLOR}20;
        border-radius: 20px;
        padding: 2.5rem 2rem;
        text-align: center;
        margin-bottom: 2rem;
    }}
    
    .neuro-hero h2 {{
        font-size: 1.75rem;
        margin-bottom: 1rem;
        color: {PRIMARY_COLOR};
    }}
    
    .neuro-hero p {{
        font-size: 1.1rem;
        color: {TEXT_SECONDARY};
        max-width: 600px;
        margin: 0 auto 1.5rem;
    }}
    
    /* Phase Intro Card */
    .neuro-phase-intro {{
        background: linear-gradient(135deg, {ACCENT_COLOR} 0%, #E8F4FD 100%);
        border: 1px solid {PRIMARY_COLOR}25;
        border-radius: 16px;
        padding: 1.75rem;
        margin-bottom: 1.5rem;
    }}
    
    .neuro-phase-intro h3 {{
        color: {PRIMARY_COLOR};
        margin-top: 0;
    }}
    
    /* Glass Card (for questions) */
    .neuro-glass {{
        background: rgba(255,255,255,0.85);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(6,67,109,0.1);
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }}
    
    /* ===== BUTTONS ===== */
    .stButton > button {{
        background: linear-gradient(135deg, {PRIMARY_COLOR} 0%, {SECONDARY_COLOR} 100%) !important;
        color: {TEXT_BUTTON} !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.75rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        letter-spacing: 0.01em !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(6,67,109,0.25) !important;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 16px rgba(6,67,109,0.35) !important;
        color: {TEXT_BUTTON} !important;
    }}
    
    .stButton > button:active {{
        transform: translateY(0) !important;
        color: {TEXT_BUTTON} !important;
    }}
    
    .stButton > button p,
    .stButton > button span,
    .stButton > button div {{
        color: {TEXT_BUTTON} !important;
    }}
    
    /* Form Submit Buttons */
    .stFormSubmitButton > button {{
        background: linear-gradient(135deg, {PRIMARY_COLOR} 0%, {SECONDARY_COLOR} 100%) !important;
        color: {TEXT_BUTTON} !important;
        border: none !important;
        border-radius: 12px !important;
        padding: 0.75rem 1.75rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        letter-spacing: 0.01em !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 2px 8px rgba(6,67,109,0.25) !important;
    }}
    
    .stFormSubmitButton > button:hover {{
        transform: translateY(-1px) !important;
        box-shadow: 0 4px 16px rgba(6,67,109,0.35) !important;
        color: {TEXT_BUTTON} !important;
    }}
    
    .stFormSubmitButton > button p,
    .stFormSubmitButton > button span,
    .stFormSubmitButton > button div {{
        color: {TEXT_BUTTON} !important;
    }}

    /* Secondary Button Style */
    .secondary-btn > button {{
        background: transparent !important;
        color: {PRIMARY_COLOR} !important;
        border: 2px solid {PRIMARY_COLOR} !important;
        box-shadow: none !important;
    }}
    
    .secondary-btn > button:hover {{
        background: {ACCENT_COLOR} !important;
        box-shadow: none !important;
    }}
    
    /* ===== PROGRESS STEPPER ===== */
    .neuro-stepper {{
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 0.5rem;
        margin: 1.5rem 0 2rem;
        padding: 1rem;
        background: {BACKGROUND_SUBTLE};
        border-radius: 12px;
    }}
    
    .neuro-step {{
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }}
    
    .neuro-step-dot {{
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 600;
        font-size: 0.875rem;
        transition: all 0.3s ease;
    }}
    
    .neuro-step-dot.active {{
        background: {PRIMARY_COLOR};
        color: white;
    }}
    
    .neuro-step-dot.completed {{
        background: {SUCCESS_COLOR};
        color: white;
    }}
    
    .neuro-step-dot.inactive {{
        background: {BORDER_COLOR};
        color: {TEXT_SECONDARY};
    }}
    
    .neuro-step-label {{
        font-size: 0.875rem;
        font-weight: 500;
        color: {TEXT_SECONDARY};
    }}
    
    .neuro-step-label.active {{
        color: {PRIMARY_COLOR};
        font-weight: 600;
    }}
    
    .neuro-step-connector {{
        width: 40px;
        height: 2px;
        background: {BORDER_COLOR};
        margin: 0 0.25rem;
    }}
    
    .neuro-step-connector.completed {{
        background: {SUCCESS_COLOR};
    }}
    
    /* ===== METRICS / KPIs ===== */
    .neuro-metric {{
        background: {BACKGROUND_LIGHT};
        border: 1px solid {BORDER_COLOR};
        border-radius: 12px;
        padding: 1.25rem;
        text-align: center;
    }}
    
    .neuro-metric-value {{
        font-size: 2rem;
        font-weight: 700;
        color: {PRIMARY_COLOR};
        line-height: 1.2;
    }}
    
    .neuro-metric-label {{
        font-size: 0.875rem;
        color: {TEXT_SECONDARY};
        margin-top: 0.25rem;
    }}
    
    .neuro-metric-delta {{
        font-size: 0.8rem;
        font-weight: 500;
        margin-top: 0.5rem;
    }}
    
    .neuro-metric-delta.positive {{ color: {SUCCESS_COLOR}; }}
    .neuro-metric-delta.negative {{ color: {DANGER_COLOR}; }}
    .neuro-metric-delta.neutral {{ color: {TEXT_SECONDARY}; }}
    
    /* ===== BADGES ===== */
    .neuro-badge {{
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 999px;
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }}
    
    .neuro-badge.calm {{ background: #DBEAFE; color: #1E40AF; }}
    .neuro-badge.boom {{ background: #D1FAE5; color: #065F46; }}
    .neuro-badge.crisis {{ background: #FEE2E2; color: #991B1B; }}
    .neuro-badge.info {{ background: {ACCENT_COLOR}; color: {PRIMARY_COLOR}; }}
    
    /* ===== TABS OVERRIDE ===== */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.5rem;
        background: {BACKGROUND_SUBTLE};
        padding: 0.5rem;
        border-radius: 12px;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        border-radius: 8px;
        padding: 0.75rem 1.25rem;
        font-weight: 500;
        color: {TEXT_SECONDARY};
    }}
    
    .stTabs [aria-selected="true"] {{
        background: {BACKGROUND_LIGHT} !important;
        color: {PRIMARY_COLOR} !important;
        font-weight: 600;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }}
    
    /* ===== EXPANDER ===== */
    .streamlit-expanderHeader {{
        background: {BACKGROUND_SUBTLE};
        border-radius: 12px;
        font-weight: 600;
        color: {PRIMARY_COLOR};
    }}
    
    /* ===== RADIO BUTTONS ===== */
    .stRadio > div {{
        gap: 0.5rem;
    }}
    
    .stRadio > label {{
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
        font-weight: 600;
        color: {TEXT_PRIMARY};
    }}
    
    .stRadio [data-testid="stWidgetLabel"] {{
        background: transparent !important;
        border: none !important;
        padding: 0 !important;
    }}
    
    .stRadio [role="radiogroup"] > label {{
        background: {BACKGROUND_LIGHT};
        border: 2px solid {BORDER_COLOR};
        border-radius: 12px;
        padding: 1rem 1.25rem;
        cursor: pointer;
        transition: all 0.2s ease;
    }}
    
    .stRadio [role="radiogroup"] > label:hover {{
        border-color: {PRIMARY_COLOR}50;
        background: {ACCENT_COLOR};
    }}
    
    .stRadio [role="radiogroup"] > label:has(input:checked) {{
        border-color: {PRIMARY_COLOR};
        background: {ACCENT_COLOR};
    }}
    
    /* ===== INFO BOX ===== */
    .neuro-info {{
        background: {ACCENT_COLOR};
        border-left: 4px solid {PRIMARY_COLOR};
        border-radius: 0 12px 12px 0;
        padding: 1rem 1.25rem;
        margin: 1rem 0;
    }}
    
    .neuro-info p {{
        margin: 0;
        color: {PRIMARY_COLOR};
        font-size: 0.95rem;
    }}
    
    /* ===== FOOTER ===== */
    .neuro-footer {{
        background: {BACKGROUND_SUBTLE};
        border-top: 1px solid {BORDER_COLOR};
        padding: 2rem 1.5rem;
        margin-top: 4rem;
        text-align: center;
        border-radius: 16px 16px 0 0;
    }}
    
    .neuro-footer p {{
        font-size: 0.875rem;
        color: {TEXT_SECONDARY};
        margin: 0.25rem 0;
    }}
    
    .neuro-footer a {{
        color: {PRIMARY_COLOR};
        text-decoration: none;
        font-weight: 500;
    }}
    
    .neuro-footer a:hover {{
        text-decoration: underline;
    }}
    
    /* ===== FEATURE TILES ===== */
    .neuro-feature {{
        background: {BACKGROUND_LIGHT};
        border: 1px solid {BORDER_COLOR};
        border-radius: 16px;
        padding: 1.5rem;
        text-align: center;
        height: 100%;
        transition: all 0.2s ease;
    }}
    
    .neuro-feature:hover {{
        border-color: {PRIMARY_COLOR}30;
        box-shadow: 0 4px 12px rgba(6,67,109,0.08);
    }}
    
    .neuro-feature-icon {{
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }}
    
    .neuro-feature h4 {{
        font-size: 1.1rem;
        margin-bottom: 0.5rem;
        color: {PRIMARY_COLOR};
    }}
    
    .neuro-feature p {{
        font-size: 0.9rem;
        color: {TEXT_SECONDARY};
        margin: 0;
    }}
    
    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {{
        .main .block-container {{
            padding: 1rem 1rem 3rem;
        }}
        
        h1 {{ font-size: 1.875rem; }}
        h2 {{ font-size: 1.5rem; }}
        
        .neuro-hero {{
            padding: 1.75rem 1.25rem;
        }}
        
        .neuro-stepper {{
            flex-wrap: wrap;
        }}
        
        .neuro-step-connector {{
            display: none;
        }}
    }}
    
    /* ===== HIDE STREAMLIT BRANDING ===== */
    #MainMenu {{ visibility: hidden; }}
    footer {{ visibility: hidden; }}
    header {{ visibility: hidden; }}
    
    </style>
    
    <div class="neuro-bg-circles"></div>
    <div class="neuro-circle-1"></div>
    <div class="neuro-circle-2"></div>
    <div class="neuro-circle-3"></div>
    <div class="neuro-circle-4"></div>
    <div class="neuro-circle-5"></div>
    """,
    unsafe_allow_html=True
)


# ---------------------------------------------------------
# HELPER: Render Stepper Progress
# ---------------------------------------------------------
def render_stepper(current_phase: str):
    """Render a visual phase stepper (Calm → Boom → Crisis)"""
    phases = ["calm", "boom", "crisis"]
    labels = {"calm": "Calm", "boom": "Boom", "crisis": "Crisis"}
    icons = {"calm": "🌊", "boom": "📈", "crisis": "⚡"}
    
    current_idx = phases.index(current_phase) if current_phase in phases else 0
    
    steps_html = ""
    for i, phase in enumerate(phases):
        if i < current_idx:
            dot_class = "completed"
            label_class = ""
            connector_class = "completed" if i < len(phases) - 1 else ""
        elif i == current_idx:
            dot_class = "active"
            label_class = "active"
            connector_class = ""
        else:
            dot_class = "inactive"
            label_class = ""
            connector_class = ""
        
        check_or_num = "✓" if dot_class == "completed" else icons[phase]
        
        steps_html += f'''
            <div class="neuro-step">
                <div class="neuro-step-dot {dot_class}">{check_or_num}</div>
                <span class="neuro-step-label {label_class}">{labels[phase]}</span>
            </div>
        '''
        
        if i < len(phases) - 1:
            steps_html += f'<div class="neuro-step-connector {connector_class}"></div>'
    
    st.markdown(f'<div class="neuro-stepper">{steps_html}</div>', unsafe_allow_html=True)

# ---------------------------------------------------------
# HELPER: Render Metric Card
# ---------------------------------------------------------
def render_metric_card(label: str, value, delta=None, delta_type="neutral", suffix=""):
    """Render a styled metric card"""
    delta_html = ""
    if delta is not None:
        delta_class = delta_type
        delta_symbol = "↑" if delta_type == "positive" else ("↓" if delta_type == "negative" else "")
        delta_html = f'<div class="neuro-metric-delta {delta_class}">{delta_symbol} {delta}</div>'
    
    st.markdown(f'''
        <div class="neuro-metric">
            <div class="neuro-metric-value">{value}{suffix}</div>
            <div class="neuro-metric-label">{label}</div>
            {delta_html}
        </div>
    ''', unsafe_allow_html=True)

# ---------------------------------------------------------
# HELPER: Render Feature Tile
# ---------------------------------------------------------
def render_feature_tile(icon: str, title: str, description: str):
    """Render a feature highlight tile"""
    st.markdown(f'''
        <div class="neuro-feature">
            <div class="neuro-feature-icon">{icon}</div>
            <h4>{title}</h4>
            <p>{description}</p>
        </div>
    ''', unsafe_allow_html=True)

def render_coming_soon_card(title: str, description: str = "Coming soon"):
    """Unified pink coming-soon card."""
    st.markdown(
        f"""
        <div class="neuro-card" style="border-left: 6px solid #EC4899; background:#fff;">
          <strong>{title}</strong><br>
          <span style="color:#EC4899;">{description}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

def render_phase_badge(phase: str):
    """Render a colored phase badge"""
    labels = {"calm": "Calm Phase", "boom": "Boom Phase", "crisis": "Crisis Phase"}
    st.markdown(f'<span class="neuro-badge {phase}">{labels.get(phase, phase)}</span>', unsafe_allow_html=True)

# ---------------------------------------------------------
# HELPER: Render Info Box
# ---------------------------------------------------------
def render_info_box(text: str):
    """Render an info callout box"""
    st.markdown(f'''
        <div class="neuro-info">
            <p>ℹ️ {text}</p>
        </div>
    ''', unsafe_allow_html=True)

# ---------------------------------------------------------
# HELPER: Render Footer
# ---------------------------------------------------------
def render_footer():
    """Render the app footer"""
    st.markdown('''
        <div class="neuro-footer">
            <p><strong>NeuroRisk AI</strong> – Behavioral Risk Profiling</p>
            <p>Turning emotion into data and compliance into confidence.</p>
            <p style="margin-top: 1rem;">
                <a href="#">Privacy</a> · 
                <a href="#">Imprint</a> · 
                <a href="#">Contact</a>
            </p>
            <p style="font-size: 0.75rem; margin-top: 1rem; color: #9CA3AF;">
                © 2025 NeuroRisk AI. All rights reserved.
            </p>
        </div>
    ''', unsafe_allow_html=True)

def compute_bias_messages(scores):
    """Create bias messages with severity levels."""
    messages = []
    la = scores.get("loss_aversion_proxy", 0.0)
    if la > 0.2:
        messages.append((
            "info",
            "🧩 **Loss Aversion:** You behave much more risk-seeking during boom phases than in crises. "
            "This indicates pronounced loss aversion."
        ))
    elif la > 0.05:
        messages.append((
            "info",
            "🧩 **Loss Aversion:** Slight tendency toward loss avoidance in crises – overall moderate."
        ))
    else:
        messages.append((
            "info",
            "🧩 **Loss Aversion:** Your risk choices hardly differ between boom and crisis – rather low loss aversion."
        ))

    herd_score = scores.get("herding_score", 0.0)
    if herd_score > 70:
        messages.append((
            "warning",
            "👥 **Herding Tendency:** You frequently follow the majority. "
            "Be careful not to base decisions solely on 'everyone's doing it'."
        ))
    elif herd_score > 30:
        messages.append((
            "info",
            "👥 **Herding Tendency:** Moderate tendency to orient yourself toward the majority."
        ))
    else:
        messages.append((
            "success",
            "👥 **Herding Tendency:** Low tendency toward herding – you make relatively independent decisions."
        ))

    disposition = scores.get("disposition")
    if disposition == "high":
        messages.append((
            "warning",
            "💰 **Disposition Effect:** You tend to realize gains quickly and completely. "
            "In the long run, this can lead to missing upside potential."
        ))
    elif disposition == "medium":
        messages.append((
            "info",
            "💰 **Disposition Effect:** Tendency to sell when in profit – normal, but observable."
        ))
    elif disposition == "slight":
        messages.append((
            "info",
            "💰 **Disposition Effect:** Slight tendency to take profits, overall balanced."
        ))
    elif disposition == "low":
        messages.append((
            "success",
            "💰 **Disposition Effect:** You let gains run relatively – little tendency to realize prematurely."
        ))

    recency = scores.get("recency")
    if recency == "strong negative":
        messages.append((
            "warning",
            "⏳ **Recency Bias:** After short-term losses, you react very defensively. "
            "This can lead to emotional selling."
        ))
    elif recency == "moderate":
        messages.append((
            "info",
            "⏳ **Recency Bias:** Your reaction to short-term losses is moderate."
        ))
    elif recency == "resilient_proactive":
        messages.append((
            "success",
            "⏳ **Recency Bias:** You not only stay calm, but also actively use downturns."
        ))
    elif recency == "resilient":
        messages.append((
            "success",
            "⏳ **Recency Bias:** Short-term losses seem to hardly dominate your behavior."
        ))


    hindsight = scores.get("hindsight")
    if hindsight == "high":
        messages.append((
            "warning",
            "🔁 **Hindsight / Regret:** In hindsight, you would clearly choose a more defensive strategy. "
            "This may indicate high emotional retrospective pressure."
        ))
    elif hindsight == "moderate":
        messages.append((
            "info",
            "🔁 **Hindsight / Regret:** You would change some, but not all decisions."
        ))
    elif hindsight == "aggressive":
        messages.append((
            "info",
            "🔁 **Hindsight:** In hindsight, you would have been even more aggressive – you accept volatility relatively well."
        ))
    elif hindsight == "low":
        messages.append((
            "success",
            "🔁 **Hindsight / Regret:** You would hardly change your strategy in hindsight."
        ))

    return messages

def generate_results_pdf(demographics, biometrics_df, stress_summary, risk_summary, scores, risk_type):
    """Render PDF export (sections 1–8) with wrapped text."""
    if canvas is None or A4 is None:
        return None

    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    margin = 40
    y = height - margin
    content_width = width - 2 * margin

    def new_page():
        nonlocal y
        pdf.showPage()
        pdf.setFont("Helvetica", 11)
        y = height - margin

    def ensure_space(required=40):
        nonlocal y
        if y - required < margin:
            new_page()

    def write_heading(text):
        nonlocal y
        ensure_space(30)
        pdf.setFont("Helvetica-Bold", 13)
        pdf.drawString(margin, y, text)
        y -= 22
        pdf.setFont("Helvetica", 11)

    def write_line(text=""):
        nonlocal y
        ensure_space(18)
        pdf.drawString(margin, y, text)
        y -= 16

    def write_wrapped(text, indent=0):
        """Wrap long lines to fit the page width."""
        nonlocal y
        ensure_space(18)
        pdf.setFont("Helvetica", 11)
        # Fallback: manual wrap at ~95 chars if simpleSplit not available
        if simpleSplit:
            lines = simpleSplit(text, "Helvetica", 11, content_width - indent)
        else:
            max_chars = 95
            words = text.split()
            lines, cur = [], ""
            for w in words:
                if len(cur) + len(w) + 1 <= max_chars:
                    cur = (cur + " " + w).strip()
                else:
                    lines.append(cur)
                    cur = w
            if cur:
                lines.append(cur)
        for i, ln in enumerate(lines):
            ensure_space(16)
            pdf.drawString(margin + indent, y, ln)
            y -= 16

    def clean_text(t: str) -> str:
        return t.replace("**", "").replace("–", "-")

    # Title block
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(margin, y, "NeuroRiskAI – Results Report")
    y -= 28
    pdf.setFont("Helvetica", 11)
    write_wrapped(f"Created on: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    write_wrapped(f"Age: {demographics.get('age', '–')} | Goal: {demographics.get('goal', '–')} | Experience: {demographics.get('experience', '–')}")
    write_line()

    # 1. Biometrics
    write_heading("1. Biometrics")
    if biometrics_df is not None and not biometrics_df.empty:
        for _, row in biometrics_df.iterrows():
            pulse = row.get("Average Pulse (bpm)")
            rt = row.get("Average Reaction Time (s)")
            txt = (
                f"{row.get('Market Phase', '–')}: Pulse {pulse:.0f} bpm, Reaction time {rt:.2f} s"
                if pd.notnull(pulse) and pd.notnull(rt)
                else f"{row.get('Market Phase', '–')}: No data available"
            )
            write_wrapped(txt)
    else:
        write_wrapped("No data available.")
    write_line()

    # 2. Stress Progression
    write_heading("2. Stress Progression")
    for phase, value in stress_summary.items():
        write_wrapped(f"{phase}: Stress (z-score) {value:.2f}")
    write_line()

    # 3. Risk Progression
    write_heading("3. Risk Progression")
    for phase, value in risk_summary.items():
        write_wrapped(f"{phase}: Risk index {value:.2f}")
    write_line()

    # 4. Key Metrics (Scores)
    write_heading("4. Key Metrics (Scores)")
    for key in ["RCS", "SSS", "RGS", "AdvisorNeedScore"]:
        if key in scores:
            write_wrapped(f"{key}: {scores[key]:.0f} / 100")
    write_line()

    # 5. Bias Cards – grouped and wrapped, no numbers, Green → Blue → Orange
    write_heading("5. Bias Cards")
    bias_msgs = compute_bias_messages(scores)
    groups = [
        ("success", "Positive (Green)"),
        ("info", "Neutral (Blue)"),
        ("warning", "Critical (Warning)"),
    ]
    for level, title in groups:
        items = [m for lvl, m in bias_msgs if lvl == level]
        if items:
            write_wrapped(f"{title}:")
            for m in items:
                write_wrapped(" - " + clean_text(m), indent=12)
            write_line()

    # 6. Risk Character
    write_heading("6. Risk Character")
    write_wrapped(f"Profile: {risk_type}")
    write_line()



    pdf.save()
    buffer.seek(0)
    return buffer.getvalue()

# ---------------------------------------------------------
# Questions & Scenarios (as before)
# ---------------------------------------------------------
SCENARIO_QUESTIONS = [
    # ---------------- CALM MARKET ----------------
    {
        "id": 1,
        "phase": "calm",
        "question": (
            "It is a calm market environment. The economy is growing moderately and markets "
            "fluctuate only slightly. You have a substantial amount of long-term capital to "
            "invest. How would you allocate it today?"
        ),
        "options": [
            {
                "label": "Very defensive: mostly cash or savings accounts, only a small equity fund position",
                "risk_level": 1,
            },
            {
                "label": "Defensive-balanced: a mix of bonds and broad equity funds",
                "risk_level": 2,
            },
            {
                "label": "Balanced: a clearly higher equity share than bonds or cash",
                "risk_level": 3,
            },
            {
                "label": "Dynamic: almost fully invested in equities or equity funds",
                "risk_level": 4,
            },
        ],
        "bias_tag": None,
        "herd_majority": None,
        "risk_relevant": True,
    },
    {
        "id": 2,
        "phase": "calm",
        "question": (
            "You receive an unexpected bonus on top of your regular income. "
            "This bonus is free capital that you could invest. How much of this bonus "
            "would you invest in equities?"
        ),
        "options": [
            {
                "label": "Nothing – keep the entire bonus in cash",
                "risk_level": 1,
            },
            {
                "label": "Invest about 25% in equities, keep 75% safe",
                "risk_level": 2,
            },
            {
                "label": "Invest about 50% in equities, 50% safe",
                "risk_level": 3,
            },
            {
                "label": "Invest about 75% or more in equities, only a small cash reserve",
                "risk_level": 4,
            },
        ],
        "bias_tag": None,
        "herd_majority": None,
        "risk_relevant": True,
    },
    {
        # Disposition Effect in gains – Q3 (Strings wichtig für compute_scores)
        "id": 3,
        "phase": "calm",
        "question": (
            "Imagine you invested a sum of money 12 months ago in a broadly diversified portfolio. "
            "Today, your portfolio shows a moderate gain. You are generally satisfied with the result. "
            "What do you do now?"
        ),
        "options": [
            {
                "label": "Sell everything and go completely to cash",
                "risk_level": 1,
            },
            {
                "label": "Take profits, sell a larger part of the portfolio",
                "risk_level": 2,
            },
            {
                "label": "Partial sale, leave part invested",
                "risk_level": 3,
            },
            {
                "label": "Leave everything invested and think long-term",
                "risk_level": 4,
            },
        ],
        "bias_tag": "disposition_gain",
        "herd_majority": None,
        "risk_relevant": True,
    },
    {
        # Grundrisikoprofil in ruhiger Phase
        "id": 4,
        "phase": "calm",
        "question": (
            "You are planning a new long-term investment for general wealth building. "
            "In a calm market environment like now, which description best matches the "
            "risk level you would choose for this new investment?"
        ),
        "options": [
            {
                "label": "Very low risk – strong focus on capital preservation, minimal fluctuations",
                "risk_level": 1,
            },
            {
                "label": "Rather low risk – some fluctuation is acceptable, capital preservation is important",
                "risk_level": 2,
            },
            {
                "label": "Medium risk – balanced between return and fluctuation",
                "risk_level": 3,
            },
            {
                "label": "High risk – focus on long-term return, strong fluctuation is acceptable",
                "risk_level": 4,
            },
        ],
        "bias_tag": "gain_frame",
        "herd_majority": None,
        "risk_relevant": True,
    },
    {
        # Herding in calm phase
        "id": 5,
        "phase": "calm",
        "question": (
            "A survey among investors with a similar profile to you shows that around 80% of them "
            "currently hold a high equity share in their portfolios. You yourself hold a more "
            "defensive allocation. How do you react?"
        ),
        "options": [
            {
                "label": "I stick with my defensive strategy and do not increase equities",
                "risk_level": 1,
            },
            {
                "label": "I increase my equity allocation slightly",
                "risk_level": 2,
            },
            {
                "label": "I increase my equity allocation significantly",
                "risk_level": 3,
            },
            {
                "label": "I adapt strongly and go very aggressively into equities to align with the majority",
                "risk_level": 4,
            },
        ],
        "bias_tag": "herding",
        "herd_majority": "I adapt strongly and go very aggressively into equities to align with the majority",
        "risk_relevant": True,  # Herding UND Risiko
    },
    {
        "id": 6,
        "phase": "calm",
        "question": (
            "You win a medium-sized lottery prize that is financially meaningful but not life-changing. "
            "You decide to invest this amount separately from your existing portfolio. How would you "
            "invest this lottery money?"
        ),
        "options": [
            {
                "label": "Keep it entirely in cash or a savings account",
                "risk_level": 1,
            },
            {
                "label": "Invest mainly in low-risk funds or bonds",
                "risk_level": 2,
            },
            {
                "label": "Invest mostly in diversified equity funds",
                "risk_level": 3,
            },
            {
                "label": "Treat it as 'play money' and invest mainly in riskier themes or individual stocks",
                "risk_level": 4,
            },
        ],
        "bias_tag": None,  # Mental Accounting / Riskverhalten
        "herd_majority": None,
        "risk_relevant": True,
    },

    # ---------------- BOOM MARKET ----------------
    {
        "id": 7,
        "phase": "boom",
        "question": (
            "Stock markets have risen strongly for several years, many indices are at or near all-time highs. "
            "You receive a new annual bonus that you do not need for current expenses. How do you invest "
            "this new money in the current boom phase?"
        ),
        "options": [
            {
                "label": "I keep the new money in cash and do not invest it for now",
                "risk_level": 1,
            },
            {
                "label": "I invest it mainly in broadly diversified equity funds",
                "risk_level": 2,
            },
            {
                "label": "I focus on more volatile growth or sector funds with higher return potential",
                "risk_level": 3,
            },
            {
                "label": "I invest in very concentrated or speculative themes to maximize upside",
                "risk_level": 4,
            },
        ],
        "bias_tag": None,
        "herd_majority": None,
        "risk_relevant": True,
    },
    {
        # Overconfidence candidate – persönliche Outperformance
        "id": 8,
        "phase": "boom",
        "question": (
            "Over the last three years, your portfolio has clearly outperformed the overall market. "
            "You attribute this partly to your good decisions. You are now considering adjusting your "
            "strategy. What do you do?"
        ),
        "options": [
            {
                "label": "I reduce risk significantly and secure a large part of the gains",
                "risk_level": 1,
            },
            {
                "label": "I take some profits and slightly reduce risk",
                "risk_level": 2,
            },
            {
                "label": "I keep my current risk level unchanged",
                "risk_level": 3,
            },
            {
                "label": "I increase risk because I trust my ability to make good decisions",
                "risk_level": 4,
            },
        ],
        "bias_tag": "overconfidence_candidate",
        "herd_majority": None,
        "risk_relevant": True,
    },
    {
        # Growth style choice in boom
        "id": 9,
        "phase": "boom",
        "question": (
            "You are about to set up a new equity investment in the current booming market. "
            "Which type of equity strategy would you choose?"
        ),
        "options": [
            {
                "label": "Mainly large, established companies with relatively stable earnings",
                "risk_level": 1,
            },
            {
                "label": "A mix of large companies and selected growth stocks",
                "risk_level": 2,
            },
            {
                "label": "Focus on growth companies with higher earnings volatility",
                "risk_level": 3,
            },
            {
                "label": "Strong focus on very young or highly speculative companies",
                "risk_level": 4,
            },
        ],
        "bias_tag": None,
        "herd_majority": None,
        "risk_relevant": True,
    },
    {
        # Classic gain-frame lottery
        "id": 10,
        "phase": "boom",
        "question": (
            "You can choose between different gain profiles for a one-year investment. "
            "All options refer to the same invested amount. Which gain profile would you prefer?"
        ),
        "options": [
            {
                "label": "Secure small gain – you know exactly what you will receive",
                "risk_level": 1,
            },
            {
                "label": "Moderate chance of a noticeably higher gain, otherwise no gain",
                "risk_level": 2,
            },
            {
                "label": "Lower chance of a very high gain, otherwise no gain",
                "risk_level": 3,
            },
            {
                "label": "No immediate payout, stay fully invested long-term with full market risk",
                "risk_level": 4,
            },
        ],
        "bias_tag": "gain_frame",
        "herd_majority": None,
        "risk_relevant": True,
    },
    {
        # Pure Herding / FOMO – OHNE Risikobeitrag
        "id": 11,
        "phase": "boom",
        "question": (
            "Several friends and colleagues tell you that they made high short-term profits with "
            "a very popular, highly discussed investment theme (for example, a specific tech or "
            "crypto asset). You have not invested in it so far. How do you react?"
        ),
        "options": [
            {
                "label": "I do not invest and consciously stick to my own strategy",
                "risk_level": 1,
            },
            {
                "label": "I inform myself, but do not change my portfolio for now",
                "risk_level": 2,
            },
            {
                "label": "I invest a moderate amount to participate",
                "risk_level": 3,
            },
            {
                "label": "I invest a significant amount quickly to not miss the opportunity",
                "risk_level": 4,
            },
        ],
        "bias_tag": "herding",
        "herd_majority": "I invest a significant amount quickly to not miss the opportunity",
        "risk_relevant": False,  # Beispiel: nur Herding-Bias, kein Beitrag zum Risk-Average
    },
    {
        # Overconfidence / bubble warnings
        "id": 12,
        "phase": "boom",
        "question": (
            "Financial media and some experts warn more and more loudly of a possible bubble and "
            "overvaluation on the markets. Your portfolio is strongly in profit. What do you do?"
        ),
        "options": [
            {
                "label": "I reduce risk significantly and secure a large part of the profits",
                "risk_level": 1,
            },
            {
                "label": "I reduce risk slightly (small profit-taking)",
                "risk_level": 2,
            },
            {
                "label": "I do not change anything, the rally continues in my view",
                "risk_level": 3,
            },
            {
                "label": "I even increase risk and expand my equity or leverage positions",
                "risk_level": 4,
            },
        ],
        "bias_tag": "overconfidence_candidate",
        "herd_majority": None,
        "risk_relevant": True,
    },

    # ---------------- CRISIS MARKET ----------------
    {
        # Loss aversion candidate – crisis
        "id": 13,
        "phase": "crisis",
        "question": (
            "Stock markets have fallen by around 30% within a year. Your long-term portfolio is "
            "clearly in the red. You realize that such losses are emotionally very stressful for you. "
            "What do you do?"
        ),
        "options": [
            {
                "label": "Sell everything, limit losses and go to cash",
                "risk_level": 1,
            },
            {
                "label": "Partial sale, leave part invested",
                "risk_level": 2,
            },
            {
                "label": "Stay invested and keep a long-term view",
                "risk_level": 3,
            },
            {
                "label": "Add additional capital and buy 'cheap'",
                "risk_level": 4,
            },
        ],
        "bias_tag": "loss_aversion_candidate",
        "herd_majority": None,
        "risk_relevant": True,
    },
    {
        # Crisis risk setting
        "id": 14,
        "phase": "crisis",
        "question": (
            "In the current market crisis you are reviewing your overall strategy. "
            "For the next years, how much risk are you willing to carry in your investments?"
        ),
        "options": [
            {
                "label": "Very defensive – strong focus on capital preservation, little fluctuation",
                "risk_level": 1,
            },
            {
                "label": "Defensive – reduced equity share, limited fluctuation acceptable",
                "risk_level": 2,
            },
            {
                "label": "Balanced – you accept clear fluctuations for long-term return",
                "risk_level": 3,
            },
            {
                "label": "Aggressive – you accept strong fluctuations to use the crisis as an opportunity",
                "risk_level": 4,
            },
        ],
        "bias_tag": None,
        "herd_majority": None,
        "risk_relevant": True,
    },
    {
        # Recency bias – Q15 (Strings wichtig)
        "id": 15,
        "phase": "crisis",
        "question": (
            "In the last weeks, markets have steadily fallen and the last two trading days were again "
            "clearly negative. Your portfolio shows large losses. How do you react now?"
        ),
        "options": [
            {
                "label": "I sell everything now and go to cash",
                "risk_level": 1,
            },
            {
                "label": "I only sell part of the portfolio",
                "risk_level": 2,
            },
            {
                "label": "I hold on, without investing further",
                "risk_level": 3,
            },
            {
                "label": "I hold on and even buy more, because I see opportunities",
                "risk_level": 4,
            },
        ],
        "bias_tag": "recency_candidate",
        "herd_majority": None,
        "risk_relevant": True,
    },
    {
        # Herding in crisis
        "id": 16,
        "phase": "crisis",
        "question": (
            "The media say: 'Everyone is selling now, this could be the beginning of a long crisis.' "
            "You also hear from acquaintances that they have sold a large part of their investments. "
            "What do you do?"
        ),
        "options": [
            {
                "label": "I sell like the majority and move largely into cash",
                "risk_level": 1,
            },
            {
                "label": "I reduce risk moderately but keep a core position",
                "risk_level": 2,
            },
            {
                "label": "I stay invested, even if it hurts",
                "risk_level": 3,
            },
            {
                "label": "I consciously use the opportunity to buy more",
                "risk_level": 4,
            },
        ],
        "bias_tag": "herding",
        "herd_majority": "I sell like the majority and move largely into cash",
        "risk_relevant": True,
    },
    {
        "id": 17,
        "phase": "crisis",
        "question": (
            "You have not yet invested a separate amount of money that you could also use as a "
            "long-term investment. Prices have fallen sharply. How do you deal with this additional capital "
            "in the current crisis?"
        ),
        "options": [
            {
                "label": "No further investment, hold everything in cash",
                "risk_level": 1,
            },
            {
                "label": "Invest a small part in a defensive mixed fund",
                "risk_level": 2,
            },
            {
                "label": "Invest a larger part in a broad equity fund",
                "risk_level": 3,
            },
            {
                "label": "Invest most of it in very risky, sharply fallen individual stocks",
                "risk_level": 4,
            },
        ],
        "bias_tag": None,
        "herd_majority": None,
        "risk_relevant": True,
    },
    {
        # Hindsight / regret – Q18 (Strings wichtig)
        "id": 18,
        "phase": "crisis",
        "question": (
            "Looking back, suppose you could rewind the last 12 months and set up your portfolio "
            "again from today's perspective. How would you decide?"
        ),
        "options": [
            {
                "label": "Yes, I would have been much more defensive in my allocation",
                "risk_level": 1,
            },
            {
                "label": "I would only make small adjustments to the portfolio",
                "risk_level": 2,
            },
            {
                "label": "No, I would have done the same",
                "risk_level": 3,
            },
            {
                "label": "I would have been even more aggressive and taken more risk",
                "risk_level": 4,
            },
        ],
        "bias_tag": "hindsight",
        "herd_majority": None,
        "risk_relevant": True,
    },
]

PHASE_ORDER = ["calm", "boom", "crisis"]




# ---------------------------------------------------------
# SQLite Database Setup
# ---------------------------------------------------------
DB_FILE = Path(__file__).parent / "neurorisk.db"

def init_db():
    """Initialize SQLite database"""
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,  -- NULL for guest sessions
            demographics TEXT NOT NULL,
            scores TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (username) REFERENCES users(username)
        )
    """)
    
    c.execute("""
        CREATE TABLE IF NOT EXISTS responses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            profile_id INTEGER NOT NULL,
            q_id INTEGER,
            phase TEXT,
            selected_label TEXT,
            mu REAL,
            sigma REAL,
            x_risk_relative REAL,
            x_reaction_time REAL,
            x_pulse REAL,
            advisor_help_used INTEGER,
            switch_action INTEGER,
            FOREIGN KEY (profile_id) REFERENCES profiles(id)
        )
    """)
    
    conn.commit()
    conn.close()

# Initialize DB on startup
init_db()

def hash_password(pw: str) -> str:
    return hashlib.sha256(pw.encode("utf-8")).hexdigest()

def user_exists(username: str) -> bool:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    exists = c.fetchone() is not None
    conn.close()
    return exists

def create_user(username: str, password: str) -> bool:
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hash_password(password))
        )
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error creating account: {e}")
        return False

def verify_user(username: str, password: str) -> bool:
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT password_hash FROM users WHERE username = ?", (username,))
    row = c.fetchone()
    conn.close()
    
    if row:
        return row[0] == hash_password(password)
    return False

def load_user_profile(username: str):
    """Load the latest profile of a user"""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute("""
        SELECT id, demographics, scores, timestamp 
        FROM profiles 
        WHERE username = ? 
        ORDER BY timestamp DESC 
        LIMIT 1
    """, (username,))
    profile = c.fetchone()
    
    if not profile:
        conn.close()
        return None
    
    profile_id = profile["id"]
    
    # Load all responses for this profile
    c.execute("""
        SELECT q_id, phase, selected_label, mu, sigma, x_risk_relative, 
               x_reaction_time, x_pulse, advisor_help_used, switch_action
        FROM responses 
        WHERE profile_id = ?
        ORDER BY id
    """, (profile_id,))
    
    responses_rows = c.fetchall()
    conn.close()
    
    # Convert to list of dicts
    responses = [dict(row) for row in responses_rows]
    
    try:
        demographics = json.loads(profile["demographics"])
        scores = json.loads(profile["scores"])
    except Exception as e:
        st.error(f"Error loading profile: {e}")
        return None
    
    return {
        "demographics": demographics,
        "responses": responses,
        "scores": scores,
        "timestamp": profile["timestamp"]
    }

def save_user_profile(username: str, demographics: dict, responses: list, scores: dict):
    """Save profile + all responses"""
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        
        # Convert pandas Series to dict before saving
        scores_clean = {}
        for key, val in scores.items():
            if hasattr(val, 'to_dict'):  # pandas Series
                scores_clean[key] = val.to_dict()
            elif isinstance(val, (int, float)):
                scores_clean[key] = float(val)
            elif isinstance(val, str):
                scores_clean[key] = val
            else:
                scores_clean[key] = str(val)
        
        # 1. Save profile metadata (as JSON)
        c.execute("""
            INSERT INTO profiles (username, demographics, scores)
            VALUES (?, ?, ?)
        """, (username, json.dumps(demographics), json.dumps(scores_clean)))
        
        profile_id = c.lastrowid
        
        # 2. Save all responses
        for resp in responses:
            c.execute("""
                INSERT INTO responses 
                (profile_id, q_id, phase, selected_label, mu, sigma, 
                 x_risk_relative, x_reaction_time, x_pulse, advisor_help_used, switch_action)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                profile_id,
                resp.get("q_id"),
                resp.get("phase"),
                resp.get("selected_label"),
                resp.get("mu"),
                resp.get("sigma"),
                resp.get("x_risk_relative"),
                resp.get("x_reaction_time"),
                resp.get("x_pulse"),
                resp.get("advisor_help_used"),
                resp.get("switch_action")
            ))
        
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        st.error(f"Error saving profile: {e}")
        return False

def save_guest_profile(demographics: dict, responses: list, scores: dict):
    """Save guest session (username = '' for old DBs with NOT NULL).
       Returns the new profile_id (int) or None on error.
    """
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        
        scores_clean = {}
        for key, val in scores.items():
            if hasattr(val, 'to_dict'):
                scores_clean[key] = val.to_dict()
            elif isinstance(val, (int, float)):
                scores_clean[key] = float(val)
            elif isinstance(val, str):
                scores_clean[key] = val
            else:
                scores_clean[key] = str(val)
        
        # username = '' instead of NULL (compatible with NOT NULL constraint)
        guest_username = ""
        c.execute("""
            INSERT INTO profiles (username, demographics, scores)
            VALUES (?, ?, ?)
        """, (guest_username, json.dumps(demographics), json.dumps(scores_clean)))
        
        profile_id = c.lastrowid
        
        for resp in responses:
            c.execute("""
                INSERT INTO responses 
                (profile_id, q_id, phase, selected_label, mu, sigma, 
                 x_risk_relative, x_reaction_time, x_pulse, advisor_help_used, switch_action)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                profile_id,
                resp.get("q_id"),
                resp.get("phase"),
                resp.get("selected_label"),
                resp.get("mu"),
                resp.get("sigma"),
                resp.get("x_risk_relative"),
                resp.get("x_reaction_time"),
                resp.get("x_pulse"),
                resp.get("advisor_help_used"),
                resp.get("switch_action")
            ))
        
        conn.commit()
        conn.close()
        return profile_id
    except Exception as e:
        st.error(f"Error saving guest session: {e}")
        return None

# ---------------------------------------------------------
# Session State Initialization
# ---------------------------------------------------------
def init_session():
    if "stage" not in st.session_state:
        st.session_state.stage = "home"
        st.session_state.demographics = {}
        st.session_state.stated_risk_raw = None
        st.session_state.responses = []
        st.session_state.current_q_index = 0
        st.session_state.current_question_id = None
        st.session_state.question_start_time = None
        st.session_state.seen_phase_intros = set()
        st.session_state.logged_in_user = None
        st.session_state.profile_saved = False
        st.session_state.saved_profile = None
        st.session_state.saved_profile_id = None  # NEW: for guest profile ID


init_session()


# ---------------------------------------------------------
# Helper Functions for Scores
# ---------------------------------------------------------
def compute_scores(demo, responses):
    if not responses:
        return {}

    df = pd.DataFrame(responses)

    # ---------- RISK: nur risk_relevante Fragen ----------
    if "risk_relevant" in df.columns:
        df_risk = df[df["risk_relevant"] == True]
    else:
        df_risk = df

    # Falls aus irgendeinem Grund alle Fragen risk_relevant=False wären:
    if df_risk.empty:
        # Fallback, damit nichts crasht
        df_risk = df.copy()

    risk_by_phase = df_risk.groupby("phase")["x_risk_relative"].mean().reindex(PHASE_ORDER)
    R_calm = risk_by_phase.get("calm", 0.0)
    R_boom = risk_by_phase.get("boom", 0.0)
    R_crisis = risk_by_phase.get("crisis", 0.0)

    R_max = risk_by_phase.max()
    R_min = risk_by_phase.min()
    delta_R = float(R_max - R_min) if pd.notnull(R_max) and pd.notnull(R_min) else 0.0
    RCS = 100 * (1 - min(max(delta_R, 0.0), 1.0))  # Risk Consistency Score

    # ---------- STRESS: alle Fragen (inkl. Bias-only) ----------
    rt = df["x_reaction_time"].values
    pulse = df["x_pulse"].values

    def zscore(x):
        x = np.array(x)
        if len(x) > 1 and x.std() > 0:
            return (x - x.mean()) / x.std()
        return np.zeros_like(x)

    z_rt = zscore(rt)
    z_pulse = zscore(pulse)

    df["stress_i"] = 0.6 * z_rt + 0.4 * z_pulse
    stress_by_phase = df.groupby("phase")["stress_i"].mean().reindex(PHASE_ORDER)
    S_calm = stress_by_phase.get("calm", 0.0)
    S_boom = stress_by_phase.get("boom", 0.0)
    S_crisis = stress_by_phase.get("crisis", 0.0)

    try:
        s_max = float(stress_by_phase.max())
        s_min = float(stress_by_phase.min())
    except Exception:
        s_max = 0.0
        s_min = 0.0
    delta_s = max(0.0, s_max - s_min)
    RANGE_MAX = 4.0
    ratio = delta_s / RANGE_MAX
    ratio_clamped = min(max(ratio, 0.0), 1.0)
    SSS = 100 * (1 - ratio_clamped)  # Stress Stability Score

    # ---------- Reality Gap ----------
    SS = demo.get("stated_risk_norm", 0.5)  # self-stated risk [0,1]

    BR = df_risk["x_risk_relative"].mean() if not df_risk.empty else 0.5
    G = abs(SS - BR)
    RGS = 100 * G

    # ---------- Advisor Need ----------
    RCS_norm = 1 - RCS / 100.0
    SSS_norm = 1 - SSS / 100.0
    RGS_norm = RGS / 100.0

    help_rate = df["advisor_help_used"].mean() if "advisor_help_used" in df else 0.0
    switch_rate = df["switch_action"].mean() if "switch_action" in df else 0.0

    ANS_raw = (
        0.3 * RCS_norm
        + 0.25 * SSS_norm
        + 0.25 * RGS_norm
        + 0.1 * help_rate
        + 0.1 * switch_rate
    )
    AdvisorNeedScore = 100 * ANS_raw

    # ---------- Bias Proxies (wie bei dir, aber mit R_boom/R_crisis aus df_risk) ----------
    loss_aversion_proxy = R_boom - R_crisis

    herd_rows = [r for r in responses if r.get("herd_majority_flag") == 1]
    herd_follow_rate = np.mean([r.get("follow_crowd", 0) for r in herd_rows]) if herd_rows else 0.0

    # Disposition (q_id 3)
    disp = None
    disp_row = next((r for r in responses if r["q_id"] == 3), None)
    if disp_row:
        label = disp_row["selected_label"].lower()
        if "sell everything" in label:
            disp = "high"
        elif "take profits" in label or "larger part" in label:
            disp = "medium"
        elif "partial sale" in label:
            disp = "slight"
        else:
            disp = "low"

    # Recency (q_id 15)
    recency = None
    q15 = next((r for r in responses if r["q_id"] == 15), None)
    if q15:
        label = q15["selected_label"].lower()
        if "sell everything now" in label:
            recency = "strong_negative"
        elif "only sell part" in label:
            recency = "moderate"
        elif "hold on" in label and "even buy more" in label:
            recency = "resilient_proactive"
        else:
            recency = "resilient"

    # Hindsight (q_id 18)
    hindsight = None
    q18 = next((r for r in responses if r["q_id"] == 18), None)
    if q18:
        label = q18["selected_label"].lower()
        if "much more defensive" in label:
            hindsight = "high"
        elif "small adjustments" in label:
            hindsight = "moderate"
        elif "more aggressive" in label:
            hindsight = "aggressive"
        else:
            hindsight = "low"

    # Overconfidence Proxy
    OC_raw = SS * (1 - RCS / 100.0) * (1 - SSS / 100.0)
    OverconfidenceScore = 100 * OC_raw

    scores = {
        "risk_by_phase": risk_by_phase,
        "stress_by_phase": stress_by_phase,
        "RCS": float(RCS),
        "SSS": float(SSS),
        "RGS": float(RGS),
        "AdvisorNeedScore": float(AdvisorNeedScore),
        "BR": float(BR),
        "SS": float(SS),
        "loss_aversion_proxy": float(loss_aversion_proxy),
        "herding_score": float(herd_follow_rate * 100),
        "disposition": disp,
        "recency": recency,
        "hindsight": hindsight,
        "OverconfidenceScore": float(OverconfidenceScore),
    }
    return scores

def classify_risk_level(BR: float) -> str:
    """Risk Level (BR) → Defensive / Balanced / Dynamic."""
    if BR < 0.33:
        return "Defensive Investor"
    elif BR < 0.66:
        return "Balanced Investor"
    return "Dynamic Investor"

def classify_stability_profile(RCS: float, SSS: float) -> str:
    """2x2 Matrix from RCS & SSS → 4 Archetypes (threshold at 50)."""
    def is_high(x): 
        return x >= 50
    def is_low(x): 
        return x < 50

    if is_high(RCS) and is_high(SSS):
        return "Calm & Consistent Investor"
    if is_high(RCS) and is_low(SSS):
        return "Calm Outside, Storm Inside"
    if is_low(RCS) and is_high(SSS):
        return "Flexible, but relaxed"
    return "Emotional Swing Investor"

# ---------------------------------------------------------
# User Management Functions
# ---------------------------------------------------------
USERS_FILE = Path(__file__).parent / "users.json"

# Cache for users (avoids repeated reading)
@st.cache_resource
def get_users_cache():
    return {"data": None, "last_modified": None}

def load_users():
    """Load users.json with local cache"""
    cache = get_users_cache()
    
    if not os.path.exists(USERS_FILE):
        return {}
    
    try:
        stat = os.stat(USERS_FILE)
        current_mtime = stat.st_mtime
        
        # Is cache current?
        if cache["data"] is not None and cache["last_modified"] == current_mtime:
            return cache["data"]
        
        # Reload
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        cache["data"] = data
        cache["last_modified"] = current_mtime
        return data
    except Exception as e:
        st.error(f"Error loading: {e}")
        return {}

def save_users(users):
    """Speichere users.json und invalidiere Cache"""
    try:
        # Ensure directory exists
        USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
        
        # Invalidate cache
        cache = get_users_cache()
        cache["data"] = None
        cache["last_modified"] = None
    except Exception as e:
        st.error(f"Error saving: {e}")

# ---------------------------------------------------------
# UI: HOME PAGE (with Login / Account)
# ---------------------------------------------------------
if st.session_state.stage == "home":
    # Insert logo – centered above the card
    logo_path = Path(__file__).parent / "logo.png"
    if logo_path.exists():
        col_logo1, col_logo_center, col_logo2 = st.columns([1, 2, 1])
        with col_logo_center:
            st.image(str(logo_path), width=4000)
        st.markdown("<br>", unsafe_allow_html=True)

    # Hero Section
    st.markdown('''
        <div class="neuro-hero">
            <h2>Discover Your True Risk Profile</h2>
            <p>
                Find out in just 3 minutes how you really react in calm, euphoric and crisis-like 
                markets – not just how you assess yourself.
            </p>
        </div>
    ''' , unsafe_allow_html=True)

    # Feature Tiles
    st.markdown("### Why NeuroRisk AI?")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_feature_tile(
            "🎯", 
            "Objective Measurement", 
            "Behavior-based analysis instead of self-assessment"
        )
    
    with col2:
        render_feature_tile(
            "📊", 
            "Personal Risk Profile", 
            "Make better investment decisions in the future"
        )
    
    with col3:
        render_feature_tile(
            "🔒", 
            "Privacy First", 
            "GDPR compliant, your data belongs to you"
        )

    st.markdown("---") 

    tab1, tab2 = st.tabs(["🔐 Login", "👤 Guest"])

    with tab1:
        st.subheader("My Account")
        with st.form("login_form", clear_on_submit=True):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            col1, col2 = st.columns(2)
            with col1:
                login_btn = st.form_submit_button("Login", width='stretch')
            with col2:
                create_btn = st.form_submit_button("Create Account", width='stretch')

        if login_btn or create_btn:
            if not username or not password:
                st.error("❌ Username and password required!")
            else:
                if create_btn:
                    if user_exists(username):
                        st.error(f"❌ Username '{username}' already exists.")
                    else:
                        if create_user(username, password):
                            st.success(f"✅ Account '{username}' created! Please login now.")
                        else:
                            st.error("❌ Error creating account.")
                
                elif login_btn:
                    if verify_user(username, password):
                        st.success(f"✅ Logged in as {username}")
                        st.session_state.logged_in_user = username
                        # Load profile (optionally store in session)
                        profile = load_user_profile(username)
                        st.session_state.saved_profile = profile if profile else None
                        # No automatic stage change here; we render the action box below.
                    else:
                        st.error("❌ Wrong username or password.")
    
    # NEW: Always render action box when logged in (not just on submit)
    if st.session_state.get("logged_in_user"):
        username = st.session_state.logged_in_user
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style="background-color: {PRIMARY_COLOR}; color: white; padding: 1.5rem; border-radius: 0.75rem; text-align: center;">
              <h3 style="margin: 0; color: white;">Welcome, {username}! 👋</h3>
              <h4 style="margin: 0.5rem 0 0 0;">Start a new simulation or view your profile if you've already completed a simulation</h4>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)




        col_sim1, col_sim2 = st.columns(2)
        with col_sim1:
            if st.button("Start New Simulation", key="new_sim_login", width='stretch'):
                # Only reset sim data; keep login
                st.session_state.responses = []
                st.session_state.demographics = {}
                st.session_state.current_q_index = 0
                st.session_state.current_question_id = None
                st.session_state.question_start_time = None
                st.session_state.seen_phase_intros = set()
                st.session_state.profile_saved = False
                st.session_state.stage = "demographics"
                st.session_state.scroll_top = True
                st.rerun()
        with col_sim2:
            if st.session_state.get("saved_profile"):
                if st.button("📊 My Risk Profile", key="view_profile_login", width='stretch'):
                    prof = st.session_state.saved_profile
                    st.session_state.demographics = prof["demographics"]
                    st.session_state.responses = prof["responses"]
                    st.session_state.profile_saved = True  # already saved
                    st.session_state.stage = "results"
                    st.session_state.scroll_top = True
                    st.rerun()
            else:
                st.write("")  # Placeholder
    else:
        with tab2:
            st.subheader("Start as Guest")
            st.markdown(
                """
                You can also start the simulation as a guest. Your data will only be stored locally in your browser 
                and not linked to an account.
                """
            )
            if st.button("Start Simulation as Guest", key="guest_start"):
                st.session_state.stage = "demographics"
                st.session_state.scroll_top = True
                st.rerun()

    st.markdown("---") 
    # How it works section
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### How It Works")
    
    st.markdown('''
        <div class="neuro-card">
            <p><strong>1. Create profile</strong> – Brief information about yourself and your experience</p>
            <p><strong>2. Complete simulation</strong> – 18 decisions in different market phases</p>
            <p><strong>3. Get results</strong> – Your personal risk profile with insights</p>
            <p><strong>4. Compare</strong> – See how you compare to others</p>
            <p><strong>5. Act</strong> – Derive measures for your investment strategy</p>
        </div>
    ''', unsafe_allow_html=True)
    

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            <div class="neuro-card" style="text-align: center;">
            <b>🧩 Bias Detection</b><br>
            Herding, Loss Aversion, Overconfidence & more
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class="neuro-card" style="text-align: center;">
            <b>📊 Score Calculation</b><br>
            RCS, SSS, RGS, Advisor Need Score
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            """
            <div class="neuro-card" style="text-align: center;">
            <b>💡 Discover Your Risk Profile</b><br>
            AI Clustering Coming Soon!
            </div>
            """,
            unsafe_allow_html=True,
        )

    render_footer()




# ---------------------------------------------------------
# UI: DEMOGRAPHICS
# ---------------------------------------------------------
elif st.session_state.stage == "demographics":
    st.title("Your Basic Data")
    
    st.markdown("Before the simulation starts, we need a few things about you.")
    
    with st.form("demographics_form"):
        st.subheader("1. Demographic Data")
        age = st.number_input("Age", min_value=18, max_value=99, value=30, step=1)
        gender = st.selectbox("Gender (optional)", ["No Information", "Female", "Male", "Diverse"])
        job = st.text_input("Occupation (optional)", "")

        st.subheader("2. Experience & Knowledge in Finance")
        knowledge = st.slider("How would you rate your financial knowledge?", 1, 5, 3)
        experience = st.selectbox(
            "How much investment experience do you have?",
            ["None", "Little", "Medium", "A lot"]
        )

        st.subheader("3. Goals & Investment Horizon")
        goal = st.selectbox(
            "What is your main goal when investing?",
            ["Wealth Accumulation", "Income/Dividends", "Capital Preservation/Security", "Speculation"]
        )

        invest_amount = st.number_input(
            "Intended investment volume (in CHF)",
            min_value=1000,
            max_value=1_000_000,
            value=10_000,
            step=1000
        )

        amount_feel = st.selectbox(
            "How large does this amount feel to you?",
            ["Rather small", "Medium size", "Very large amount for me"]
        )

        current_investments = st.multiselect(
            "What have you invested in so far?",
            ["Stocks", "Funds/ETFs", "Bonds", "Crypto", "Real Estate", "Cash", "Nothing yet"]
        )

        horizon = st.selectbox(
            "Investment horizon",
            ["Short-term (< 3 years)", "Medium (3–10 years)", "Long-term (> 10 years)"]
        )

        st.subheader("4. Self-assessment of Risk")
        stated_risk_raw = st.slider(
            "How risk-tolerant are you (1 = very cautious, 7 = very risk-seeking)?",
            1, 7, 4
        )
        risk_constant = st.radio(
            "In your opinion, is your risk tolerance the same in all market situations?",
            ["Yes", "No", "Don't know"],
        )

        submitted = st.form_submit_button("To Simulation")

    if submitted:
        SS_norm = (stated_risk_raw - 1) / 6.0

        st.session_state.demographics = {
            "age": age,
            "gender": gender,
            "job": job,
            "knowledge": knowledge,
            "experience": experience,
            "goal": goal,
            "invest_amount": invest_amount,
            "amount_feel": amount_feel,
            "current_investments": current_investments,
            "horizon": horizon,
            "stated_risk_raw": stated_risk_raw,
            "stated_risk_norm": SS_norm,
            "risk_constant_self_view": risk_constant,
        }
        st.session_state.stated_risk_raw = stated_risk_raw
        st.session_state.stage = "simulation"
        st.session_state.scroll_top = True
        st.rerun()

# ---------------------------------------------------------
# Phase intro texts
# ---------------------------------------------------------
def render_phase_intro(phase: str):
    invest_amount = st.session_state.demographics.get("invest_amount", 10_000)

    if phase == "calm":
        title = "Phase 1 – Calm Market"
        text = (
            f"The economy is growing moderately, unemployment is low, and markets fluctuate only slightly. "
            f"You have approx. {invest_amount:,.0f} CHF that you want to invest. "
            "In the following questions, you will make decisions in a <b>calm, stable market environment</b>."
        )
    elif phase == "boom":
        title = "Phase 2 – Boom / Euphoria"
        text = (
            "Stock indices are at or near all-time highs, media reports of a 'super rally'. "
            "Your portfolio is in profit, the environment feels optimistic. "
            "In the following questions, you decide in the context of an <b>overheated, euphoric market</b>."
        )
    else:
        title = "Phase 3 – Crisis / Crash"
        text = (
            "Markets have fallen sharply, negative headlines dominate. "
            "Your invested amount has lost significant value. "
            "In the following questions, you decide in a <b>stressful crisis environment</b>."
        )

    st.subheader(title)
    st.markdown(f'<div class="neuro-phase-intro">{text}</div>', unsafe_allow_html=True)
    st.write("When you're ready, start the questions for this market phase.")
    if st.button("Continue to first question in this phase ▶"):
        st.session_state.seen_phase_intros.add(phase)
        st.session_state.scroll_top = True
        st.rerun()

# ---------------------------------------------------------
# UI: SIMULATION (wie bisherig)
# ---------------------------------------------------------
if st.session_state.stage == "simulation":
    st.title("Market Simulation")



    idx = st.session_state.current_q_index
    total = len(SCENARIO_QUESTIONS)

    if idx >= total:
        st.session_state.stage = "results"
        st.rerun()
    else:
        q = SCENARIO_QUESTIONS[idx]
        phase = q["phase"]

        # Show phase intro if not seen yet
        if phase not in st.session_state.seen_phase_intros:
            render_phase_intro(phase)
            st.stop()

        # Set start time if new question
        if st.session_state.current_question_id != q["id"]:
            st.session_state.current_question_id = q["id"]
            st.session_state.question_start_time = time.time()

        phase_label = {
            "calm": "Calm Market",
            "boom": "Boom / Euphoria",
            "crisis": "Crisis / Crash"
        }.get(q["phase"], q["phase"])

        st.markdown(f"**Question {idx + 1} of {total}**")
        st.markdown(f"**Market situation:** {phase_label}")

        invest_amount = st.session_state.demographics.get("invest_amount", 10_000.0)

        # Dynamic question text for Q1 & Q2
        if q["id"] == 1:
            q_text = (
                f"Markets are stable, the economy is growing moderately. "
                f"You have **approx. {invest_amount:,.0f} CHF** available to invest. "
                "How would you invest it now?"
            )
        elif q["id"] == 2:
            bonus = 0.10 * invest_amount
           
            q_text = (
                f"You receive a **bonus of approx. {bonus:,.0f} CHF** in addition to your original amount "
                f"of approx. {invest_amount:,.0f} CHF. How much of this bonus would you invest in stocks?"
            )
        else:
            q_text = q["question"]

        st.write(q_text)

        # Option labels with absolute values (return + volatility)
        def format_option_label(opt):
            base = opt["label"]
            mu = opt.get("mu")
            sigma = opt.get("sigma")

            if mu is None or sigma is None:
                return base

            try:
                ret_amt = invest_amount * mu / 100.0
                vol_amt = invest_amount * sigma / 100.0

                # +/- for return depending on sign
                if mu > 0:
                    ret_str = f"≈ +{ret_amt:,.0f} CHF p.a."
                elif mu < 0:
                    ret_str = f"≈ {ret_amt:,.0f} CHF p.a."
                else:
                    ret_str = "≈ 0 CHF p.a."

                base = (
                    f"{base} "
                    f"({ret_str}; "
                    f"Volatility approx. ±{sigma:.0f}% ≈ ±{vol_amt:,.0f} CHF)"
                )
            except Exception:
                # Fallback: only base text
                pass

            return base

        # Display plain labels only; risk ranks remain hidden
        display_labels = [format_option_label(opt) for opt in q["options"]]

        selected_index = st.radio(
            "Choose an option:",
            options=list(range(len(display_labels))),
            format_func=lambda i: display_labels[i],
            index=0
        )

        advisor_help_used = st.checkbox(
            "I would like help from an advisor here.",
            key=f"help_{q['id']}"
        )

        # Pulse slider at end of question, below answers
        pulse_value = st.slider(
            "If you look at your smartwatch: What is your current pulse (bpm)?",
            min_value=40,
            max_value=180,
            value=75,
            key=f"pulse_{q['id']}"
        )

        col1, col2 = st.columns([1, 1])
        with col1:
            next_clicked = st.button("Continue ▶", key=f"next_{q['id']}")
        with col2:
            st.write("")

        if next_clicked:
            reaction_time = time.time() - st.session_state.question_start_time

            chosen_opt = q["options"][selected_index]

            # Compute risk from explicit risk_level (1..4); fallback to sigma rank if not provided
            chosen_opt_risk_level = q["options"][selected_index].get("risk_level")
            if isinstance(chosen_opt_risk_level, (int, float)):
                # Normalize to [0,1] with 4 options
                x_risk_relative = (float(chosen_opt_risk_level) - 1.0) / 3.0
            else:
                # Fallback: per-question ranking by sigma ascending
                sigmas_with_index = [(opt.get("sigma", 0), idx) for idx, opt in enumerate(q["options"])]
                sorted_by_sigma = sorted(sigmas_with_index, key=lambda t: t[0])
                rank_map = {idx: (pos + 1) for pos, (_, idx) in enumerate(sorted_by_sigma)}
                n_opts = len(q["options"]) 
                denom = max(n_opts - 1, 1)
                chosen_rank = rank_map.get(selected_index, 1)
                x_risk_relative = (float(chosen_rank) - 1.0) / float(denom)

            prev_risk = (
                st.session_state.responses[-1]["x_risk_relative"]
                if st.session_state.responses else x_risk_relative
            )
            switch_action = 1 if abs(x_risk_relative - prev_risk) > 0.5 else 0

            # NEW: Flag whether question is a real herding majority question
            is_herd_majority_q = int(q.get("bias_tag") == "herding" and q.get("herd_majority") is not None)
            
            follow_crowd = 0
            if is_herd_majority_q == 1:
                if chosen_opt["label"] == q["herd_majority"]:
                    follow_crowd = 1
            
            mu_val = chosen_opt.get("mu")
            sigma_val = chosen_opt.get("sigma")

            resp = {
                "q_id": q["id"],
                "phase": q["phase"],
                "question": q["question"],
                "selected_label": chosen_opt["label"],
                "mu": mu_val,
                "sigma": sigma_val,
                "risk_level": chosen_opt.get("risk_level"),
                "risk_relevant": bool(q.get("risk_relevant", True)),
                "x_objective_risk_mean": mu_val,
                "x_objective_risk_std": sigma_val,
                "x_risk_relative": x_risk_relative,
                "x_reaction_time": reaction_time,
                "x_pulse": float(pulse_value),
                "x_eyes": 0.0,
                "x_mimic": 0.0,
                "advisor_help_used": int(advisor_help_used),
                "switch_action": switch_action,
                "bias_tag": q.get("bias_tag"),
                "follow_crowd": follow_crowd,
                "herd_majority_flag": is_herd_majority_q,  # NEW: Flag for actual herding questions
            }

            st.session_state.responses.append(resp)
            st.session_state.current_q_index += 1
            st.session_state.current_question_id = None
            st.session_state.question_start_time = None
            st.session_state.rerun_needed = True
            st.session_state.scroll_top = True
            st.rerun()


# ---------------------------------------------------------
# Peer comparison: Load, Filter, Aggregate
# ---------------------------------------------------------
def get_peer_stats(exclude_username=None, exclude_profile_id=None):
    """Load all profiles (users + guests) for peer comparison.
       Guests: username = ''.
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    if exclude_profile_id:
        c.execute("SELECT demographics, scores FROM profiles WHERE id != ?", (exclude_profile_id,))
    elif exclude_username:
        # Guests have username = '' (empty). We want all except the specified user.
        c.execute("SELECT demographics, scores FROM profiles WHERE username != ?", (exclude_username,))
    else:
        c.execute("SELECT demographics, scores FROM profiles")

    rows = c.fetchall()
    conn.close()

    data = []
    for r in rows:
        try:
            demo = json.loads(r["demographics"])
            scores = json.loads(r["scores"])
            data.append({"demo": demo, "scores": scores})
        except Exception:
            pass

    return data


def filter_peer_data(all_data, age_buckets=None, goals=None, genders=None, regions=None):
    """Filter peer data by criteria (multiple selection supported)."""
    if not all_data:
        return []

    filtered = all_data[:]

    # Age: Buckets as list of tuples [(min,max), ...]
    if age_buckets:
        def in_any_bucket(age):
            return any((age >= a and age <= b) for (a, b) in age_buckets)
        filtered = [d for d in filtered if in_any_bucket(d["demo"].get("age", 0))]

    # Investment objective: OR logic over list
    if goals:
        filtered = [d for d in filtered if d["demo"].get("goal") in goals]

    # Gender: OR logic over list
    if genders:
        filtered = [d for d in filtered if d["demo"].get("gender") in genders]

    # Region (optional, if available)
    if regions:
        filtered = [d for d in filtered if d["demo"].get("region") in regions]

    return filtered


def calculate_aggregate_scores(filtered_data):
    """Calculate average values and phase averages for comparison group."""
    if not filtered_data:
        return None

    rcs_vals, SSS_vals, rgs_vals, ans_vals = [], [], [], []
    risk_by_phase = {"calm": [], "boom": [], "crisis": []}
    stress_by_phase = {"calm": [], "boom": [], "crisis": []}

    for d in filtered_data:
        s = d["scores"]
        rcs_vals.append(s.get("RCS", 50))
        SSS_vals.append(s.get("SSS", 50))
        rgs_vals.append(s.get("RGS", 50))
        ans_vals.append(s.get("AdvisorNeedScore", 50))

        rbp = s.get("risk_by_phase", {})
        sbp = s.get("stress_by_phase", {})
        if isinstance(rbp, dict):
            for ph in ["calm", "boom", "crisis"]:
                if ph in rbp and rbp[ph] is not None:
                    risk_by_phase[ph].append(float(rbp[ph]))
        if isinstance(sbp, dict):
            for ph in ["calm", "boom", "crisis"]:
                if ph in sbp and sbp[ph] is not None:
                    stress_by_phase[ph].append(float(sbp[ph]))

    def avg(lst, default=0.0):
        return float(np.mean(lst)) if lst else default

    return {
        "count": len(filtered_data),
        "rcs_avg": avg(rcs_vals, 50),
        "SSS_avg": avg(SSS_vals, 50),
        "rgs_avg": avg(rgs_vals, 50),
        "ans_avg": avg(ans_vals, 50),
        "risk_by_phase": {
            "calm": avg(risk_by_phase["calm"], 0.5),
            "boom": avg(risk_by_phase["boom"], 0.5),
            "crisis": avg(risk_by_phase["crisis"], 0.5),
        },
        "stress_by_phase": {
            "calm": avg(stress_by_phase["calm"], 0.0),
            "boom": avg(stress_by_phase["boom"], 0.0),
            "crisis": avg(stress_by_phase["crisis"], 0.0),
        },
    }





# ---------------------------------------------------------
# UI: RESULTATE
# ---------------------------------------------------------
if st.session_state.stage == "results":
    st.title("Your NeuroRisk Profile 🧠")

    responses = st.session_state.responses
    demo = st.session_state.demographics

    if not responses:
        st.warning("No responses found – please restart the simulation.")
        if st.button("Back to Simulation"):
            # Only reset sim data; keep login
            st.session_state.responses = []
            st.session_state.demographics = {}
            st.session_state.current_q_index = 0
            st.session_state.current_question_id = None
            st.session_state.question_start_time = None
            st.session_state.seen_phase_intros = set()
            st.session_state.profile_saved = False
            st.session_state.stage = "demographics"
            st.rerun()
        st.stop()

    scores = compute_scores(demo, responses)
    df = pd.DataFrame(responses)

    # Save profile (ONLY ONCE with flag) — WITHOUT success message
    if not st.session_state.get("profile_saved"):
        if st.session_state.get("logged_in_user"):
            username = st.session_state.logged_in_user
            if save_user_profile(username, demo, responses, scores):
                st.session_state.profile_saved = True
                # ← Erfolgsmeldung entfernt!

    # Header with welcome message + options (only for logged-in user)
    if st.session_state.get("logged_in_user"):
        username = st.session_state.logged_in_user
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style="background-color: {PRIMARY_COLOR}; color: white; padding: 1.5rem; border-radius: 0.75rem; text-align: center;">
            <h3 style="margin: 0; color: white;">{username}, here is your risk profile 📊</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)



 # Buttons nicely in one line
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Start New Simulation", key="new_sim_results", width='stretch'):
            st.session_state.responses = []
            st.session_state.demographics = {}
            st.session_state.current_q_index = 0
            st.session_state.current_question_id = None
            st.session_state.question_start_time = None
            st.session_state.seen_phase_intros = set()
            st.session_state.profile_saved = False
            st.session_state.stage = "demographics"
            st.session_state.scroll_top = True
            st.rerun()

    with col2:
        if st.session_state.get("logged_in_user"):
            if st.button("Logout", key="logout_button", width='stretch'):
                st.session_state.logged_in_user = None
                st.session_state.stage = "home"
                st.session_state.scroll_top = True
                st.rerun()   

    
    # Save guest sessions
    if not st.session_state.get("profile_saved"):
        if not st.session_state.get("logged_in_user"):
            # Save guest session and profile_id
            profile_id = save_guest_profile(demo, responses, scores)
            if profile_id:
                st.session_state.profile_saved = True
                st.session_state.saved_profile_id = profile_id


    # --- Chart 1: Biometrics ---
    st.subheader("1. Biometrics")

    biometrics = df.groupby("phase")[["x_pulse", "x_reaction_time"]].mean().reindex(PHASE_ORDER)
    biometrics = biometrics.rename(columns={"x_pulse": "Average Pulse (bpm)", "x_reaction_time": "Average Reaction Time (s)"}).reset_index()
    biometrics["Market Phase"] = biometrics["phase"].map({"calm": "Calm", "boom": "Boom", "crisis": "Crisis"})

    # Short finding at bottom in section 3 incl. explanation & formula
    st.markdown("""
    Here you can see your average pulse (bpm) and average reaction time (seconds) per market phase.
    Higher values indicate stronger physiological stress, which can manifest as stress and tension.
    """)

    # Charts next to each other
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Pulse**")
        pulse_chart = (
            alt.Chart(biometrics)
            .mark_bar(color=PRIMARY_COLOR)
            .encode(
                x=alt.X("Market Phase:N", title="Market Phase"),
                y=alt.Y("Average Pulse (bpm):Q", title="Average Pulse (bpm)"),
                tooltip=[alt.Tooltip("Market Phase:N"), alt.Tooltip("Average Pulse (bpm):Q", format=".0f")]
            )
            .properties(height=200)
        )
        st.altair_chart(pulse_chart, width='stretch')

    with col_b:
        st.markdown("**Reaction Time**")
        rt_chart = (
            alt.Chart(biometrics)
            .mark_bar(color=PRIMARY_COLOR)
            .encode(
                x=alt.X("Market Phase:N", title="Market Phase"),
                y=alt.Y("Average Reaction Time (s):Q", title="Average Reaction Time (s)"),
                tooltip=[alt.Tooltip("Market Phase:N"), alt.Tooltip("Average Reaction Time (s):Q", format=".2f")]
            )
            .properties(height=200)
        )
        st.altair_chart(rt_chart, width='stretch')

    st.table(biometrics[["Market Phase", "Average Pulse (bpm)", "Average Reaction Time (s)"]].style.format({
        "Average Pulse (bpm)": "{:.0f}",
        "Average Reaction Time (s)": "{:.2f}"
    }))

    # Additional line: Facial expressions & Eye movements (Coming Soon) – two boxes side by side
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        render_coming_soon_card("Facial Expressions", "Coming soon")
    with col_c2:
        render_coming_soon_card("Eye Movements", "Coming soon")

    # --- Chart 2: Stress Progression ---
    st.subheader("2. Stress Curve")
    
    # z-score stress per phase (display directly, without 0..1 normalization)
    raw_stress = [scores["stress_by_phase"].get(p, 0.0) for p in PHASE_ORDER]

    stress_df = pd.DataFrame({
        "Market Phase": PHASE_ORDER,
        "Stress (zscore)": raw_stress
    })

    stress_chart = (
        alt.Chart(stress_df)
        .mark_line(point=True, color=PRIMARY_COLOR)
        .encode(
            x=alt.X("Market Phase:N", title="Market Phase"),
            y=alt.Y(
                "Stress (zscore):Q",
                title="Stress Index (0 = your average, >0 = more stress, <0 = less stress)",
                scale=alt.Scale(domain=[-2, 2])
            ),
            tooltip=[alt.Tooltip("Market Phase:N", title="Phase"),
                     alt.Tooltip("Stress (zscore):Q", title="Stress (z-score)", format=".2f")]
        )
        .properties(height=400)  
    )
    st.altair_chart(stress_chart, width='stretch')

    st.markdown("""
    The stress score per decision is calculated as a weighted combination of z-scores from reaction time and pulse:
    Stress_i = 0.6 · z(Reaction Time) + 0.4 · z(Pulse). The stress is then averaged over all questions per market phase.
    """)


    # --- Chart 3: Risk Progression (no filter) ---
    st.subheader("3. Risk Curve")
    risk_df = pd.DataFrame({
        "Market Phase": PHASE_ORDER,
        "Risk (0 = cautious, 1 = risk-seeking)": [scores["risk_by_phase"].get(p, 0.0) for p in PHASE_ORDER]
    })
    risk_chart = (
        alt.Chart(risk_df)
        .mark_line(point=True, color=PRIMARY_COLOR)
        .encode(
            x=alt.X("Market Phase:N", title="Market Phase"),
            y=alt.Y(
                "Risk (0 = cautious, 1 = risk-seeking):Q",
                title="Risk (0 = cautious, 1 = risk-seeking)",
                scale=alt.Scale(domain=[0,1])
            ),
        )
        .properties(height=400)  # same height as stress chart
    )
    st.altair_chart(risk_chart, width='stretch')
    
    st.markdown("""
    The risk score per decision is calculated from the relative riskiness rank of the chosen option within the question.
    By default, options are ranked 1..4 (1 = least risky, 4 = most risky). Risk_i = (risk_level − 1) / 3.0  → normalized to [0,1].
    The risk value is then averaged over all questions per market phase (0 = cautious, 1 = risk-seeking).
    """)

    # --- Scores (as before) ---
    st.subheader("4. Key Metrics (Scores)")

    def score_color_and_label(name, value, better_high=True):
        """Return HTML color and short interpretation for score."""
        val = float(value)
        if better_high:
            # high is good → green
            if val >= 75:
                color = "#16a34a"  # green
                label = "good — consistent/robust"
            elif val >= 50:
                color = "#2563eb"  # blue (instead of orange)
                label = "moderate — partially variable"
            else:
                color = "#f59e0b"  # orange (instead of red)
                label = "low — increased variability"
        else:
            # low is good → green
            if val <= 25:
                color = "#16a34a"  # green
                label = "good — low problem"
            elif val <= 50:
                color = "#2563eb"  # blue (instead of orange)
                label = "moderate — observable"
            else:
                color = "#f59e0b"  # orange (instead of red)
                label = "high — possible need for action"
        return color, label

    def render_score_card(title, score_val, desc, better_high=True):
        color, short = score_color_and_label(title, score_val, better_high)
        html = f"""
        <div style="border:1px solid #e5e7eb;border-left:6px solid {color};padding:10px;border-radius:8px;margin-bottom:8px;background:#fff;">
            <div style="font-weight:700;color:#06436D;">{title}</div>
            <div style="font-size:20px;margin-top:6px;">{int(score_val)} / 100</div>
            <div style="color:{color};font-weight:600;margin-top:6px;">{short}</div>
            <div style="margin-top:6px;color:#374151;">{desc}</div>
        </div>
        """
        st.markdown(html, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        render_score_card(
            "Risk Consistency Score",
            scores["RCS"],
            "How consistent you are with risk – across market phases. Higher = more stable.",
            better_high=True,
        )
        render_score_card(
            "Reality Gap Score",
            scores["RGS"],
            "Difference between self-image and actual behavior. Lower = better.",
            better_high=False,
        )
    with col2:
        render_score_card(
            "Stress Stability Score",
            scores["SSS"],
            "How consistent your stress is – across market phases. Higher = better.",
            better_high=True,
        )
        render_score_card(
            "Advisor Need Score",
            scores["AdvisorNeedScore"],
            "Estimate of whether external advice could be helpful. Lower = less need.",
            better_high=False,
        )

    # --- Bias interpretations (as before) ---
    st.subheader("5. Bias Cards")


    # Loss Aversion
    la = scores["loss_aversion_proxy"]
    if la > 0.2:
        st.info("🧩 **Loss Aversion:** You behave significantly more risk-seeking in boom phases than in crises. "
                "This indicates pronounced loss aversion.")
    elif la > 0.05:
        st.info("🧩 **Loss Aversion:** Slight tendency toward loss avoidance in crises – overall moderate.")
    else:
        st.info("🧩 **Loss Aversion:** Your risk choices hardly differ between boom and crisis – rather low loss aversion.")

    # Herding
    herd_score = scores["herding_score"]
    if herd_score > 70:
        st.warning("👥 **Herding Tendency:** You often follow the majority. "
                   "Make sure not to base decisions solely on 'everyone does it'.")
    elif herd_score > 30:
        st.info("👥 **Herding Tendency:** Moderate tendency to orient yourself toward the majority.")
    else:
        st.success("👥 **Herding Tendency:** Low tendency to herd – you make relatively independent decisions.")

    # Disposition Effect
    if scores["disposition"] == "high":
        st.warning("💰 **Disposition Effect:** You tend to realize gains quickly and completely. "
                   "Long-term, this can cause you to miss upside potential.")
    elif scores["disposition"] == "medium":
        st.info("💰 **Disposition Effect:** Tendency to sell on gains – normal, but observable.")

    elif scores["disposition"] == "slight":
        st.info("💰 **Disposition Effect:** Slight inclination to take profits, overall balanced.")
    elif scores["disposition"] == "low":
        st.success("💰 **Disposition Effect:** You let gains run relatively – little tendency for premature realization.")

    # Recency / Hindsight
    if scores["recency"] == "strong_negative":
        st.warning("⏳ **Recency Bias:** After short-term losses, you react very defensively. "
                   "This can lead to emotional sales.")
    elif scores["recency"] == "moderate":
        st.info("⏳ **Recency Bias:** Your reaction to short-term losses is moderate.")
    elif scores["recency"] == "resilient_proactive":
        st.success("⏳ **Recency Bias:** You not only stay calm, but also actively use declines in part.")
    elif scores["recency"] == "resilient":
        st.success("⏳ **Recency Bias:** Short-term losses seem to hardly dominate your behavior.")

    hindsight = scores.get("hindsight")
    if hindsight == "high":
        st.warning("🔁 **Hindsight / Regret:** You would clearly choose your strategy more defensively in hindsight. "
                   "This can indicate high emotional retrospective pressure.")
    elif hindsight == "moderate":
        st.info("🔁 **Hindsight / Regret:** You would change some, but not all, decisions.")
    elif hindsight == "aggressive":
        st.info("🔁 **Hindsight:** In hindsight, you would have been even more aggressive – you accept volatility relatively well.")
    elif hindsight == "low":
        st.success("🔁 **Hindsight / Regret:** You would hardly change your strategy in hindsight.")

    st.markdown("""
    <div class="neuro-card" style="background:#fff;">

      <span style="color:#16a34a;">Green</span>: positive/uncritical·
      <span style="color:#2563eb;">Blue</span>: neutral ·
      <span style="color:#f59e0b;">Orange</span>: observe/critical
    </div>
    """, unsafe_allow_html=True)

    # --- Investment Profile (new logic) ---
    st.subheader("6. Risk Character")

    risk_level = classify_risk_level(scores["BR"])
    stability_profile = classify_stability_profile(scores["RCS"], scores["SSS"])
    combined_title = f"{risk_level}, {stability_profile}"

    # Save combined name for PDF export
    risk_type = combined_title

    # Brief description and tips per archetype
    desc_map = {
        "Calm & Consistent Investor": {
            "desc": "Makes relatively similar risk decisions across all market phases. Physical signals remain stable.",
            "tips": [
                "Define long-term target allocation and consistently rebalance.",
                "Set clear rules and automate (e.g., savings plans, rebalancing).",
                "Watch for overconfidence – regular position checks."
            ],
        },
        "Calm Outside, Storm Inside": {
            "desc": "Decisions are stable, but stress indicators rise significantly in boom/crisis.",
            "tips": [
                "Schedule regular psychological check-ins.",
                "Discuss drawdown scenarios in advance, avoid surprises.",
                "Build liquidity reserve/buffer, slightly more defensive than theoretically tolerable."
            ],
        },
        "Flexible, but relaxed": {
            "desc": "Risk decisions jump between phases, stress remains calm.",
            "tips": [
                "Strengthen strategy discipline: clear guardrails for when NOT to reallocate.",
                "Define and stick to long-term target risk level.",
                "Use auto-rebalancing/savings plans, reduce spontaneous moves."
            ],
        },
        "Emotional Swing Investor": {
            "desc": "Risk and stress vary greatly between Calm/Boom/Crisis. Danger of procyclical behavior.",
            "tips": [
                "Close guidance and clear decision rules instead of ad-hoc.",
                "More structure: robust, psychologically tolerable portfolios.",
                "Use bank coaching/education modules."
            ],
        },
    }

    profile_info = desc_map.get(stability_profile, {"desc": "", "tips": []})
    tips_html = "".join(f"<li>{t}</li>" for t in profile_info["tips"])

    profile_box_html = f"""
    <div class="neuro-card" style="background:#fff;">
      <div style="font-size:1.1rem;margin:.25rem 0;color:#06436D;"><b>{combined_title}</b></div>
      <p style="margin:.5rem 0;color:#374151;">– {profile_info['desc']}</p>
      <ul style="margin:.5rem 0 .25rem 1rem;color:#374151;">
        {tips_html}
      </ul>
    </div>
    """
    st.markdown(profile_box_html, unsafe_allow_html=True)

    # Optional: Derive Advisor Need Flag from score
    ans = float(scores.get("AdvisorNeedScore", 50))
    if ans >= 66:
        advisor_flag = "high"
    elif ans >= 40:
        advisor_flag = "medium"
    else:
        advisor_flag = "low"
    st.markdown(f"<div class='neuro-card' style='background:#fff;'>📌 Advisor Need: <b>{advisor_flag}</b></div>", unsafe_allow_html=True)

    # Matrix chart (RCS vs. SSS), 0-100 scale, square, thresholds at 40 & 70
    st.markdown("**Risk Consistency Score (RCS) × Stress Stability Score (SSS) Matrix**")

    point_df = pd.DataFrame({
        "Dimension": ["Your Profile"],
        "RCS": [scores["RCS"]],
        "SSS": [scores["SSS"]],
    })


    bg_df = pd.DataFrame({
        "x1": [0,   50,  0,  50],
        "x2": [50, 100, 50, 100],
        "y1": [50,  50,  0,   0],
        "y2": [100,100, 50,  50],
        "Label": [
            "Low RCS / High SSS",
            "High RCS / High SSS",
            "Low RCS / Low SSS",
            "High RCS / Low SSS",
        ],
        "color": ["#2564eb32", "#16a34a3f", "#efc57e4b", "#2564eb32"] 
    })

    bg_layer = (
        alt.Chart(bg_df)
        .mark_rect()
        .encode(
            x=alt.X("x1:Q", title="Risk Consistency Score (RCS)", scale=alt.Scale(domain=[0, 100])),
            x2="x2:Q",
            y=alt.Y("y1:Q", title="Stress Stability Score (SSS)", scale=alt.Scale(domain=[0, 100])),
            y2="y2:Q",
            color=alt.Color("color:N", scale=None, legend=None),
        )
    )

    # Threshold lines at 50 (consistent with classification)
    rules = (
        alt.Chart(pd.DataFrame({"pos": [50]}))
        .mark_rule(color="#6b7280", strokeDash=[6, 4])
        .encode(x="pos:Q")
    ) + (
        alt.Chart(pd.DataFrame({"pos": [50]}))
        .mark_rule(color="#6b7280", strokeDash=[6, 4])
        .encode(y="pos:Q")
    )

    # Profile point
    point_layer = (
        alt.Chart(point_df)
        .mark_circle(size=420, color=PRIMARY_COLOR)
        .encode(
            x=alt.X("RCS:Q", scale=alt.Scale(domain=[0, 100])),
            y=alt.Y("SSS:Q", scale=alt.Scale(domain=[0, 100])),
            tooltip=[
                alt.Tooltip("RCS:Q", format=".0f"),
                alt.Tooltip("SSS:Q", format=".0f"),
                alt.Tooltip("Dimension:N"),
            ],
        )
    )

    # Square representation (fixed width/height)
    matrix_chart = (bg_layer + rules + point_layer).properties(width=500, height=500)
    st.altair_chart(matrix_chart, width='content')

    render_coming_soon_card(
        "AI Clustering Analysis (15 Risk Characters)",
        "Coming soon"
    )

    st.subheader("7. Interpretation")
    render_coming_soon_card("AI Analysis of your profile", "Coming soon")

    # --- NEW: 8. What-if Analyses ---
    st.markdown("---")
    st.subheader("8. What-if Analyses")
    col_w1, col_w2, col_w3 = st.columns(3)
    with col_w1:
        render_coming_soon_card("AI Prediction of your Stresslevel", "Coming soon")
    with col_w2:
        render_coming_soon_card("AI Prediction of your Panic Probability", "Coming soon")
    with col_w3:
        render_coming_soon_card("AI Prediction of your Product Misspecification", "Coming soon")

    st.markdown("---")
    st.subheader("9. Comparison with Other Users")
    
    # Determine which profiles to exclude when loading
    # IMPORTANT: Always exclude via profile_id to load ALL other profiles (users + guests)
    if st.session_state.get("logged_in_user"):
        # For logged in user: Load newest profile to get its ID
        username = st.session_state.logged_in_user
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute(
            "SELECT id FROM profiles WHERE username = ? ORDER BY timestamp DESC LIMIT 1",
            (username,)
        )
        user_profile_row = c.fetchone()
        conn.close()
        
        if user_profile_row:
            excl_id = user_profile_row["id"]
            all_peer_data = get_peer_stats(exclude_profile_id=excl_id)
        else:
            # No saved profile → show all
            all_peer_data = get_peer_stats()
    else:
        # If guest: try to exclude the just-saved profile_id (if available)
        excl_id = st.session_state.get("saved_profile_id")
        all_peer_data = get_peer_stats(exclude_profile_id=excl_id) if excl_id else get_peer_stats()
    
    if all_peer_data and len(all_peer_data) > 0:
        with st.expander("🔍 Filter & Peer Comparison", expanded=False):
            st.write(f"**Total Number of Risk Profiles:** {len(all_peer_data)}")
            
            # Multiselect filters
            col_f1, col_f2, col_f3 = st.columns(3)

            with col_f1:
                age_opts = ["18-25", "26-35", "36-45", "46-55", "56-65", "65+"]
                age_sel = st.multiselect("Age (Multiple Selection)", age_opts)

            with col_f2:
                gender_opts = ["Female", "Male", "Diverse", "No Information"]
                gender_sel = st.multiselect("Gender (Multiple Selection)", gender_opts)

            with col_f3:
                goal_opts = ["Wealth Accumulation", "Income/Dividends", "Capital Preservation/Security", "Speculation"]
                goal_sel = st.multiselect("Investment Goal (Multiple Selection)", goal_opts)

            # Derive age buckets
            age_bucket_map = {
                "18-25": (18, 25),
                "26-35": (26, 35),
                "36-45": (36, 45),
                "46-55": (46, 55),
                "56-65": (56, 65),
                "65+":   (65, 120),
            }
            age_buckets = [age_bucket_map[a] for a in age_sel] if age_sel else None
            genders = gender_sel if gender_sel else None
            goals = goal_sel if goal_sel else None

            # Filter data with multiple selection
            filtered_data = filter_peer_data(all_peer_data, age_buckets, goals, genders)

            peer_agg = calculate_aggregate_scores(filtered_data)
            
            if peer_agg and peer_agg["count"] > 0:
                st.success(f"✅ Number of Risk Profiles for Comparison: {peer_agg['count']}")
                
                # --- Risk Comparison ---
                st.markdown("#### Risk Progression (Comparison)")
                
                risk_comparison = pd.DataFrame({
                    "Market Phase": ["Calm", "Boom", "Crisis"],
                    "You": [
                        scores["risk_by_phase"].get("calm", 0.5),
                        scores["risk_by_phase"].get("boom", 0.5),
                        scores["risk_by_phase"].get("crisis", 0.5),
                    ],
                    "Ø Comparison Group": [
                        peer_agg["risk_by_phase"]["calm"],
                        peer_agg["risk_by_phase"]["boom"],
                        peer_agg["risk_by_phase"]["crisis"],
                    ]
                })
                
                risk_comp_chart = (
                    alt.Chart(risk_comparison.melt(id_vars="Market Phase", var_name="Group", value_name="Risk"))
                    .mark_line(point=True)
                    .encode(
                        x=alt.X("Market Phase:N", title="Market Phase"),
                        y=alt.Y("Risk:Q", title="Risk (0=cautious, 1=risk-seeking)", scale=alt.Scale(domain=[0, 1])),
                        color=alt.Color("Group:N", scale=alt.Scale(domain=["You", "Ø Comparison Group"], range=[PRIMARY_COLOR, "#9ca3af"])),
                        strokeDash=alt.StrokeDash("Group:N", scale=alt.Scale(domain=["You", "Ø Comparison Group"], range=[0, [5, 5]]))
                    )
                )
                st.altair_chart(risk_comp_chart, width='stretch')
                
                # --- Stress Comparison ---
                st.markdown("#### Stress Progression (Comparison)")
                
                stress_comparison = pd.DataFrame({
                    "Market Phase": ["Calm", "Boom", "Crisis"],
                    "You": [
                        scores["stress_by_phase"].get("calm", 0.0),
                        scores["stress_by_phase"].get("boom", 0.0),
                        scores["stress_by_phase"].get("crisis", 0.0),
                    ],
                    "Ø Comparison Group": [
                        peer_agg["stress_by_phase"]["calm"],
                        peer_agg["stress_by_phase"]["boom"],
                        peer_agg["stress_by_phase"]["crisis"],
                    ]
                })
                
                stress_comp_chart = (
                    alt.Chart(stress_comparison.melt(id_vars="Market Phase", var_name="Group", value_name="Stress"))
                    .mark_line(point=True)
                    .encode(
                        x=alt.X("Market Phase:N", title="Market Phase"),
                        y=alt.Y("Stress:Q", title="Stress (z-score)"),
                        color=alt.Color("Group:N", scale=alt.Scale(domain=["You", "Ø Comparison Group"], range=[PRIMARY_COLOR, "#9ca3af"])),
                        strokeDash=alt.StrokeDash("Group:N", scale=alt.Scale(domain=["You", "Ø Comparison Group"], range=[0, [5, 5]]))
                    )
                )
                st.altair_chart(stress_comp_chart, width='stretch')
                
                # --- Metrics Comparison ---
                st.markdown("#### Key Metrics (Comparison)")

                metrics = pd.DataFrame({
                    "Metric": ["RCS", "SSS", "RGS", "Advisor Need"],
                    "You": [scores["RCS"], scores["SSS"], scores["RGS"], scores["AdvisorNeedScore"]],
                    "Ø Group": [peer_agg["rcs_avg"], peer_agg["SSS_avg"], peer_agg["rgs_avg"], peer_agg["ans_avg"]]
                })

                col_m1, col_m2, col_m3, col_m4 = st.columns(4)

                for idx, row in metrics.iterrows():
                    with [col_m1, col_m2, col_m3, col_m4][idx]:
                        diff = int(row["You"] - row["Ø Group"])
                        delta_str = f"{diff:+d}" if diff != 0 else "0"
                        
                        # RCS & SSS: higher = better → normal (plus green, minus red)
                        # RGS & Advisor Need: lower = better → inverse (minus green, plus red)
                        if row["Metric"] in ["RCS", "SSS"]:
                            delta_color = "normal"
                        else:
                            delta_color = "inverse"
                        
                        st.metric(
                            row["Metric"],
                            f"{int(row['You'])}",
                            delta=delta_str,
                            delta_color=delta_color
                        )
            else:
                st.warning("❌ No users in the comparison group (filter too specific).")
    else:
        st.info("ℹ️ Not enough data available for peer comparison.")
    st.markdown("---")
    st.subheader("10. Export")

    stress_summary = {label: float(scores["stress_by_phase"].get(phase, 0.0)) for phase, label in zip(PHASE_ORDER, ["Calm", "Boom", "Crisis"])}
    risk_summary = {label: float(scores["risk_by_phase"].get(phase, 0.0)) for phase, label in zip(PHASE_ORDER, ["Calm", "Boom", "Crisis"])}

    pdf_bytes = generate_results_pdf(demo, biometrics, stress_summary, risk_summary, scores, risk_type)

    if pdf_bytes:
        st.download_button(
            "📄 Export Results as PDF",
            data=pdf_bytes,
            file_name="NeuroRiskAI_Report.pdf",
            mime="application/pdf"
        )
    else:
        st.info("PDF export requires the Python package reportlab.")

