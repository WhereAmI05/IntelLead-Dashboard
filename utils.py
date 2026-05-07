"""
FinancePilot 360 - Utilities
Shared helper functions for data loading, KPI cards, formatting, alerts.
"""

import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import os
import subprocess
import sys

from config import CSV_FILES, DATA_PROCESSED, RISK_COLORS, RISK_EMOJI, COLORS, PLOTLY_TEMPLATE


# ─────────────────────────────────────────────
# DATA LOADING
# ─────────────────────────────────────────────
@st.cache_data(ttl=300)
def load_csv(key: str) -> pd.DataFrame:
    """Load a processed CSV by key. Auto-triggers data_preparation if missing."""
    path = CSV_FILES.get(key)
    if not path or not os.path.exists(path):
        _run_data_preparation()
        if not os.path.exists(path):
            st.error(f"Fichier introuvable : {path}")
            return pd.DataFrame()
    return pd.read_csv(path, encoding="utf-8-sig")


def _run_data_preparation():
    """Run data_preparation.py if processed files don't exist."""
    prep_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data_preparation.py")
    if os.path.exists(prep_script):
        with st.spinner("⚙️ Préparation des données en cours..."):
            result = subprocess.run([sys.executable, prep_script], capture_output=True, text=True)
            if result.returncode != 0:
                st.error(f"Erreur data_preparation:\n{result.stderr}")
            else:
                st.success("✅ Données préparées avec succès !")
                st.cache_data.clear()


def check_data_ready() -> bool:
    """Returns True if all processed CSV files exist."""
    return all(os.path.exists(p) for p in CSV_FILES.values())


# ─────────────────────────────────────────────
# FORMATTING
# ─────────────────────────────────────────────
def fmt_mad(value: float, decimals: int = 0) -> str:
    """Format a number as MAD currency."""
    if pd.isna(value):
        return "—"
    if abs(value) >= 1_000_000:
        return f"{value/1_000_000:.2f}M MAD"
    if abs(value) >= 1_000:
        return f"{value:,.{decimals}f} MAD".replace(",", " ")
    return f"{value:.{decimals}f} MAD"


def fmt_pct(value: float) -> str:
    """Format as percentage."""
    if pd.isna(value):
        return "—"
    return f"{value:.1f}%"


def fmt_number(value: float) -> str:
    """Format a plain number with thousand separator."""
    if pd.isna(value):
        return "—"
    return f"{value:,.0f}".replace(",", " ")


# ─────────────────────────────────────────────
# KPI CARDS
# ─────────────────────────────────────────────
def kpi_card(label: str, value: str, delta: str = "", color: str = "#2E86AB", icon: str = "📊", fiabilite: str = ""):
    """Render a styled KPI card using Streamlit markdown."""
    delta_html = f'<p style="font-size:0.75rem;color:#aaa;margin:2px 0">{delta}</p>' if delta else ""
    fiab_html = f'<p style="font-size:0.65rem;color:#888;margin:2px 0">🔍 {fiabilite}</p>' if fiabilite else ""
    st.markdown(
        f"""
        <div style="
            background: {COLORS['card_bg']};
            border-left: 4px solid {color};
            border-radius: 8px;
            padding: 14px 18px;
            margin-bottom: 8px;
        ">
            <p style="font-size:0.8rem;color:#aaa;margin:0">{icon} {label}</p>
            <p style="font-size:1.5rem;font-weight:bold;color:{color};margin:4px 0">{value}</p>
            {delta_html}
            {fiab_html}
        </div>
        """,
        unsafe_allow_html=True,
    )


def risk_badge(level: str) -> str:
    """Return colored HTML badge for risk level."""
    color = RISK_COLORS.get(level, "#7F8C8D")
    emoji = RISK_EMOJI.get(level, "⚪")
    return f'<span style="background:{color};color:white;padding:2px 8px;border-radius:12px;font-size:0.75rem;font-weight:bold">{emoji} {level}</span>'


# ─────────────────────────────────────────────
# ALERTS
# ─────────────────────────────────────────────
def render_alert(message: str, level: str = "warning"):
    """Render a styled alert banner."""
    colors = {"error": "#E74C3C", "warning": "#F39C12", "info": "#2E86AB", "success": "#27AE60"}
    icons = {"error": "🚨", "warning": "⚠️", "info": "ℹ️", "success": "✅"}
    c = colors.get(level, "#F39C12")
    i = icons.get(level, "⚠️")
    st.markdown(
        f"""
        <div style="background:{c}22;border-left:4px solid {c};padding:10px 14px;border-radius:6px;margin:6px 0">
            {i} <span style="color:{c};font-weight:bold">{message}</span>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ─────────────────────────────────────────────
# CHARTS
# ─────────────────────────────────────────────
def bar_chart(df: pd.DataFrame, x: str, y: str, title: str, color: str = None,
              height: int = 380, text_col: str = None) -> go.Figure:
    """Simple styled bar chart."""
    fig = px.bar(
        df, x=x, y=y, title=title, text=text_col,
        color_discrete_sequence=[color or COLORS["primary"]],
        template=PLOTLY_TEMPLATE,
        height=height,
    )
    fig.update_layout(
        margin=dict(l=20, r=20, t=40, b=20),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(size=12),
    )
    fig.update_traces(textposition="outside")
    return fig


def donut_chart(labels: list, values: list, title: str, height: int = 350) -> go.Figure:
    """Styled donut chart."""
    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            hole=0.5,
            textinfo="label+percent",
            marker=dict(colors=px.colors.qualitative.Set2),
        )
    )
    fig.update_layout(
        title=title,
        template=PLOTLY_TEMPLATE,
        height=height,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def line_chart(df: pd.DataFrame, x: str, y_cols: list, title: str, height: int = 380) -> go.Figure:
    """Multi-line chart for timeseries."""
    palette = [COLORS["primary"], COLORS["danger"], COLORS["success"], COLORS["warning"]]
    fig = go.Figure()
    for i, col in enumerate(y_cols):
        if col in df.columns:
            fig.add_trace(
                go.Scatter(
                    x=df[x], y=df[col], mode="lines+markers",
                    name=col, line=dict(color=palette[i % len(palette)], width=2),
                )
            )
    fig.update_layout(
        title=title,
        template=PLOTLY_TEMPLATE,
        height=height,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02),
    )
    return fig


def gauge_chart(value: float, title: str, max_val: float = 100, unit: str = "%") -> go.Figure:
    """Gauge chart for progress/consumption."""
    color = COLORS["success"] if value < 60 else COLORS["warning"] if value < 85 else COLORS["danger"]
    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=value,
            title={"text": title, "font": {"size": 13}},
            number={"suffix": unit, "font": {"size": 20}},
            gauge={
                "axis": {"range": [0, max_val]},
                "bar": {"color": color},
                "steps": [
                    {"range": [0, max_val * 0.6], "color": "#1e3a2f"},
                    {"range": [max_val * 0.6, max_val * 0.85], "color": "#3a2e1a"},
                    {"range": [max_val * 0.85, max_val], "color": "#3a1a1a"},
                ],
            },
        )
    )
    fig.update_layout(
        template=PLOTLY_TEMPLATE,
        height=220,
        margin=dict(l=20, r=20, t=60, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def waterfall_chart(categories: list, values: list, title: str) -> go.Figure:
    """Waterfall chart for budget breakdown."""
    fig = go.Figure(
        go.Waterfall(
            name="Budget",
            orientation="v",
            measure=["relative"] * len(values),
            x=categories,
            y=values,
            connector={"line": {"color": "rgb(63,63,63)"}},
            decreasing={"marker": {"color": COLORS["danger"]}},
            increasing={"marker": {"color": COLORS["success"]}},
        )
    )
    fig.update_layout(
        title=title,
        template=PLOTLY_TEMPLATE,
        height=380,
        margin=dict(l=20, r=20, t=40, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


# ─────────────────────────────────────────────
# RECOMMENDATIONS ENGINE
# ─────────────────────────────────────────────
def generate_recommendations(df_kpis: pd.DataFrame, df_regul: pd.DataFrame) -> list:
    """Generate automatic recommendations based on KPIs."""
    recs = []
    kpi_dict = dict(zip(df_kpis["kpi"], df_kpis["valeur"])) if not df_kpis.empty else {}

    # Net trésorerie
    net = kpi_dict.get("Net trésorerie", 0)
    if net < 0:
        recs.append({
            "priorité": "🔴 URGENT",
            "domaine": "Trésorerie",
            "recommandation": f"Net trésorerie négatif ({fmt_mad(net)}). Accélérer les encaissements en attente.",
            "action": "Relancer les clients avec factures impayées. Vérifier le poste 'Autres dépenses' (> 1.3M MAD).",
        })

    # Obligations élevées
    nb_urgences = kpi_dict.get("Obligations ÉLEVÉ risque", 0)
    if nb_urgences >= 3:
        recs.append({
            "priorité": "🔴 URGENT",
            "domaine": "Régularisation",
            "recommandation": f"{int(nb_urgences)} obligations fiscales/sociales à risque ÉLEVÉ identifiées.",
            "action": "Mandater un expert-comptable dans les 30 jours. Prioriser les bilans 2024.",
        })

    # Reste à encaisser NORA
    reste_nora = kpi_dict.get("Reste à encaisser NORA", 0)
    if reste_nora > 20000:
        recs.append({
            "priorité": "🟡 IMPORTANT",
            "domaine": "NORA Académie",
            "recommandation": f"{fmt_mad(reste_nora)} de factures NORA non encore encaissées.",
            "action": "Envoyer des relances aux clients avec factures ouvertes. Vérifier les statuts bancaires.",
        })

    # Budget SalesX consommation
    conso = kpi_dict.get("Consommation budget SalesX (%)", 0)
    if conso > 85:
        recs.append({
            "priorité": "🟡 IMPORTANT",
            "domaine": "SalesX Budget",
            "recommandation": f"Budget SalesX consommé à {conso}%. Risque de dépassement.",
            "action": "Geler les dépenses non essentielles. Prioriser la livraison du MVP.",
        })

    # Pricing SalesX
    recs.append({
        "priorité": "🟡 IMPORTANT",
        "domaine": "SalesX Pricing",
        "recommandation": "Incohérence détectée dans le pricing : 5 000–54 000 MAD/an selon les sources.",
        "action": "Clarifier le prix d'abonnement avec le dirigeant avant le lancement commercial.",
    })

    # CNSS
    if not df_regul.empty:
        cnss_row = df_regul[df_regul["Obligation"].str.contains("CNSS", na=False)]
        if not cnss_row.empty and cnss_row.iloc[0]["Niveau_risque"] == "ÉLEVÉ":
            recs.append({
                "priorité": "🔴 URGENT",
                "domaine": "CNSS",
                "recommandation": "Retards CNSS historiques confirmés chez Intelead.",
                "action": "Contacter Damancom pour établir un plan d'apurement des arriérés CNSS.",
            })

    return recs
