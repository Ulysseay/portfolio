# Datlas — j'analyse mes propres données de créateur

Data analyst le jour, créateur le reste du temps : ce projet transforme mes statistiques de streaming et de contenu en décisions de croissance. Plutôt qu'un dataset générique, j'analyse **mes propres données** — parce que le meilleur moyen de prouver qu'on sait lire la donnée, c'est de s'en servir sur soi.

**Démo en ligne :** _[lien Streamlit à venir]_

## Question business
Qu'est-ce qui fait réellement décoller mon contenu ?
- Quels volumes et quelle régularité de stream font croître l'audience ?
- _(À venir)_ Peut-on estimer les vues d'une vidéo TikTok à partir de ses caractéristiques ?

## Ce que montre le projet — étape 1 : Twitch
À partir de 7 mois de statistiques Twitch (juin → décembre 2025) :
- Nettoyage et consolidation de 7 exports mensuels en un jeu de données propre.
- Dashboard interactif (Streamlit + Plotly) : KPIs, régularité de stream vs croissance de followers, audience, rétention.
- **Insight principal : la régularité est le premier levier de croissance.** L'arrêt quasi total de septembre a cassé l'élan — jamais totalement retrouvé ensuite.

## Données
- Source : exports natifs Twitch (Creator Dashboard, statistiques mensuelles).
- Granularité : une ligne par mois — heures streamées / regardées, spectateurs moyens / max, nouveaux followers, vues live, messages chat, revenus.
- Les exports bruts personnels vivent dans `data/raw/` (non versionnés) ; le jeu consolidé est dans `data/twitch_monthly.csv`.

## Stack
Python · pandas · Plotly · Streamlit

## Lancer en local
```bash
pip install -r requirements.txt
streamlit run app.py
```
Pour régénérer le jeu consolidé depuis les exports bruts :
```bash
python src/load_data.py
```

## Structure
```
datlas/
├── app.py                       # dashboard Streamlit
├── data/
│   ├── raw/                     # exports Twitch bruts (non versionnés)
│   └── twitch_monthly.csv       # données consolidées
├── notebooks/
│   └── 01_exploration_twitch.ipynb
├── src/
│   └── load_data.py             # nettoyage / consolidation
├── requirements.txt
└── README.md
```

## Roadmap
- [ ] Export TikTok par vidéo (vues, durée, hashtags, horaire de publication…).
- [ ] Modèle prédictif des vues d'une vidéo (régression, évaluation MAE / R²).
- [ ] Analyse « qu'est-ce qui fait percer une vidéo » (le clip à ~200K vues).

## Auteur
**Ulysse Ayivi** — Data & IA · [LinkedIn](https://www.linkedin.com/in/ulysseayivi/)
