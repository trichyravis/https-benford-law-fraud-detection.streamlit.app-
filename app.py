
"""
Benford's Law Fraud Analytics Platform
The Mountain Path Academy — Prof. V. Ravichandran
A guided journey through fraud analytics: Learn, Analyze, Apply.
"""

import streamlit as st
import pandas as pd
import numpy as np
import math
import plotly.graph_objects as go
import plotly.express as px
from scipy import stats

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE CONFIG & MOUNTAIN PATH ACADEMY THEME
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.set_page_config(
    page_title="Benford's Law Fraud Analytics | Mountain Path Academy",
    page_icon="🏔️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Mountain Path Academy CSS — deep navy, gold accents, clean typography
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;600;700&family=Inter:wght@300;400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');

    :root {
        --mpa-navy: #1a1f3a;
        --mpa-dark: #0f1225;
        --mpa-gold: #d4a843;
        --mpa-gold-light: #e8c36a;
        --mpa-blue: #3a7bd5;
        --mpa-blue-light: #5b9bef;
        --mpa-teal: #2ec4b6;
        --mpa-red: #e63946;
        --mpa-green: #06d6a0;
        --mpa-orange: #f77f00;
        --mpa-bg: #fafbfd;
        --mpa-card: #ffffff;
        --mpa-text: #2d3142;
        --mpa-text-light: #6b7394;
        --mpa-border: #e8ecf4;
    }

    .stApp {
        background: linear-gradient(180deg, #f0f2f8 0%, var(--mpa-bg) 100%);
    }

    /* Sidebar — full override for dark background */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, var(--mpa-navy) 0%, var(--mpa-dark) 100%) !important;
    }
    section[data-testid="stSidebar"] > div {
        background: transparent !important;
    }
    /* All text inside sidebar: white/light for readability */
    section[data-testid="stSidebar"] * {
        color: #e0e4ef !important;
    }
    /* Radio button labels — brighter for active selection */
    section[data-testid="stSidebar"] .stRadio label {
        color: #c9cee0 !important;
        background: transparent !important;
        border-radius: 8px;
        padding: 0.3rem 0.5rem;
        margin: 0.1rem 0;
        transition: all 0.2s ease;
    }
    section[data-testid="stSidebar"] .stRadio label:hover {
        background: rgba(212, 168, 67, 0.15) !important;
        color: #ffffff !important;
    }
    section[data-testid="stSidebar"] .stRadio label span {
        color: #dce1f0 !important;
        font-family: 'Inter', sans-serif !important;
        font-size: 0.92rem !important;
    }
    /* Selected radio — gold highlight */
    section[data-testid="stSidebar"] .stRadio [data-checked="true"] span,
    section[data-testid="stSidebar"] .stRadio input:checked + div span {
        color: #ffffff !important;
        font-weight: 600 !important;
    }
    section[data-testid="stSidebar"] .stRadio [data-checked="true"],
    section[data-testid="stSidebar"] .stRadio input:checked + div {
        background: rgba(212, 168, 67, 0.2) !important;
    }
    /* Radio circles/dots */
    section[data-testid="stSidebar"] .stRadio svg {
        fill: var(--mpa-gold) !important;
        color: var(--mpa-gold) !important;
    }
    /* NAVIGATE header */
    section[data-testid="stSidebar"] .stRadio > label,
    section[data-testid="stSidebar"] .stRadio > div > label:first-child {
        color: var(--mpa-gold-light) !important;
        font-weight: 700 !important;
        font-size: 0.8rem !important;
        letter-spacing: 1.5px !important;
        text-transform: uppercase !important;
    }
    /* Sidebar horizontal rules */
    section[data-testid="stSidebar"] hr {
        border-color: #2a3158 !important;
    }
    /* Sidebar markdown bold text */
    section[data-testid="stSidebar"] strong {
        color: var(--mpa-gold-light) !important;
    }

    /* Headers */
    .mpa-header {
        background: linear-gradient(135deg, var(--mpa-navy) 0%, #2a3158 100%);
        padding: 2rem 2.5rem;
        border-radius: 16px;
        margin-bottom: 2rem;
        border-left: 5px solid var(--mpa-gold);
        box-shadow: 0 8px 32px rgba(26,31,58,0.12);
    }
    .mpa-header h1 {
        font-family: 'Playfair Display', serif;
        color: #ffffff;
        font-size: 2rem;
        margin: 0 0 0.3rem 0;
    }
    .mpa-header p {
        color: var(--mpa-gold-light);
        font-family: 'Inter', sans-serif;
        font-size: 1rem;
        margin: 0;
    }

    /* Section cards */
    .mpa-card {
        background: var(--mpa-card);
        border-radius: 12px;
        padding: 1.5rem 2rem;
        margin-bottom: 1.5rem;
        border: 1px solid var(--mpa-border);
        box-shadow: 0 2px 12px rgba(0,0,0,0.04);
    }
    .mpa-card h3 {
        font-family: 'Playfair Display', serif;
        color: var(--mpa-navy);
        border-bottom: 2px solid var(--mpa-gold);
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }

    /* Info boxes */
    .mpa-formula {
        background: linear-gradient(135deg, #f8f4e8 0%, #fdf6e3 100%);
        border-left: 4px solid var(--mpa-gold);
        padding: 1.2rem 1.5rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.05rem;
        color: var(--mpa-navy);
    }
    .mpa-insight {
        background: linear-gradient(135deg, #e8f4fd 0%, #f0f7ff 100%);
        border-left: 4px solid var(--mpa-blue);
        padding: 1rem 1.5rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }
    .mpa-warning {
        background: linear-gradient(135deg, #fff3e0 0%, #fff8f0 100%);
        border-left: 4px solid var(--mpa-orange);
        padding: 1rem 1.5rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }
    .mpa-danger {
        background: linear-gradient(135deg, #fde8ea 0%, #fff0f1 100%);
        border-left: 4px solid var(--mpa-red);
        padding: 1rem 1.5rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }
    .mpa-success {
        background: linear-gradient(135deg, #e6f9f1 0%, #f0fdf7 100%);
        border-left: 4px solid var(--mpa-green);
        padding: 1rem 1.5rem;
        border-radius: 0 8px 8px 0;
        margin: 1rem 0;
    }

    /* Metric cards */
    .metric-row {
        display: flex;
        gap: 1rem;
        margin: 1rem 0;
    }
    .metric-card {
        flex: 1;
        background: var(--mpa-card);
        border-radius: 12px;
        padding: 1.2rem;
        text-align: center;
        border: 1px solid var(--mpa-border);
        box-shadow: 0 2px 8px rgba(0,0,0,0.03);
    }
    .metric-card .metric-value {
        font-family: 'Playfair Display', serif;
        font-size: 1.8rem;
        font-weight: 700;
        color: var(--mpa-navy);
    }
    .metric-card .metric-label {
        font-family: 'Inter', sans-serif;
        font-size: 0.8rem;
        color: var(--mpa-text-light);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Navigation pills */
    .nav-flow {
        display: flex;
        align-items: center;
        gap: 0.3rem;
        flex-wrap: wrap;
        margin: 1rem 0;
        padding: 1rem;
        background: #f5f7fc;
        border-radius: 12px;
    }
    .nav-pill {
        background: var(--mpa-navy);
        color: #fff;
        padding: 0.4rem 1rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-family: 'Inter', sans-serif;
    }
    .nav-arrow {
        color: var(--mpa-gold);
        font-size: 1.2rem;
        font-weight: bold;
    }

    /* Footer */
    .mpa-footer {
        text-align: center;
        padding: 2rem;
        color: var(--mpa-text-light);
        font-family: 'Inter', sans-serif;
        font-size: 0.85rem;
        border-top: 1px solid var(--mpa-border);
        margin-top: 3rem;
    }

    /* Table styling */
    .styled-table {
        width: 100%;
        border-collapse: collapse;
        font-family: 'Inter', sans-serif;
        font-size: 0.9rem;
    }
    .styled-table th {
        background: var(--mpa-navy);
        color: #fff;
        padding: 0.8rem 1rem;
        text-align: left;
        font-weight: 500;
    }
    .styled-table td {
        padding: 0.7rem 1rem;
        border-bottom: 1px solid var(--mpa-border);
        color: var(--mpa-text);
    }
    .styled-table tr:nth-child(even) {
        background: #f8f9fc;
    }
    .styled-table tr:hover {
        background: #eef1f8;
    }
</style>
""", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# HELPER FUNCTIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

def benford_prob(d):
    """First-digit Benford probability."""
    return math.log10(1 + 1 / d)

def benford_second_digit_prob(d2):
    """Second-digit Benford probability."""
    return sum(math.log10(1 + 1 / (10 * k + d2)) for k in range(1, 10))

def benford_two_digit_prob(d):
    """Two-digit Benford probability (d from 10 to 99)."""
    return math.log10(1 + 1 / d)

BENFORD_FIRST = {d: benford_prob(d) for d in range(1, 10)}
BENFORD_SECOND = {d: benford_second_digit_prob(d) for d in range(0, 10)}

def get_first_digit(x):
    """Extract the first significant digit from a number."""
    x = abs(x)
    if x == 0:
        return None
    while x < 1:
        x *= 10
    while x >= 10:
        x /= 10
    return int(x)

def get_second_digit(x):
    """Extract the second significant digit."""
    x = abs(x)
    if x == 0:
        return None
    while x < 1:
        x *= 10
    while x >= 10:
        x /= 10
    return int((x * 10) % 10)

def get_first_two_digits(x):
    """Extract first two significant digits."""
    x = abs(x)
    if x == 0:
        return None
    while x < 10:
        x *= 10
    while x >= 100:
        x /= 10
    return int(x)

def compute_chi_squared(observed_counts, expected_probs, n):
    """Compute chi-squared statistic."""
    chi2 = 0
    for d, obs in observed_counts.items():
        exp = expected_probs[d] * n
        if exp > 0:
            chi2 += (obs - exp) ** 2 / exp
    return chi2

def compute_mad(observed_props, expected_probs):
    """Compute Mean Absolute Deviation."""
    diffs = [abs(observed_props.get(d, 0) - expected_probs[d]) for d in expected_probs]
    return np.mean(diffs)

def compute_ks(observed_props, expected_probs, digits):
    """Compute Kolmogorov-Smirnov statistic."""
    cum_obs = 0
    cum_exp = 0
    max_diff = 0
    for d in digits:
        cum_obs += observed_props.get(d, 0)
        cum_exp += expected_probs[d]
        max_diff = max(max_diff, abs(cum_obs - cum_exp))
    return max_diff

def compute_z_scores(observed_props, expected_probs, n):
    """Compute Z-score for each digit."""
    z_scores = {}
    for d in expected_probs:
        p_obs = observed_props.get(d, 0)
        p_exp = expected_probs[d]
        se = math.sqrt(p_exp * (1 - p_exp) / n) if n > 0 else 1
        z = (abs(p_obs - p_exp) - 1 / (2 * n)) / se if se > 0 and n > 0 else 0
        z_scores[d] = max(z, 0)
    return z_scores

def run_benford_analysis(data, test_type="first"):
    """Run complete Benford analysis on a numeric series."""
    data = data.dropna()
    data = data[data != 0]
    n = len(data)

    if test_type == "first":
        digits = data.apply(get_first_digit).dropna().astype(int)
        expected = BENFORD_FIRST
        digit_range = range(1, 10)
    elif test_type == "second":
        digits = data.apply(get_second_digit).dropna().astype(int)
        expected = BENFORD_SECOND
        digit_range = range(0, 10)
    else:
        digits = data.apply(get_first_two_digits).dropna().astype(int)
        expected = {d: benford_two_digit_prob(d) for d in range(10, 100)}
        digit_range = range(10, 100)

    counts = digits.value_counts().to_dict()
    total = sum(counts.values())
    props = {d: counts.get(d, 0) / total for d in digit_range}

    chi2 = compute_chi_squared(counts, expected, total)
    mad = compute_mad(props, expected)
    ks = compute_ks(props, expected, digit_range)
    z_scores = compute_z_scores(props, expected, total)

    return {
        "counts": counts, "props": props, "expected": expected,
        "n": total, "chi2": chi2, "mad": mad, "ks": ks,
        "z_scores": z_scores, "digit_range": digit_range,
    }

def plot_benford_comparison(results, title="Benford's Law Analysis"):
    """Create a comparison bar chart."""
    digit_range = list(results["digit_range"])
    observed = [results["props"].get(d, 0) * 100 for d in digit_range]
    expected = [results["expected"][d] * 100 for d in digit_range]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[str(d) for d in digit_range], y=observed,
        name="Observed", marker_color="#3a7bd5",
        text=[f"{v:.1f}%" for v in observed], textposition="outside",
    ))
    fig.add_trace(go.Scatter(
        x=[str(d) for d in digit_range], y=expected,
        name="Benford Expected", mode="lines+markers",
        line=dict(color="#d4a843", width=3), marker=dict(size=8),
    ))
    fig.update_layout(
        title=dict(text=title, font=dict(family="Playfair Display", size=20, color="#1a1f3a")),
        xaxis_title="Digit", yaxis_title="Frequency (%)",
        plot_bgcolor="#fafbfd", paper_bgcolor="#ffffff",
        font=dict(family="Inter"), legend=dict(orientation="h", y=-0.15),
        margin=dict(t=60, b=60), hovermode="x unified",
        yaxis=dict(gridcolor="#e8ecf4"),
    )
    return fig


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# SIDEBAR NAVIGATION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

with st.sidebar:
    st.markdown("""
    <div style="text-align:center; padding: 1rem 0;">
        <div style="font-size: 2.5rem;">🏔️</div>
        <div style="font-family: 'Playfair Display', serif; font-size: 1.3rem; color: #d4a843; font-weight: 700;">
            The Mountain Path Academy
        </div>
        <div style="font-size: 0.75rem; color: #8891b0; margin-top: 0.3rem; letter-spacing: 1px;">
            FRAUD ANALYTICS PLATFORM
        </div>
    </div>
    <hr style="border-color: #2a3158; margin: 0.5rem 0 1rem 0;">
    """, unsafe_allow_html=True)

    page = st.radio(
        "**NAVIGATE**",
        [
            "🏠 Home",
            "📘 Learn: Benford's Law",
            "🔍 Interactive Analyzer",
            "💼 Case Study 1: GST Invoice Fraud",
            "💳 Case Study 2: Expense Report Fraud",
            "🏛️ Case Study 3: Bank Structuring",
            "🤖 ML Anomaly Detection",
            "❓ Quiz & Assessment",
            "📖 Glossary & Abbreviations",
        ],
        label_visibility="visible",
    )

    st.markdown("""
    <hr style="border-color: #2a3158; margin: 1.5rem 0 1rem 0;">
    <div style="font-size: 0.75rem; color: #6b7394; text-align: center;">
        <em>"Numbers do not lie — unless someone forces them to."</em><br>
        <span style="color: #d4a843;">— Prof. V. Ravichandran</span>
    </div>
    """, unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: HOME
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

if page == "🏠 Home":
    st.markdown("""
    <div class="mpa-header">
        <h1>Benford's Law — Fraud Analytics Platform</h1>
        <p>A Guided Journey Through Fraud Detection | The Mountain Path Academy</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="nav-flow">
        <span class="nav-pill">🏠 Home</span> <span class="nav-arrow">→</span>
        <span class="nav-pill">📘 Learn</span> <span class="nav-arrow">→</span>
        <span class="nav-pill">🔍 Analyze</span> <span class="nav-arrow">→</span>
        <span class="nav-pill">💼 Case Studies</span> <span class="nav-arrow">→</span>
        <span class="nav-pill">🤖 ML Detection</span> <span class="nav-arrow">→</span>
        <span class="nav-pill">❓ Quiz</span> <span class="nav-arrow">→</span>
        <span class="nav-pill">📖 Glossary</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Global Fraud Loss", "5% of Revenue", "ACFE 2024 Report")
    with col2:
        st.metric("India Banking Fraud", "₹13,930 Cr", "RBI FY2023")
    with col3:
        st.metric("Median Detection Lag", "12 Months", "Before Analytics")

    st.markdown("---")

    st.markdown("""
    <div class="mpa-card">
        <h3>What Is This Platform?</h3>
        <p style="font-family: 'Inter', sans-serif; color: #2d3142; line-height: 1.7;">
            This is not just an analytics tool — it is a <strong>guided learning journey</strong> through fraud detection.
            Built for students, finance professionals, and audit practitioners, this platform combines
            <strong>theory</strong>, <strong>interactive analysis</strong>, and <strong>real-world case studies</strong>
            into a single, cohesive experience.
        </p>
        <p style="font-family: 'Inter', sans-serif; color: #2d3142; line-height: 1.7;">
            <strong>Benford's Law</strong> states that in many naturally occurring datasets, lower digits
            (1, 2, 3) appear as the leading digit far more frequently than higher digits (7, 8, 9).
            When someone fabricates financial data, they unknowingly violate this natural pattern —
            and that is exactly what we detect.
        </p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("""
        <div class="mpa-card" style="text-align:center; min-height: 200px;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">📘</div>
            <h3 style="border: none; text-align: center;">Learn</h3>
            <p style="color: #6b7394; font-family: 'Inter', sans-serif;">
                Understand the mathematics, intuition, and statistical tests behind Benford's Law.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown("""
        <div class="mpa-card" style="text-align:center; min-height: 200px;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">🔍</div>
            <h3 style="border: none; text-align: center;">Analyze</h3>
            <p style="color: #6b7394; font-family: 'Inter', sans-serif;">
                Upload your dataset and run Benford analysis with Chi-Squared, MAD, KS, and Z-Score tests.
            </p>
        </div>
        """, unsafe_allow_html=True)
    with c3:
        st.markdown("""
        <div class="mpa-card" style="text-align:center; min-height: 200px;">
            <div style="font-size: 2.5rem; margin-bottom: 0.5rem;">💼</div>
            <h3 style="border: none; text-align: center;">Apply</h3>
            <p style="color: #6b7394; font-family: 'Inter', sans-serif;">
                Explore real-world case studies in GST fraud, expense manipulation, and bank structuring.
            </p>
        </div>
        """, unsafe_allow_html=True)

    # Benford distribution quick visual
    st.markdown("### Benford's Law at a Glance")
    digits = list(range(1, 10))
    probs = [benford_prob(d) * 100 for d in digits]
    fig = go.Figure(go.Bar(
        x=[str(d) for d in digits], y=probs,
        marker_color=["#1a1f3a", "#2a3158", "#3a4578", "#4a5998", "#3a7bd5",
                       "#5b9bef", "#7cb5f5", "#9dcefb", "#bde3ff"],
        text=[f"{p:.1f}%" for p in probs], textposition="outside",
    ))
    fig.update_layout(
        xaxis_title="Leading Digit", yaxis_title="Probability (%)",
        plot_bgcolor="#fafbfd", paper_bgcolor="#ffffff",
        font=dict(family="Inter"), margin=dict(t=30, b=50),
        yaxis=dict(gridcolor="#e8ecf4", range=[0, 35]),
    )
    st.plotly_chart(fig, use_container_width=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: LEARN BENFORD'S LAW
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

elif page == "📘 Learn: Benford's Law":
    st.markdown("""
    <div class="mpa-header">
        <h1>Learn: Benford's Law</h1>
        <p>The Mathematical Foundation of Fraud Detection</p>
    </div>
    """, unsafe_allow_html=True)

    # Section 1: The Story
    st.markdown("## 1. A Discovery Born from a Worn Logarithm Table")
    st.markdown("""
    In **1881**, astronomer **Simon Newcomb** noticed that early pages of shared logarithm tables
    were more worn than later pages — numbers starting with 1 were looked up far more often than
    those starting with 9.

    In **1938**, physicist **Frank Benford** rediscovered this pattern with **20,229 observations**
    across 20 different datasets — river areas, populations, addresses, death rates, and more.
    He found the same remarkable pattern every time.
    """)

    st.markdown("""
    <div class="mpa-formula">
        <strong>BENFORD'S LAW — THE CORE FORMULA</strong><br><br>
        P(d) = log₁₀(1 + 1/d) &nbsp;&nbsp; where d ∈ {1, 2, 3, 4, 5, 6, 7, 8, 9}<br><br>
        ~30.1% of numbers start with 1, ~17.6% with 2, down to ~4.6% for digit 9.
    </div>
    """, unsafe_allow_html=True)

    # Distribution table
    st.markdown("## 2. The Benford Distribution")
    benford_df = pd.DataFrame({
        "Leading Digit": range(1, 10),
        "Formula": [f"log₁₀({d+1}/{d})" for d in range(1, 10)],
        "Probability": [f"{benford_prob(d):.4f}" for d in range(1, 10)],
        "Percentage": [f"{benford_prob(d)*100:.1f}%" for d in range(1, 10)],
        "Approx. Frequency": [
            "~1 in 3", "~1 in 6", "~1 in 8", "~1 in 10", "~1 in 13",
            "~1 in 15", "~1 in 17", "~1 in 20", "~1 in 22",
        ],
    })
    st.dataframe(benford_df, use_container_width=True, hide_index=True)

    st.markdown("""
    <div class="mpa-insight">
        <strong>Key Insight:</strong> Digits 1 through 3 alone account for <strong>60.2%</strong>
        of all leading digits in naturally occurring data. This is counterintuitive — most people
        expect a uniform ~11.1% per digit.
    </div>
    """, unsafe_allow_html=True)

    # Why it works
    st.markdown("## 3. Why Does Benford's Law Work?")
    st.markdown("""
    **The Logarithmic Scale Argument:** Natural quantities grow multiplicatively.
    On a logarithmic scale, the interval from 1 to 2 (where digit = 1) is **log₁₀(2) - log₁₀(1) = 0.301**,
    which is 30.1% of the total scale from 1 to 10. The interval from 9 to 10 is only
    **log₁₀(10) - log₁₀(9) = 0.046** — just 4.6%.

    **The Growth Intuition:** Think of a stock price growing at 5% per month starting at $100.
    It takes about 7 months to pass through $100-$199 (all starting with digit 1),
    but only about 1 month to pass through $900-$999 (starting with 9).
    The stock "lingers" longer in lower-digit territory.
    """)

    # Interactive log-scale visualization
    st.markdown("### Logarithmic Scale Visualization")
    log_data = []
    for d in range(1, 10):
        log_data.append({"Digit": d, "Log Interval Width": math.log10(1 + 1/d),
                         "Start": math.log10(d), "End": math.log10(d + 1)})
    log_df = pd.DataFrame(log_data)

    fig = go.Figure()
    colors = px.colors.sequential.Blues_r[:9]
    for i, row in log_df.iterrows():
        fig.add_trace(go.Bar(
            x=[row["Log Interval Width"]], y=[str(row["Digit"])],
            orientation="h", name=f"Digit {row['Digit']}",
            marker_color=colors[i], showlegend=False,
            text=f"{row['Log Interval Width']:.3f}", textposition="inside",
        ))
    fig.update_layout(
        title="Log-Scale Interval Width per Digit",
        xaxis_title="Width on Log Scale", yaxis_title="Leading Digit",
        plot_bgcolor="#fafbfd", paper_bgcolor="#ffffff",
        font=dict(family="Inter"), barmode="stack", margin=dict(t=50),
    )
    st.plotly_chart(fig, use_container_width=True)

    # When Benford applies / doesn't
    st.markdown("## 4. When Does Benford's Law Apply?")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="mpa-success">
            <strong>✅ APPLIES TO:</strong><br>
            • Financial transactions (invoices, expenses, payments)<br>
            • Stock prices, market data<br>
            • Population figures, city sizes<br>
            • Tax returns, accounting ledgers<br>
            • River lengths, geographic areas<br>
            • Utility bills, insurance claims<br>
            • Data spanning multiple orders of magnitude
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="mpa-danger">
            <strong>❌ DOES NOT APPLY TO:</strong><br>
            • Lottery numbers (uniform by design)<br>
            • Telephone numbers (fixed format)<br>
            • Employee IDs, zip codes (assigned numbers)<br>
            • Small-range data (e.g., ages 0–100)<br>
            • Pre-set prices (₹99, ₹199, ₹299)<br>
            • Data with artificial floor/ceiling constraints<br>
            • Very small sample sizes (n < 100)
        </div>
        """, unsafe_allow_html=True)

    # Extended analysis - Second digit
    st.markdown("## 5. Beyond the First Digit")

    st.markdown("### Second Digit Distribution")
    st.markdown("""
    Benford's Law extends to the second digit, though the distribution flattens
    (range: 8.5% to 12.0% vs. the uniform 10.0%).
    """)
    st.markdown("""
    <div class="mpa-formula">
        P(second digit = d₂) = Σ(k=1 to 9) log₁₀(1 + 1/(10k + d₂)) &nbsp;&nbsp; where d₂ ∈ {0,1,...,9}
    </div>
    """, unsafe_allow_html=True)

    second_df = pd.DataFrame({
        "Digit": range(0, 10),
        "Probability %": [f"{benford_second_digit_prob(d)*100:.2f}" for d in range(0, 10)],
    })
    st.dataframe(second_df, use_container_width=True, hide_index=True)

    st.markdown("### The Two-Digit Test — Most Powerful")
    st.markdown("""
    <div class="mpa-warning">
        <strong>⚠️ WHY THIS IS THE MOST SENSITIVE TEST:</strong><br>
        Fraudsters who know "1" should be most common often overweight digit 1 but get the
        <em>granular</em> two-digit distribution (10, 11, 12, ..., 19) wrong. This test catches
        sophisticated manipulators who pass the first-digit test.
    </div>
    """, unsafe_allow_html=True)

    # Statistical Tests
    st.markdown("## 6. Statistical Tests — Is the Deviation Significant?")

    tests_data = {
        "Test": [
            "Chi-Squared (Chi-Squared Goodness-of-Fit)",
            "MAD (Mean Absolute Deviation)",
            "KS (Kolmogorov-Smirnov Test)",
            "Z-Score (Per-Digit Z-Score Test)",
        ],
        "Formula": [
            "χ² = Σ [(Oᵈ - Eᵈ)² / Eᵈ],  degrees of freedom = 8",
            "MAD = (1/9) × Σ |P(obs)ᵈ - P(Benford)ᵈ|",
            "D = max |F(obs)(d) - F(Benford)(d)|",
            "Zᵈ = (|Pobs - PBen| - 1/2n) / √(PBen(1-PBen)/n)",
        ],
        "When to Use": [
            "Overall conformity test (caution: inflated by large n)",
            "Preferred in forensic accounting — sample-size independent",
            "Small samples (n < 100); less sensitive to outliers",
            "Identify WHICH specific digit is anomalous",
        ],
    }
    st.dataframe(pd.DataFrame(tests_data), use_container_width=True, hide_index=True)

    st.markdown("### MAD Decision Thresholds (Preferred in Forensic Accounting)")
    mad_data = {
        "MAD Range": ["0.000 – 0.006", "0.006 – 0.012", "0.012 – 0.015", "> 0.015"],
        "Interpretation": ["Close conformity", "Acceptable conformity", "Marginal conformity", "Non-conformity"],
        "Action": ["No issue ✅", "Monitor 👀", "Review ⚠️", "INVESTIGATE 🚨"],
    }
    st.dataframe(pd.DataFrame(mad_data), use_container_width=True, hide_index=True)

    st.markdown("### Chi-Squared Critical Values (degrees of freedom = 8)")
    chi_data = {
        "Significance Level": ["5%", "1%", "0.1%"],
        "Critical Value": ["15.51", "20.09", "26.12"],
        "Interpretation": ["Moderate evidence", "Strong evidence", "Very strong evidence"],
    }
    st.dataframe(pd.DataFrame(chi_data), use_container_width=True, hide_index=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# PAGE: INTERACTIVE ANALYZER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

elif page == "🔍 Interactive Analyzer":
    st.markdown("""
    <div class="mpa-header">
        <h1>Interactive Benford Analyzer</h1>
        <p>Upload Your Dataset — Run Analysis Instantly — Identify Suspicious Patterns</p>
    </div>
    """, unsafe_allow_html=True)

    uploaded = st.file_uploader(
        "Upload your dataset (CSV or Excel)", type=["csv", "xlsx", "xls"],
        help="Upload a file with numeric columns to analyze.",
    )

    use_demo = st.checkbox("Use demo dataset (10,000 simulated expense claims)", value=not bool(uploaded))

    if uploaded:
        try:
            if uploaded.name.endswith(".csv"):
                df = pd.read_csv(uploaded)
            else:
                df = pd.read_excel(uploaded)
            st.success(f"Loaded **{uploaded.name}** — {len(df):,} rows, {len(df.columns)} columns")
        except Exception as e:
            st.error(f"Error reading file: {e}")
            df = None
    elif use_demo:
        np.random.seed(42)
        # Generate Benford-conforming data with some anomalies injected
        clean = np.random.lognormal(mean=8, sigma=1.5, size=9000).round(2)
        # Inject fraudulent: clustering around 49,000–49,999 (threshold gaming)
        fraud_threshold = np.random.uniform(48000, 49999, size=500).round(2)
        # Inject round numbers
        fraud_round = np.random.choice([5000, 10000, 15000, 20000, 25000, 50000], size=500)
        all_amounts = np.concatenate([clean, fraud_threshold, fraud_round])
        np.random.shuffle(all_amounts)
        df = pd.DataFrame({
            "Claim_ID": [f"CLM-{i+1:05d}" for i in range(len(all_amounts))],
            "Amount": all_amounts,
            "Department": np.random.choice(["Sales", "Marketing", "IT", "HR", "Finance"], len(all_amounts)),
        })
        st.info("Using **demo dataset**: 10,000 simulated expense claims with injected anomalies.")
    else:
        df = None

    if df is not None:
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        if not numeric_cols:
            st.error("No numeric columns found in your dataset.")
        else:
            col_to_analyze = st.selectbox("Select the numeric column to analyze:", numeric_cols)
            test_type = st.radio(
                "Analysis type:",
                ["First Digit", "Second Digit", "First Two Digits"],
                horizontal=True,
            )
            type_map = {"First Digit": "first", "Second Digit": "second", "First Two Digits": "two"}

            if st.button("🔍 Run Benford Analysis", type="primary"):
                data_series = df[col_to_analyze].dropna()
                data_series = data_series[data_series != 0]

                results = run_benford_analysis(data_series, type_map[test_type])

                # Summary metrics
                st.markdown("### Analysis Results")
                m1, m2, m3, m4 = st.columns(4)
                m1.metric("Sample Size (n)", f"{results['n']:,}")

                chi2_val = results["chi2"]
                chi2_status = "🚨" if chi2_val > 26.12 else ("⚠️" if chi2_val > 15.51 else "✅")
                m2.metric(f"Chi-Squared {chi2_status}", f"{chi2_val:.2f}")

                mad_val = results["mad"]
                if mad_val > 0.015: mad_status = "🚨 Non-conforming"
                elif mad_val > 0.012: mad_status = "⚠️ Marginal"
                elif mad_val > 0.006: mad_status = "👀 Acceptable"
                else: mad_status = "✅ Close"
                m3.metric("MAD", f"{mad_val:.4f}", mad_status)

                m4.metric("KS Statistic", f"{results['ks']:.4f}")

                # Chart
                fig = plot_benford_comparison(results, f"{test_type} — Benford Analysis: {col_to_analyze}")
                st.plotly_chart(fig, use_container_width=True)

                # Detailed results table
                st.markdown("### Detailed Digit Analysis")
                detail_rows = []
                for d in results["digit_range"]:
                    obs_count = results["counts"].get(d, 0)
                    exp_count = results["expected"][d] * results["n"]
                    obs_pct = results["props"].get(d, 0) * 100
                    exp_pct = results["expected"][d] * 100
                    z = results["z_scores"].get(d, 0)
                    flag = "🚨" if z > 2.576 else ("⚠️" if z > 1.96 else "✅")
                    detail_rows.append({
                        "Digit": d, "Observed": obs_count, "Expected": f"{exp_count:.0f}",
                        "Obs %": f"{obs_pct:.2f}%", "Benford %": f"{exp_pct:.2f}%",
                        "Diff": f"{obs_pct - exp_pct:+.2f}%", "Z-Score": f"{z:.2f}",
                        "Flag": flag,
                    })
                detail_df = pd.DataFrame(detail_rows)
                st.dataframe(detail_df, use_container_width=True, hide_index=True)

                # Z-score heatmap
                if type_map[test_type] != "two":
                    st.markdown("### Z-Score per Digit")
                    z_digits = list(results["z_scores"].keys())
                    z_vals = list(results["z_scores"].values())
                    fig_z = go.Figure(go.Bar(
                        x=[str(d) for d in z_digits], y=z_vals,
                        marker_color=["#e63946" if z > 2.576 else ("#f77f00" if z > 1.96 else "#06d6a0") for z in z_vals],
                        text=[f"{z:.2f}" for z in z_vals], textposition="outside",
                    ))
                    fig_z.add_hline(y=1.96, line_dash="dash", line_color="#f77f00", annotation_text="5% threshold")
                    fig_z.add_hline(y=2.576, line_dash="dash", line_color="#e63946", annotation_text="1% threshold")
                    fig_z.update_layout(
                        xaxis_title="Digit", yaxis_title="Z-Score",
                        plot_bgcolor="#fafbfd", paper_bgcolor="#ffffff",
                        font=dict(family="Inter"), margin=dict(t=30),
                    )
                    st.plotly_chart(fig_z, use_container_width=True)

                # Interpretation
                st.markdown("### Interpretation")
                if mad_val > 0.015:
                    st.markdown("""
                    <div class="mpa-danger">
                        <strong>🚨 NON-CONFORMING:</strong> The data significantly deviates from Benford's Law.
                        This warrants a detailed investigation. Check for data fabrication, round-number bias,
                        or threshold gaming.
                    </div>
                    """, unsafe_allow_html=True)
                elif mad_val > 0.012:
                    st.markdown("""
                    <div class="mpa-warning">
                        <strong>⚠️ MARGINAL CONFORMITY:</strong> The data shows marginal deviation.
                        Review the flagged digits and consider additional tests (summation test, per-entity analysis).
                    </div>
                    """, unsafe_allow_html=True)
                elif mad_val > 0.006:
                    st.markdown("""
                    <div class="mpa-insight">
                        <strong>👀 ACCEPTABLE CONFORMITY:</strong> Deviations are within monitoring range.
                        Continue periodic monitoring.
                    </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown("""
                    <div class="mpa-success">
                        <strong>✅ CLOSE CONFORMITY:</strong> The data closely follows Benford's Law.
                        No immediate concerns.
                    </div>
                    """, unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CASE STUDY 1: GST INVOICE FRAUD
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

elif page == "💼 Case Study 1: GST Invoice Fraud":
    st.markdown("""
    <div class="mpa-header">
        <h1>Case Study 1: GST Invoice Fraud Detection</h1>
        <p>Detecting Fake Input Tax Credit (ITC) Claims Using Benford's Law</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="mpa-card">
        <h3>Background</h3>
        <p style="font-family: 'Inter', sans-serif; color: #2d3142; line-height: 1.7;">
            The <strong>Goods and Services Tax Network (GSTN)</strong> in India processes billions of invoices annually.
            Fraudsters create <strong>shell companies</strong> to generate fake invoices and claim
            <strong>Input Tax Credit (ITC)</strong> — a form of tax evasion worth thousands of crores.
        </p>
        <p style="font-family: 'Inter', sans-serif; color: #2d3142; line-height: 1.7;">
            A genuine business generates invoices with amounts driven by market forces — pricing is varied,
            negotiated, and organic. Fabricated invoices, however, tend to use <strong>round numbers</strong>,
            repeat similar amounts, and exhibit <strong>unnatural digit patterns</strong> that violate Benford's Law.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Simulated GST data
    np.random.seed(101)
    legit_invoices = np.random.lognormal(mean=10, sigma=1.2, size=8000).round(2)
    # Fraudulent: round numbers and specific clustering
    fraud_invoices = np.random.choice(
        [25000, 50000, 100000, 75000, 150000, 200000, 49999, 99999], size=2000,
        p=[0.15, 0.20, 0.15, 0.10, 0.10, 0.10, 0.10, 0.10],
    ).astype(float)
    fraud_invoices += np.random.uniform(-500, 500, size=2000)
    all_invoices = np.concatenate([legit_invoices, fraud_invoices])
    np.random.shuffle(all_invoices)
    all_invoices = np.abs(all_invoices)

    gst_df = pd.DataFrame({"Invoice_Amount": all_invoices})

    st.markdown("### How a GST Fraudster Fails the Benford Test")
    st.markdown("""
    <div class="mpa-warning">
        <strong>Red Flags in Fake Invoice Patterns:</strong><br>
        • Uses "round" numbers: ₹25,000; ₹50,000; ₹1,00,000<br>
        • Repeats the same amounts across multiple invoices<br>
        • Amounts cluster just below audit thresholds<br>
        • Digit distribution deviates sharply from Benford's Law<br>
        • ITC claimed is disproportionate to business turnover
    </div>
    """, unsafe_allow_html=True)

    results = run_benford_analysis(gst_df["Invoice_Amount"], "first")
    fig = plot_benford_comparison(results, "First-Digit Analysis — GST Invoice Amounts (10,000 Invoices)")
    st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    col1.metric("Chi-Squared", f"{results['chi2']:.2f}", "🚨" if results["chi2"] > 26.12 else "✅")
    col2.metric("MAD", f"{results['mad']:.4f}", "🚨 Non-conforming" if results["mad"] > 0.015 else "✅")
    col3.metric("Sample Size", f"{results['n']:,}")

    # Summation test
    st.markdown("### Summation Test — Detecting Concentration")
    st.markdown("""
    The summation test checks whether certain two-digit combinations contribute a
    disproportionate share of total value. In a clean dataset, each of the 90 combinations
    (10 through 99) should contribute approximately **1/90 = 1.11%** of total value.
    """)

    two_digits = gst_df["Invoice_Amount"].apply(get_first_two_digits).dropna().astype(int)
    gst_df_temp = gst_df.copy()
    gst_df_temp["TwoDigit"] = two_digits
    summation = gst_df_temp.groupby("TwoDigit")["Invoice_Amount"].sum()
    total_value = summation.sum()
    summation_pct = (summation / total_value * 100).sort_values(ascending=False).head(10)

    fig_sum = go.Figure(go.Bar(
        x=[str(d) for d in summation_pct.index],
        y=summation_pct.values,
        marker_color=["#e63946" if v > 2.0 else "#3a7bd5" for v in summation_pct.values],
        text=[f"{v:.2f}%" for v in summation_pct.values], textposition="outside",
    ))
    fig_sum.add_hline(y=1.11, line_dash="dash", line_color="#d4a843", annotation_text="Expected: 1.11%")
    fig_sum.update_layout(
        title="Top 10 Two-Digit Combinations by Value Share",
        xaxis_title="First Two Digits", yaxis_title="% of Total Value",
        plot_bgcolor="#fafbfd", paper_bgcolor="#ffffff", font=dict(family="Inter"),
    )
    st.plotly_chart(fig_sum, use_container_width=True)

    st.markdown("""
    <div class="mpa-danger">
        <strong>🚨 Findings:</strong><br>
        • Significant concentration in round-number two-digit combinations (50, 49, 10, 25)<br>
        • These concentrations indicate systematic invoice fabrication<br>
        • Recommended action: Flag all invoices from vendors where individual MAD > 0.04 for deep investigation
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="mpa-success">
        <strong>✅ Detection Outcome:</strong><br>
        • Benford analysis flagged 2,000+ suspicious invoices out of 10,000<br>
        • Per-vendor analysis identified shell companies generating identical-pattern invoices<br>
        • ITC fraud ring worth ₹18 crore uncovered through digit-pattern analysis
    </div>
    """, unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CASE STUDY 2: EXPENSE REPORT FRAUD
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

elif page == "💳 Case Study 2: Expense Report Fraud":
    st.markdown("""
    <div class="mpa-header">
        <h1>Case Study 2: Expense Reimbursement Fraud</h1>
        <p>Detecting Inflated Claims, Round-Number Bias & Threshold Gaming</p>
    </div>
    """, unsafe_allow_html=True)

    # Use case study data from the Excel
    expense_observed = {1: 4521, 2: 5704, 3: 3224, 4: 3348, 5: 3050, 6: 1736, 7: 1364, 8: 1116, 9: 737}
    total_n = sum(expense_observed.values())

    st.markdown("""
    <div class="mpa-card">
        <h3>Scenario: Project Eagle Eye — Expense Domain</h3>
        <p style="font-family: 'Inter', sans-serif; color: #2d3142; line-height: 1.7;">
            <strong>MountainPath National Bank (MPNB)</strong> processed <strong>24,800 employee expense claims</strong>
            in FY2022. Internal audit flagged ₹87 crore in potential fraud losses across all domains.
            The Board Audit Committee sanctioned a 6-month analytics project called <strong>Project Eagle Eye</strong>.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Build results from the real data
    exp_props = {d: expense_observed[d] / total_n for d in range(1, 10)}
    chi2 = compute_chi_squared(expense_observed, BENFORD_FIRST, total_n)
    mad = compute_mad(exp_props, BENFORD_FIRST)
    z_scores = compute_z_scores(exp_props, BENFORD_FIRST, total_n)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Claims", f"{total_n:,}")
    col2.metric("Chi-Squared", f"{chi2:.2f}", "🚨 >> 26.12")
    col3.metric("MAD", f"{mad:.4f}", "🚨 Non-conforming" if mad > 0.015 else "⚠️")
    col4.metric("Most Anomalous", "Digit 2", f"Z = {z_scores[2]:.1f}")

    # Comparison chart
    digit_range = list(range(1, 10))
    observed_pct = [exp_props[d] * 100 for d in digit_range]
    expected_pct = [BENFORD_FIRST[d] * 100 for d in digit_range]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[str(d) for d in digit_range], y=observed_pct,
        name="Observed (Expense Claims)", marker_color="#e63946",
        text=[f"{v:.1f}%" for v in observed_pct], textposition="outside",
    ))
    fig.add_trace(go.Scatter(
        x=[str(d) for d in digit_range], y=expected_pct,
        name="Benford Expected", mode="lines+markers",
        line=dict(color="#d4a843", width=3), marker=dict(size=8),
    ))
    fig.update_layout(
        title="First-Digit Analysis — Employee Expense Claims (24,800 Claims)",
        xaxis_title="Leading Digit", yaxis_title="Frequency (%)",
        plot_bgcolor="#fafbfd", paper_bgcolor="#ffffff",
        font=dict(family="Inter"), legend=dict(orientation="h", y=-0.15),
    )
    st.plotly_chart(fig, use_container_width=True)

    # Detailed findings
    st.markdown("### Red Flags Detected")
    st.markdown("""
    <div class="mpa-danger">
        <strong>🚨 Critical Anomalies Found:</strong><br>
        <strong>1. Digit-1 Severely Under-represented:</strong> Only 18.1% vs expected 30.1% — a massive shortfall
        indicating claims are NOT naturally distributed.<br><br>
        <strong>2. Digit-2 Spike:</strong> 22.8% vs expected 17.6% — clustering around ₹20,000–₹29,999 range.<br><br>
        <strong>3. Digits 4 & 5 Over-represented:</strong> Claims clustering around ₹40K–₹49K and ₹50K thresholds.<br><br>
        <strong>4. Round-Number Score:</strong> 3.4 (34% of last digits are 0 or 5) — massive fabrication signal.
        Expected is ~20%. Score > 2.0 indicates significant fabrication.<br><br>
        <strong>5. Threshold Gaming:</strong> 23% of claims are exactly ₹5,000 / ₹10,000 / ₹25,000 / ₹50,000.
    </div>
    """, unsafe_allow_html=True)

    # Z-Score chart
    st.markdown("### Per-Digit Z-Scores")
    z_vals = [z_scores[d] for d in digit_range]
    fig_z = go.Figure(go.Bar(
        x=[str(d) for d in digit_range], y=z_vals,
        marker_color=["#e63946" if z > 2.576 else ("#f77f00" if z > 1.96 else "#06d6a0") for z in z_vals],
        text=[f"{z:.1f}" for z in z_vals], textposition="outside",
    ))
    fig_z.add_hline(y=1.96, line_dash="dash", line_color="#f77f00", annotation_text="5% threshold (1.96)")
    fig_z.add_hline(y=2.576, line_dash="dash", line_color="#e63946", annotation_text="1% threshold (2.576)")
    fig_z.update_layout(
        xaxis_title="Digit", yaxis_title="Z-Score",
        plot_bgcolor="#fafbfd", paper_bgcolor="#ffffff", font=dict(family="Inter"),
    )
    st.plotly_chart(fig_z, use_container_width=True)

    st.markdown("""
    <div class="mpa-success">
        <strong>✅ Investigation Outcome (from Project Eagle Eye):</strong><br>
        • 7 employees submitted 340 fabricated expense claims over 14 months — ₹3.2 Cr<br>
        • 1 senior manager approved 180 inflated travel claims (kickback arrangement) — ₹1.4 Cr<br>
        • <strong>Total fraud confirmed:</strong> ₹4.6 Crore | Employees terminated, FIR filed, ₹1.8 Cr recovered
    </div>
    """, unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# CASE STUDY 3: BANK STRUCTURING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

elif page == "🏛️ Case Study 3: Bank Structuring":
    st.markdown("""
    <div class="mpa-header">
        <h1>Case Study 3: Bank Structuring Detection</h1>
        <p>Detecting Transactions Below Regulatory Limits — PMLA Framework</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="mpa-card">
        <h3>What is Structuring?</h3>
        <p style="font-family: 'Inter', sans-serif; color: #2d3142; line-height: 1.7;">
            <strong>Structuring</strong> (also called "smurfing") is the practice of breaking large cash transactions
            into smaller amounts to avoid triggering regulatory reporting thresholds. Under India's
            <strong>Prevention of Money Laundering Act (PMLA), 2002</strong>, cash transactions of
            <strong>₹10 lakh or above</strong> must be reported to the <strong>Financial Intelligence Unit (FIU)</strong>.
        </p>
        <p style="font-family: 'Inter', sans-serif; color: #2d3142; line-height: 1.7;">
            Structurers deliberately keep transactions just below ₹10,00,000 — amounts like ₹9,50,000 or ₹9,99,000.
            This creates an unnatural spike in digit-9 as the leading digit, which Benford's Law detects instantly.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # Loan disbursement data from the Excel
    loan_observed = {1: 1526, 2: 1091, 3: 769, 4: 614, 5: 521, 6: 428, 7: 354, 8: 329, 9: 568}
    loan_n = sum(loan_observed.values())
    loan_props = {d: loan_observed[d] / loan_n for d in range(1, 10)}
    loan_chi2 = compute_chi_squared(loan_observed, BENFORD_FIRST, loan_n)
    loan_mad = compute_mad(loan_props, BENFORD_FIRST)
    loan_z = compute_z_scores(loan_props, BENFORD_FIRST, loan_n)

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Loan Records", f"{loan_n:,}")
    col2.metric("Chi-Squared", f"{loan_chi2:.2f}", "🚨" if loan_chi2 > 26.12 else "✅")
    col3.metric("MAD", f"{loan_mad:.4f}", "🚨" if loan_mad > 0.015 else "✅")
    col4.metric("Digit-9 Z-Score", f"{loan_z[9]:.1f}", "🚨 Highly Anomalous")

    # Chart
    digit_range = list(range(1, 10))
    observed_pct = [loan_props[d] * 100 for d in digit_range]
    expected_pct = [BENFORD_FIRST[d] * 100 for d in digit_range]

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=[str(d) for d in digit_range], y=observed_pct,
        name="Observed (Loan Disbursements)", marker_color="#e63946",
        text=[f"{v:.1f}%" for v in observed_pct], textposition="outside",
    ))
    fig.add_trace(go.Scatter(
        x=[str(d) for d in digit_range], y=expected_pct,
        name="Benford Expected", mode="lines+markers",
        line=dict(color="#d4a843", width=3), marker=dict(size=8),
    ))
    fig.update_layout(
        title="First-Digit Analysis — Loan Disbursements (6,200 Records)",
        xaxis_title="Leading Digit", yaxis_title="Frequency (%)",
        plot_bgcolor="#fafbfd", paper_bgcolor="#ffffff",
        font=dict(family="Inter"), legend=dict(orientation="h", y=-0.15),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div class="mpa-danger">
        <strong>🚨 Key Findings — Loan Structuring Detected:</strong><br>
        • <strong>Digit 9 massively over-represented:</strong> 9.2% vs expected 4.6% —
        loans clustering in ₹9,00,000–₹9,99,999 range to avoid ₹10L reporting threshold<br><br>
        • <strong>Digit 1 under-represented:</strong> 24.6% vs expected 30.1% —
        loans being split to stay below thresholds<br><br>
        • <strong>Branch-level analysis:</strong> 3 of 12 branches account for 72% of digit-9 anomalies —
        collusion suspected at specific locations<br><br>
        • <strong>PMLA Structuring Rule Triggered:</strong> Multiple customers with 3+ cash transactions
        totalling ≥ ₹10 lakh within rolling 30-day windows
    </div>
    """, unsafe_allow_html=True)

    # PMLA framework
    st.markdown("### PMLA Detection Framework")
    pmla_rules = {
        "Rule": [
            "Cash Transaction Reporting",
            "Structuring Detection",
            "Velocity Rule",
            "Threshold Proximity",
            "Suspicious Transaction Report (STR)",
        ],
        "Threshold": [
            "Single cash transaction ≥ ₹10 lakh",
            "3+ transactions totalling ≥ ₹10L in 30 days",
            "> mean + 3σ transactions in 1-hour window",
            "Amounts in [T - 0.5%, T] where T = approval limit",
            "Mandatory filing to FIU for flagged patterns",
        ],
        "Benford Signal": [
            "Digit-9 spike at ₹9L–₹9.99L",
            "Repeated digit patterns across transactions",
            "Abnormal frequency clustering",
            "Two-digit combination '95', '96', '97', '98', '99' elevated",
            "Aggregate non-conformity score",
        ],
    }
    st.dataframe(pd.DataFrame(pmla_rules), use_container_width=True, hide_index=True)

    st.markdown("""
    <div class="mpa-success">
        <strong>✅ Investigation Outcome:</strong><br>
        • Branch manager at 2 branches approved 84 loans at ₹9.5L–₹9.99L to avoid ₹10L regulatory reporting — ₹7.8 Cr<br>
        • Loan officer colluded with Direct Selling Agent (DSA) to fabricate income documents — ₹4.2 Cr<br>
        • <strong>Total fraud confirmed:</strong> ₹12.0 Crore | Managers suspended; loans recalled; RBI informed
    </div>
    """, unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# ML ANOMALY DETECTION
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

elif page == "🤖 ML Anomaly Detection":
    st.markdown("""
    <div class="mpa-header">
        <h1>Beyond Benford: Machine Learning Anomaly Detection</h1>
        <p>Multi-Layer Detection Framework — Isolation Forest, Autoencoders & Ensemble Scoring</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("## Multi-Method Anomaly Detection Framework")
    st.markdown("""
    Modern fraud analytics uses multiple complementary techniques layered together.
    No single method catches all fraud — ensemble approaches dramatically improve detection rates.
    """)

    layers = {
        "Layer": ["1: Rule-Based", "2: Statistical", "3: Machine Learning", "4: Network & Behavioural", "5: Human Review"],
        "Method": ["Rule-Based Detection", "Statistical Detection", "Machine Learning", "Network & Behavioural", "Human Review"],
        "Components": [
            "Transaction limits, Threshold proximity, Duplicate checks",
            "Benford's Law, Z-score, IQR, Time-series anomaly",
            "Isolation Forest, Autoencoder, DBSCAN, LOF",
            "Graph analytics, Peer comparison, Velocity checks",
            "Prioritised case queue from aggregated anomaly scores",
        ],
    }
    st.dataframe(pd.DataFrame(layers), use_container_width=True, hide_index=True)

    # Rule-based
    st.markdown("### Layer 1: Rule-Based Detection")
    rules = {
        "Rule": [
            "PMLA Structuring Rule (India)",
            "Velocity Rule",
            "Threshold Proximity Rule",
            "Duplicate / Near-Duplicate Rule",
            "Employee-Vendor Relationship",
            "Off-Hours Rule",
            "New Vendor Rule",
        ],
        "Definition": [
            "Flag customer with 3+ cash transactions totalling ≥ ₹10 Lakh in 30 days",
            "Flag accounts with > (mean + 3σ) transactions in 1-hour window",
            "Flag invoices in range [T - 0.5%, T] where T = approval threshold",
            "Flag same (vendor, amount) within 5 business days",
            "Flag transactions where employee address matches vendor address",
            "Flag transactions between 10pm–6am IST or weekend corporate transactions",
            "Flag large payments (> ₹5L) to vendors registered < 90 days ago",
        ],
    }
    st.dataframe(pd.DataFrame(rules), use_container_width=True, hide_index=True)

    # Isolation Forest
    st.markdown("### Layer 3: Isolation Forest")
    st.markdown("""
    <div class="mpa-card">
        <h3>How Isolation Forest Works</h3>
        <p style="font-family: 'Inter', sans-serif; color: #2d3142; line-height: 1.7;">
            An ensemble of random trees that isolates anomalies by requiring <strong>fewer random splits</strong>
            to separate them from the rest of the data. Normal points are deep in the tree; anomalies are
            isolated quickly (short path length).
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="mpa-formula">
        Key Parameters:<br>
        • n_estimators = 200<br>
        • contamination = 0.03 (expect ~3% anomalies)<br>
        • Features: log(amount), hour, day_of_week, txn_per_day, days_since_last, benford_deviation<br>
        • Output: anomaly_score where -1 = anomaly, +1 = normal
    </div>
    """, unsafe_allow_html=True)

    # Demo Isolation Forest
    st.markdown("### Interactive Demo: Isolation Forest on Transaction Data")

    try:
        from sklearn.ensemble import IsolationForest

        np.random.seed(42)
        n_normal = 970
        n_anomaly = 30
        normal_amounts = np.random.lognormal(mean=8, sigma=1.0, size=n_normal)
        normal_freq = np.random.poisson(5, size=n_normal)
        anomaly_amounts = np.random.uniform(40000, 50000, size=n_anomaly)
        anomaly_freq = np.random.poisson(15, size=n_anomaly)

        amounts = np.concatenate([normal_amounts, anomaly_amounts])
        freqs = np.concatenate([normal_freq, anomaly_freq])
        labels = np.array([0] * n_normal + [1] * n_anomaly)

        X = np.column_stack([np.log(amounts + 1), freqs])

        clf = IsolationForest(n_estimators=200, contamination=0.03, random_state=42)
        preds = clf.fit_predict(X)
        scores = clf.decision_function(X)

        fig = go.Figure()
        normal_mask = preds == 1
        anomaly_mask = preds == -1

        fig.add_trace(go.Scatter(
            x=amounts[normal_mask], y=freqs[normal_mask],
            mode="markers", name="Normal",
            marker=dict(color="#3a7bd5", size=5, opacity=0.5),
        ))
        fig.add_trace(go.Scatter(
            x=amounts[anomaly_mask], y=freqs[anomaly_mask],
            mode="markers", name="Anomaly",
            marker=dict(color="#e63946", size=10, symbol="x", line=dict(width=2)),
        ))
        fig.update_layout(
            title="Isolation Forest — Transaction Anomaly Detection",
            xaxis_title="Transaction Amount (₹)", yaxis_title="Transaction Frequency",
            plot_bgcolor="#fafbfd", paper_bgcolor="#ffffff",
            font=dict(family="Inter"), legend=dict(orientation="h", y=-0.15),
        )
        st.plotly_chart(fig, use_container_width=True)

        detected = sum(anomaly_mask & (labels == 1))
        st.markdown(f"""
        <div class="mpa-success">
            <strong>Results:</strong> Detected <strong>{sum(anomaly_mask)}</strong> anomalies
            out of {len(amounts)} transactions.
            True positives: <strong>{detected}</strong> of {n_anomaly} injected anomalies
            ({detected/n_anomaly*100:.0f}% recall).
        </div>
        """, unsafe_allow_html=True)

    except ImportError:
        st.warning("scikit-learn not installed. Install with `pip install scikit-learn` to see the interactive demo.")

    # Autoencoder explanation
    st.markdown("### Autoencoder — Learning 'Normal' to Find Abnormal")
    st.markdown("""
    <div class="mpa-card">
        <h3>How Autoencoders Detect Fraud</h3>
        <p style="font-family: 'Inter', sans-serif; color: #2d3142; line-height: 1.7;">
            A neural network trained <strong>ONLY on normal transactions</strong> learns to compress and
            reconstruct "normal" patterns. When a fraudulent transaction is fed in, the network
            <strong>cannot reconstruct it well</strong> — the reconstruction error spikes.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="mpa-formula">
        Anomaly Score = ‖xᵢ − x̂ᵢ‖² (Mean Squared Error)<br>
        Threshold: Flag observations with reconstruction error > Q₉₉ of training errors
    </div>
    """, unsafe_allow_html=True)

    # Ensemble scoring
    st.markdown("### Ensemble Anomaly Scoring")
    st.markdown("""
    <div class="mpa-formula">
        FraudRiskScoreᵢ = w₁·S(Benford) + w₂·S(IsolationForest) + w₃·S(Rules) + w₄·S(Network)
    </div>
    """, unsafe_allow_html=True)
    ensemble_weights = {
        "Component": ["Rule-Based Score", "Benford's Law Score", "Isolation Forest", "Network / Behavioural"],
        "Suggested Weight": ["0.25", "0.20", "0.30", "0.25"],
        "Rationale": [
            "High precision; known fraud patterns",
            "Effective for fabricated amounts",
            "Captures multivariate anomalies",
            "Catches collaborative fraud",
        ],
    }
    st.dataframe(pd.DataFrame(ensemble_weights), use_container_width=True, hide_index=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# QUIZ & ASSESSMENT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

elif page == "❓ Quiz & Assessment":
    st.markdown("""
    <div class="mpa-header">
        <h1>Quiz & Assessment</h1>
        <p>Test Your Understanding of Benford's Law & Fraud Analytics</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### Reinforce your learning through applied questions")

    score = 0
    total_q = 10

    with st.form("quiz_form"):
        st.markdown("---")
        st.markdown("**Q1.** What is the probability that a naturally occurring number starts with digit 3?")
        q1 = st.radio("", ["10.0%", "12.5%", "15.0%", "33.3%"], key="q1", index=None)

        st.markdown("**Q2.** A dataset of 1,000 invoices shows 180 starting with digit 1. Is this suspicious?")
        q2 = st.radio("", [
            "No — 18% is close to the expected 11.1%",
            "Yes — expected is 30.1%, so 18% is severely under-represented",
            "No — Benford's Law doesn't apply to invoices",
            "Cannot determine without more information",
        ], key="q2", index=None)

        st.markdown("**Q3.** Why is MAD (Mean Absolute Deviation) preferred over Chi-Squared in forensic accounting?")
        q3 = st.radio("", [
            "MAD is more mathematically complex",
            "MAD is not inflated by large sample sizes unlike Chi-Squared",
            "Chi-Squared cannot be computed for digit analysis",
            "MAD uses more degrees of freedom",
        ], key="q3", index=None)

        st.markdown("**Q4.** What does a Round Number Score of 2.35 indicate?")
        q4 = st.radio("", [
            "Normal distribution — no issues",
            "Marginal — monitor only",
            "Significant fabrication signal (score > 2.0)",
            "Insufficient data to determine",
        ], key="q4", index=None)

        st.markdown("**Q5.** Which datasets do NOT follow Benford's Law?")
        q5 = st.radio("", [
            "Stock prices, invoice amounts, tax returns",
            "Lottery numbers, telephone numbers, employee IDs",
            "Population data, river areas, death rates",
            "Insurance claims, utility bills, financial statements",
        ], key="q5", index=None)

        st.markdown("**Q6.** In the summation test, what is the expected proportion for each two-digit combination?")
        q6 = st.radio("", [
            "1/9 ≈ 11.1%",
            "1/90 ≈ 1.11%",
            "1/100 = 1.0%",
            "Varies by digit combination",
        ], key="q6", index=None)

        st.markdown("**Q7.** An auditor finds χ² = 18.2 with df = 8. At what level can Benford be rejected?")
        q7 = st.radio("", [
            "Cannot reject at any level",
            "Reject at 5% (18.2 > 15.51) but not at 1% (18.2 < 20.09)",
            "Reject at 1% level",
            "Reject at 0.1% level",
        ], key="q7", index=None)

        st.markdown("**Q8.** What is 'structuring' in the context of banking fraud?")
        q8 = st.radio("", [
            "Organizing data into structured databases",
            "Breaking large transactions into smaller amounts to avoid regulatory reporting",
            "Creating organizational hierarchy for bank employees",
            "Building a financial model with structured assumptions",
        ], key="q8", index=None)

        st.markdown("**Q9.** In Principal Component Regression (PCR), which Benford test is the most sensitive?")
        q9 = st.radio("", [
            "First-digit test",
            "Chi-squared test",
            "Two-digit test (first two significant digits)",
            "MAD test",
        ], key="q9", index=None)

        st.markdown("**Q10.** What was the ROI of Project Eagle Eye?")
        q10 = st.radio("", [
            "2.5x", "5.8x", "12.4x", "25.0x",
        ], key="q10", index=None)

        submitted = st.form_submit_button("📊 Submit Answers", type="primary")

    if submitted:
        answers = {
            "q1": "12.5%", "q2": "Yes — expected is 30.1%, so 18% is severely under-represented",
            "q3": "MAD is not inflated by large sample sizes unlike Chi-Squared",
            "q4": "Significant fabrication signal (score > 2.0)",
            "q5": "Lottery numbers, telephone numbers, employee IDs",
            "q6": "1/90 ≈ 1.11%",
            "q7": "Reject at 5% (18.2 > 15.51) but not at 1% (18.2 < 20.09)",
            "q8": "Breaking large transactions into smaller amounts to avoid regulatory reporting",
            "q9": "Two-digit test (first two significant digits)",
            "q10": "12.4x",
        }
        user_answers = {"q1": q1, "q2": q2, "q3": q3, "q4": q4, "q5": q5,
                        "q6": q6, "q7": q7, "q8": q8, "q9": q9, "q10": q10}

        score = sum(1 for k, v in answers.items() if user_answers.get(k) == v)

        if score >= 9:
            st.balloons()
            grade = "Excellent! 🏆"
            color = "#06d6a0"
        elif score >= 7:
            grade = "Good! 👍"
            color = "#3a7bd5"
        elif score >= 5:
            grade = "Fair — Review the Learn section 📘"
            color = "#f77f00"
        else:
            grade = "Needs Improvement — Study the materials carefully 📚"
            color = "#e63946"

        st.markdown(f"""
        <div style="background: {color}22; border-left: 5px solid {color}; padding: 1.5rem; border-radius: 0 12px 12px 0; margin: 1rem 0;">
            <h2 style="color: {color}; margin: 0;">Score: {score}/{total_q} — {grade}</h2>
        </div>
        """, unsafe_allow_html=True)

        # Show correct answers
        with st.expander("View Correct Answers"):
            for i, (k, v) in enumerate(answers.items(), 1):
                user_ans = user_answers.get(k, "Not answered")
                is_correct = user_ans == v
                icon = "✅" if is_correct else "❌"
                st.markdown(f"**Q{i}.** {icon} Correct: {v}")
                if not is_correct and user_ans:
                    st.markdown(f"   Your answer: {user_ans}")


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# GLOSSARY & ABBREVIATIONS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

elif page == "📖 Glossary & Abbreviations":
    st.markdown("""
    <div class="mpa-header">
        <h1>Glossary & Abbreviations</h1>
        <p>Complete Reference — 22 Abbreviations, Key Terms & Formulas</p>
    </div>
    """, unsafe_allow_html=True)

    # Quick Reference Cheat Sheet
    st.markdown("## Quick Reference — Essential Formulas")
    formulas = {
        "Test / Formula": [
            "First-Digit Probability",
            "Second-Digit Probability",
            "Two-Digit Probability",
            "Chi-Squared Test",
            "MAD (Mean Absolute Deviation)",
            "KS Test (Kolmogorov-Smirnov)",
            "Z-Score per Digit",
            "Summation Test",
            "Round Number Score",
        ],
        "Mathematical Expression": [
            "P(d) = log₁₀(1 + 1/d),  d ∈ {1,...,9}",
            "P(d₂) = Σ(k=1→9) log₁₀(1 + 1/(10k+d₂))",
            "P(D₁D₂) = log₁₀(1 + 1/d),  d ∈ {10,...,99}",
            "χ² = Σ [(Oᵈ - Eᵈ)² / Eᵈ],  df = 8",
            "MAD = (1/9) × Σ |P(obs)ᵈ - P(Benford)ᵈ|",
            "D = max |F(obs)(d) - F(Benford)(d)|",
            "Zᵈ = (|Pobs - PBen| - 1/2n) / √(PBen(1-PBen)/n)",
            "Sᵈ = Σ(txns starting d) / Σ(all txns), expect ≈1/90",
            "P(last digit ∈ {0,5})obs / P(expected) ≈ 20%",
        ],
        "When to Use": [
            "Primary screening test for any financial dataset",
            "When first-digit test passes but fraud suspected",
            "Most sensitive test — catches sophisticated manipulators",
            "Overall conformity test (caution with n > 5,000)",
            "Preferred forensic test — sample-size independent",
            "Small samples (n < 100); less sensitive to outliers",
            "Identify WHICH specific digit is anomalous",
            "Detect round-number manipulation & threshold gaming",
            "Detect fabricated amounts — flag if score > 2.0",
        ],
    }
    st.dataframe(pd.DataFrame(formulas), use_container_width=True, hide_index=True)

    # Decision Thresholds
    st.markdown("## Decision Thresholds — Quick Lookup")
    thresholds = {
        "Test": ["Chi-Squared (df=8)", "MAD", "Z-Score", "Round Number Score", "Summation Proportion"],
        "Threshold": [
            "> 15.51 (5%) / > 20.09 (1%) / > 26.12 (0.1%)",
            "0–0.006 ✅ / 0.006–0.012 👀 / 0.012–0.015 ⚠️ / > 0.015 🚨",
            "> 1.96 (5%) / > 2.576 (1%)",
            "> 2.0 (i.e., > 40% last digits are 0 or 5)",
            "Any Sᵈ >> 1/90 (≈1.11%)",
        ],
        "Interpretation": [
            "Reject Benford's Law at given confidence level",
            "Close / Acceptable / Marginal / Non-conforming",
            "Individual digit is significantly anomalous",
            "Significant fabrication signal",
            "Concentration — possible threshold manipulation",
        ],
    }
    st.dataframe(pd.DataFrame(thresholds), use_container_width=True, hide_index=True)

    # Full Abbreviations
    st.markdown("## Abbreviations — All 22 Terms Expanded")
    abbreviations = {
        "Abbreviation": [
            "ACFE", "AML", "BAU", "CBS", "CBI", "CUSUM", "DBSCAN", "DSA",
            "FIR", "GST", "GSTN", "IQR", "ITC", "KS Test", "LOF", "MAD",
            "NEFT", "PMLA", "RBI", "RTGS", "STR", "UPI",
        ],
        "Full Form / Definition": [
            "Association of Certified Fraud Examiners — global anti-fraud professional body",
            "Anti-Money Laundering — regulations to prevent conversion of illicit funds",
            "Business As Usual — ongoing operations after project implementation",
            "Core Banking Solution — centralized banking software system",
            "Central Bureau of Investigation — India's premier investigating agency",
            "Cumulative Sum — control chart method for detecting drift in time series",
            "Density-Based Spatial Clustering of Applications with Noise — unsupervised ML clustering algorithm",
            "Direct Selling Agent — third-party loan originator in Indian banking",
            "First Information Report — initial police complaint registered under CrPC (Code of Criminal Procedure)",
            "Goods and Services Tax — India's unified indirect tax system (from July 2017)",
            "GST Network — Information Technology backbone managing GST filings and matching",
            "Interquartile Range — robust measure of statistical dispersion (Q3 - Q1)",
            "Input Tax Credit — GST credit claimed on purchases (frequent fraud target)",
            "Kolmogorov-Smirnov Test — non-parametric test comparing distributions",
            "Local Outlier Factor — density-based anomaly detection algorithm",
            "Mean Absolute Deviation — preferred conformity measure in forensic accounting",
            "National Electronic Funds Transfer — Indian electronic payment system",
            "Prevention of Money Laundering Act, 2002 — India's primary AML legislation",
            "Reserve Bank of India — central bank and banking regulator",
            "Real-Time Gross Settlement — high-value instant payment system in India",
            "Suspicious Transaction Report — mandatory filing to FIU (Financial Intelligence Unit) under PMLA",
            "Unified Payments Interface — India's real-time mobile payment system",
        ],
    }
    st.dataframe(pd.DataFrame(abbreviations), use_container_width=True, hide_index=True)

    # Glossary
    st.markdown("## Key Terms Glossary")
    glossary = {
        "Term": [
            "Multicollinearity", "Principal Component (PC)", "Loading", "Score",
            "Eigenvalue (λ)", "Eigenvector (v)", "Explained Variance",
            "Scree Plot", "Standardisation", "VIF (Variance Inflation Factor)",
            "PCR (Principal Component Regression)", "PLS (Partial Least Squares)",
            "SVD (Singular Value Decomposition)", "Structuring / Smurfing",
            "Isolation Forest", "Autoencoder",
        ],
        "Definition": [
            "High correlation among predictor variables in regression, causing unstable coefficients",
            "Linear combination of original variables; new uncorrelated axis capturing maximum variance",
            "Weight of an original variable in a PC (entry of the eigenvector)",
            "Value of a PC for a specific observation (projection onto eigenvector)",
            "Variance captured by its corresponding eigenvector / PC",
            "Direction in feature space along which variance is computed; defines a PC",
            "λᵢ / Σλ — fraction of total variance captured by PCᵢ",
            "Bar/line plot of eigenvalues used to choose k (look for the elbow)",
            "Transform each variable to mean 0, standard deviation 1 before PCA",
            "Measures how much multicollinearity inflates a coefficient's variance: VIFᵢ = 1/(1-Rᵢ²)",
            "Multiple Linear Regression using PC scores as predictors instead of original variables",
            "Like PCR but components also account for correlation with Y (response variable)",
            "Singular Value Decomposition — stable numerical method to compute PCA",
            "Breaking large transactions into smaller amounts to avoid regulatory reporting thresholds",
            "Ensemble ML method that isolates anomalies using random splits — anomalies have short path lengths",
            "Neural network trained on normal data; high reconstruction error flags anomalies",
        ],
    }
    st.dataframe(pd.DataFrame(glossary), use_container_width=True, hide_index=True)

    # References
    st.markdown("## References & Further Reading")
    refs = {
        "#": [f"R{i}" for i in range(1, 11)],
        "Reference": [
            "Nigrini, M.J. (2012). Benford's Law: Applications for Forensic Accounting, Auditing, and Fraud Detection. Wiley.",
            "Nigrini, M.J. (2019). Forensic Analytics: Methods and Techniques for Forensic Accounting. 2nd Ed.",
            "Benford, F. (1938). The Law of Anomalous Numbers. Proc. of the American Philosophical Society.",
            "Hill, T.P. (1995). A Statistical Derivation of the Significant-Digit Law. Statistical Science.",
            "ACFE (2024). Report to the Nations: 2024 Global Study on Occupational Fraud and Abuse.",
            "RBI (2023). Annual Report on Trend and Progress of Banking in India 2022-23.",
            "Durtschi, C., Hillison, W., & Pacini, C. (2004). The Effective Use of Benford's Law.",
            "Liu, F.H.M. & Vasarhelyi, M.A. (2009). Application of Benford's Law in Fraud Detection.",
            "Amiram, D., Bozanic, Z., & Rouen, E. (2015). Financial Statement Errors: Evidence from Benford's Law.",
            "ICAI (2019). Standard on Auditing 240: The Auditor's Responsibilities Relating to Fraud.",
        ],
    }
    st.dataframe(pd.DataFrame(refs), use_container_width=True, hide_index=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# FOOTER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

st.markdown("""
<div class="mpa-footer">
    <strong>The Mountain Path Academy</strong> — Fraud Analytics Platform<br>
    © 2024 Prof. V. Ravichandran | For educational use only<br>
    <em>"Numbers do not lie — unless someone forces them to. Benford's Law gives us the tools to find out."</em>
</div>
""", unsafe_allow_html=True)
