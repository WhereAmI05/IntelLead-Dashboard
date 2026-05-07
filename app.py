"""
FinancePilot 360 - Tableau de Bord Financier Multiprojet
Application Streamlit V1 - 4 pages principales

Pages:
  1. Executive Dashboard
  2. Régularisation & Risques
  3. SalesX + NORA Rentabilité
  4. Trésorerie & Analyse Financière
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import os

from config import (
    PROJECT_NAME, PERIOD, SALESX, NORA as NORA_CFG,
    RISK_COLORS, RISK_EMOJI, COLORS, PLOTLY_TEMPLATE
)
from utils import (
    load_csv, check_data_ready, _run_data_preparation,
    kpi_card, risk_badge, render_alert, fmt_mad, fmt_pct, fmt_number,
    bar_chart, donut_chart, line_chart, gauge_chart, waterfall_chart,
    generate_recommendations,
)

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="FinancePilot 360",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS
st.markdown("""
<style>
    /* Main background */
    .stApp { background-color: #0E1117; }
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #161B2E; }
    /* Remove default padding */
    .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    /* Metric cards */
    [data-testid="stMetric"] { background-color: #1C2333; border-radius: 8px; padding: 12px; }
    /* Dataframe */
    .stDataFrame { border-radius: 8px; }
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    /* Divider */
    hr { border-color: #2C3A5A; }
    /* Section header */
    h2 { color: #2E86AB; border-bottom: 2px solid #2E86AB; padding-bottom: 6px; }
    h3 { color: #E0E0E0; }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.image("https://img.icons8.com/color/96/financial-analytics.png", width=60)
    st.title("FinancePilot 360")
    st.caption(f"Version 1.0 · {PERIOD}")
    st.divider()

    page = st.radio(
        "Navigation",
        [
            "🏠 Executive Dashboard",
            "⚠️ Régularisation & Risques",
            "📈 SalesX + NORA Rentabilité",
            "💰 Trésorerie & Finances",
        ],
        label_visibility="collapsed",
    )
    st.divider()

    # Data refresh button
    if st.button("🔄 Actualiser les données", use_container_width=True):
        _run_data_preparation()
        st.cache_data.clear()
        st.rerun()

    # Data readiness indicator
    if check_data_ready():
        st.success("✅ Données chargées")
    else:
        st.warning("⚠️ Données manquantes\nCliquez sur Actualiser")

    st.divider()
    st.caption("⚠️ Données partiellement estimées.\nNe pas utiliser pour décisions légales officielles.")
    st.caption("🔍 Fiabilité indiquée sur chaque indicateur.")


# ─────────────────────────────────────────────
# AUTO PREPARE DATA IF NEEDED
# ─────────────────────────────────────────────
if not check_data_ready():
    _run_data_preparation()
    st.cache_data.clear()


# ─────────────────────────────────────────────
# PAGE 1: EXECUTIVE DASHBOARD
# ─────────────────────────────────────────────
if page == "🏠 Executive Dashboard":
    st.title("💼 Executive Dashboard")
    st.caption(f"Vue synthétique · {PERIOD} · FinancePilot 360")

    # Load data
    df_kpis = load_csv("kpis")
    df_regul = load_csv("regul")
    df_nora = load_csv("nora_rentabilite")
    df_dep = load_csv("depenses")
    df_enc = load_csv("encaissements")
    df_treso = load_csv("tresorerie")
    df_quality = load_csv("data_quality")

    kpi_dict = dict(zip(df_kpis["kpi"], df_kpis["valeur"])) if not df_kpis.empty else {}

    # ── ALERTES PRIORITAIRES ──
    st.markdown("### 🚨 Alertes prioritaires")
    col_a1, col_a2, col_a3 = st.columns(3)
    with col_a1:
        nb_urgent = int(kpi_dict.get("Obligations ÉLEVÉ risque", 0))
        render_alert(f"{nb_urgent} obligations fiscales/sociales à risque ÉLEVÉ", "error")
    with col_a2:
        reste = kpi_dict.get("Reste à encaisser NORA", 0)
        render_alert(f"{fmt_mad(reste)} de factures NORA non encaissées", "warning")
    with col_a3:
        render_alert("Incohérence pricing SalesX détectée (5k–54k MAD/an)", "warning")

    st.divider()

    # ── KPI CARDS ROW 1: TRÉSORERIE ──
    st.markdown("### 💰 Trésorerie Globale")
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        val = kpi_dict.get("Encaissements totaux (2024-2025)", 0)
        kpi_card("Encaissements totaux", fmt_mad(val), "2024-2025", COLORS["success"], "📥", "Réelle")
    with c2:
        val = kpi_dict.get("Dépenses totales (2024-2025)", 0)
        kpi_card("Dépenses totales", fmt_mad(val), "2024-2025", COLORS["danger"], "📤", "Réelle")
    with c3:
        val = kpi_dict.get("Net trésorerie", 0)
        color = COLORS["success"] if val >= 0 else COLORS["danger"]
        kpi_card("Net trésorerie", fmt_mad(val), "▲ Positif" if val >= 0 else "▼ Négatif", color, "⚖️", "Réelle")
    with c4:
        val = kpi_dict.get("Reste à encaisser NORA", 0)
        kpi_card("Reste à encaisser NORA", fmt_mad(val), "Factures ouvertes", COLORS["warning"], "🔔", "Réelle")

    st.markdown("### 🚀 SalesX & NORA")
    c5, c6, c7, c8 = st.columns(4)
    with c5:
        val = kpi_dict.get("Budget SalesX prévu", 0)
        kpi_card("Budget SalesX prévu", fmt_mad(val), "Coût total projet", COLORS["primary"], "📋", "Réelle")
    with c6:
        val = kpi_dict.get("Subvention Startup Maroc", 0)
        kpi_card("Subvention reçue", fmt_mad(val), "Tech Start / Startup Maroc", COLORS["success"], "🏆", "Réelle")
    with c7:
        val = kpi_dict.get("CA NORA HT (factures)", 0)
        kpi_card("CA NORA HT", fmt_mad(val), "Factures attribuées", COLORS["primary"], "🎓", "Réelle")
    with c8:
        val = kpi_dict.get("Taux marge brute NORA (%)", 0)
        kpi_card("Marge brute NORA", fmt_pct(val), "Estimée (coûts hypothèse)", COLORS["success"] if val > 50 else COLORS["warning"], "📊", "Estimée")

    st.divider()

    # ── CHARTS ROW ──
    col_g1, col_g2 = st.columns([1, 1])
    with col_g1:
        st.markdown("#### 📊 Dépenses par catégorie (2024-2025)")
        if not df_dep.empty:
            fig = donut_chart(
                df_dep["categorie"].tolist(),
                df_dep["total"].tolist(),
                "Répartition des dépenses",
                height=340,
            )
            st.plotly_chart(fig, use_container_width=True)

    with col_g2:
        st.markdown("#### 📈 Évolution trésorerie mensuelle")
        if not df_treso.empty:
            fig = line_chart(
                df_treso, "mois",
                ["encaissements", "depenses", "net"],
                "Encaissements vs Dépenses (mensuel)",
                height=340,
            )
            st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ── RECOMMANDATIONS AUTOMATIQUES ──
    st.markdown("### 🧠 Recommandations automatiques")
    recs = generate_recommendations(df_kpis, df_regul)
    for rec in recs:
        with st.expander(f"{rec['priorité']} · {rec['domaine']} — {rec['recommandation'][:70]}..."):
            st.markdown(f"**Problème :** {rec['recommandation']}")
            st.markdown(f"**Action recommandée :** {rec['action']}")

    st.divider()

    # ── DATA QUALITY SUMMARY ──
    st.markdown("### 🔍 Qualité des données")
    if not df_quality.empty:
        high = (df_quality["Sévérité"] == "ÉLEVÉE").sum()
        med = (df_quality["Sévérité"] == "MOYENNE").sum()
        low = (df_quality["Sévérité"] == "FAIBLE").sum()
        cq1, cq2, cq3 = st.columns(3)
        cq1.metric("Problèmes ÉLEVÉS", high, delta=None)
        cq2.metric("Problèmes MOYENS", med, delta=None)
        cq3.metric("Problèmes FAIBLES", low, delta=None)


# ─────────────────────────────────────────────
# PAGE 2: RÉGULARISATION & RISQUES
# ─────────────────────────────────────────────
elif page == "⚠️ Régularisation & Risques":
    st.title("⚠️ Régularisation Fiscale & Sociale 2024-2025")
    st.caption("Suivi des obligations, risques, pièces manquantes et plan d'action")

    df_regul = load_csv("regul")

    if df_regul.empty:
        st.error("Données régularisation non disponibles.")
        st.stop()

    # ── KPIs RISQUE ──
    nb_eleve = (df_regul["Niveau_risque"] == "ÉLEVÉ").sum()
    nb_moyen = (df_regul["Niveau_risque"] == "MOYEN").sum()
    nb_total = len(df_regul)

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        kpi_card("Obligations totales", str(nb_total), "à surveiller", COLORS["primary"], "📋")
    with c2:
        kpi_card("Risque ÉLEVÉ", str(nb_eleve), "action urgente", COLORS["danger"], "🔴")
    with c3:
        kpi_card("Risque MOYEN", str(nb_moyen), "à surveiller", COLORS["warning"], "🟡")
    with c4:
        # Horizon 30 jours
        n30 = (df_regul["Horizon"] == "30 jours").sum()
        kpi_card("À traiter sous 30j", str(n30), "priorité absolue", COLORS["danger"], "⏰")

    st.divider()

    # ── PLAN 30/60/90 JOURS ──
    st.markdown("### 📅 Plan d'action 30 / 60 / 90 jours")
    tabs = st.tabs(["🔴 30 jours", "🟡 60 jours", "🟢 90 jours"])

    for tab, horizon in zip(tabs, ["30 jours", "60 jours", "90 jours"]):
        with tab:
            df_h = df_regul[df_regul["Horizon"] == horizon]
            if df_h.empty:
                st.info("Aucune obligation sur cet horizon.")
            else:
                for _, row in df_h.iterrows():
                    with st.expander(f"{RISK_EMOJI.get(row['Niveau_risque'], '⚪')} {row['Obligation']} — {row['Entité']}"):
                        co1, co2 = st.columns([1, 2])
                        with co1:
                            st.markdown(f"**Type :** {row['Type']}")
                            st.markdown(f"**Statut :** `{row['Statut']}`")
                            st.markdown(f"**Fiabilité :** {row['Fiabilité']}")
                        with co2:
                            st.markdown(f"**Pièces manquantes :** {row['Pièces_manquantes']}")
                            st.markdown(f"**Action prioritaire :** {row['Action_prioritaire']}")
                            st.markdown(f"**Responsable :** {row['Responsable']}")

    st.divider()

    # ── TABLE COMPLÈTE ──
    st.markdown("### 📋 Table complète des obligations")

    # Filter controls
    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        risk_filter = st.multiselect(
            "Niveau de risque",
            options=df_regul["Niveau_risque"].unique().tolist(),
            default=df_regul["Niveau_risque"].unique().tolist(),
        )
    with col_f2:
        entite_filter = st.multiselect(
            "Entité",
            options=df_regul["Entité"].unique().tolist(),
            default=df_regul["Entité"].unique().tolist(),
        )
    with col_f3:
        horizon_filter = st.multiselect(
            "Horizon",
            options=df_regul["Horizon"].unique().tolist(),
            default=df_regul["Horizon"].unique().tolist(),
        )

    df_filtered = df_regul[
        df_regul["Niveau_risque"].isin(risk_filter) &
        df_regul["Entité"].isin(entite_filter) &
        df_regul["Horizon"].isin(horizon_filter)
    ]

    # Display with color coding
    def style_risk(val):
        color = RISK_COLORS.get(val, "#7F8C8D")
        return f"background-color: {color}33; color: {color}; font-weight: bold"

    display_cols = ["Obligation", "Entité", "Type", "Statut", "Niveau_risque", "Horizon", "Action_prioritaire"]
    st.dataframe(
        df_filtered[display_cols].style.applymap(style_risk, subset=["Niveau_risque"]),
        use_container_width=True,
        height=380,
    )

    st.divider()

    # ── CHART RISQUES ──
    col_ch1, col_ch2 = st.columns(2)
    with col_ch1:
        risk_counts = df_regul["Niveau_risque"].value_counts().reset_index()
        risk_counts.columns = ["Risque", "Nombre"]
        fig = bar_chart(risk_counts, "Risque", "Nombre", "Répartition par niveau de risque",
                        height=300)
        st.plotly_chart(fig, use_container_width=True)
    with col_ch2:
        type_counts = df_regul["Type"].value_counts().reset_index()
        type_counts.columns = ["Type", "Nombre"]
        fig2 = donut_chart(type_counts["Type"].tolist(), type_counts["Nombre"].tolist(),
                           "Répartition par type d'obligation", height=300)
        st.plotly_chart(fig2, use_container_width=True)

    # ── DATA QUALITY ──
    st.divider()
    df_quality = load_csv("data_quality")
    st.markdown("### 🔍 Alertes qualité données — Régularisation")
    dq_regul = df_quality[df_quality["Source"].str.contains("REGUL", na=False)] if not df_quality.empty else pd.DataFrame()
    if not dq_regul.empty:
        for _, row in dq_regul.iterrows():
            render_alert(f"[{row['Source']}] {row['Problème']} → {row['Recommandation']}", "warning")


# ─────────────────────────────────────────────
# PAGE 3: SALESX + NORA RENTABILITÉ
# ─────────────────────────────────────────────
elif page == "📈 SalesX + NORA Rentabilité":
    st.title("📈 SalesX & NORA Académie — Rentabilité & Projections")

    tab_sx, tab_nora = st.tabs(["🚀 SalesX / SalesFlow", "🎓 NORA Académie"])

    # ── SALESX TAB ──
    with tab_sx:
        st.markdown("### 🚀 SalesX — Suivi Budget & Scénarios")
        df_salesx = load_csv("salesx_budget")

        if not df_salesx.empty:
            # KPIs
            budget_total = df_salesx["Budget_prévu"].sum()
            realise = df_salesx["Réalisé_estimé"].sum()
            reste = df_salesx["Reste"].sum()
            conso_pct = realise / budget_total * 100

            c1, c2, c3, c4 = st.columns(4)
            with c1:
                kpi_card("Budget total SalesX", fmt_mad(budget_total), "Coût projet total", COLORS["primary"], "📋", "Réelle")
            with c2:
                kpi_card("Subvention Tech Start", fmt_mad(SALESX["subvention"]), f"Taux {SALESX['taux_financement']*100:.0f}%", COLORS["success"], "🏆", "Réelle")
            with c3:
                kpi_card("Réalisé estimé", fmt_mad(realise), f"Consommé {conso_pct:.1f}%", COLORS["warning"], "💸", "Estimée")
            with c4:
                kpi_card("Budget restant", fmt_mad(reste), "À engager", COLORS["primary"], "🏦", "Calculée")

            # Budget gauge
            col_g, col_bar = st.columns([1, 2])
            with col_g:
                fig_gauge = gauge_chart(conso_pct, "Consommation budget (%)", 100, "%")
                st.plotly_chart(fig_gauge, use_container_width=True)
            with col_bar:
                fig_bar = bar_chart(
                    df_salesx, "Sous_catégorie", "Budget_prévu",
                    "Budget prévu vs Réalisé par poste", height=300
                )
                fig_bar.add_bar(x=df_salesx["Sous_catégorie"], y=df_salesx["Réalisé_estimé"],
                                name="Réalisé", marker_color=COLORS["success"])
                st.plotly_chart(fig_bar, use_container_width=True)

            # Budget table
            st.markdown("#### 📋 Détail budget par poste")
            display_cols = ["Catégorie", "Sous_catégorie", "Budget_prévu", "Réalisé_estimé", "Reste", "Consommation_%", "Statut", "Fiabilité"]
            st.dataframe(df_salesx[display_cols], use_container_width=True, hide_index=True)

            # Alert: dépenses manquantes
            render_alert("Les dépenses réalisées SalesX sont partiellement estimées. Collecte des justificatifs recommandée.", "warning")
            render_alert("Incohérence pricing abonnement : 5 000–54 000 MAD/an selon sources. À clarifier avant lancement.", "error")

        st.divider()

        # ── SCÉNARIOS ──
        st.markdown("### 🔭 Scénarios de rentabilité SalesX")
        st.info("ℹ️ Hypothèses modifiables. Ajustez le prix et le nombre de clients pour simuler différents scénarios.", icon="💡")

        col_hyp1, col_hyp2, col_hyp3 = st.columns(3)
        with col_hyp1:
            prix_client = st.number_input("Prix/client/an (MAD)", min_value=1000, max_value=100000,
                                          value=int(SALESX["prix_realiste_client_an"]), step=500)
        with col_hyp2:
            nb_clients_1 = st.number_input("Clients an 1", min_value=1, max_value=500, value=20)
        with col_hyp3:
            nb_clients_2 = st.number_input("Clients an 2", min_value=1, max_value=500, value=50)

        charges_fixes = st.slider("Charges fixes annuelles (MAD)", 50000, 300000,
                                  int(SALESX["charges_fixes_annuelles"]), 10000)

        # Compute scenarios
        scenarios = {
            "Prudent (5 clients)": 5,
            "Réaliste (20 clients)": nb_clients_1,
            "Ambitieux (40 clients)": nb_clients_2,
        }
        sc_data = []
        for name, nb_c in scenarios.items():
            ca = nb_c * prix_client
            cac = SALESX["budget_marketing"] / max(nb_c, 1)
            marge = ca - charges_fixes
            seuil = charges_fixes / prix_client
            sc_data.append({
                "Scénario": name,
                "Nb clients": nb_c,
                "CA annuel (MAD)": ca,
                "CAC (MAD/client)": round(cac, 0),
                "Charges fixes": charges_fixes,
                "Marge nette estimée": marge,
                "Rentable": "✅" if marge > 0 else "❌",
                "Seuil rentabilité (clients)": round(seuil, 1),
            })

        df_sc = pd.DataFrame(sc_data)
        st.dataframe(df_sc, use_container_width=True, hide_index=True)

        fig_sc = px.bar(
            df_sc, x="Scénario", y="CA annuel (MAD)",
            color="Rentable", color_discrete_map={"✅": COLORS["success"], "❌": COLORS["danger"]},
            title="CA par scénario vs Seuil de rentabilité",
            template=PLOTLY_TEMPLATE, height=320,
        )
        fig_sc.add_hline(y=charges_fixes, line_dash="dash", line_color=COLORS["warning"],
                         annotation_text=f"Seuil: {fmt_mad(charges_fixes)}")
        st.plotly_chart(fig_sc, use_container_width=True)

    # ── NORA TAB ──
    with tab_nora:
        st.markdown("### 🎓 NORA Académie — Rentabilité des Formations")
        df_nora = load_csv("nora_rentabilite")
        df_couts = load_csv("nora_couts")
        df_nora_syn = load_csv("kpis")

        if not df_nora.empty:
            # KPIs
            ca_total = df_nora["ca_ht"].sum()
            encaisse = df_nora["encaisse"].sum()
            reste = df_nora["reste_a_encaisser"].sum()
            marge = df_nora["marge_brute_estimee"].sum()
            taux_marge = (marge / ca_total * 100) if ca_total > 0 else 0
            cout_total = df_nora["cout_direct_estime"].sum()

            c1, c2, c3 = st.columns(3)
            with c1:
                kpi_card("CA HT total NORA", fmt_mad(ca_total), "21 factures B2B", COLORS["primary"], "🎓", "Réelle")
                kpi_card("Encaissé banque", fmt_mad(encaisse), "rapproché confirmé", COLORS["success"], "✅", "Réelle")
            with c2:
                kpi_card("Reste à encaisser", fmt_mad(reste), "factures ouvertes", COLORS["warning"], "🔔", "Réelle")
                kpi_card("Coûts directs estimés", fmt_mad(cout_total), "hypothèse 2k MAD/session", COLORS["neutral"], "💼", "Estimée")
            with c3:
                kpi_card("Marge brute estimée", fmt_mad(marge), "", COLORS["success"] if marge > 0 else COLORS["danger"], "📊", "Estimée")
                kpi_card("Taux marge brute", fmt_pct(taux_marge), "", COLORS["success"] if taux_marge > 50 else COLORS["warning"], "📈", "Estimée")

            st.divider()

            # ── CHARTS NORA ──
            col_n1, col_n2 = st.columns(2)
            with col_n1:
                st.markdown("#### 📊 CA par client")
                client_ca = df_nora.groupby("client")["ca_ht"].sum().sort_values(ascending=False).reset_index()
                client_ca.columns = ["Client", "CA HT"]
                fig = bar_chart(client_ca, "Client", "CA HT", "CA HT par client (MAD)", COLORS["primary"], height=320)
                st.plotly_chart(fig, use_container_width=True)

            with col_n2:
                st.markdown("#### 🎯 CA par type de formation")
                type_ca = df_nora.groupby("type_formation")["ca_ht"].sum().sort_values(ascending=False).reset_index()
                type_ca.columns = ["Type", "CA HT"]
                fig2 = donut_chart(type_ca["Type"].tolist(), type_ca["CA HT"].tolist(),
                                   "Répartition CA par type de formation", height=320)
                st.plotly_chart(fig2, use_container_width=True)

            st.divider()

            # ── TABLE FACTURES ──
            st.markdown("#### 📋 Table des factures — Rentabilité par formation")

            # Filter
            statut_options = df_nora["statut_encaissement"].dropna().unique().tolist()
            statut_sel = st.multiselect("Filtrer par statut encaissement",
                                        options=statut_options, default=statut_options)
            df_nora_f = df_nora[df_nora["statut_encaissement"].isin(statut_sel)] if statut_sel else df_nora

            cols_show = ["id", "client", "type_formation", "annee", "nb_sessions",
                         "ca_ht", "encaisse", "reste_a_encaisser",
                         "marge_brute_estimee", "taux_marge_brute", "alerte"]
            st.dataframe(df_nora_f[cols_show], use_container_width=True, hide_index=True, height=360)

            st.divider()

            # ── COÛTS NORA ──
            st.markdown("#### 💼 Coûts retenus à ventiler")
            if not df_couts.empty:
                cat_couts = df_couts.groupby("categorie")["montant"].sum().reset_index()
                cat_couts.columns = ["Catégorie", "Montant"]
                fig_c = bar_chart(cat_couts, "Catégorie", "Montant", "Coûts NORA par catégorie", COLORS["danger"], 300)
                col_cc1, col_cc2 = st.columns(2)
                with col_cc1:
                    st.plotly_chart(fig_c, use_container_width=True)
                with col_cc2:
                    kpi_card("Total coûts à ventiler", fmt_mad(df_couts["montant"].sum()),
                             "Hôtel + ONCF + Prestataires + Espèces + OpenAI", COLORS["warning"], "💼", "Réelle")
                    render_alert("Tous les coûts sont marqués 'À ventiler'. Attribution par formation recommandée.", "info")


# ─────────────────────────────────────────────
# PAGE 4: TRÉSORERIE & ANALYSE FINANCIÈRE
# ─────────────────────────────────────────────
elif page == "💰 Trésorerie & Finances":
    st.title("💰 Trésorerie & Analyse Financière")
    st.caption("Encaissements, dépenses, tendances et alertes — 2024-2025")

    df_treso = load_csv("tresorerie")
    df_dep = load_csv("depenses")
    df_enc = load_csv("encaissements")

    # ── KPIs TRÉSORERIE ──
    if not df_treso.empty:
        enc_total = df_treso["encaissements"].sum() if "encaissements" in df_treso.columns else 0
        dep_total = df_treso["depenses"].sum() if "depenses" in df_treso.columns else 0
        net_total = enc_total - dep_total
        solde_final = df_treso["solde_cumulé"].iloc[-1] if "solde_cumulé" in df_treso.columns else net_total

        # Trend (last 3 months net)
        df_recent = df_treso.tail(3)
        net_recent = df_recent["net"].mean() if "net" in df_recent.columns else 0
        trend = "📈 Haussière" if net_recent > 0 else "📉 Baissière"

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            kpi_card("Encaissements totaux", fmt_mad(enc_total), "2024-2025", COLORS["success"], "📥", "Réelle")
        with c2:
            kpi_card("Dépenses totales", fmt_mad(dep_total), "2024-2025", COLORS["danger"], "📤", "Réelle")
        with c3:
            color = COLORS["success"] if net_total >= 0 else COLORS["danger"]
            kpi_card("Net cumulé", fmt_mad(net_total), "", color, "⚖️", "Réelle")
        with c4:
            kpi_card("Tendance récente (3m)", trend, f"Net moy: {fmt_mad(net_recent)}", COLORS["primary"], "📊")

    st.divider()

    # ── CHARTS TRÉSORERIE ──
    if not df_treso.empty:
        # Monthly evolution
        st.markdown("### 📈 Évolution mensuelle de la trésorerie")

        col_t1, col_t2 = st.columns([2, 1])
        with col_t1:
            fig_line = line_chart(
                df_treso, "mois",
                ["encaissements", "depenses", "net"],
                "Flux mensuels : Encaissements / Dépenses / Net",
                height=360,
            )
            st.plotly_chart(fig_line, use_container_width=True)
        with col_t2:
            fig_solde = line_chart(
                df_treso, "mois",
                ["solde_cumulé"],
                "Solde cumulé",
                height=360,
            )
            st.plotly_chart(fig_solde, use_container_width=True)

        # Alerts
        neg_months = df_treso[df_treso.get("net", pd.Series([0])) < 0] if "net" in df_treso.columns else pd.DataFrame()
        if not neg_months.empty:
            render_alert(f"{len(neg_months)} mois avec net négatif détectés. Analyser les causes.", "warning")

    st.divider()

    # ── DÉPENSES PAR CATÉGORIE ──
    st.markdown("### 💸 Dépenses par catégorie")
    if not df_dep.empty:
        col_d1, col_d2 = st.columns([2, 1])
        with col_d1:
            fig_dep_bar = px.bar(
                df_dep.sort_values("total", ascending=True),
                x="total", y="categorie", orientation="h",
                title="Total dépenses par catégorie (2024-2025)",
                template=PLOTLY_TEMPLATE, height=380,
                color="total",
                color_continuous_scale="Reds",
                text="pct_total",
            )
            fig_dep_bar.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            fig_dep_bar.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                margin=dict(l=20, r=40, t=40, b=20),
                coloraxis_showscale=False,
            )
            st.plotly_chart(fig_dep_bar, use_container_width=True)
        with col_d2:
            st.markdown("**Top dépenses**")
            top_dep = df_dep.nlargest(5, "total")[["categorie", "total", "pct_total"]]
            top_dep.columns = ["Catégorie", "Total MAD", "%"]
            st.dataframe(top_dep, use_container_width=True, hide_index=True)

            render_alert("'Autres dépenses' représente >60% du total. Ventilation recommandée.", "warning")

    st.divider()

    # ── ENCAISSEMENTS PAR CLIENT ──
    st.markdown("### 📥 Top clients encaissements")
    if not df_enc.empty:
        df_enc_clean = df_enc.dropna(subset=["total"]).copy()
        df_enc_clean["montant_2024"] = pd.to_numeric(df_enc_clean["montant_2024"], errors="coerce").fillna(0)
        df_enc_clean["montant_2025"] = pd.to_numeric(df_enc_clean["montant_2025"], errors="coerce").fillna(0)
        df_enc_clean["total"] = pd.to_numeric(df_enc_clean["total"], errors="coerce").fillna(0)

        top_clients = df_enc_clean.nlargest(10, "total")

        fig_clients = px.bar(
            top_clients,
            x="categorie",
            y=["montant_2024", "montant_2025"],
            title="Top 10 clients — Encaissements 2024 vs 2025",
            template=PLOTLY_TEMPLATE,
            height=380,
            barmode="group",
            labels={"value": "MAD", "variable": "Année"},
            color_discrete_map={"montant_2024": COLORS["primary"], "montant_2025": COLORS["success"]},
        )
        fig_clients.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=20, r=20, t=40, b=60),
            xaxis_tickangle=-30,
        )
        st.plotly_chart(fig_clients, use_container_width=True)

        # Table
        st.markdown("#### 📋 Détail encaissements par client")
        st.dataframe(df_enc_clean[["categorie", "montant_2024", "montant_2025", "total", "pct_total"]].rename(
            columns={"categorie": "Client/Catégorie", "montant_2024": "2024 (MAD)",
                     "montant_2025": "2025 (MAD)", "total": "Total (MAD)", "pct_total": "%"}
        ), use_container_width=True, hide_index=True)

    st.divider()

    # ── ANALYSE FINANCIÈRE ──
    st.markdown("### 🧠 Analyse financière automatique")
    if not df_dep.empty and not df_enc.empty:
        total_enc = pd.to_numeric(df_enc["total"], errors="coerce").sum()
        total_dep = pd.to_numeric(df_dep["total"], errors="coerce").sum()
        rh_dep = pd.to_numeric(
            df_dep[df_dep["categorie"].str.contains("RH|salaire", case=False, na=False)]["total"],
            errors="coerce"
        ).sum()

        col_an1, col_an2 = st.columns(2)
        with col_an1:
            taux_rh = (rh_dep / total_dep * 100) if total_dep > 0 else 0
            taux_rentab = (total_enc / total_dep * 100) if total_dep > 0 else 0
            st.markdown(f"""
            | Indicateur | Valeur |
            |---|---|
            | Ratio encaissements/dépenses | **{taux_rentab:.1f}%** |
            | Part RH dans dépenses totales | **{taux_rh:.1f}%** |
            | Net global 2024-2025 | **{fmt_mad(total_enc - total_dep)}** |
            | Année la plus chargée | **2024** (1 318k MAD dépenses) |
            """)
        with col_an2:
            if taux_rentab >= 100:
                render_alert(f"Ratio enc/dep : {taux_rentab:.1f}% — Trésorerie positive sur la période.", "success")
            else:
                render_alert(f"Ratio enc/dep : {taux_rentab:.1f}% — Dépenses supérieures aux encaissements.", "error")

            render_alert("La catégorie 'Autres dépenses' (1.3M MAD) nécessite une ventilation approfondie.", "info")
            render_alert("2025 : Net négatif (-12 637 MAD). Surveiller la trésorerie H2 2025.", "warning")
