"""
FinancePilot 360 - Configuration
Central configuration: paths, colors, constants, hypotheses.
"""

import os

# ─────────────────────────────────────────────
# PATHS
# ─────────────────────────────────────────────
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_RAW = os.path.join(BASE_DIR, "data", "raw")
DATA_PROCESSED = os.path.join(BASE_DIR, "data", "processed")
OUTPUTS_DIR = os.path.join(BASE_DIR, "outputs")

CSV_FILES = {
    "regul": os.path.join(DATA_PROCESSED, "regul_obligations.csv"),
    "salesx_budget": os.path.join(DATA_PROCESSED, "salesx_budget.csv"),
    "nora_rentabilite": os.path.join(DATA_PROCESSED, "nora_rentabilite.csv"),
    "nora_couts": os.path.join(DATA_PROCESSED, "nora_couts.csv"),
    "tresorerie": os.path.join(DATA_PROCESSED, "tresorerie.csv"),
    "depenses": os.path.join(DATA_PROCESSED, "depenses_categories.csv"),
    "encaissements": os.path.join(DATA_PROCESSED, "encaissements_categories.csv"),
    "kpis": os.path.join(DATA_PROCESSED, "dashboard_kpis.csv"),
    "data_quality": os.path.join(DATA_PROCESSED, "data_quality.csv"),
}

# ─────────────────────────────────────────────
# PROJECT META
# ─────────────────────────────────────────────
PROJECT_NAME = "FinancePilot 360"
PROJECT_VERSION = "V1"
ENTITIES = ["SalesFlow SARL AU", "Intelead SARL"]
PERIOD = "2024 - 2025"

# ─────────────────────────────────────────────
# SALESX HYPOTHESES (visible & modifiable)
# ─────────────────────────────────────────────
SALESX = {
    "budget_total": 250_000,          # MAD - Coût total projet (Réelle)
    "subvention": 200_000,            # MAD - Subvention Startup Maroc (Réelle)
    "autofinancement": 50_000,        # MAD - Autofinancement (Calculé)
    "taux_financement": 0.80,         # 80% (Calculé)
    "prix_min_client_an": 5_000,      # MAD - Hypothèse basse BP
    "prix_max_client_an": 54_000,     # MAD - Hypothèse haute (à clarifier)
    "prix_realiste_client_an": 10_000,# MAD - Hypothèse pitch deck
    "clients_scenario_prudent": 5,
    "clients_scenario_realiste": 20,
    "clients_scenario_ambitieux": 40,
    "budget_marketing": 60_000,       # MAD - Total marketing prévu
    "charges_fixes_annuelles": 100_000,# MAD - Estimation charges fixes
}

# Calculs dérivés SalesX
SALESX["cac_realiste"] = SALESX["budget_marketing"] / SALESX["clients_scenario_realiste"]
SALESX["cac_prudent"] = SALESX["budget_marketing"] / SALESX["clients_scenario_prudent"]
SALESX["cac_ambitieux"] = SALESX["budget_marketing"] / SALESX["clients_scenario_ambitieux"]

for scenario, nb_clients in [
    ("prudent", SALESX["clients_scenario_prudent"]),
    ("realiste", SALESX["clients_scenario_realiste"]),
    ("ambitieux", SALESX["clients_scenario_ambitieux"]),
]:
    SALESX[f"ca_{scenario}"] = nb_clients * SALESX["prix_realiste_client_an"]

SALESX["seuil_rentabilite_clients"] = SALESX["charges_fixes_annuelles"] / SALESX["prix_realiste_client_an"]

# ─────────────────────────────────────────────
# NORA HYPOTHESES
# ─────────────────────────────────────────────
NORA = {
    "cout_par_session_estime": 2_000,  # MAD - Hypothèse coût direct par session
    "taux_couts_partages": 0.15,       # 15% du CA affecté aux coûts partagés
    "taux_tva": 0.20,                  # 20% TVA applicable
}

# ─────────────────────────────────────────────
# COLORS (matching Streamlit theme)
# ─────────────────────────────────────────────
COLORS = {
    "primary": "#2E86AB",
    "success": "#27AE60",
    "warning": "#F39C12",
    "danger": "#E74C3C",
    "neutral": "#7F8C8D",
    "background": "#0E1117",
    "card_bg": "#1C2333",
}

RISK_COLORS = {
    "ÉLEVÉ": "#E74C3C",
    "MOYEN": "#F39C12",
    "FAIBLE": "#27AE60",
    "INCONNU": "#7F8C8D",
}

RISK_EMOJI = {
    "ÉLEVÉ": "🔴",
    "MOYEN": "🟡",
    "FAIBLE": "🟢",
    "INCONNU": "⚪",
}

STATUS_COLORS = {
    "Non déclaré": "#E74C3C",
    "Retard historique": "#E74C3C",
    "Inconnu": "#7F8C8D",
    "À collecter": "#F39C12",
    "Déclaré": "#27AE60",
    "Payé": "#27AE60",
}

# ─────────────────────────────────────────────
# CHART CONFIG
# ─────────────────────────────────────────────
PLOTLY_TEMPLATE = "plotly_dark"
CHART_HEIGHT = 400
CHART_HEIGHT_SMALL = 300
