"""
FinancePilot 360 - Data Preparation Script
Reads raw Excel files, cleans data, generates CSV files and KPIs.
Run this script once before launching the Streamlit app.
"""

import pandas as pd
import numpy as np
import os
import warnings
warnings.filterwarnings("ignore")

# Paths
RAW_DIR = os.path.join("data", "raw")
PROCESSED_DIR = os.path.join("data", "processed")
os.makedirs(PROCESSED_DIR, exist_ok=True)

EXCEL_REGUL = os.path.join(RAW_DIR, "FinancePilot360_version_etudiants_3_projets_ENRICHI.xlsx")
EXCEL_NORA = os.path.join(RAW_DIR, "NORA_formations_version_etudiants_corrigee_factures_opportunites_couts.xlsx")
EXCEL_TRESO = os.path.join(RAW_DIR, "tableau_depenses_encaissements_2024_2025_ANONYMISE_ETUDIANTS_pip.xlsx")


# ─────────────────────────────────────────────
# 1. RÉGULARISATION FISCALE & SOCIALE
# ─────────────────────────────────────────────
def build_regul_obligations():
    """
    Builds the regulatory obligations table from the FinancePilot360 REGUL sheet.
    Assigns risk levels, statuses and action plans.
    """
    print("[1/7] Building regul_obligations.csv ...")

    obligations = [
        {
            "Obligation": "Bilan 2024 - SalesFlow",
            "Entité": "SalesFlow SARL AU",
            "Année": 2024,
            "Type": "Bilan comptable",
            "Statut": "Non déclaré",
            "Niveau_risque": "ÉLEVÉ",
            "Pièces_manquantes": "Grand-livre 2024, balance, attestation comptable",
            "Responsable": "Expert-comptable",
            "Échéance_cible": "30 jours",
            "Action_prioritaire": "Mandater expert-comptable en urgence pour clôture 2024",
            "Fiabilité": "Déclaratif",
            "Horizon": "30 jours",
            "Montant_estimé": None,
        },
        {
            "Obligation": "Bilan 2025 - SalesFlow",
            "Entité": "SalesFlow SARL AU",
            "Année": 2025,
            "Type": "Bilan comptable",
            "Statut": "Non déclaré",
            "Niveau_risque": "ÉLEVÉ",
            "Pièces_manquantes": "Grand-livre 2025, balance, relevés bancaires complets",
            "Responsable": "Expert-comptable",
            "Échéance_cible": "60 jours",
            "Action_prioritaire": "Préparer dossier comptable 2025 en parallèle du 2024",
            "Fiabilité": "Déclaratif",
            "Horizon": "60 jours",
            "Montant_estimé": None,
        },
        {
            "Obligation": "Bilan 2024 - Intelead",
            "Entité": "Intelead SARL",
            "Année": 2024,
            "Type": "Bilan comptable",
            "Statut": "Non déclaré",
            "Niveau_risque": "ÉLEVÉ",
            "Pièces_manquantes": "Grand-livre 2024, factures fournisseurs, paie",
            "Responsable": "Expert-comptable",
            "Échéance_cible": "30 jours",
            "Action_prioritaire": "Rassembler toutes les pièces justificatives 2024 Intelead",
            "Fiabilité": "Déclaratif",
            "Horizon": "30 jours",
            "Montant_estimé": None,
        },
        {
            "Obligation": "Bilan 2025 - Intelead",
            "Entité": "Intelead SARL",
            "Année": 2025,
            "Type": "Bilan comptable",
            "Statut": "Non déclaré",
            "Niveau_risque": "ÉLEVÉ",
            "Pièces_manquantes": "Grand-livre 2025, balance provisoire",
            "Responsable": "Expert-comptable",
            "Échéance_cible": "60 jours",
            "Action_prioritaire": "Synchroniser avec comptable Intelead pour plan de rattrapage",
            "Fiabilité": "Déclaratif",
            "Horizon": "60 jours",
            "Montant_estimé": None,
        },
        {
            "Obligation": "TVA 2024-2025",
            "Entité": "SalesFlow / Intelead",
            "Année": "2024-2025",
            "Type": "Déclaration fiscale",
            "Statut": "Inconnu",
            "Niveau_risque": "ÉLEVÉ",
            "Pièces_manquantes": "Tableaux DGI, déclarations TVA par période",
            "Responsable": "Expert-comptable / DGI",
            "Échéance_cible": "30 jours",
            "Action_prioritaire": "Consulter DGI pour état TVA due/récupérable par entité",
            "Fiabilité": "Manquant",
            "Horizon": "30 jours",
            "Montant_estimé": None,
        },
        {
            "Obligation": "IS / Acomptes provisionnels",
            "Entité": "SalesFlow / Intelead",
            "Année": "2024-2025",
            "Type": "Impôt société",
            "Statut": "Inconnu",
            "Niveau_risque": "MOYEN",
            "Pièces_manquantes": "Déclarations IS, avis d'imposition",
            "Responsable": "Expert-comptable",
            "Échéance_cible": "60 jours",
            "Action_prioritaire": "Calculer base imposable estimée pour provisionner l'IS",
            "Fiabilité": "Manquant",
            "Horizon": "60 jours",
            "Montant_estimé": None,
        },
        {
            "Obligation": "IR - Salaires 2024-2025",
            "Entité": "SalesFlow / Intelead",
            "Année": "2024-2025",
            "Type": "IR / Social",
            "Statut": "Inconnu",
            "Niveau_risque": "MOYEN",
            "Pièces_manquantes": "Fiches de paie, déclarations IR annuelles",
            "Responsable": "Expert-comptable / RH",
            "Échéance_cible": "60 jours",
            "Action_prioritaire": "Établir liste des salariés et montants IR déclarés",
            "Fiabilité": "Manquant",
            "Horizon": "60 jours",
            "Montant_estimé": None,
        },
        {
            "Obligation": "CNSS 2024-2025",
            "Entité": "Intelead SARL",
            "Année": "2024-2025",
            "Type": "Cotisations sociales",
            "Statut": "Retard historique",
            "Niveau_risque": "ÉLEVÉ",
            "Pièces_manquantes": "État CNSS/Damancom, attestation paiement",
            "Responsable": "Direction / RH",
            "Échéance_cible": "30 jours",
            "Action_prioritaire": "Régulariser arriérés CNSS via plan de paiement Damancom",
            "Fiabilité": "Partiel",
            "Horizon": "30 jours",
            "Montant_estimé": None,
        },
        {
            "Obligation": "Modèle J / Attestation fiscale",
            "Entité": "SalesFlow / Intelead",
            "Année": "2024-2025",
            "Type": "Documents légaux",
            "Statut": "À collecter",
            "Niveau_risque": "MOYEN",
            "Pièces_manquantes": "Modèle J RC, attestation fiscale DGI",
            "Responsable": "Direction",
            "Échéance_cible": "90 jours",
            "Action_prioritaire": "Commander Modèle J et attestation de régularité fiscale",
            "Fiabilité": "À collecter",
            "Horizon": "90 jours",
            "Montant_estimé": None,
        },
    ]

    df = pd.DataFrame(obligations)
    df.to_csv(os.path.join(PROCESSED_DIR, "regul_obligations.csv"), index=False, encoding="utf-8-sig")
    print(f"   → {len(df)} obligations enregistrées.")
    return df


# ─────────────────────────────────────────────
# 2. SALESX BUDGET
# ─────────────────────────────────────────────
def build_salesx_budget():
    """
    Builds the SalesX budget tracking table.
    Data sourced from FinancePilot360 SALESX_SALESFLOW sheet.
    """
    print("[2/7] Building salesx_budget.csv ...")

    budget_items = [
        {
            "Catégorie": "Développement produit",
            "Sous_catégorie": "Plateforme front-end + liaison backend",
            "Budget_prévu": 40000,
            "Réalisé_estimé": 12000,
            "Reste": 28000,
            "Statut": "En cours",
            "Fiabilité": "Réelle",
            "Éligible_subvention": True,
            "Commentaire": "Plateforme front-end en préparation selon brief",
        },
        {
            "Catégorie": "Développement produit",
            "Sous_catégorie": "Optimisation scripts",
            "Budget_prévu": 40000,
            "Réalisé_estimé": 35000,
            "Reste": 5000,
            "Statut": "Avancé",
            "Fiabilité": "Estimée",
            "Éligible_subvention": True,
            "Commentaire": "Scripts opérationnels et testés selon brief",
        },
        {
            "Catégorie": "Ressources humaines",
            "Sous_catégorie": "Ingénieur data science",
            "Budget_prévu": 50000,
            "Réalisé_estimé": 45000,
            "Reste": 5000,
            "Statut": "Avancé",
            "Fiabilité": "Estimée",
            "Éligible_subvention": True,
            "Commentaire": "Freelance actif sur le projet",
        },
        {
            "Catégorie": "Ressources humaines",
            "Sous_catégorie": "Second ingénieur support",
            "Budget_prévu": 40000,
            "Réalisé_estimé": 15000,
            "Reste": 25000,
            "Statut": "En cours",
            "Fiabilité": "Estimée",
            "Éligible_subvention": True,
            "Commentaire": "Recrutement en cours",
        },
        {
            "Catégorie": "Marketing & commercial",
            "Sous_catégorie": "Campagnes acquisition",
            "Budget_prévu": 30000,
            "Réalisé_estimé": 5000,
            "Reste": 25000,
            "Statut": "Non démarré",
            "Fiabilité": "Estimée",
            "Éligible_subvention": True,
            "Commentaire": "Lancement prévu au MVP - budget non encore engagé",
        },
        {
            "Catégorie": "Marketing & commercial",
            "Sous_catégorie": "Support commercial",
            "Budget_prévu": 30000,
            "Réalisé_estimé": 3000,
            "Reste": 27000,
            "Statut": "Non démarré",
            "Fiabilité": "Estimée",
            "Éligible_subvention": True,
            "Commentaire": "À démarrer après MVP",
        },
        {
            "Catégorie": "Frais opérationnels",
            "Sous_catégorie": "Hébergement & outils SaaS",
            "Budget_prévu": 20000,
            "Réalisé_estimé": 8500,
            "Reste": 11500,
            "Statut": "En cours",
            "Fiabilité": "Estimée",
            "Éligible_subvention": True,
            "Commentaire": "OpenAI, outils cloud, domaines",
        },
    ]

    df = pd.DataFrame(budget_items)
    df["Consommation_%"] = (df["Réalisé_estimé"] / df["Budget_prévu"] * 100).round(1)
    df["Écart"] = df["Budget_prévu"] - df["Réalisé_estimé"]

    df.to_csv(os.path.join(PROCESSED_DIR, "salesx_budget.csv"), index=False, encoding="utf-8-sig")
    print(f"   → {len(df)} lignes budget SalesX. Budget total prévu: {df['Budget_prévu'].sum():,.0f} MAD")
    return df


# ─────────────────────────────────────────────
# 3. NORA RENTABILITÉ
# ─────────────────────────────────────────────
def build_nora_rentabilite():
    """
    Builds the NORA profitability table from the NORA factures sheet.
    Calculates margins, identifies unpaid invoices, etc.
    """
    print("[3/7] Building nora_rentabilite.csv ...")

    df_factures = pd.read_excel(
        EXCEL_NORA,
        sheet_name="Factures_attribuees",
    )

    # Rename columns for clean usage
    df_factures = df_factures.rename(columns={
        "ID": "id",
        "Code client": "code_client",
        "Client anonymisé": "client",
        "Secteur": "secteur",
        "Pays": "pays",
        "Type de formation": "type_formation",
        "Format": "format",
        "Dates / période": "dates",
        "Nb sessions/jours": "nb_sessions",
        "Nb participants": "nb_participants",
        "Prix HT confirmé": "ca_ht",
        "Montant TTC facturé": "montant_ttc",
        "Montant encaissé banque": "encaisse",
        "Écart TTC - encaissé": "ecart",
        "Statut rapprochement": "statut_encaissement",
        "Référence facture": "ref_facture",
        "Source document": "source",
    })

    # Calculate derived columns
    df_factures["tva_estimee"] = df_factures["montant_ttc"] - df_factures["ca_ht"]
    df_factures["encaisse"] = pd.to_numeric(df_factures["encaisse"], errors="coerce").fillna(0)
    df_factures["ca_ht"] = pd.to_numeric(df_factures["ca_ht"], errors="coerce").fillna(0)
    df_factures["montant_ttc"] = pd.to_numeric(df_factures["montant_ttc"], errors="coerce").fillna(0)
    df_factures["reste_a_encaisser"] = df_factures["montant_ttc"] - df_factures["encaisse"]
    df_factures["nb_sessions"] = pd.to_numeric(df_factures["nb_sessions"], errors="coerce").fillna(1)

    # Coût moyen estimé par session (hypothèse: 2000 MAD/session formateur + logistique)
    COUT_PAR_SESSION_ESTIME = 2000
    df_factures["cout_direct_estime"] = df_factures["nb_sessions"] * COUT_PAR_SESSION_ESTIME
    df_factures["marge_brute_estimee"] = df_factures["ca_ht"] - df_factures["cout_direct_estime"]
    df_factures["taux_marge_brute"] = np.where(
        df_factures["ca_ht"] > 0,
        (df_factures["marge_brute_estimee"] / df_factures["ca_ht"] * 100).round(1),
        0,
    )

    # Risk flag
    df_factures["alerte"] = df_factures.apply(
        lambda r: "⚠ Non encaissé" if r["reste_a_encaisser"] > 0 else "✅ Encaissé", axis=1
    )

    # Extract year from dates column (best-effort)
    df_factures["annee"] = df_factures["dates"].astype(str).str.extract(r"(202[0-9])")
    df_factures["annee"] = df_factures["annee"].fillna("2025")

    keep = [
        "id", "client", "secteur", "type_formation", "format", "dates", "annee",
        "nb_sessions", "ca_ht", "montant_ttc", "encaisse", "reste_a_encaisser",
        "cout_direct_estime", "marge_brute_estimee", "taux_marge_brute",
        "statut_encaissement", "alerte",
    ]
    df_out = df_factures[keep].copy()

    df_out.to_csv(os.path.join(PROCESSED_DIR, "nora_rentabilite.csv"), index=False, encoding="utf-8-sig")
    print(f"   → {len(df_out)} factures. CA HT total: {df_out['ca_ht'].sum():,.0f} MAD | Encaissé: {df_out['encaisse'].sum():,.0f} MAD")
    return df_out


# ─────────────────────────────────────────────
# 4. NORA COUTS
# ─────────────────────────────────────────────
def build_nora_couts():
    """
    Builds the NORA costs breakdown from the Couts_retenus sheet.
    """
    print("[4/7] Building nora_couts.csv ...")

    df_syn = pd.read_excel(EXCEL_NORA, sheet_name="Synthese")
    df_syn.columns = ["indicateur", "valeur", "commentaire"]
    df_syn["valeur"] = pd.to_numeric(df_syn["valeur"], errors="coerce")

    df_couts = pd.read_excel(EXCEL_NORA, sheet_name="Couts_retenus")
    df_couts = df_couts.rename(columns={
        "ID coût": "id",
        "Date banque": "date",
        "Référence banque": "ref",
        "Catégorie retenue": "categorie",
        "Sous-catégorie": "sous_categorie",
        "Montant débit": "montant",
        "Affectation formation": "affectation",
        "Source relevé": "source",
    })

    df_couts["montant"] = pd.to_numeric(df_couts["montant"], errors="coerce").fillna(0)
    df_couts["date"] = pd.to_datetime(df_couts["date"], errors="coerce")
    df_couts["mois"] = df_couts["date"].dt.to_period("M").astype(str)

    df_couts.to_csv(os.path.join(PROCESSED_DIR, "nora_couts.csv"), index=False, encoding="utf-8-sig")
    print(f"   → {len(df_couts)} lignes de coûts. Total: {df_couts['montant'].sum():,.2f} MAD")
    return df_couts


# ─────────────────────────────────────────────
# 5. TRÉSORERIE
# ─────────────────────────────────────────────
def build_tresorerie():
    """
    Builds the treasury timeseries from the Détails sheet.
    """
    print("[5/7] Building tresorerie.csv ...")

    df = pd.read_excel(EXCEL_TRESO, sheet_name="Details")
    df["date_operation"] = pd.to_datetime(df["date_operation"], errors="coerce")
    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)

    # Separate encaissements / dépenses
    df_enc = df[df["direction"] == "Encaissement"].copy()
    df_dep = df[df["direction"] == "Depense"].copy()

    # Monthly aggregation
    df["mois"] = df["date_operation"].dt.to_period("M")
    monthly = df.groupby(["mois", "direction"])["amount"].sum().unstack(fill_value=0).reset_index()
    monthly.columns.name = None
    monthly = monthly.rename(columns={"Encaissement": "encaissements", "Depense": "depenses"})
    monthly["net"] = monthly.get("encaissements", 0) - monthly.get("depenses", 0)
    monthly["solde_cumulé"] = monthly["net"].cumsum()
    monthly["mois"] = monthly["mois"].astype(str)

    monthly.to_csv(os.path.join(PROCESSED_DIR, "tresorerie.csv"), index=False, encoding="utf-8-sig")
    print(f"   → {len(monthly)} mois de trésorerie.")
    return monthly


# ─────────────────────────────────────────────
# 6. DÉPENSES & ENCAISSEMENTS PAR CATÉGORIE
# ─────────────────────────────────────────────
def build_depenses_encaissements():
    """
    Builds clean category-level tables for spending and receipts.
    """
    print("[6/7] Building depenses & encaissements CSV ...")

    df_dep = pd.read_excel(EXCEL_TRESO, sheet_name="Depenses par categorie")
    df_dep.columns = [str(c).strip() for c in df_dep.columns]
    df_dep = df_dep.rename(columns={
        "Catégorie": "categorie",
        "Montant 2024": "montant_2024",
        "Montant 2025": "montant_2025",
        "Total 2024-2025": "total",
        "Nb 2024": "nb_2024",
        "Nb 2025": "nb_2025",
        "Nb total": "nb_total",
    })
    df_dep["pct_total"] = (df_dep["total"] / df_dep["total"].sum() * 100).round(1)
    df_dep.to_csv(os.path.join(PROCESSED_DIR, "depenses_categories.csv"), index=False, encoding="utf-8-sig")

    df_enc = pd.read_excel(EXCEL_TRESO, sheet_name="Encaissements par categorie")
    df_enc.columns = [str(c).strip() for c in df_enc.columns]
    # Keep only relevant columns
    df_enc = df_enc[["Catégorie", "Montant 2024", "Montant 2025", "Total 2024-2025", "Nb 2024", "Nb 2025", "Nb total"]].copy()
    df_enc = df_enc.rename(columns={
        "Catégorie": "categorie",
        "Montant 2024": "montant_2024",
        "Montant 2025": "montant_2025",
        "Total 2024-2025": "total",
        "Nb 2024": "nb_2024",
        "Nb 2025": "nb_2025",
        "Nb total": "nb_total",
    })
    df_enc["pct_total"] = (df_enc["total"] / df_enc["total"].sum() * 100).round(1)
    df_enc.to_csv(os.path.join(PROCESSED_DIR, "encaissements_categories.csv"), index=False, encoding="utf-8-sig")

    print(f"   → Dépenses: {len(df_dep)} catégories | Encaissements: {len(df_enc)} clients/catégories")
    return df_dep, df_enc


# ─────────────────────────────────────────────
# 7. DASHBOARD KPIs
# ─────────────────────────────────────────────
def build_dashboard_kpis(df_regul, df_salesx, df_nora, df_treso, df_dep, df_enc):
    """
    Aggregates all key metrics into a single KPI table.
    """
    print("[7/7] Building dashboard_kpis.csv ...")

    # Trésorerie
    enc_total = df_enc["total"].sum() if "total" in df_enc.columns else 0
    dep_total = df_dep["total"].sum() if "total" in df_dep.columns else 0
    net_treso = enc_total - dep_total

    # SalesX
    budget_prevu = df_salesx["Budget_prévu"].sum()
    realise = df_salesx["Réalisé_estimé"].sum()
    subvention = 200000
    autofinancement = 50000
    reste_budget = budget_prevu - realise
    conso_pct = realise / budget_prevu * 100

    # NORA
    ca_nora_ht = df_nora["ca_ht"].sum()
    encaisse_nora = df_nora["encaisse"].sum()
    reste_encaisser_nora = df_nora["reste_a_encaisser"].sum()
    marge_nora = df_nora["marge_brute_estimee"].sum()
    taux_marge_nora = (marge_nora / ca_nora_ht * 100) if ca_nora_ht > 0 else 0
    nb_factures_non_encaissees = (df_nora["reste_a_encaisser"] > 0).sum()

    # Régularisation
    nb_urgences = (df_regul["Niveau_risque"] == "ÉLEVÉ").sum()
    nb_moyen = (df_regul["Niveau_risque"] == "MOYEN").sum()

    # CAC SalesX (scénario réaliste: 20 clients, budget marketing 60 000)
    cac_realiste = 60000 / 20
    # Seuil rentabilité SalesX (charges fixes / marge par client estimée)
    prix_moyen_client = 7500  # MAD/an (fourchette basse)
    charges_fixes_annuelles = 100000
    seuil_clients = charges_fixes_annuelles / prix_moyen_client

    kpis = {
        "kpi": [
            "Encaissements totaux (2024-2025)",
            "Dépenses totales (2024-2025)",
            "Net trésorerie",
            "Budget SalesX prévu",
            "Budget SalesX réalisé (estimé)",
            "Budget SalesX restant",
            "Consommation budget SalesX (%)",
            "Subvention Startup Maroc",
            "CA NORA HT (factures)",
            "Montant encaissé NORA",
            "Reste à encaisser NORA",
            "Marge brute NORA estimée",
            "Taux marge brute NORA (%)",
            "Factures NORA non soldées",
            "Obligations ÉLEVÉ risque",
            "Obligations MOYEN risque",
            "CAC prévisionnel SalesX (scénario réaliste)",
            "Seuil rentabilité SalesX (nb clients)",
        ],
        "valeur": [
            enc_total, dep_total, net_treso,
            budget_prevu, realise, reste_budget, round(conso_pct, 1),
            subvention,
            ca_nora_ht, encaisse_nora, reste_encaisser_nora,
            marge_nora, round(taux_marge_nora, 1),
            nb_factures_non_encaissees,
            nb_urgences, nb_moyen,
            cac_realiste, round(seuil_clients, 1),
        ],
        "unité": [
            "MAD", "MAD", "MAD",
            "MAD", "MAD", "MAD", "%",
            "MAD",
            "MAD", "MAD", "MAD",
            "MAD", "%",
            "factures",
            "obligations", "obligations",
            "MAD/client", "clients",
        ],
        "fiabilité": [
            "Réelle", "Réelle", "Réelle",
            "Réelle", "Estimée", "Calculée", "Calculée",
            "Réelle",
            "Réelle", "Réelle", "Calculée",
            "Estimée", "Estimée",
            "Réelle",
            "Réelle", "Réelle",
            "Hypothèse BP", "Hypothèse",
        ],
    }

    df_kpis = pd.DataFrame(kpis)
    df_kpis.to_csv(os.path.join(PROCESSED_DIR, "dashboard_kpis.csv"), index=False, encoding="utf-8-sig")
    print(f"   → {len(df_kpis)} KPIs générés.")
    return df_kpis


# ─────────────────────────────────────────────
# 8. DATA QUALITY LOG
# ─────────────────────────────────────────────
def build_data_quality():
    issues = [
        {"Source": "FinancePilot360 REGUL", "Champ": "TVA 2024-2025", "Problème": "Données manquantes", "Sévérité": "ÉLEVÉE", "Recommandation": "Consulter DGI"},
        {"Source": "FinancePilot360 REGUL", "Champ": "IS / Acomptes", "Problème": "Données manquantes", "Sévérité": "ÉLEVÉE", "Recommandation": "Calculer base imposable"},
        {"Source": "FinancePilot360 SALESX", "Champ": "Dépenses réalisées SalesX", "Problème": "Non exhaustif", "Sévérité": "ÉLEVÉE", "Recommandation": "Collecter justificatifs"},
        {"Source": "FinancePilot360 SALESX", "Champ": "Prix abonnement/licence", "Problème": "Contradiction (5k-54k MAD/an)", "Sévérité": "ÉLEVÉE", "Recommandation": "Clarifier avec dirigeant"},
        {"Source": "NORA Factures", "Champ": "Nb participants", "Problème": "Toutes valeurs manquantes", "Sévérité": "MOYENNE", "Recommandation": "Compléter pour calcul CAC"},
        {"Source": "NORA Coûts", "Champ": "Affectation formation", "Problème": "Tous 'À ventiler'", "Sévérité": "MOYENNE", "Recommandation": "Ventiler par formation"},
        {"Source": "Trésorerie", "Champ": "Code client", "Problème": "Absent pour certaines dépenses", "Sévérité": "FAIBLE", "Recommandation": "Tracer les virements anonymes"},
        {"Source": "FinancePilot360 NORA", "Champ": "Coûts réels par formation", "Problème": "Non trouvé exhaustivement", "Sévérité": "ÉLEVÉE", "Recommandation": "Créer table de coûts par session"},
    ]
    df = pd.DataFrame(issues)
    df.to_csv(os.path.join(PROCESSED_DIR, "data_quality.csv"), index=False, encoding="utf-8-sig")
    print(f"   → {len(df)} problèmes qualité documentés.")
    return df


# ─────────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────────
def main():
    print("=" * 60)
    print("  FinancePilot 360 - Data Preparation")
    print("=" * 60)

    df_regul = build_regul_obligations()
    df_salesx = build_salesx_budget()
    df_nora = build_nora_rentabilite()
    df_couts = build_nora_couts()
    df_treso = build_tresorerie()
    df_dep, df_enc = build_depenses_encaissements()
    df_kpis = build_dashboard_kpis(df_regul, df_salesx, df_nora, df_treso, df_dep, df_enc)
    build_data_quality()

    print("=" * 60)
    print("✅ Data preparation complete. All CSV files saved to data/processed/")
    print("=" * 60)


if __name__ == "__main__":
    main()
