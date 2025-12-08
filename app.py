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
TEXT_BUTTON = "#FFFFFF"  # Weisse Schrift für Buttons
BACKGROUND_LIGHT = "#FFFFFF"
BACKGROUND_SUBTLE = "#F9FAFB"
BORDER_COLOR = "#E5E7EB"


# ---------------------------------------------------------
# GLOBAL CSS – Professionelles B2C Design
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
# Grundkonfiguration & Branding
# ---------------------------------------------------------
st.set_page_config(
    page_title="NeuroRiskAI",
    page_icon="🧠",
    layout="centered"
)

st.markdown(
    f"""
    <style>
    /* Ergänzende Styles - überschreibt NICHT die Button-Styles */
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
# HELPER: Render Stepper Progress
# ---------------------------------------------------------
def render_stepper(current_phase: str):
    """Render a visual phase stepper (Calm → Boom → Crisis)"""
    phases = ["calm", "boom", "crisis"]
    labels = {"calm": "Ruhig", "boom": "Boom", "crisis": "Krise"}
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

# ---------------------------------------------------------
# HELPER: Render Phase Badge
# ---------------------------------------------------------
def render_phase_badge(phase: str):
    """Render a colored phase badge"""
    labels = {"calm": "Ruhige Phase", "boom": "Boom Phase", "crisis": "Krisen Phase"}
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
                <a href="#">Datenschutz</a> · 
                <a href="#">Impressum</a> · 
                <a href="#">Kontakt</a>
            </p>
            <p style="font-size: 0.75rem; margin-top: 1rem; color: #9CA3AF;">
                © 2025 NeuroRisk AI. Alle Rechte vorbehalten.
            </p>
        </div>
    ''', unsafe_allow_html=True)

# ---------------------------------------------------------
# Fragen & Szenarien (wie bisherig)
# ---------------------------------------------------------
SCENARIO_QUESTIONS = [
    # ---------------- CALM MARKET ----------------
    {
        "id": 1,
        "phase": "calm",
        "question": (
            "Die Märkte sind stabil, die Wirtschaft wächst moderat. "
            "Du hast den Betrag zur Verfügung, den du zu Beginn angegeben hast. "
            "Wie würdest du ihn jetzt investieren?"
        ),
        "options": [
            {"label": "Alles in Cash auf dem Konto lassen (0% Rendite, 0% Schwankung)", "mu": 0, "sigma": 0},
            {"label": "Konservativer Mischfonds: 4% erwartete Rendite, 5% Schwankung", "mu": 4, "sigma": 5},
            {"label": "Ausgewogener Fonds: 6% erwartete Rendite, 10% Schwankung", "mu": 6, "sigma": 10},
            {"label": "Dynamischer Aktienfonds: 8% erwartete Rendite, 15% Schwankung", "mu": 8, "sigma": 15},
        ],
        "bias_tag": None,
        "herd_majority": None,
    },
    {
        "id": 2,
        "phase": "calm",
        "question": (
            "Du erhältst einen Bonus zusätzlich zum ursprünglichen Betrag. "
            "Wie viel davon würdest du in Aktien investieren?"
        ),
        "options": [
            {"label": "Nichts – alles sicher halten", "mu": 1, "sigma": 1},
            {"label": "20% in Aktien, Rest sicher", "mu": 3, "sigma": 4},
            {"label": "50% in Aktien, 50% sicher", "mu": 4.5, "sigma": 8},
            {"label": "80% in Aktien, 20% sicher", "mu": 6, "sigma": 14},
        ],
        "bias_tag": None,
        "herd_majority": None,
    },
    {
        "id": 3,
        "phase": "calm",
        "question": (
            "Nach drei Monaten in einem eher ruhigen Markt liegt dein Portfolio leicht im Plus. "
            "Du hast mit deinem Startbetrag investiert und bist grundsätzlich zufrieden. Was tust du jetzt?"
        ),
        "options": [
            {"label": "Alles verkaufen und komplett in Cash gehen", "mu": 0.5, "sigma": 1},
            {"label": "Gewinne mitnehmen, einen grösseren Teil verkaufen", "mu": 2, "sigma": 3},
            {"label": "Teilverkauf, Teil investiert lassen", "mu": 3, "sigma": 5},
            {"label": "Alles investiert lassen, langfristig denken", "mu": 4, "sigma": 8},
        ],
        "bias_tag": "disposition_gain",
        "herd_majority": None,
    },
    {
        # Sharpe-Anker (calm)
        "id": 4,
        "phase": "calm",
        "question": (
            "Dein:e Berater:in zeigt dir vier Modellportfolios mit ähnlichem Chance-Risiko-Verhältnis. "
            "Alle haben ein ähnliches Verhältnis von Rendite zu Schwankung, unterscheiden sich aber im Niveau. "
            "Welches Risikoniveau fühlt sich für dich am passendsten an?"
        ),
        "options": [
            {"label": "Sehr defensiv: 2% Rendite, 3% Schwankung", "mu": 2, "sigma": 3},
            {"label": "Defensiv: 3% Rendite, 5% Schwankung", "mu": 3, "sigma": 5},
            {"label": "Ausgewogen: 4.5% Rendite, 7.5% Schwankung", "mu": 4.5, "sigma": 7.5},
            {"label": "Dynamisch: 6% Rendite, 10% Schwankung", "mu": 6, "sigma": 10},
        ],
        "bias_tag": "gain_frame",
        "herd_majority": None,
    },
    {
        "id": 5,
        "phase": "calm",
        "question": (
            "Du liest, dass 80% der anderen Anleger aktuell in Aktienfonds investiert sind. "
            "Dein Startbetrag ist noch nicht vollständig investiert. Wie reagierst du?"
        ),
        "options": [
            {"label": "Ich bleibe bei meiner defensiven Strategie", "mu": 2, "sigma": 3},
            {"label": "Ich erhöhe meine Aktienquote leicht", "mu": 3, "sigma": 5},
            {"label": "Ich erhöhe meine Aktienquote deutlich", "mu": 4.5, "sigma": 9},
            {"label": "Ich passe mich stark an und gehe sehr offensiv in Aktien", "mu": 6, "sigma": 13},
        ],
        "bias_tag": "herding",
        "herd_majority": "Ich passe mich stark an und gehe sehr offensiv in Aktien",
    },
    {
        "id": 6,
        "phase": "calm",
        "question": (
            "Es gibt keine besonderen Nachrichten. Dein Portfolio entwickelt sich in etwa wie erwartet. "
            "Was tust du mit deiner Anlagestrategie?"
        ),
        "options": [
            {"label": "Alles so lassen, gar nichts tun", "mu": 3, "sigma": 4},
            {"label": "Leicht in etwas mehr Risiko umschichten", "mu": 4, "sigma": 7},
            {"label": "Deutlich in riskantere Anlagen umschichten", "mu": 5, "sigma": 12},
            {"label": "Etwas Kapital aus dem Markt nehmen (mehr Cash)", "mu": 2, "sigma": 3},
        ],
        "bias_tag": None,
        "herd_majority": None,
    },

    # ---------------- BOOM MARKET ----------------
    {
        "id": 7,
        "phase": "boom",
        "question": (
            "Die Märkte sind in einer Rallye, viele Indizes sind auf Allzeithoch. "
            "Dein Startbetrag ist teilweise investiert, dein Portfolio ist deutlich im Plus. "
            "Wie investierst du jetzt zusätzliches Kapital?"
        ),
        "options": [
            {"label": "Ich bleibe defensiv, kein zusätzliches Risiko", "mu": 3, "sigma": 4},
            {"label": "Breiter Aktienfonds: 6% Rendite, 10% Schwankung", "mu": 6, "sigma": 10},
            {"label": "Wachstumsfonds: 9% Rendite, 18% Schwankung", "mu": 9, "sigma": 18},
            {"label": "Sektor-/Techfonds: 12% Rendite, 25% Schwankung", "mu": 12, "sigma": 25},
        ],
        "bias_tag": None,
        "herd_majority": None,
    },
    {
        "id": 8,
        "phase": "boom",
        "question": (
            "Dein Portfolio ist in den letzten 12 Monaten um 25% gestiegen. "
            "Du hast das Gefühl, 'gut im Markt' zu liegen. Was tust du?"
        ),
        "options": [
            {"label": "Gewinne realisieren, 80% verkaufen und in Cash gehen", "mu": 1, "sigma": 2},
            {"label": "Teilgewinne realisieren, 50% investiert lassen", "mu": 3, "sigma": 5},
            {"label": "Nur leicht reduzieren, grösstenteils investiert bleiben", "mu": 4.5, "sigma": 9},
            {"label": "Investiert bleiben oder sogar aufstocken, Rallye weiterreiten", "mu": 6, "sigma": 14},
        ],
        "bias_tag": "overconfidence_candidate",
        "herd_majority": None,
    },
    {
        # Sharpe-Anker (boom)
        "id": 9,
        "phase": "boom",
        "question": (
            "Nach der starken Rallye möchtest du prüfen, wie viel Wachstumsrisiko du wirklich tragen möchtest. "
            "Du kannst zwischen vier Wachstumsfonds mit ähnlichem Chance-Risiko-Verhältnis wählen, "
            "aber unterschiedlichen Risiko-Niveaus."
        ),
        "options": [
            {"label": "Defensiver Wachstumsfonds: 6% Rendite, 10% Schwankung", "mu": 6, "sigma": 10},
            {"label": "Moderater Wachstumsfonds: 7.5% Rendite, 12.5% Schwankung", "mu": 7.5, "sigma": 12.5},
            {"label": "Ausgewogener Wachstumsfonds: 9% Rendite, 15% Schwankung", "mu": 9, "sigma": 15},
            {"label": "Aggressiver Wachstumsfonds: 12% Rendite, 20% Schwankung", "mu": 12, "sigma": 20},
        ],
        "bias_tag": None,
        "herd_majority": None,
    },
    {
        "id": 10,
        "phase": "boom",
        "question": "Du kannst zwischen sicheren und riskanteren Gewinnen wählen.",
        "options": [
            {"label": "Sicherer Gewinn von 500 CHF", "mu": 5, "sigma": 0},
            {"label": "70% Chance auf 800 CHF, sonst 0 CHF", "mu": 5.6, "sigma": 12},
            {"label": "40% Chance auf 1'500 CHF, sonst 0 CHF", "mu": 6, "sigma": 20},
            {"label": "Kein sofortiger Gewinn, langfristig investiert bleiben", "mu": 4, "sigma": 8},
        ],
        "bias_tag": "gain_frame",
        "herd_majority": None,
    },
    {
        "id": 11,
        "phase": "boom",
        "question": (
            "In den Medien heisst es: 'Alle kaufen jetzt Aktien, wer nicht investiert ist, verpasst den Boom.' "
            "Du hast noch Liquidität aus deinem ursprünglichen Betrag. Wie reagierst du?"
        ),
        "options": [
            {"label": "Ich bleibe bei meiner bisherigen Strategie", "mu": 3, "sigma": 5},
            {"label": "Ich erhöhe moderat meine Aktienquote", "mu": 5, "sigma": 10},
            {"label": "Ich gehe stark in Aktien, um nichts zu verpassen", "mu": 7, "sigma": 18},
            {"label": "Ich nehme sogar Gewinne mit und reduziere Risiko", "mu": 2, "sigma": 4},
        ],
        "bias_tag": "herding",
        "herd_majority": "Ich gehe stark in Aktien, um nichts zu verpassen",
    },
    {
        "id": 12,
        "phase": "boom",
        "question": (
            "Dein Portfolio ist stark im Plus, aber du liest erste Warnungen vor einer möglichen Blase. "
            "Wie reagierst du?"
        ),
        "options": [
            {"label": "Ich reduziere Risiko deutlich", "mu": 2, "sigma": 4},
            {"label": "Ich reduziere Risiko leicht", "mu": 3, "sigma": 6},
            {"label": "Ich ändere nichts, die Rallye geht weiter", "mu": 5, "sigma": 11},
            {"label": "Ich erhöhe sogar das Risiko (Hebelprodukte, mehr Aktien)", "mu": 7, "sigma": 18},
        ],
        "bias_tag": "overconfidence_candidate",
        "herd_majority": None,
    },

    # ---------------- CRISIS MARKET ----------------
    {
        "id": 13,
        "phase": "crisis",
        "question": (
            "Die Märkte sind um 20% gefallen, dein Portfolio ist deutlich im Minus. "
            "Dein ursprünglich investierter Betrag ist spürbar geschrumpft. Was tust du?"
        ),
        "options": [
            {"label": "Alles verkaufen, Verluste begrenzen und in Cash gehen", "mu": -5, "sigma": 3},
            {"label": "Teilverkauf, Teil investiert lassen", "mu": -2, "sigma": 6},
            {"label": "Investiert bleiben, langfristige Sicht", "mu": 1, "sigma": 10},
            {"label": "Zusätzlich Kapital nachschiessen und 'billig' nachkaufen", "mu": 3, "sigma": 14},
        ],
        "bias_tag": "loss_aversion_candidate",
        "herd_majority": None,
    },
    {
        # Sharpe-Anker (crisis)
        "id": 14,
        "phase": "crisis",
        "question": (
            "Du kannst zwischen vier Strategien mit ähnlichem Chance-Risiko-Verhältnis wählen, "
            "aber auf Krisenniveau."
        ),
        "options": [
            {"label": "Sehr defensiv: -1% erwartete Rendite, 3% Schwankung", "mu": -1, "sigma": 3},
            {"label": "Defensiv: 1% Rendite, 6% Schwankung", "mu": 1, "sigma": 6},
            {"label": "Moderat offensiv: 3% Rendite, 9% Schwankung", "mu": 3, "sigma": 9},
            {"label": "Offensiv: 5% Rendite, 12% Schwankung", "mu": 5, "sigma": 12},
        ],
        "bias_tag": None,
        "herd_majority": None,
    },
    {
        "id": 15,
        "phase": "crisis",
        "question": (
            "Nach zwei weiteren negativen Börsentagen hat dein Portfolio nochmals verloren. "
            "Wie reagierst du jetzt?"
        ),
        "options": [
            {"label": "Ich verkaufe jetzt alles", "mu": -6, "sigma": 2},
            {"label": "Ich verkaufe nur einen Teil", "mu": -3, "sigma": 5},
            {"label": "Ich halte durch, ohne weiter zu investieren", "mu": 0, "sigma": 6},
            {"label": "Ich halte durch und kaufe sogar nach", "mu": 1, "sigma": 9},
        ],
        "bias_tag": "recency_candidate",
        "herd_majority": None,
    },
    {
        "id": 16,
        "phase": "crisis",
        "question": (
            "In den Medien heisst es: 'Alle verkaufen jetzt, es könnte der Beginn einer langen Krise sein.' "
            "Was tust du?"
        ),
        "options": [
            {"label": "Ich bleibe investiert, auch wenn es weh tut", "mu": 0, "sigma": 8},
            {"label": "Ich reduziere Risiko moderat", "mu": -2, "sigma": 5},
            {"label": "Ich verkaufe wie die Mehrheit", "mu": -4, "sigma": 3},
            {"label": "Ich nutze die Gelegenheit bewusst zum Nachkaufen", "mu": 2, "sigma": 10},
        ],
        "bias_tag": "herding",
        "herd_majority": "Ich verkaufe wie die Mehrheit",
    },
    {
        "id": 17,
        "phase": "crisis",
        "question": (
            "Du hast noch Liquidität aus deinem Startbetrag. Die Kurse sind stark gefallen. "
            "Wie gehst du mit zusätzlichem Kapital um?"
        ),
        "options": [
            {"label": "Keine weitere Investition, alles in Cash halten", "mu": 0, "sigma": 0},
            {"label": "Defensiven Mischfonds kaufen", "mu": 2, "sigma": 5},
            {"label": "Breiten Aktienfonds kaufen", "mu": 4, "sigma": 10},
            {"label": "Sehr riskante, stark gefallene Einzelaktien nachkaufen", "mu": 6, "sigma": 18},
        ],
        "bias_tag": None,
        "herd_majority": None,
    },
    {
        "id": 18,
        "phase": "crisis",
        "question": (
            "Angenommen, du könntest die letzten 6 Monate zurückspulen – "
            "würdest du dein Portfolio anders aufstellen?"
        ),
        "options": [
            {"label": "Ja, ich wäre viel defensiver gewesen", "mu": -1, "sigma": 2},
            {"label": "Ich würde nur kleine Anpassungen vornehmen", "mu": 0, "sigma": 4},
            {"label": "Nein, ich hätte es gleich gemacht", "mu": 1, "sigma": 6},
            {"label": "Ich wäre sogar offensiver gewesen und hätte mehr Risiko genommen", "mu": 2, "sigma": 8},
        ],
        "bias_tag": "hindsight",
        "herd_majority": None,
    },
]
PHASE_ORDER = ["calm", "boom", "crisis"]


# ---------------------------------------------------------
# SQLite Database Setup
# ---------------------------------------------------------
DB_FILE = Path(__file__).parent / "neurorisk.db"

def init_db():
    """Initialisiere SQLite-Datenbank"""
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
            username TEXT,  -- NULL für Gast-Sessions
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

# Initialisiere DB beim Start
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
        st.error(f"Fehler beim Erstellen des Accounts: {e}")
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
    """Lade das neueste Profil eines Users"""
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
    
    # Lade alle Responses für dieses Profil
    c.execute("""
        SELECT q_id, phase, selected_label, mu, sigma, x_risk_relative, 
               x_reaction_time, x_pulse, advisor_help_used, switch_action
        FROM responses 
        WHERE profile_id = ?
        ORDER BY id
    """, (profile_id,))
    
    responses_rows = c.fetchall()
    conn.close()
    
    # Konvertiere zu List of Dicts
    responses = [dict(row) for row in responses_rows]
    
    try:
        demographics = json.loads(profile["demographics"])
        scores = json.loads(profile["scores"])
    except Exception as e:
        st.error(f"Fehler beim Laden des Profils: {e}")
        return None
    
    return {
        "demographics": demographics,
        "responses": responses,
        "scores": scores,
        "timestamp": profile["timestamp"]
    }

def save_user_profile(username: str, demographics: dict, responses: list, scores: dict):
    """Speichere Profil + alle Responses"""
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        
        # Konvertiere pandas Series zu dict vor dem Speichern
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
        
        # 1. Speichere Profil-Metadaten (als JSON)
        c.execute("""
            INSERT INTO profiles (username, demographics, scores)
            VALUES (?, ?, ?)
        """, (username, json.dumps(demographics), json.dumps(scores_clean)))
        
        profile_id = c.lastrowid
        
        # 2. Speichere alle Responses
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
        st.error(f"Fehler beim Speichern des Profils: {e}")
        return False

def save_guest_profile(demographics: dict, responses: list, scores: dict):
    """Speichere Gast-Session (username = NULL).
       Liefert die neue profile_id (int) oder None bei Fehler.
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
        
        # username = NULL für Gäste
        c.execute("""
            INSERT INTO profiles (username, demographics, scores)
            VALUES (?, ?, ?)
        """, (None, json.dumps(demographics), json.dumps(scores_clean)))
        
        profile_id = c.lastrowid
        
        # Speichere Responses
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
        st.error(f"Fehler beim Speichern der Gast-Session: {e}")
        return None

# ---------------------------------------------------------
# Session State initialisieren
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
        st.session_state.saved_profile_id = None  # NEU: für Gast-Profile-ID


init_session()


# ---------------------------------------------------------
# Hilfsfunktionen für Scores
# ---------------------------------------------------------
def compute_scores(demo, responses):
    if not responses:
        return {}

    df = pd.DataFrame(responses)

    # --- Risk pro Phase ---
    risk_by_phase = df.groupby("phase")["x_risk_relative"].mean().reindex(PHASE_ORDER)
    R_calm = risk_by_phase.get("calm", 0.0)
    R_boom = risk_by_phase.get("boom", 0.0)
    R_crisis = risk_by_phase.get("crisis", 0.0)

    R_max = risk_by_phase.max()
    R_min = risk_by_phase.min()
    delta_R = float(R_max - R_min) if pd.notnull(R_max) and pd.notnull(R_min) else 0.0
    RCS = 100 * (1 - min(max(delta_R, 0.0), 1.0))  # Risk Consistency Score

    # --- Stress aus Reaktionszeit + Puls ---
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

    # --- Stress Resilience Score: konsistent mit Risk Consistency Score (max - min über alle Phasen)
    try:
        s_max = float(stress_by_phase.max())
        s_min = float(stress_by_phase.min())
    except Exception:
        s_max = 0.0
        s_min = 0.0
    delta_s = max(0.0, s_max - s_min)
    delta_s_clamped = min(max(delta_s, 0.0), 1.0)
    SRS = 100 * (1 - delta_s_clamped)  # Stress Resilience Score

    # --- Reality Gap ---
    SR = demo.get("stated_risk_norm", 0.5)
    BR = df["x_risk_relative"].mean()
    G = abs(SR - BR)
    RGS = 100 * G

    # --- Advisor Need Score ---
    RCS_norm = 1 - RCS / 100.0
    SRS_norm = 1 - SRS / 100.0
    RGS_norm = RGS / 100.0

    help_rate = df["advisor_help_used"].mean() if "advisor_help_used" in df else 0.0
    switch_rate = df["switch_action"].mean() if "switch_action" in df else 0.0

    ANS_raw = (
        0.3 * RCS_norm
        + 0.25 * SRS_norm
        + 0.25 * RGS_norm
        + 0.1 * help_rate
        + 0.1 * switch_rate
    )
    AdvisorNeedScore = 100 * ANS_raw

    # --- Bias-Proxies ---
    # Loss Aversion: Unterschied Risiko Wahl Boom vs Crisis
    loss_aversion_proxy = R_boom - R_crisis

    # Herding
    herd_rows = [r for r in responses if r.get("bias_tag") == "herding"]
    herd_follow_rate = 0.0
    if herd_rows:
        herd_follow_rate = np.mean([r.get("follow_crowd", 0) for r in herd_rows])

    # Disposition (q_id 3)
    disp = None
    disp_row = next((r for r in responses if r["q_id"] == 3), None)
    if disp_row:
        label = disp_row["selected_label"].lower()
        if "alles verkaufen" in label:
            disp = "hoch"
        elif "gewinne mitnehmen" in label or "grösseren teil" in label:
            disp = "mittel"
        elif "teilverkauf" in label:
            disp = "leicht"
        else:
            disp = "niedrig"

    # Recency (q_id 15)
    recency = None
    q15 = next((r for r in responses if r["q_id"] == 15), None)
    if q15:
        label = q15["selected_label"].lower()
        if "verkaufe jetzt alles" in label:
            recency = "stark_negativ"
        elif "verkaufe nur einen teil" in label:
            recency = "moderat"
        elif "halte durch" in label and "kaufe sogar nach" in label:
            recency = "resilient_proaktiv"
        else:
            recency = "resilient"

    # Hindsight (q_id 18)
    hindsight = None
    q18 = next((r for r in responses if r["q_id"] == 18), None)
    if q18:
        label = q18["selected_label"].lower()
        if "viel defensiver" in label:
            hindsight = "hoch"
        elif "kleine anpassungen" in label:
            hindsight = "moderat"
        elif "offensiver" in label:
            hindsight = "offensiver"
        else:
            hindsight = "gering"

    # Overconfidence-Proxy
    OC_raw = SR * (1 - RCS / 100.0) * (1 - SRS / 100.0)
    OverconfidenceScore = 100 * OC_raw

    scores = {
        "risk_by_phase": risk_by_phase,
        "stress_by_phase": stress_by_phase,
        "RCS": float(RCS),
        "SRS": float(SRS),
        "RGS": float(RGS),
        "AdvisorNeedScore": float(AdvisorNeedScore),
        "BR": float(BR),
        "SR": float(SR),
        "loss_aversion_proxy": float(loss_aversion_proxy),
        "herding_score": float(herd_follow_rate * 100),
        "disposition": disp,
        "recency": recency,
        "hindsight": hindsight,
        "OverconfidenceScore": float(OverconfidenceScore),
    }
    return scores

# ---------------------------------------------------------
# User-Management Funktionen
# ---------------------------------------------------------
USERS_FILE = Path(__file__).parent / "users.json"

# Cache für Users (vermeidet wiederholtes Lesen)
@st.cache_resource
def get_users_cache():
    return {"data": None, "last_modified": None}

def load_users():
    """Lade users.json mit lokalem Cache"""
    cache = get_users_cache()
    
    if not os.path.exists(USERS_FILE):
        return {}
    
    try:
        stat = os.stat(USERS_FILE)
        current_mtime = stat.st_mtime
        
        # Cache ist aktuell?
        if cache["data"] is not None and cache["last_modified"] == current_mtime:
            return cache["data"]
        
        # Neu laden
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        cache["data"] = data
        cache["last_modified"] = current_mtime
        return data
    except Exception as e:
        st.error(f"Fehler beim Laden: {e}")
        return {}

def save_users(users):
    """Speichere users.json und invalidiere Cache"""
    try:
        # Stelle sicher, dass Verzeichnis existiert
        USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        with open(USERS_FILE, "w", encoding="utf-8") as f:
            json.dump(users, f, ensure_ascii=False, indent=2)
        
        # Cache invalidieren
        cache = get_users_cache()
        cache["data"] = None
        cache["last_modified"] = None
    except Exception as e:
        st.error(f"Fehler beim Speichern: {e}")

# ---------------------------------------------------------
# UI: HOME-SEITE (mit Login / Konto)
# ---------------------------------------------------------
if st.session_state.stage == "home":
    # Logo einfügen – mittig zentriert OBERHALB der Card
    logo_path = Path(__file__).parent / "logo.png"
    if logo_path.exists():
        col_logo1, col_logo_center, col_logo2 = st.columns([1, 2, 1])
        with col_logo_center:
            st.image(str(logo_path), width=4000)
        st.markdown("<br>", unsafe_allow_html=True)

    # Hero Section
    st.markdown('''
        <div class="neuro-hero">
            <h2>Entdecke dein wahres Risikoprofil</h2>
            <p>
                Erfahre in nur 3 Minuten, wie du in ruhigen, euphorischen und krisenhaften 
                Märkten wirklich reagierst – nicht nur, wie du dich selbst einschätzt.
            </p>
        </div>
    ''' , unsafe_allow_html=True)

    # Feature Tiles
    st.markdown("### Warum NeuroRisk AI?")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        render_feature_tile(
            "🎯", 
            "Objektive Messung", 
            "Verhaltensbasierte Analyse statt Selbsteinschätzung"
        )
    
    with col2:
        render_feature_tile(
            "📊", 
            "Persönliches Risikoprofil", 
            "Treffe zukünftig bessere Anlageentscheidungen"
        )
    
    with col3:
        render_feature_tile(
            "🔒", 
            "Datenschutz first", 
            "DSGVO-konform, deine Daten gehören dir"
        )

    st.markdown("---") 

    tab1, tab2 = st.tabs(["🔐 Login", "👤 Gast"])

    with tab1:
        st.subheader("Mein Konto")
        with st.form("login_form", clear_on_submit=True):
            username = st.text_input("Benutzername")
            password = st.text_input("Passwort", type="password")
            col1, col2 = st.columns(2)
            with col1:
                login_btn = st.form_submit_button("Login", use_container_width=True)
            with col2:
                create_btn = st.form_submit_button("Account erstellen", use_container_width=True)

        if login_btn or create_btn:
            if not username or not password:
                st.error("❌ Benutzername und Passwort erforderlich!")
            else:
                if create_btn:
                    if user_exists(username):
                        st.error(f"❌ Benutzername '{username}' bereits vorhanden.")
                    else:
                        if create_user(username, password):
                            st.success(f"✅ Account '{username}' erstellt! Bitte jetzt einloggen.")
                        else:
                            st.error("❌ Fehler beim Erstellen des Accounts.")
                
                elif login_btn:
                    if verify_user(username, password):
                        st.success(f"✅ Eingeloggt als {username}")
                        st.session_state.logged_in_user = username
                        # Profil laden (optional in Session speichern)
                        profile = load_user_profile(username)
                        st.session_state.saved_profile = profile if profile else None
                        # Kein automatischer Wechsel der Stage hier; wir rendern die Aktionsbox unten.
                    else:
                        st.error("❌ Falscher Benutzername oder Passwort.")
    
    # NEU: Aktionsbox IMMER rendern, wenn eingeloggt (nicht nur beim Submit)
    if st.session_state.get("logged_in_user"):
        username = st.session_state.logged_in_user
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style="background-color: {PRIMARY_COLOR}; color: white; padding: 1.5rem; border-radius: 0.75rem; text-align: center;">
              <h3 style="margin: 0; color: white;">Willkommen, {username}! 👋</h3>
              <h4 style="margin: 0.5rem 0 0 0;">Starte eine neue Simulation oder sieh dir dein Profil, sofern bereits eine Simulation durchgeführt wurde</h4>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)




        col_sim1, col_sim2 = st.columns(2)
        with col_sim1:
            if st.button("Neue Simulation starten", key="new_sim_login", width="stretch"):
                # Nur Sim-Daten resetten; Login erhalten
                st.session_state.responses = []
                st.session_state.demographics = {}
                st.session_state.current_q_index = 0
                st.session_state.current_question_id = None
                st.session_state.question_start_time = None
                st.session_state.seen_phase_intros = set()
                st.session_state.profile_saved = False
                st.session_state.stage = "demographics"
                st.rerun()
        with col_sim2:
            if st.session_state.get("saved_profile"):
                if st.button("📊 My Risk Profile", key="view_profile_login", width="stretch"):
                    prof = st.session_state.saved_profile
                    st.session_state.demographics = prof["demographics"]
                    st.session_state.responses = prof["responses"]
                    st.session_state.profile_saved = True  # bereits gespeichert
                    st.session_state.stage = "results"
                    st.rerun()
            else:
                st.write("")  # Platzhalter
    else:
        with tab2:
            st.subheader("Als Gast starten")
            st.markdown(
                """
                Du kannst die Simulation auch als Gast starten. Deine Daten werden nur lokal in deinem Browser gespeichert 
                und nicht mit einem Konto verknüpft.
                """
            )
            if st.button("Simulation als Gast starten", key="guest_start"):
                st.session_state.stage = "demographics"
                st.rerun()

    st.markdown("---") 
    # How it works section
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("### So funktioniert's")
    
    st.markdown('''
        <div class="neuro-card">
            <p><strong>1. Profil erstellen</strong> – Kurze Angaben zu deiner Person und Erfahrung</p>
            <p><strong>2. Simulation durchlaufen</strong> – 18 Entscheidungen in verschiedenen Marktphasen</p>
            <p><strong>3. Ergebnis erhalten</strong> – Dein persönliches Risikoprofil mit Insights</p>
            <p><strong>4. Vergleichen</strong> – Sieh, wie du im Vergleich zu anderen abschneidest</p>
            <p><strong>5. Handeln</strong> – Leite Massnahmen ab oder optimiere dein Portfolio</p>
        </div>
    ''', unsafe_allow_html=True)
    

    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            """
            <div class="neuro-card" style="text-align: center;">
            <b>🧩 Biases erkennen</b><br>
            Herding, Loss Aversion, Overconfidence & mehr
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class="neuro-card" style="text-align: center;">
            <b>📊 Scores berechnen</b><br>
            RCS, SRS, RGS, Advisor Need Score
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            """
            <div class="neuro-card" style="text-align: center;">
            <b>💡 Profil erstellen</b><br>
            Defensiv, Ausgewogen oder Dynamisch
            </div>
            """,
            unsafe_allow_html=True,
        )

    render_footer()




# ---------------------------------------------------------
# UI: DEMOGRAFIE
# ---------------------------------------------------------
elif st.session_state.stage == "demographics":
    st.title("NeuroRisk AI – Deine Basisdaten")
    
    st.markdown("Bevor die Simulation startet, möchten wir ein paar Dinge über dich wissen.")
    
    with st.form("demographics_form"):
        st.subheader("1. Deine Basisdaten")
        age = st.number_input("Alter", min_value=18, max_value=99, value=30, step=1)
        gender = st.selectbox("Geschlecht (optional)", ["Keine Angabe", "Weiblich", "Männlich", "Divers"])
        job = st.text_input("Beruf (optional)", "")

        st.subheader("2. Erfahrung & Wissen")
        knowledge = st.slider("Wie gut schätzt du dein Finanzwissen ein?", 1, 5, 3)
        experience = st.selectbox(
            "Wie viel Anlageerfahrung hast du?",
            ["Keine", "Wenig", "Mittel", "Viel"]
        )

        st.subheader("3. Ziele & Anlagehorizont")
        goal = st.selectbox(
            "Was ist dein Hauptziel beim Anlegen?",
            ["Vermögensaufbau", "Einkommen/Dividenden", "Kapitalerhalt/Sicherheit", "Spekulation"]
        )

        invest_amount = st.number_input(
            "Gedachtes Anlagevolumen (in CHF)",
            min_value=1000,
            max_value=1_000_000,
            value=10_000,
            step=1000
        )

        amount_feel = st.selectbox(
            "Wie gross fühlt sich dieser Betrag für dich an?",
            ["Eher klein", "Mittlere Grössenordnung", "Sehr grosser Betrag für mich"]
        )

        current_investments = st.multiselect(
            "In was hast du bisher investiert?",
            ["Aktien", "Fonds/ETFs", "Obligationen", "Krypto", "Immobilien", "Cash", "Noch nichts"]
        )

        horizon = st.selectbox(
            "Anlagehorizont",
            ["Kurzfristig (< 3 Jahre)", "Mittel (3–10 Jahre)", "Langfristig (> 10 Jahre)"]
        )

        st.subheader("4. Selbstbild beim Risiko")
        stated_risk_raw = st.slider(
            "Wie risikofreudig bist du (1 = sehr vorsichtig, 7 = sehr risikofreudig)?",
            1, 7, 4
        )
        risk_constant = st.radio(
            "Ist deine Risikoneigung deiner Meinung nach in allen Marktsituationen gleich?",
            ["Ja", "Nein", "Weiss nicht"],
        )

        submitted = st.form_submit_button("Zur Simulation")

    if submitted:
        SR_norm = (stated_risk_raw - 1) / 6.0

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
            "stated_risk_norm": SR_norm,
            "risk_constant_self_view": risk_constant,
        }
        st.session_state.stated_risk_raw = stated_risk_raw
        st.session_state.stage = "simulation"
        st.rerun()

# ---------------------------------------------------------
# Phase-Intro Texte
# ---------------------------------------------------------
def render_phase_intro(phase: str):
    invest_amount = st.session_state.demographics.get("invest_amount", 10_000)

    if phase == "calm":
        title = "Phase 1 – Ruhiger Markt"
        text = (
            f"Die Wirtschaft wächst moderat, die Arbeitslosigkeit ist tief, und die Märkte schwanken nur leicht. "
            f"Du hast ca. {invest_amount:,.0f} CHF, die du anlegen möchtest. "
            "In den nächsten Fragen triffst du Entscheidungen in einem <b>ruhigen, stabilen Marktumfeld</b>."
        )
    elif phase == "boom":
        title = "Phase 2 – Boom / Euphorie"
        text = (
            "Aktienindizes sind auf oder nahe Allzeithochs, Medien berichten von einer 'Super-Rallye'. "
            "Dein Portfolio ist im Plus, das Umfeld fühlt sich optimistisch an. "
            "In den nächsten Fragen entscheidest du im Kontext eines <b>überhitzten, euphorischen Marktes</b>."
        )
    else:
        title = "Phase 3 – Krise / Crash"
        text = (
            "Die Märkte sind stark gefallen, negative Schlagzeilen dominieren. "
            "Dein investierter Betrag hat deutlich an Wert verloren. "
            "In den nächsten Fragen entscheidest du in einem <b>stressigen Krisenumfeld</b>."
        )

    st.subheader(title)
    st.markdown(f'<div class="neuro-phase-intro">{text}</div>', unsafe_allow_html=True)
    st.write("Wenn du bereit bist, starte die Fragen zu dieser Marktphase.")
    if st.button("Weiter zur ersten Frage in dieser Phase ▶"):
        st.session_state.seen_phase_intros.add(phase)
        st.rerun()

# ---------------------------------------------------------
# UI: SIMULATION (wie bisherig)
# ---------------------------------------------------------
if st.session_state.stage == "simulation":
    st.title("Markt-Simulation")

    idx = st.session_state.current_q_index
    total = len(SCENARIO_QUESTIONS)

    if idx >= total:
        st.session_state.stage = "results"
        st.rerun()
    else:
        q = SCENARIO_QUESTIONS[idx]
        phase = q["phase"]

        # Phase-Intro anzeigen, falls noch nicht gesehen
        if phase not in st.session_state.seen_phase_intros:
            render_phase_intro(phase)
            st.stop()

        # Startzeit setzen, wenn neue Frage
        if st.session_state.current_question_id != q["id"]:
            st.session_state.current_question_id = q["id"]
            st.session_state.question_start_time = time.time()

        phase_label = {
            "calm": "Ruhiger Markt",
            "boom": "Boom / Euphorie",
            "crisis": "Krise / Crash"
        }.get(q["phase"], q["phase"])

        st.markdown(f"**Frage {idx + 1} von {total}**")
        st.markdown(f"**Marktsituation:** {phase_label}")

        invest_amount = st.session_state.demographics.get("invest_amount", 10_000.0)

        # Dynamischer Fragetext für Q1 & Q2
        if q["id"] == 1:
            q_text = (
                f"Die Märkte sind stabil, die Wirtschaft wächst moderat. "
                f"Du hast **ca. {invest_amount:,.0f} CHF** zur Verfügung, die du anlegen möchtest. "
                "Wie würdest du ihn jetzt investieren?"
            )
        elif q["id"] == 2:
            bonus = 0.10 * invest_amount
            q_text = (
                f"Du erhältst einen **Bonus von ca. {bonus:,.0f} CHF** zusätzlich zu deinem ursprünglichen Betrag "
                f"von ca. {invest_amount:,.0f} CHF. Wie viel dieses Bonusbetrags würdest du in Aktien investieren?"
            )
        else:
            q_text = q["question"]

        st.write(q_text)

        # Option-Labels mit absoluten Beträgen (Rendite + Schwankung)
        def format_option_label(opt):
            base = opt["label"]
            mu = opt.get("mu")
            sigma = opt.get("sigma")

            if mu is None or sigma is None:
                return base

            try:
                ret_amt = invest_amount * mu / 100.0
                vol_amt = invest_amount * sigma / 100.0

                # +/- für Rendite je nach Vorzeichen
                if mu > 0:
                    ret_str = f"≈ +{ret_amt:,.0f} CHF p.a."
                elif mu < 0:
                    ret_str = f"≈ {ret_amt:,.0f} CHF p.a."
                else:
                    ret_str = "≈ 0 CHF p.a."

                base = (
                    f"{base} "
                    f"({ret_str}; "
                    f"Schwankung ca. ±{sigma:.0f}% ≈ ±{vol_amt:,.0f} CHF)"
                )
            except Exception:
                # Fallback: nur Basistext
                pass

            return base

        display_labels = [format_option_label(opt) for opt in q["options"]]

        selected_index = st.radio(
            "Wähle eine Option:",
            options=list(range(len(display_labels))),
            format_func=lambda i: display_labels[i],
            index=0
        )

        advisor_help_used = st.checkbox(
            "Ich würde hier gerne Hilfe von einer Beraterin / einem Berater haben.",
            key=f"help_{q['id']}"
        )

        # Puls-Slider am Ende der Frage, unter den Antworten
        pulse_value = st.slider(
            "Wenn du auf deine Smartwatch schaust: Wie hoch ist dein Puls gerade (bpm)?",
            min_value=40,
            max_value=180,
            value=75,
            key=f"pulse_{q['id']}"
        )

        col1, col2 = st.columns([1, 1])
        with col1:
            next_clicked = st.button("Weiter ▶", key=f"next_{q['id']}")
        with col2:
            st.write("")

        if next_clicked:
            reaction_time = time.time() - st.session_state.question_start_time

            chosen_opt = q["options"][selected_index]

            sigmas = [opt["sigma"] for opt in q["options"]]
            sigma_min = min(sigmas)
            sigma_max = max(sigmas)
            sigma_chosen = chosen_opt["sigma"]

            if sigma_max > sigma_min:
                x_risk_relative = (sigma_chosen - sigma_min) / (sigma_max - sigma_min)
            else:
                x_risk_relative = 0.0

            prev_risk = (
                st.session_state.responses[-1]["x_risk_relative"]
                if st.session_state.responses else x_risk_relative
            )
            switch_action = 1 if abs(x_risk_relative - prev_risk) > 0.5 else 0

            follow_crowd = 0
            if q.get("bias_tag") == "herding" and q.get("herd_majority") is not None:
                if chosen_opt["label"] == q["herd_majority"]:
                    follow_crowd = 1

            resp = {
                "q_id": q["id"],
                "phase": q["phase"],
                "question": q["question"],
                "selected_label": chosen_opt["label"],
                "mu": chosen_opt["mu"],
                "sigma": chosen_opt["sigma"],
                "x_objective_risk_mean": chosen_opt["mu"],
                "x_objective_risk_std": chosen_opt["sigma"],
                "x_risk_relative": x_risk_relative,
                "x_reaction_time": reaction_time,
                "x_pulse": float(pulse_value),
                "x_eyes": 0.0,
                "x_mimic": 0.0,
                "advisor_help_used": int(advisor_help_used),
                "switch_action": switch_action,
                "bias_tag": q.get("bias_tag"),
                "follow_crowd": follow_crowd,
            }

            st.session_state.responses.append(resp)
            st.session_state.current_q_index += 1
            st.session_state.current_question_id = None
            st.session_state.question_start_time = None
            st.rerun()


# ---------------------------------------------------------
# Peer-Vergleich: Laden, Filtern, Aggregieren
# ---------------------------------------------------------
def get_peer_stats(exclude_username=None, exclude_profile_id=None):
    """Lade alle Profile (User + Gäste) für Peer-Vergleich.
       Optional: einen username ODER eine profile_id ausschliessen.
    """
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    if exclude_profile_id:
        c.execute(
            "SELECT demographics, scores FROM profiles WHERE id != ?",
            (exclude_profile_id,),
        )
    elif exclude_username:
        c.execute(
            "SELECT demographics, scores FROM profiles WHERE (username != ? OR username IS NULL)",
            (exclude_username,),
        )
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
    """Filtere Peer-Daten nach Kriterien (Mehrfachauswahl unterstützt)."""
    if not all_data:
        return []

    filtered = all_data[:]

    # Alter: Buckets als Liste von Tupeln [(min,max), ...]
    if age_buckets:
        def in_any_bucket(age):
            return any((age >= a and age <= b) for (a, b) in age_buckets)
        filtered = [d for d in filtered if in_any_bucket(d["demo"].get("age", 0))]

    # Anlageziel: OR-Logik über Liste
    if goals:
        filtered = [d for d in filtered if d["demo"].get("goal") in goals]

    # Geschlecht: OR-Logik über Liste
    if genders:
        filtered = [d for d in filtered if d["demo"].get("gender") in genders]

    # Region (optional, falls vorhanden)
    if regions:
        filtered = [d for d in filtered if d["demo"].get("region") in regions]

    return filtered


def calculate_aggregate_scores(filtered_data):
    """Berechne Durchschnittswerte und Phasen‑Durchschnitte für Vergleichsgruppe."""
    if not filtered_data:
        return None

    rcs_vals, srs_vals, rgs_vals, ans_vals = [], [], [], []
    risk_by_phase = {"calm": [], "boom": [], "crisis": []}
    stress_by_phase = {"calm": [], "boom": [], "crisis": []}

    for d in filtered_data:
        s = d["scores"]
        rcs_vals.append(s.get("RCS", 50))
        srs_vals.append(s.get("SRS", 50))
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
        "srs_avg": avg(srs_vals, 50),
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
    st.title("Dein NeuroRisk‑Profil 🧠")

    responses = st.session_state.responses
    demo = st.session_state.demographics

    if not responses:
        st.warning("Keine Antworten gefunden – bitte starte die Simulation neu.")
        if st.button("Zurück zur Simulation"):
            # Nur Sim-Daten zurücksetzen; Login bleibt erhalten
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

    # Speichere Profil (NUR EINMAL mit Flag) — OHNE Erfolgsmeldung
    if not st.session_state.get("profile_saved"):
        if st.session_state.get("logged_in_user"):
            username = st.session_state.logged_in_user
            if save_user_profile(username, demo, responses, scores):
                st.session_state.profile_saved = True
                # ← Erfolgsmeldung entfernt!

    # Header mit Willkommensmeldung + Optionen (nur bei eingeloggtem User)
    if st.session_state.get("logged_in_user"):
        username = st.session_state.logged_in_user
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            f"""
            <div style="background-color: {PRIMARY_COLOR}; color: white; padding: 1.5rem; border-radius: 0.75rem; text-align: center;">
            <h3 style="margin: 0; color: white;">{username} hier ist dein Risikoprofil 📊</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("<br>", unsafe_allow_html=True)



 # Buttons schön in einer Zeile
    col1, col2 = st.columns(2)

    with col1:
        if st.button("Neue Simulation starten", key="new_sim_results", width="stretch"):
            st.session_state.responses = []
            st.session_state.demographics = {}
            st.session_state.current_q_index = 0
            st.session_state.current_question_id = None
            st.session_state.question_start_time = None
            st.session_state.seen_phase_intros = set()
            st.session_state.profile_saved = False
            st.session_state.stage = "demographics"
            st.rerun()

    with col2:
        if st.session_state.get("logged_in_user"):
            if st.button("Logout", key="logout_button", width="stretch"):
                st.session_state.logged_in_user = None
                st.session_state.stage = "home"
                st.rerun()   

    
    # Speichere auch Gast-Sessions
    if not st.session_state.get("profile_saved"):
        if not st.session_state.get("logged_in_user"):
            # Gast-Session speichern und profile_id speichern
            profile_id = save_guest_profile(demo, responses, scores)
            if profile_id:
                st.session_state.profile_saved = True
                st.session_state.saved_profile_id = profile_id


    # --- Chart 1: Risiko-Verlauf (ohne Filter) ---
    st.subheader("1. Risiko‑Verlauf" if not st.session_state.get("logged_in_user") else "1. Dein Risiko‑Verlauf")
    risk_df = pd.DataFrame({
        "Marktphase": PHASE_ORDER,
        "Risiko (0 = vorsichtig, 1 = risikofreudig)": [scores["risk_by_phase"].get(p, 0.0) for p in PHASE_ORDER]
    })
    risk_chart = (
        alt.Chart(risk_df)
        .mark_line(point=True, color="black")
        .encode(
            x=alt.X("Marktphase:N", title="Marktphase (Ruhig / Boom / Krise)"),
            y=alt.Y(
                "Risiko (0 = vorsichtig, 1 = risikofreudig):Q",
                title="Durchschnittliches Risiko (0 = vorsichtig, 1 = risikofreudig)",
                scale=alt.Scale(domain=[0,1])
            ),
        )
    )
    st.altair_chart(risk_chart, use_container_width=True)

    # --- Chart 2: Stress-Verlauf ---
    st.subheader("2. Stress‑Verlauf")

    # Roh‑z‑Scores pro Phase (können negativ/positiv sein)
    raw_stress = [scores["stress_by_phase"].get(p, 0.0) for p in PHASE_ORDER]

    # Normalisierung für die Visualisierung: 0..1 (clamped)
    s_min = min(raw_stress)
    s_max = max(raw_stress)
    if s_max - s_min == 0:
        stress_norm = [0.5 for _ in PHASE_ORDER]
    else:
        stress_norm = [max(0.0, min(1.0, (v - s_min) / (s_max - s_min))) for v in raw_stress]

    stress_df = pd.DataFrame({
        "Marktphase": PHASE_ORDER,
        "Stress (normalisiert)": stress_norm,
        "Stress (zscore)": raw_stress
    })

    stress_chart = (
        alt.Chart(stress_df)
        .mark_line(point=True, color="black")
        .encode(
            x=alt.X("Marktphase:N", title="Marktphase"),
            y=alt.Y("Stress (normalisiert):Q", title="Stress (0 = niedrigste, 1 = höchste gemessene Belastung)", scale=alt.Scale(domain=[0,1])),
            tooltip=[alt.Tooltip("Marktphase:N", title="Phase"),
                     alt.Tooltip("Stress (zscore):Q", title="Stress (z‑score)", format=".2f"),
                     alt.Tooltip("Stress (normalisiert):Q", title="Stress (normalisiert)", format=".2f")]
        )
    )
    st.altair_chart(stress_chart, use_container_width=True)

    st.caption("Skalierung: 0 = geringste gemessene Belastung in deinen Phasen, 1 = höchste. Tooltip zeigt rohe z‑Scores (Standardwerte).")

    # --- Chart 3: Biometrie (NUR EINMAL) ---
    st.subheader("3. Biometrie: Puls & Reaktionszeit pro Marktphase")

    biometrics = df.groupby("phase")[["x_pulse", "x_reaction_time"]].mean().reindex(PHASE_ORDER)
    biometrics = biometrics.rename(columns={"x_pulse": "Durchschnittspuls (bpm)", "x_reaction_time": "Durchschnittliche Reaktionszeit (s)"}).reset_index()
    biometrics["Marktphase"] = biometrics["phase"].map({"calm": "Ruhig", "boom": "Boom", "crisis": "Krise"})

    # Tabelle
    st.table(biometrics[["Marktphase", "Durchschnittspuls (bpm)", "Durchschnittliche Reaktionszeit (s)"]].style.format({
        "Durchschnittspuls (bpm)": "{:.0f}",
        "Durchschnittliche Reaktionszeit (s)": "{:.2f}"
    }))

    # Charts nebeneinander
    col_a, col_b = st.columns(2)
    with col_a:
        pulse_chart = (
            alt.Chart(biometrics)
            .mark_bar(color=PRIMARY_COLOR)
            .encode(
                x=alt.X("Marktphase:N", title="Marktphase"),
                y=alt.Y("Durchschnittspuls (bpm):Q", title="Durchschnittspuls (bpm)"),
                tooltip=[alt.Tooltip("Marktphase:N"), alt.Tooltip("Durchschnittspuls (bpm):Q", format=".0f")]
            )
            .properties(height=200)
        )
        st.altair_chart(pulse_chart, use_container_width=True)

    with col_b:
        rt_chart = (
            alt.Chart(biometrics)
            .mark_bar(color="#04293A")
            .encode(
                x=alt.X("Marktphase:N", title="Marktphase"),
                y=alt.Y("Durchschnittliche Reaktionszeit (s):Q", title="Durchschnittliche Reaktionszeit (s)"),
                tooltip=[alt.Tooltip("Marktphase:N"), alt.Tooltip("Durchschnittliche Reaktionszeit (s):Q", format=".2f")]
            )
            .properties(height=200)
        )
        st.altair_chart(rt_chart, use_container_width=True)

    st.markdown("**Kurzbefund:** Tabelle und Charts zeigen deinen mittleren Puls (bpm) und die durchschnittliche Reaktionszeit (Sekunden) in jeder Marktphase.")

    # --- Scores (wie bisherig) ---
    st.subheader("4. Kennzahlen (Scores)")

    def score_color_and_label(name, value, better_high=True):
        """Return HTML color and short interpretation for score."""
        val = float(value)
        if better_high:
            # green high
            if val >= 75:
                color = "#16a34a"  # green
                label = "gut — konsistent/robust"
            elif val >= 50:
                color = "#f59e0b"  # amber
                label = "moderat — teilweise variabel"
            else:
                color = "#dc2626"  # red
                label = "niedrig — erhöhte Variabilität"
        else:
            # low is good
            if val <= 25:
                color = "#16a34a"
                label = "gut — geringes Problem"
            elif val <= 50:
                color = "#f59e0b"
                label = "moderat — beobachtbar"
            else:
                color = "#dc2626"
                label = "hoch — Handlungsbedarf möglich"
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
            "Wie gleichbleibend du bei Risiko bist. Höher = stabiler.",
            better_high=True,
        )
        render_score_card(
            "Reality Gap Score",
            scores["RGS"],
            "Unterschied zwischen Selbstbild und tatsächlichem Verhalten. Niedriger = besser.",
            better_high=False,
        )
    with col2:
        render_score_card(
            "Stress Resilience Score",
            scores["SRS"],
            "Wie konstant dein Stress ist. Höher = besser.",
            better_high=True,
        )
        render_score_card(
            "Advisor Need Score",
            scores["AdvisorNeedScore"],
            "Abschätzung, ob externe Beratung hilfreich sein könnte. Niedriger = weniger Bedarf.",
            better_high=False,
        )

    # --- Bias-Interpretationen (wie bisherig) ---
    st.subheader("5. Interpretation & Bias-Karten")

    # Loss Aversion
    la = scores["loss_aversion_proxy"]
    if la > 0.2:
        st.info("🧩 **Loss Aversion:** Du verhältst dich in Boom-Phasen deutlich risikoreicher als in Krisen. "
                "Das deutet auf eine ausgeprägte Verlustaversion hin.")
    elif la > 0.05:
        st.info("🧩 **Loss Aversion:** Leichte Tendenz zur Verlustvermeidung in Krisen – insgesamt moderat.")
    else:
        st.info("🧩 **Loss Aversion:** Deine Risikowahl unterscheidet sich kaum zwischen Boom und Krise – eher geringe Loss Aversion.")

    # Herding
    herd_score = scores["herding_score"]
    if herd_score > 70:
        st.warning("👥 **Herding-Neigung:** Du folgst häufig der Mehrheit. "
                   "Achte darauf, Entscheidungen nicht nur an 'alle machen es' auszurichten.")
    elif herd_score > 30:
        st.info("👥 **Herding-Neigung:** Moderate Tendenz, dich an der Mehrheit zu orientieren.")
    else:
        st.success("👥 **Herding-Neigung:** Geringe Tendenz zum Herding – du triffst relativ eigenständige Entscheidungen.")

    # Disposition Effect
    if scores["disposition"] == "hoch":
        st.warning("💰 **Disposition Effect:** Du neigst dazu, Gewinne schnell komplett zu realisieren. "
                   "Langfristig kann das dazu führen, dass du Aufwärtspotenzial verpasst.")
    elif scores["disposition"] == "mittel":
        st.info("💰 **Disposition Effect:** Tendenz, bei Gewinnen eher zu verkaufen – normal, aber beobachtbar.")

    elif scores["disposition"] == "leicht":
        st.info("💰 **Disposition Effect:** Leichter Hang zum Gewinnmitnehmen, insgesamt ausgewogen.")
    elif scores["disposition"] == "niedrig":
        st.success("💰 **Disposition Effect:** Du lässt Gewinne relativ laufen – wenig Tendenz zu vorschnellem Realisieren.")

    # Recency / Hindsight
    if scores["recency"] == "stark_negativ":
        st.warning("⏳ **Recency Bias:** Nach kurzfristigen Verlusten reagierst du sehr defensiv. "
                   "Das kann zu emotionalen Verkäufen führen.")
    elif scores["recency"] == "moderat":
        st.info("⏳ **Recency Bias:** Deine Reaktion auf kurzfristige Verluste ist moderat.")
    elif scores["recency"] == "resilient_proaktiv":
        st.success("⏳ **Recency Bias:** Du bleibst nicht nur ruhig, sondern nutzt Rückgänge teilweise aktiv.")
    elif scores["recency"] == "resilient":
        st.success("⏳ **Recency Bias:** Kurzfristige Verluste scheinen dein Verhalten kaum zu dominieren.")

    if scores["hindsight"] == "hoch":
        st.warning("🔁 **Hindsight / Regret:** Du würdest deine Strategie im Rückblick klar defensiver wählen. "
                   "Das kann auf hohen emotionalen Rückblickdruck hindeuten.")
    elif scores["hindsight"] == "moderat":
        st.info("🔁 **Hindsight / Regret:** Du würdest einige, aber nicht alle Entscheidungen ändern.")
    elif scores["hindsight"] == "offensiver":
        st.info("🔁 **Hindsight:** Im Rückblick wärst du sogar offensiver gewesen – du akzeptierst Schwankungen relativ gut.")
    elif scores["hindsight"] == "gering":
        st.success("🔁 **Hindsight / Regret:** Du würdest deine Strategie im Rückblick kaum ändern.")

    # Overconfidence (Proxy)
    oc = scores["OverconfidenceScore"]
    if oc > 60:
        st.warning("🚀 **Overconfidence:** Dein Selbstbild, deine Konsistenz und dein Stressverhalten deuten auf "
                   "eine erhöhte Selbstüberschätzung hin – besonders in guten Marktphasen.")
    elif oc > 30:
        st.info("🚀 **Overconfidence:** Leichte Tendenz zu Overconfidence – grundsätzlich normal, aber beobachtbar.")
    else:
               st.success("🚀 **Overconfidence:** Keine starke Tendenz zu Overconfidence ersichtlich.")

    # Reality Gap
    SR = scores["SR"]
    BR = scores["BR"]
    if abs(SR - BR) > 0.3:
        st.warning("🪞 **Reality Gap:** Dein Selbstbild ('Wie risikofreudig bin ich?') "
                   "weicht deutlich von deinem tatsächlichen Verhalten in der Simulation ab.")
    else:
        st.success("🪞 **Reality Gap:** Dein Selbstbild und dein Verhalten in der Simulation sind relativ gut im Einklang.")

    # --- Anlageprofil (wie bisherig) ---
    st.subheader("6. Anlageprofil")

    BR_val = scores["BR"]
    if BR_val < 0.33:
        risk_type = "Defensiver Anleger"
    elif BR_val < 0.66:
        risk_type = "Ausgewogener Anleger"
    else:
        risk_type = "Dynamischer Anleger"

    st.write(f"**Profil:** {risk_type}")

    # Profil-Box mit beschreibungen (ohne konkrete Prozent-Angaben)
    if risk_type == "Defensiver Anleger":
        prof_html = """

        <div class="neuro-card">
        <strong>Defensiver Anleger</strong>
        <ul>
            <li>Bevorzugt Kapitalerhalt und geringe Schwankungen.</li>
            <li>Wählt eher sichere Instrumente und reduziert Risiko in unsicheren Phasen.</li>
            <li>Geeignet, wenn kurzfristige Verluste emotional stark belasten.</li>
        </ul>
        </div>
        """
    elif risk_type == "Ausgewogener Anleger":
        prof_html = """
        <div class="neuro-card">
        <strong>Ausgewogener Anleger</strong>
        <ul>
            <li>Sucht Balance zwischen Wachstumschancen und Risiko.</li>
            <li>Reagiert moderat auf Marktveränderungen, nutzt Likely sowohl Aktien- als auch sicherere Anlagen.</li>
            <li>Geeignet für einen mittelfristigen Anlagehorizont mit kontrollierter Volatilität.</li>
        </ul>
        </div>
        """
    else:
        prof_html = """
        <div class="neuro-card">
        <strong>Dynamischer Anleger</strong>
        <ul>
            <li>Akzeptiert höhere Schwankungen zugunsten größerer Chancen.</li>
            <li>Ist eher langfristig orientiert oder emotional belastbar bei Rückschlägen.</li>
            <li>Kann in Boom‑Phasen stärker zulegen, reagiert aber in Krisen möglicherweise emotionaler.</li>
        </ul>
        </div>
        """

    st.markdown(prof_html, unsafe_allow_html=True)

    # --- PEER-VERGLEICH SECTION ---
    st.markdown("---")
    st.subheader("7. Vergleich mit anderen Nutzenden")
    
    # Bestimme, welche Profile wir beim Laden ausschliessen sollen
    # WICHTIG: Immer über profile_id ausschliessen, um ALLE anderen Profile zu laden (User + Gäste)
    if st.session_state.get("logged_in_user"):
        # Beim eingeloggten User: Lade das neueste Profil, um dessen ID zu erhalten
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
            # Kein gespeichertes Profil → zeige alle
            all_peer_data = get_peer_stats()
    else:
        # Wenn Gast: versuche die gerade gespeicherte profile_id auszuschliessen (falls vorhanden)
        excl_id = st.session_state.get("saved_profile_id")
        all_peer_data = get_peer_stats(exclude_profile_id=excl_id) if excl_id else get_peer_stats()
    
    if all_peer_data and len(all_peer_data) > 0:
        with st.expander("🔍 Filter & Peer-Vergleich", expanded=False):
            st.write(f"**Totale Anzahl an Risk Profilen:** {len(all_peer_data)}")
            
            # Multiselect-Filter
            col_f1, col_f2, col_f3 = st.columns(3)

            with col_f1:
                age_opts = ["18-25", "26-35", "36-45", "46-55", "56-65", "65+"]
                age_sel = st.multiselect("Alter (Mehrfachauswahl)", age_opts)

            with col_f2:
                gender_opts = ["Weiblich", "Männlich", "Divers", "Keine Angabe"]
                gender_sel = st.multiselect("Geschlecht (Mehrfachauswahl)", gender_opts)

            with col_f3:
                goal_opts = ["Vermögensaufbau", "Einkommen/Dividenden", "Kapitalerhalt/Sicherheit", "Spekulation"]
                goal_sel = st.multiselect("Anlageziel (Mehrfachauswahl)", goal_opts)

            # Age Buckets ableiten
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

            # Filtere Daten mit Mehrfachauswahl
            filtered_data = filter_peer_data(all_peer_data, age_buckets, goals, genders)

            peer_agg = calculate_aggregate_scores(filtered_data)
            
            if peer_agg and peer_agg["count"] > 0:
                st.success(f"✅ Anzahl an Risk Profilen zum Vergleich: {peer_agg['count']}")
                
                # --- Risiko-Vergleich ---
                st.markdown("#### Risiko-Verlauf (Vergleich)")
                
                risk_comparison = pd.DataFrame({
                    "Marktphase": ["Ruhig", "Boom", "Krise"],
                    "Du": [
                        scores["risk_by_phase"].get("calm", 0.5),
                        scores["risk_by_phase"].get("boom", 0.5),
                        scores["risk_by_phase"].get("crisis", 0.5),
                    ],
                    "Ø Vergleichsgruppe": [
                        peer_agg["risk_by_phase"]["calm"],
                        peer_agg["risk_by_phase"]["boom"],
                        peer_agg["risk_by_phase"]["crisis"],
                    ]
                })
                
                risk_comp_chart = (
                    alt.Chart(risk_comparison.melt(id_vars="Marktphase", var_name="Gruppe", value_name="Risiko"))
                    .mark_line(point=True)
                    .encode(
                        x=alt.X("Marktphase:N", title="Marktphase"),
                        y=alt.Y("Risiko:Q", title="Risiko (0=vorsichtig, 1=risikofreudig)", scale=alt.Scale(domain=[0, 1])),
                        color=alt.Color("Gruppe:N", scale=alt.Scale(domain=["Du", "Ø Vergleichsgruppe"], range=[PRIMARY_COLOR, "#9ca3af"])),
                        strokeDash=alt.StrokeDash("Gruppe:N", scale=alt.Scale(domain=["Du", "Ø Vergleichsgruppe"], range=[0, [5, 5]]))
                    )
                )
                st.altair_chart(risk_comp_chart, use_container_width=True)
                
                # --- Stress-Vergleich ---
                st.markdown("#### Stress-Verlauf (Vergleich)")
                
                stress_comparison = pd.DataFrame({
                    "Marktphase": ["Ruhig", "Boom", "Krise"],
                    "Du": [
                        scores["stress_by_phase"].get("calm", 0.0),
                        scores["stress_by_phase"].get("boom", 0.0),
                        scores["stress_by_phase"].get("crisis", 0.0),
                    ],
                    "Ø Vergleichsgruppe": [
                        peer_agg["stress_by_phase"]["calm"],
                        peer_agg["stress_by_phase"]["boom"],
                        peer_agg["stress_by_phase"]["crisis"],
                    ]
                })
                
                stress_comp_chart = (
                    alt.Chart(stress_comparison.melt(id_vars="Marktphase", var_name="Gruppe", value_name="Stress"))
                    .mark_line(point=True)
                    .encode(
                        x=alt.X("Marktphase:N", title="Marktphase"),
                        y=alt.Y("Stress:Q", title="Stress (z-score)"),
                        color=alt.Color("Gruppe:N", scale=alt.Scale(domain=["Du", "Ø Vergleichsgruppe"], range=[PRIMARY_COLOR, "#9ca3af"])),
                        strokeDash=alt.StrokeDash("Gruppe:N", scale=alt.Scale(domain=["Du", "Ø Vergleichsgruppe"], range=[0, [5, 5]]))
                    )
                )
                st.altair_chart(stress_comp_chart, use_container_width=True)
                
                # --- Kennzahlen-Vergleich ---
                st.markdown("#### Kennzahlen (Vergleich)")
                
                metrics = pd.DataFrame({
                    "Kennzahl": ["RCS", "SRS", "RGS", "Advisor Need"],
                    "Du": [scores["RCS"], scores["SRS"], scores["RGS"], scores["AdvisorNeedScore"]],
                    "Ø Gruppe": [peer_agg["rcs_avg"], peer_agg["srs_avg"], peer_agg["rgs_avg"], peer_agg["ans_avg"]]
                })
                
                col_m1, col_m2, col_m3, col_m4 = st.columns(4)
                
                for idx, row in metrics.iterrows():
                    with [col_m1, col_m2, col_m3, col_m4][idx]:
                        diff = int(row["Du"] - row["Ø Gruppe"])
                        delta_str = f"{diff:+d}" if diff != 0 else "0"
                        st.metric(
                            row["Kennzahl"],
                            f"{int(row['Du'])}",
                            delta=delta_str,
                            delta_color="inverse" if row["Kennzahl"] in ["RCS", "SRS"] else "off"
                        )
            else:
                st.warning("❌ Keine Nutzer in der Vergleichsgruppe (zu spezifischer Filter).")
    else:
        st.info("ℹ️ Nicht genug Daten für Peer-Vergleich verfügbar.")

    render_footer()

