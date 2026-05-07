# 💼 FinancePilot 360

> **Tableau de bord financier multiprojet — V1 Fonctionnelle**  
> Créé avec Python, Streamlit & Plotly | PIP 2026

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.32+-red.svg)](https://streamlit.io)
[![Plotly](https://img.shields.io/badge/Plotly-5.18+-blue.svg)](https://plotly.com)

---

## 📋 Présentation du projet

FinancePilot 360 est un prototype de tableau de bord financier intelligent couvrant **trois problématiques réelles** d'un entrepreneur gérant deux entités (SalesFlow SARL AU + Intelead SARL) :

| Module | Problématique | Ce que l'outil permet |
|--------|--------------|----------------------|
| 🔴 Régularisation | Bilans 2024-2025 non déclarés, TVA, IS, CNSS | Suivi des obligations, risques, plan 30/60/90j |
| 🚀 SalesX | Projet R&D en phase subvention | Budget prévu/réalisé, scénarios, CAC, rentabilité |
| 🎓 NORA Académie | Formations B2B à piloter | CA, marges, factures, coûts, reste à encaisser |

---

## 🏗️ Architecture du projet

```
financepilot360/
│
├── app.py                    # Application Streamlit principale (4 pages)
├── data_preparation.py       # Nettoyage données + génération CSV
├── config.py                 # Configuration : chemins, couleurs, hypothèses
├── utils.py                  # Fonctions partagées : charts, KPIs, alertes
├── requirements.txt          # Dépendances Python
├── README.md                 # Ce fichier
├── .gitignore
│
├── data/
│   ├── raw/                  # Fichiers Excel sources (non modifiés)
│   │   ├── FinancePilot360_version_etudiants_3_projets_ENRICHI.xlsx
│   │   ├── NORA_formations_version_etudiants_corrigee_factures_opportunites_couts.xlsx
│   │   └── tableau_depenses_encaissements_2024_2025_ANONYMISE_ETUDIANTS_pip.xlsx
│   │
│   └── processed/            # CSV nettoyés (générés automatiquement)
│       ├── regul_obligations.csv
│       ├── salesx_budget.csv
│       ├── nora_rentabilite.csv
│       ├── nora_couts.csv
│       ├── tresorerie.csv
│       ├── depenses_categories.csv
│       ├── encaissements_categories.csv
│       ├── dashboard_kpis.csv
│       └── data_quality.csv
│
├── docs/
│   ├── installation_guide.md
│   ├── deployment_guide.md
│   ├── project_architecture.md
│   ├── business_rules.md
│   └── data_dictionary.md
│
├── outputs/                  # Exports générés
│
└── .streamlit/
    └── config.toml           # Thème dark professionnel
```

---

## ⚡ Installation rapide

### 1. Prérequis
- Python 3.9 ou supérieur
- pip

### 2. Cloner le projet
```bash
git clone https://github.com/VOTRE_USERNAME/financepilot360.git
cd financepilot360
```

### 3. Créer un environnement virtuel (recommandé)
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 5. Préparer les données
```bash
python data_preparation.py
```

Sortie attendue :
```
============================================================
  FinancePilot 360 - Data Preparation
============================================================
[1/7] Building regul_obligations.csv ...   → 9 obligations
[2/7] Building salesx_budget.csv ...       → 7 lignes
[3/7] Building nora_rentabilite.csv ...    → 21 factures
...
✅ Data preparation complete.
```

### 6. Lancer l'application
```bash
streamlit run app.py
```

L'application s'ouvre automatiquement sur : **http://localhost:8501**

---

## 📊 Les 4 pages du dashboard

### 🏠 Page 1 — Executive Dashboard
Vue synthétique pour le dirigeant :
- 8 KPI cards principales (trésorerie, SalesX, NORA)
- Alertes prioritaires automatiques
- Graphiques : répartition dépenses + évolution trésorerie
- Recommandations automatiques basées sur les indicateurs
- Score qualité des données

### ⚠️ Page 2 — Régularisation & Risques
Suivi des obligations fiscales/sociales :
- Plan d'action 30/60/90 jours interactif
- Tableau filtrable par risque / entité / horizon
- Codes couleur (🔴 ÉLEVÉ / 🟡 MOYEN / 🟢 FAIBLE)
- Graphiques répartition des risques
- Alertes qualité données spécifiques

### 📈 Page 3 — SalesX + NORA Rentabilité
Deux onglets distincts :
- **SalesX** : budget gauge, budget vs réalisé, simulateur de scénarios interactif
- **NORA** : CA par client, rentabilité par facture, coûts à ventiler

### 💰 Page 4 — Trésorerie & Finances
Analyse financière complète :
- Évolution mensuelle (24 mois) avec courbe solde cumulé
- Dépenses par catégorie (horizontal bar chart)
- Top clients encaissements 2024 vs 2025
- Analyse ratios financiers automatique

---

## 📁 Description des fichiers CSV

| Fichier | Contenu | Source |
|---------|---------|--------|
| `regul_obligations.csv` | 9 obligations fiscales/sociales avec risque et actions | FinancePilot360 REGUL + règles métier |
| `salesx_budget.csv` | 7 postes budgétaires SalesX avec prévu/réalisé/reste | FinancePilot360 SALESX |
| `nora_rentabilite.csv` | 21 factures B2B avec CA, encaissé, marge estimée | NORA Factures_attribuees |
| `nora_couts.csv` | 79 lignes de coûts (hôtel, ONCF, prestataires, OpenAI) | NORA Couts_retenus |
| `tresorerie.csv` | 24 mois de flux : encaissements, dépenses, net, cumulé | Détails relevé bancaire |
| `depenses_categories.csv` | 9 catégories de dépenses 2024+2025 | Dépenses par catégorie |
| `encaissements_categories.csv` | 32 clients/catégories d'encaissements | Encaissements par catégorie |
| `dashboard_kpis.csv` | 18 KPIs agrégés avec fiabilité | Calculé depuis tous les CSV |
| `data_quality.csv` | 8 problèmes qualité documentés | Analyse automatique |

---

## 🔧 Hypothèses importantes

> ⚠️ Les données sont partiellement estimées. Ne pas utiliser pour décisions légales.

| Hypothèse | Valeur | Statut |
|-----------|--------|--------|
| Coût direct par session NORA | 2 000 MAD | Estimée |
| Prix client SalesX/an | 10 000 MAD | Hypothèse pitch |
| Budget marketing SalesX | 60 000 MAD | Réelle |
| Charges fixes SalesX/an | 100 000 MAD | Estimée |
| Taux TVA | 20% | Réelle |
| Taux coûts partagés NORA | 15% CA | Hypothèse |

Toutes les hypothèses sont visibles et modifiables dans `config.py`.

---

## 🌐 Déploiement sur Streamlit Cloud

### Étapes complètes
```bash
# 1. Pousser sur GitHub
git add .
git commit -m "FinancePilot 360 V1"
git push origin main

# 2. Sur https://share.streamlit.io
# - New app
# - Repository: VOTRE_USERNAME/financepilot360
# - Branch: main
# - Main file: app.py
# - Deploy!
```

Voir `docs/deployment_guide.md` pour le guide complet.

---

## 🔄 Workflow GitHub recommandé

```bash
# Initialisation
git init
git add .
git commit -m "feat: FinancePilot 360 V1 - dashboard financier multiprojet"
git remote add origin https://github.com/VOTRE_USERNAME/financepilot360.git
git push -u origin main

# Mises à jour
git add .
git commit -m "fix: correction calcul marge NORA"
git push
```

---

## 🛠️ Troubleshooting

| Problème | Solution |
|----------|----------|
| `ModuleNotFoundError` | `pip install -r requirements.txt` |
| CSV manquants | Lancer `python data_preparation.py` |
| Graphiques vides | Vérifier que les CSV existent dans `data/processed/` |
| Erreur Excel | Vérifier que les fichiers `.xlsx` sont dans `data/raw/` |
| Port occupé | `streamlit run app.py --server.port 8502` |
| Données non actualisées | Cliquer "🔄 Actualiser" dans la sidebar |

---

## 📦 Dépendances

```
streamlit>=1.32.0    # Framework dashboard web
pandas>=2.0.0        # Manipulation données
numpy>=1.24.0        # Calculs numériques
plotly>=5.18.0       # Graphiques interactifs
openpyxl>=3.1.0     # Lecture fichiers Excel
xlsxwriter>=3.1.0   # Export Excel
```

---

## 🗺️ Roadmap V2

- [ ] Connexion directe aux relevés bancaires (CSV automatique)
- [ ] Alertes par email (CNSS, TVA)
- [ ] Export PDF du rapport exécutif
- [ ] Module prévisionnel 12 mois
- [ ] Intégration CRM NORA (leads → facturation)
- [ ] Module comparaison multi-entités SalesFlow/Intelead

---

## ⚖️ Limites de la V1

1. Données partiellement estimées (coûts directs NORA, dépenses réalisées SalesX)
2. Pricing SalesX contradictoire selon les sources (à clarifier)
3. Coûts NORA non ventilés par formation (tous en "À ventiler")
4. TVA, IS, IR : données fiscales manquantes (statuts inconnus)
5. Participants NORA manquants (calcul CAC formation incomplet)

---

## 👥 Utilisation de l'IA

Ce projet a été construit avec l'aide de Claude (Anthropic) pour :
- Analyse des fichiers Excel et extraction automatique des données
- Génération du code Streamlit, Plotly et pandas
- Détection des incohérences dans les données (pricing SalesX)
- Génération automatique des règles métier et recommandations
- Structure du projet et documentation

Corrections humaines apportées : vérification des formules de marge, validation des niveaux de risque, ajustement des hypothèses budgétaires.

---

*FinancePilot 360 — PIP 2026 — Données anonymisées et partiellement estimées*
