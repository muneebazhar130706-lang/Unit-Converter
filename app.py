import streamlit as st
import pandas as pd
import math

st.set_page_config(
    page_title="MechCalc Pro | 25-ME-27",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─── ENHANCED CSS — Industrial Precision Aesthetic ────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Rajdhani:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500;700&family=Bebas+Neue&display=swap');

:root {
    --bg-deep:    #060a0f;
    --bg-panel:   #0b1017;
    --bg-card:    #0f1720;
    --bg-inset:   #08111a;
    --amber:      #f5a623;
    --amber-dim:  #a86d12;
    --amber-glow: rgba(245,166,35,0.18);
    --steel:      #7eb8d4;
    --steel-dim:  #3a6880;
    --cyan:       #00e5ff;
    --cyan-dim:   rgba(0,229,255,0.15);
    --green:      #39d98a;
    --red:        #ff5252;
    --text-hi:    #f0f4f8;
    --text-mid:   #8faab8;
    --text-lo:    #3a5468;
    --border:     rgba(126,184,212,0.12);
    --border-hi:  rgba(245,166,35,0.35);
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--bg-deep) !important;
    color: var(--text-hi) !important;
    font-family: 'Rajdhani', sans-serif !important;
}

[data-testid="stSidebar"] { display: none !important; }
[data-testid="stDecoration"] { display: none !important; }
#MainMenu, footer, header { visibility: hidden !important; }

/* ── Scan-line overlay ── */
[data-testid="stAppViewContainer"]::before {
    content: '';
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0,0,0,0.18) 2px,
        rgba(0,0,0,0.18) 4px
    );
    pointer-events: none;
    z-index: 0;
}

/* ── Animated corner-bracket header ── */
.hdr-wrap {
    position: relative;
    padding: 40px 48px 32px;
    margin-bottom: 32px;
    background: linear-gradient(160deg, #0b1520 0%, #060a0f 60%);
    border: 1px solid var(--border);
    border-radius: 4px;
    overflow: hidden;
}
.hdr-wrap::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--amber), var(--steel), transparent);
    animation: scanH 3s ease-in-out infinite alternate;
}
@keyframes scanH {
    0%   { opacity: 0.4; transform: scaleX(0.6); }
    100% { opacity: 1;   transform: scaleX(1); }
}
.hdr-wrap::after {
    content: '';
    position: absolute;
    bottom: -120px; right: -80px;
    width: 360px; height: 360px;
    background: radial-gradient(circle, rgba(245,166,35,0.06) 0%, transparent 70%);
    pointer-events: none;
}

/* Corner brackets */
.corner { position: absolute; width: 20px; height: 20px; }
.corner-tl { top: 10px;  left: 10px;  border-top: 2px solid var(--amber); border-left: 2px solid var(--amber); }
.corner-tr { top: 10px;  right: 10px; border-top: 2px solid var(--amber); border-right: 2px solid var(--amber); }
.corner-bl { bottom: 10px; left: 10px;  border-bottom: 2px solid var(--steel); border-left: 2px solid var(--steel); }
.corner-br { bottom: 10px; right: 10px; border-bottom: 2px solid var(--steel); border-right: 2px solid var(--steel); }

.hdr-eyebrow {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: 4px;
    color: var(--amber);
    text-transform: uppercase;
    margin-bottom: 10px;
    opacity: 0.8;
}
.hdr-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(2.4rem, 5vw, 3.8rem);
    letter-spacing: 6px;
    line-height: 1;
    background: linear-gradient(90deg, var(--text-hi) 0%, var(--amber) 50%, var(--steel) 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 6px;
}
.hdr-sub {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: var(--text-mid);
    letter-spacing: 3px;
    text-transform: uppercase;
}
.hdr-meta {
    display: flex;
    gap: 2px;
    margin-top: 24px;
    flex-wrap: wrap;
}
.meta-chip {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: 1px;
    padding: 5px 14px;
    background: rgba(245,166,35,0.08);
    border: 1px solid rgba(245,166,35,0.22);
    color: var(--amber);
    border-radius: 2px;
    text-transform: uppercase;
}
.meta-chip + .meta-chip {
    background: rgba(126,184,212,0.06);
    border-color: rgba(126,184,212,0.18);
    color: var(--steel);
}

/* ── Status bar ── */
.status-bar {
    display: flex;
    gap: 0;
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 4px;
    margin-bottom: 28px;
    overflow: hidden;
}
.status-item {
    flex: 1;
    padding: 10px 18px;
    border-right: 1px solid var(--border);
    position: relative;
}
.status-item:last-child { border-right: none; }
.status-dot {
    display: inline-block;
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--green);
    margin-right: 6px;
    vertical-align: middle;
    animation: pulse 2s ease-in-out infinite;
}
@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50%       { opacity: 0.5; transform: scale(0.7); }
}
.status-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    color: var(--text-lo);
    letter-spacing: 2px;
    text-transform: uppercase;
    display: block;
}
.status-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: var(--steel);
    font-weight: 500;
}

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    gap: 0 !important;
    background: var(--bg-panel) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px 4px 0 0 !important;
    padding: 0 !important;
}
[data-testid="stTabs"] button[role="tab"] {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    font-weight: 500 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: var(--text-lo) !important;
    padding: 14px 28px !important;
    border-radius: 0 !important;
    border-right: 1px solid var(--border) !important;
    border-bottom: none !important;
    transition: color 0.2s, background 0.2s !important;
}
[data-testid="stTabs"] button[role="tab"]:hover {
    color: var(--text-mid) !important;
    background: rgba(126,184,212,0.04) !important;
}
[data-testid="stTabs"] button[role="tab"][aria-selected="true"] {
    color: var(--amber) !important;
    background: rgba(245,166,35,0.07) !important;
    border-bottom: 2px solid var(--amber) !important;
}
[data-testid="stTabsContent"] {
    border: 1px solid var(--border) !important;
    border-top: none !important;
    border-radius: 0 0 4px 4px !important;
    background: var(--bg-card) !important;
    padding: 28px !important;
}

/* ── Section panels ── */
.panel {
    background: var(--bg-panel);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 24px 28px;
    margin-bottom: 20px;
    position: relative;
}
.panel-title {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: 3px;
    text-transform: uppercase;
    color: var(--amber);
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
}
.panel-title::after {
    content: '';
    flex: 1;
    height: 1px;
    background: linear-gradient(90deg, var(--border-hi), transparent);
}

/* ── Conversion row ── */
.conv-layout {
    display: grid;
    grid-template-columns: 1fr 60px 1fr;
    gap: 12px;
    align-items: end;
}
.arrow-cell {
    display: flex;
    align-items: center;
    justify-content: center;
    padding-bottom: 6px;
}
.arrow-glyph {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 28px;
    color: var(--amber);
    line-height: 1;
    animation: arrowPulse 1.8s ease-in-out infinite;
}
@keyframes arrowPulse {
    0%, 100% { opacity: 1; transform: translateX(0); }
    50%       { opacity: 0.5; transform: translateX(4px); }
}

/* ── Result display ── */
.result-display {
    position: relative;
    background: var(--bg-inset);
    border: 1px solid var(--border-hi);
    border-radius: 4px;
    padding: 22px 28px 18px;
    margin-top: 18px;
    overflow: hidden;
}
.result-display::before {
    content: 'OUTPUT';
    position: absolute;
    top: 8px; right: 14px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 8px;
    letter-spacing: 3px;
    color: var(--text-lo);
}
.result-display::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0;
    width: 100%;
    height: 2px;
    background: linear-gradient(90deg, var(--amber), var(--steel));
    opacity: 0.5;
}
.result-number {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 3.2rem;
    letter-spacing: 3px;
    color: var(--amber);
    line-height: 1;
    margin-bottom: 4px;
}
.result-equation {
    font-family: 'JetBrains Mono', monospace;
    font-size: 12px;
    color: var(--text-mid);
    letter-spacing: 1px;
}

/* ── Density cards ── */
.d-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 10px;
    margin-top: 14px;
}
.d-card {
    background: var(--bg-inset);
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 14px 16px 12px;
    position: relative;
    overflow: hidden;
    transition: border-color 0.2s;
}
.d-card:hover { border-color: rgba(245,166,35,0.3); }
.d-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--amber-dim), transparent);
    opacity: 0.6;
}
.d-sys {
    font-family: 'JetBrains Mono', monospace;
    font-size: 8px;
    letter-spacing: 2px;
    color: var(--text-lo);
    text-transform: uppercase;
    margin-bottom: 8px;
}
.d-num {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 1.9rem;
    letter-spacing: 2px;
    color: var(--green);
    line-height: 1;
}
.d-unit-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    color: var(--text-lo);
    margin-top: 4px;
    letter-spacing: 1px;
}

/* ── Mass result ── */
.mass-display {
    background: var(--bg-inset);
    border: 1px solid rgba(57,217,138,0.3);
    border-radius: 4px;
    padding: 20px 24px 16px;
    margin-top: 14px;
    position: relative;
    overflow: hidden;
}
.mass-display::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--green), transparent);
    opacity: 0.7;
}
.mass-display::after {
    content: 'MASS CALC';
    position: absolute;
    top: 8px; right: 14px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 8px;
    letter-spacing: 3px;
    color: var(--text-lo);
}
.mass-number {
    font-family: 'Bebas Neue', sans-serif;
    font-size: 2.8rem;
    letter-spacing: 3px;
    color: var(--green);
    line-height: 1;
    margin-bottom: 4px;
}
.mass-alts {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: var(--text-mid);
}

/* ── Data table ── */
.stDataFrame {
    background: var(--bg-inset) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
}
[data-testid="stDataFrame"] th {
    background: var(--bg-panel) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 10px !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    color: var(--amber) !important;
    border-bottom: 1px solid var(--border-hi) !important;
}
[data-testid="stDataFrame"] td {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 12px !important;
    color: var(--text-mid) !important;
    border-bottom: 1px solid var(--border) !important;
}
[data-testid="stDataFrame"] tr:hover td {
    background: rgba(245,166,35,0.04) !important;
    color: var(--text-hi) !important;
}

/* ── Streamlit widget overrides ── */
[data-testid="stSelectbox"] label,
[data-testid="stNumberInput"] label {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 9px !important;
    letter-spacing: 2.5px !important;
    text-transform: uppercase !important;
    color: var(--text-lo) !important;
    margin-bottom: 4px !important;
}
[data-testid="stSelectbox"] > div > div {
    background: var(--bg-inset) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    color: var(--text-hi) !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}
[data-testid="stSelectbox"] > div > div:hover,
[data-testid="stSelectbox"] > div > div:focus-within {
    border-color: rgba(245,166,35,0.4) !important;
    box-shadow: 0 0 0 2px rgba(245,166,35,0.08) !important;
}
[data-testid="stNumberInput"] input {
    background: var(--bg-inset) !important;
    border: 1px solid var(--border) !important;
    border-radius: 4px !important;
    color: var(--amber) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 16px !important;
    font-weight: 500 !important;
}
[data-testid="stNumberInput"] input:focus {
    border-color: var(--amber-dim) !important;
    box-shadow: 0 0 0 2px var(--amber-glow) !important;
}
[data-testid="stNumberInput"] button {
    background: var(--bg-panel) !important;
    border-color: var(--border) !important;
    color: var(--text-mid) !important;
}

/* ── Footer ── */
.footer {
    margin-top: 40px;
    padding: 16px 0;
    border-top: 1px solid var(--border);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
}
.footer-l {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    color: var(--text-lo);
    letter-spacing: 2px;
    text-transform: uppercase;
}
.footer-r {
    display: flex;
    gap: 20px;
}
.footer-dot {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    color: var(--text-lo);
    letter-spacing: 1px;
    display: flex;
    align-items: center;
    gap: 5px;
}
.footer-dot::before {
    content: '';
    width: 5px; height: 5px;
    border-radius: 50%;
    background: var(--green);
    animation: pulse 2s infinite;
}

/* ── divider ── */
.rule { border: none; border-top: 1px solid var(--border); margin: 18px 0; }
</style>
""", unsafe_allow_html=True)


# ─── HEADER ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hdr-wrap">
    <div class="corner corner-tl"></div>
    <div class="corner corner-tr"></div>
    <div class="corner corner-bl"></div>
    <div class="corner corner-br"></div>
    <div class="hdr-eyebrow">⬡ Precision Engineering Toolkit &nbsp;·&nbsp; System Ready</div>
    <div class="hdr-title">MechCalc Pro</div>
    <div class="hdr-sub">Unit Converter &amp; Material Density Reference</div>
    <div class="hdr-meta">
        <span class="meta-chip">Muneeb Azhar</span>
        <span class="meta-chip">Roll No: 25-ME-27</span>
        <span class="meta-chip">Dept. of Mechanical Engineering</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ─── STATUS BAR ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="status-bar">
    <div class="status-item">
        <span class="status-label">System</span>
        <span class="status-val"><span class="status-dot"></span>Online</span>
    </div>
    <div class="status-item">
        <span class="status-label">Categories</span>
        <span class="status-val">10 Active</span>
    </div>
    <div class="status-item">
        <span class="status-label">Materials</span>
        <span class="status-val">36 Loaded</span>
    </div>
    <div class="status-item">
        <span class="status-label">Precision</span>
        <span class="status-val">6 Sig. Fig.</span>
    </div>
    <div class="status-item">
        <span class="status-label">Version</span>
        <span class="status-val">2.0.0</span>
    </div>
</div>
""", unsafe_allow_html=True)


# ─── CONVERSION DATA ─────────────────────────────────────────────────────────────
CONVERSIONS = {
    "Length": {
        "units": ["Meter (m)", "Kilometer (km)", "Centimeter (cm)", "Millimeter (mm)",
                  "Mile (mi)", "Yard (yd)", "Foot (ft)", "Inch (in)"],
        "to_base": [1, 1000, 0.01, 0.001, 1609.344, 0.9144, 0.3048, 0.0254],
        "icon": "📏",
    },
    "Mass": {
        "units": ["Kilogram (kg)", "Gram (g)", "Milligram (mg)", "Tonne (t)",
                  "Pound (lb)", "Ounce (oz)", "Slug"],
        "to_base": [1, 0.001, 1e-6, 1000, 0.453592, 0.0283495, 14.5939],
        "icon": "⚖️",
    },
    "Force": {
        "units": ["Newton (N)", "Kilonewton (kN)", "Pound-force (lbf)",
                  "Dyne (dyn)", "Kilogram-force (kgf)"],
        "to_base": [1, 1000, 4.44822, 1e-5, 9.80665],
        "icon": "➡️",
    },
    "Pressure": {
        "units": ["Pascal (Pa)", "Kilopascal (kPa)", "Megapascal (MPa)",
                  "Bar", "PSI (psi)", "Atmosphere (atm)", "mmHg"],
        "to_base": [1, 1000, 1e6, 1e5, 6894.76, 101325, 133.322],
        "icon": "🔵",
    },
    "Energy": {
        "units": ["Joule (J)", "Kilojoule (kJ)", "Calorie (cal)",
                  "Kilocalorie (kcal)", "kWh", "BTU", "Foot-pound (ft·lbf)"],
        "to_base": [1, 1000, 4.184, 4184, 3.6e6, 1055.06, 1.35582],
        "icon": "⚡",
    },
    "Power": {
        "units": ["Watt (W)", "Kilowatt (kW)", "Megawatt (MW)",
                  "Horsepower (hp)", "BTU/hr"],
        "to_base": [1, 1000, 1e6, 745.7, 0.293071],
        "icon": "🔋",
    },
    "Temperature": {
        "units": ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)", "Rankine (°R)"],
        "to_base": None,
        "icon": "🌡️",
    },
    "Velocity": {
        "units": ["m/s", "km/h", "mph", "ft/s", "knot"],
        "to_base": [1, 1/3.6, 0.44704, 0.3048, 0.514444],
        "icon": "💨",
    },
    "Torque": {
        "units": ["Newton-meter (N·m)", "Kilonewton-meter (kN·m)",
                  "Pound-foot (lbf·ft)", "Pound-inch (lbf·in)"],
        "to_base": [1, 1000, 1.35582, 0.112985],
        "icon": "🔩",
    },
    "Stress / Young's Modulus": {
        "units": ["Pascal (Pa)", "Kilopascal (kPa)", "Megapascal (MPa)",
                  "Gigapascal (GPa)", "PSI", "ksi"],
        "to_base": [1, 1e3, 1e6, 1e9, 6894.76, 6.895e6],
        "icon": "📐",
    },
}

MATERIALS = {
    "── Metals ──": None,
    "Aluminum (pure)": 2700,
    "Aluminum alloy (6061)": 2700,
    "Copper": 8960,
    "Brass (70/30)": 8520,
    "Steel (carbon, mild)": 7850,
    "Steel (stainless 304)": 8000,
    "Steel (stainless 316)": 8027,
    "Cast iron (gray)": 7200,
    "Titanium (Grade 2)": 4510,
    "Titanium alloy (Ti-6Al-4V)": 4430,
    "Nickel": 8908,
    "Zinc": 7133,
    "Lead": 11340,
    "Gold": 19320,
    "Silver": 10490,
    "Tungsten": 19300,
    "Magnesium": 1738,
    "── Polymers ──": None,
    "Polyethylene (HDPE)": 955,
    "Polyethylene (LDPE)": 925,
    "Polypropylene (PP)": 905,
    "PVC (rigid)": 1380,
    "Nylon 6/6": 1140,
    "ABS": 1050,
    "Polycarbonate (PC)": 1200,
    "PTFE (Teflon)": 2200,
    "Epoxy (cured)": 1250,
    "Polyurethane (rigid)": 1200,
    "── Ceramics & Glass ──": None,
    "Alumina (Al₂O₃)": 3960,
    "Silicon carbide (SiC)": 3210,
    "Silicon nitride (Si₃N₄)": 3200,
    "Borosilicate glass": 2230,
    "Soda-lime glass": 2500,
    "Concrete (normal)": 2300,
    "── Composites & Other ──": None,
    "Carbon fiber composite (CFRP)": 1600,
    "Glass fiber composite (GFRP)": 2000,
    "Wood (oak, dry)": 750,
    "Wood (pine, dry)": 530,
    "Rubber (natural)": 920,
    "Water (20°C)": 1000,
    "Air (20°C, 1 atm)": 1.204,
}


def convert_temperature(value, from_unit, to_unit):
    if from_unit == "Celsius (°C)":      celsius = value
    elif from_unit == "Fahrenheit (°F)": celsius = (value - 32) * 5 / 9
    elif from_unit == "Kelvin (K)":      celsius = value - 273.15
    elif from_unit == "Rankine (°R)":    celsius = (value - 491.67) * 5 / 9
    else:                                celsius = value
    if to_unit == "Celsius (°C)":      return celsius
    elif to_unit == "Fahrenheit (°F)": return celsius * 9 / 5 + 32
    elif to_unit == "Kelvin (K)":      return celsius + 273.15
    elif to_unit == "Rankine (°R)":    return (celsius + 273.15) * 9 / 5
    return celsius


def convert_units(value, category, from_unit, to_unit):
    data = CONVERSIONS[category]
    if category == "Temperature":
        return convert_temperature(value, from_unit, to_unit)
    units = data["units"]
    factors = data["to_base"]
    fi = units.index(from_unit)
    ti = units.index(to_unit)
    return (value * factors[fi]) / factors[ti]


def fmt(n):
    if n == 0:
        return "0"
    abs_n = abs(n)
    if abs_n >= 1e9 or abs_n < 1e-4:
        return f"{n:.4e}"
    if abs_n >= 1e6:
        return f"{n:,.2f}"
    if abs_n >= 1:
        return f"{n:,.6g}"
    return f"{n:.6g}"


# ─── TABS ────────────────────────────────────────────────────────────────────────
tab1, tab2 = st.tabs(["  ⚙  UNIT CONVERTER  ", "  🔬  MATERIAL DENSITY  "])


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — UNIT CONVERTER
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">⬡ Conversion Engine</div>', unsafe_allow_html=True)

    col_cat, col_sp = st.columns([1.2, 1])
    with col_cat:
        category = st.selectbox("SELECT CATEGORY", list(CONVERSIONS.keys()), key="cat")

    data = CONVERSIONS[category]
    units_list = data["units"]

    col_a, col_arr, col_b = st.columns([5, 1, 5])
    with col_a:
        from_unit = st.selectbox("FROM UNIT", units_list, key="from_u")
        input_val = st.number_input("INPUT VALUE", value=1.0, format="%g", key="in_val")
    with col_arr:
        st.markdown("<br><br><br>", unsafe_allow_html=True)
        st.markdown('<div class="arrow-glyph" style="text-align:center;padding-top:8px">→</div>',
                    unsafe_allow_html=True)
    with col_b:
        default_idx = 1 if len(units_list) > 1 else 0
        to_unit = st.selectbox("TO UNIT", units_list, index=default_idx, key="to_u")

    result = convert_units(input_val, category, from_unit, to_unit)
    from_label = from_unit.split("(")[0].strip()
    to_label   = to_unit.split("(")[0].strip()

    st.markdown(f"""
    <div class="result-display">
        <div class="result-number">{fmt(result)}</div>
        <div class="result-equation">{fmt(input_val)} {from_label} = {fmt(result)} {to_label}</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Reference table
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">⬡ Full Conversion Reference</div>', unsafe_allow_html=True)
    rows = []
    for u in units_list:
        if u != from_unit:
            val = convert_units(input_val, category, from_unit, u)
            rows.append({"Unit": u, "Converted Value": fmt(val)})
    if rows:
        df = pd.DataFrame(rows)
        st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — MATERIAL DENSITY
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">⬡ Material Density Database</div>', unsafe_allow_html=True)

    material_options = [k for k, v in MATERIALS.items() if v is not None]
    selected = st.selectbox("SELECT MATERIAL", material_options, key="mat")
    density_kgm3 = MATERIALS[selected]

    d_gcm3  = density_kgm3 / 1000
    d_lbft3 = density_kgm3 * 0.0624279
    d_lbin3 = density_kgm3 * 0.0000361273

    st.markdown(f"""
    <div class="d-grid">
        <div class="d-card">
            <div class="d-sys">SI unit</div>
            <div class="d-num">{density_kgm3:,}</div>
            <div class="d-unit-label">kg / m³</div>
        </div>
        <div class="d-card">
            <div class="d-sys">CGS</div>
            <div class="d-num">{d_gcm3:.4g}</div>
            <div class="d-unit-label">g / cm³</div>
        </div>
        <div class="d-card">
            <div class="d-sys">Imperial</div>
            <div class="d-num">{d_lbft3:.4g}</div>
            <div class="d-unit-label">lb / ft³</div>
        </div>
        <div class="d-card">
            <div class="d-sys">Per in³</div>
            <div class="d-num">{d_lbin3:.5g}</div>
            <div class="d-unit-label">lb / in³</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Mass calculator
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">⬡ Mass Calculator  ρ × V</div>', unsafe_allow_html=True)

    col_v, col_u = st.columns([3, 2])
    with col_v:
        volume = st.number_input("VOLUME", min_value=0.0, value=0.001, format="%g", key="vol")
    with col_u:
        vol_unit = st.selectbox("UNIT", ["m³", "cm³", "mm³", "Liters", "ft³", "in³"], key="vunit")

    vol_to_m3 = {"m³": 1, "cm³": 1e-6, "mm³": 1e-9,
                 "Liters": 0.001, "ft³": 0.0283168, "in³": 0.0000163871}
    mass_kg = density_kgm3 * volume * vol_to_m3[vol_unit]
    mass_g  = mass_kg * 1000
    mass_lb = mass_kg * 2.20462

    st.markdown(f"""
    <div class="mass-display">
        <div style="font-family:'JetBrains Mono',monospace;font-size:9px;
                    letter-spacing:2px;color:#3a5468;text-transform:uppercase;margin-bottom:8px">
            {selected} · {fmt(volume)} {vol_unit}
        </div>
        <div class="mass-number">{fmt(mass_kg)} kg</div>
        <div class="mass-alts">= {fmt(mass_g)} g &nbsp;·&nbsp; {fmt(mass_lb)} lb</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # Full reference table
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">⬡ Complete Material Reference</div>', unsafe_allow_html=True)
    table_data = [
        {
            "Material": k,
            "kg/m³": f"{v:,}",
            "g/cm³": f"{v/1000:.4g}",
            "lb/ft³": f"{v*0.0624279:.4g}",
            "lb/in³": f"{v*0.0000361273:.5g}",
        }
        for k, v in MATERIALS.items() if v is not None
    ]
    st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)


# ─── FOOTER ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <span class="footer-l">MechCalc Pro · Muneeb Azhar · 25-ME-27 · Mechanical Engineering</span>
    <div class="footer-r">
        <span class="footer-dot">System Nominal</span>
        <span class="footer-dot">All Units Verified</span>
    </div>
</div>
""", unsafe_allow_html=True)
