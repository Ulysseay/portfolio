"""Chargement et nettoyage des donnees Twitch mensuelles."""
from pathlib import Path
import glob
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
CLEAN_CSV = ROOT / "data" / "twitch_monthly.csv"


def build_clean_from_raw(raw_dir: Path = RAW_DIR) -> pd.DataFrame:
    """Consolide tous les exports mensuels bruts en un jeu de donnees propre."""
    files = sorted(glob.glob(str(raw_dir / "*.csv")))
    if not files:
        raise FileNotFoundError(f"Aucun CSV dans {raw_dir}")
    df = pd.concat([pd.read_csv(f) for f in files], ignore_index=True)
    df["Date"] = pd.to_datetime(df["Date"], format="%a %b %d %Y", errors="coerce")
    df = df.dropna(subset=["Date"]).drop_duplicates("Date").sort_values("Date")
    rev = [c for c in df.columns if c.startswith("Revenu")]
    clean = pd.DataFrame({
        "month": df["Date"],
        "avg_viewers": df["Spectateurs en moyenne"].round(2),
        "peak_viewers": df["Spectateurs max."].astype(int),
        "new_followers": df["Nouveaux followers"].astype(int),
        "hours_streamed": (df["Minutes passées en stream"] / 60).round(1),
        "hours_watched": (df["Minutes regardées"] / 60).round(1),
        "live_views": df["Vues live"].astype(int),
        "chat_messages": df["Messages du chat"].astype(int),
        "revenue_eur": df[rev].sum(axis=1).round(2),
    })
    return clean.reset_index(drop=True)


def load() -> pd.DataFrame:
    """Charge le jeu propre ; le regenere depuis data/raw au besoin."""
    if CLEAN_CSV.exists():
        return pd.read_csv(CLEAN_CSV, parse_dates=["month"])
    out = build_clean_from_raw()
    out.to_csv(CLEAN_CSV, index=False)
    return out


if __name__ == "__main__":
    out = build_clean_from_raw()
    out.to_csv(CLEAN_CSV, index=False)
    print(f"OK : {len(out)} mois -> {CLEAN_CSV}")
