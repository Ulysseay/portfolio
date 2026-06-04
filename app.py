"""Datlas - dashboard de mes donnees de createur (Streamlit)."""
from pathlib import Path
import pandas as pd
import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.set_page_config(page_title="Datlas", layout="wide")
DATA = Path(__file__).parent / "data" / "twitch_monthly.csv"


@st.cache_data
def load():
    df = pd.read_csv(DATA, parse_dates=["month"])
    return df.sort_values("month")


df = load()

st.title("Datlas - j'analyse mes propres donnees de createur")
st.caption("Twitch | datch__7 | juin -> decembre 2025")

k = st.columns(4)
k[0].metric("Heures streamees", f"{df.hours_streamed.sum():.0f} h")
k[1].metric("Heures regardees", f"{df.hours_watched.sum():.0f} h")
k[2].metric("Nouveaux followers", int(df.new_followers.sum()))
k[3].metric("Revenus", f"{df.revenue_eur.sum():.2f} EUR")

st.divider()
st.subheader("Regularite de stream vs croissance de followers")
fig = make_subplots(specs=[[{"secondary_y": True}]])
fig.add_bar(x=df.month, y=df.hours_streamed, name="Heures streamees", marker_color="#185FA5")
fig.add_scatter(x=df.month, y=df.new_followers, name="Nouveaux followers",
                mode="lines+markers", line=dict(color="#D85A30", width=3), secondary_y=True)
fig.update_layout(height=430, margin=dict(t=40, b=10), legend=dict(orientation="h", y=1.12))
fig.update_yaxes(title_text="Heures streamees", secondary_y=False)
fig.update_yaxes(title_text="Nouveaux followers", secondary_y=True)
st.plotly_chart(fig, use_container_width=True)

st.info(
    "**Lecture :** mes meilleurs mois de croissance (juillet-aout) sont aussi mes "
    "plus gros volumes de stream. En septembre, l'arret quasi total a casse l'elan, "
    "et la croissance n'est jamais totalement repartie. La regularite est le premier levier."
)

st.divider()
c1, c2 = st.columns(2)
with c1:
    st.subheader("Heures regardees / mois")
    st.bar_chart(df.set_index("month")["hours_watched"], color="#0F6E56")
with c2:
    st.subheader("Spectateurs (moyenne & pic)")
    st.line_chart(df.set_index("month")[["avg_viewers", "peak_viewers"]])

with st.expander("Voir les donnees brutes"):
    st.dataframe(df, use_container_width=True)

st.divider()
st.caption("Prochaine etape : donnees TikTok par video -> modele predictif des vues. -- Ulysse Ayivi")
