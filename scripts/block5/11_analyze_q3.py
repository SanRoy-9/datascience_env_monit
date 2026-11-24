from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
# Paths
daily_path = Path("data/processed/site_daily_q3.csv")
static_path = Path("data/processed/site_static.csv")
fig_dir = Path("outputs/figures")
tab_dir = Path("outputs/tables")
fig_dir.mkdir(parents=True, exist_ok=True)
tab_dir.mkdir(parents=True, exist_ok=True)
df = pd.read_csv(daily_path, parse_dates=["date"])
static = pd.read_csv(static_path)
df = df.merge(static[["site_id", "igbp", "country", "first_year", "last_year"]], on="site_id", how="left")
# Colorblind-safe Okabe-Ito palette & markers per tower
SITE_ORDER = ["ID-PaD", "US-Vcm", "NL-Vkp", "BE-Lon", "AU-How"]
SITE_STYLE = {
    "ID-PaD": {"color": "#0072B2", "marker": "o", "label": "ID-PaD (EBF, Indonesia)"},
    "US-Vcm": {"color": "#D55E00", "marker": "s", "label": "US-Vcm (ENF, USA)"},
    "NL-Vkp": {"color": "#009E73", "marker": "^", "label": "NL-Vkp (GRA, Netherlands)"},
    "BE-Lon": {"color": "#CC79A7", "marker": "D", "label": "BE-Lon (CRO, Belgium)"},
    "AU-How": {"color": "#E69F00", "marker": "v", "label": "AU-How (WSA, Australia)"},
}
# Restrict Dheed comparison to 2001-2023 (where Dheed label cube is defined)
valid = df[df["dheed_valid"].notna()].copy()
events_all = valid[valid["dheed_valid"] == 1].copy()
normal_all = valid[valid["dheed_valid"] == 0].copy()
# -------------------------------------------------------------------------
# 1. TABLE 1: Descriptive summary of ERA5-Land & Dheed across the 5 towers
# -------------------------------------------------------------------------
rows = []
for s in SITE_ORDER:
    g_all = valid[valid["site_id"] == s]
    g_ev = events_all[events_all["site_id"] == s]
    g_no = normal_all[normal_all["site_id"] == s]
    meta = static[static["site_id"] == s].iloc[0]
    rows.append({
        "site_id": s,
        "igbp": meta["igbp"],
        "country": meta["country"],
        "years_dheed": f"{int(g_all['year'].min())}-{int(g_all['year'].max())}",
        "dheed_events": int(g_ev["dheed_label"].nunique()),
        "event_days_total": int(len(g_ev)),
        "event_days_qc50": int(g_ev["NEE_VUT_REF"].notna().sum()),
        "normal_days_qc50": int(g_no["NEE_VUT_REF"].notna().sum()),
        "swvl1_norm_m3m3": round(g_no["era5l_swvl1"].mean(), 3),
        "swvl1_ev_m3m3": round(g_ev["era5l_swvl1"].mean(), 3),
        "swvl3_norm_m3m3": round(g_no["era5l_swvl3"].mean(), 3),
        "swvl3_ev_m3m3": round(g_ev["era5l_swvl3"].mean(), 3),
        "dNEE_mean_gCm2d": round(g_ev["NEE_VUT_REF_anom"].mean(), 2),
        "dGPP_mean_gCm2d": round(g_ev["GPP_NT_VUT_REF_anom"].mean(), 2),
    })
table1 = pd.DataFrame(rows)
table1.to_csv(tab_dir / "table1_datasets_overview.csv", index=False)
print("\n=== TABLE 1: Dheed Events, ERA5-Land Soil Moisture & Flux Anomalies (2001-2023) ===")
print(table1.to_string(index=False))
# -------------------------------------------------------------------------
# 2. EVENT-LEVEL & TOWER-LEVEL AGGREGATION (Honest unit of replication)
# -------------------------------------------------------------------------
ev_level = (
    events_all.groupby(["site_id", "igbp", "dheed_label"], as_index=False)
    .agg(
        n_days=("date", "count"),
        n_qc_days=("NEE_VUT_REF", lambda x: x.notna().sum()),
        dNEE=("NEE_VUT_REF_anom", "mean"),
        dGPP=("GPP_NT_VUT_REF_anom", "mean"),
        dRECO=("RECO_NT_VUT_REF_anom", "mean"),
        dSWVL1=("era5l_swvl1_anom", "mean"),
        dSWVL3=("era5l_swvl3_anom", "mean"),
        dTA=("TA_F_anom", "mean"),
        dVPD=("VPD_F_anom", "mean"),
    )
)
tower_level = (
    ev_level.dropna(subset=["dNEE"])
    .groupby(["site_id", "igbp"], as_index=False)
    .agg(
        n_events=("dheed_label", "count"),
        dNEE=("dNEE", "mean"),
        dGPP=("dGPP", "mean"),
        dRECO=("dRECO", "mean"),
        dSWVL1=("dSWVL1", "mean"),
        dSWVL3=("dSWVL3", "mean"),
    )
)
# Headline summary statistics
mean_dNEE_towers = tower_level["dNEE"].mean()
sd_dNEE_towers = tower_level["dNEE"].std(ddof=1)
mean_dGPP_towers = tower_level["dGPP"].mean()
t_stat, p_val_t = stats.ttest_1samp(tower_level["dNEE"], 0.0)
# Cross-tower regression: dNEE vs root-zone soil moisture anomaly (dSWVL3)
reg_t = stats.linregress(tower_level["dSWVL3"], tower_level["dNEE"])
# Event-level correlation (n = events with valid QC NEE)
ev_valid_nee = ev_level.dropna(subset=["dNEE", "dSWVL3"])
r_ev, p_ev = stats.pearsonr(ev_valid_nee["dSWVL3"], ev_valid_nee["dNEE"])
print("\n=== PART D SUMMARY STATISTICS & SAMPLE SIZE (n) ===")
print(f"Towers (n_towers)                 : {len(tower_level)} towers (2001-2023 overlap)")
print(f"Dheed events (n_events)           : {events_all['dheed_label'].nunique()} total events ({len(ev_valid_nee)} with QC >= 0.50 flux data)")
print(f"Event days (n_days)               : {len(events_all)} total event days ({events_all['NEE_VUT_REF'].notna().sum()} with QC >= 0.50; {normal_all['NEE_VUT_REF'].notna().sum()} normal baseline days)")
print(f"Headline #1 (Tower-mean dNEE)     : {mean_dNEE_towers:+.2f} +/- {sd_dNEE_towers:.2f} g C m-2 d-1 (mean +/- SD across n = 5 towers; one-sample t = {t_stat:.2f}, p = {p_val_t:.3f})")
print(f"Headline #2 (Tower-mean dGPP)     : {mean_dGPP_towers:+.2f} g C m-2 d-1 across n = 5 towers")
print(f"Cross-tower slope (dNEE ~ dSWVL3) : slope = {reg_t.slope:.2f} g C m-2 d-1 per m3 m-3, r = {reg_t.rvalue:.2f}, p = {reg_t.pvalue:.3f} (n = 5 towers)")
print(f"Event-level corr (dNEE ~ dSWVL3)  : r = {r_ev:.2f}, p = {p_ev:.3f} (n = {len(ev_valid_nee)} independent events)")
# -------------------------------------------------------------------------
# 3. FIGURE 1: Dataset Description (Soil Moisture Regimes & Dheed Timing)
# -------------------------------------------------------------------------
plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False})
fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.5, 4.8), dpi=300)
# Panel A: Topsoil (swvl1) vs Root-zone (swvl3) moisture on normal vs Dheed days
x = np.arange(len(SITE_ORDER))
w = 0.36
norm_s1 = [normal_all[normal_all["site_id"] == s]["era5l_swvl1"].mean() for s in SITE_ORDER]
ev_s1 = [events_all[events_all["site_id"] == s]["era5l_swvl1"].mean() for s in SITE_ORDER]
norm_s3 = [normal_all[normal_all["site_id"] == s]["era5l_swvl3"].mean() for s in SITE_ORDER]
ev_s3 = [events_all[events_all["site_id"] == s]["era5l_swvl3"].mean() for s in SITE_ORDER]
ax1.bar(x - w/2, norm_s1, width=w, color="#7F9EB2", label="Normal days: 0-7 cm (swvl1)")
ax1.bar(x + w/2, ev_s1, width=w, color="#D55E00", label="Dheed days: 0-7 cm (swvl1)")
ax1.scatter(x - w/2, norm_s3, color="#1B365D", zorder=5, s=45, label="Normal days: 28-100 cm (swvl3)")
ax1.scatter(x + w/2, ev_s3, color="#000000", marker="D", zorder=5, s=45, label="Dheed days: 28-100 cm (swvl3)")
ax1.set_xticks(x)
ax1.set_xticklabels([f"{s}\n({static.loc[static['site_id']==s, 'igbp'].values[0]})" for s in SITE_ORDER])
ax1.set_ylabel("Volumetric Soil Water Content (m³ m⁻³)")
ax1.set_title("A. ERA5-Land Soil Moisture: Normal vs. Dheed Days")
ax1.legend(frameon=False, fontsize=8.5, loc="upper right")
ax1.set_ylim(0, 0.44)
ax1.grid(axis="y", linestyle=":", alpha=0.5)
# Panel B: Dheed event days per year by tower (2001-2023)
for idx, s in enumerate(SITE_ORDER):
    g_s = valid[valid["site_id"] == s]
    yr_span = g_s["year"].unique()
    ax2.plot([yr_span.min(), yr_span.max()], [idx, idx], color="#CCCCCC", linewidth=3, zorder=1)
    ev_yr = events_all[events_all["site_id"] == s].groupby("year").size()
    ax2.scatter(
        ev_yr.index,
        np.repeat(idx, len(ev_yr)),
        s=ev_yr.values * 28,
        color=SITE_STYLE[s]["color"],
        edgecolors="black",
        linewidth=0.7,
        zorder=3,
    )
ax2.set_yticks(range(len(SITE_ORDER)))
ax2.set_yticklabels([SITE_STYLE[s]["label"] for s in SITE_ORDER])
ax2.set_xlabel("Year (Dheed coverage: 2001–2023)")
ax2.set_title("B. Tower Record Span & Dheed Event Days per Year")
ax2.set_xlim(2000, 2024)
ax2.grid(axis="x", linestyle=":", alpha=0.5)
fig1.tight_layout()
fig1_out = fig_dir / "fig1_datasets_overview.png"
fig1.savefig(fig1_out, dpi=300)
plt.close(fig1)
# -------------------------------------------------------------------------
# 4. FIGURE 2: Direct Answer — Flux Anomalies vs Soil Moisture Deficits
# -------------------------------------------------------------------------
fig2, (bx1, bx2) = plt.subplots(1, 2, figsize=(12.8, 5.2), dpi=300)
# Panel A: dGPP vs dNEE (event means & tower means)
bx1.axhline(0, color="black", linestyle="--", linewidth=0.9, alpha=0.6)
bx1.axvline(0, color="black", linestyle="--", linewidth=0.9, alpha=0.6)
for s in SITE_ORDER:
    st = SITE_STYLE[s]
    sub_ev = ev_level[(ev_level["site_id"] == s)].dropna(subset=["dGPP", "dNEE"])
    bx1.scatter(
        sub_ev["dGPP"], sub_ev["dNEE"],
        color=st["color"], marker=st["marker"], alpha=0.45, s=45, edgecolors="none"
    )
    sub_tw = tower_level[tower_level["site_id"] == s]
    bx1.scatter(
        sub_tw["dGPP"], sub_tw["dNEE"],
        color=st["color"], marker=st["marker"], s=140, edgecolors="black", linewidth=1.2,
        label=st["label"], zorder=5
    )
bx1.set_xlabel("GPP Anomaly, ΔGPP (g C m⁻² d⁻¹)\n[← suppressed photosynthesis]")
bx1.set_ylabel("NEE Anomaly, ΔNEE (g C m⁻² d⁻¹)\n[+ = weakened sink / stronger C source →]")
bx1.set_title("A. Carbon Flux Response During Dheed Events")
bx1.legend(frameon=False, fontsize=8.5, loc="upper right")
bx1.set_ylim(-0.6, 6.1)
bx1.grid(linestyle=":", alpha=0.5)
# Panel B: dNEE vs Root-Zone Soil Moisture Deficit (dSWVL3)
bx2.axhline(0, color="black", linestyle="--", linewidth=0.9, alpha=0.6)
bx2.axvline(0, color="black", linestyle="--", linewidth=0.9, alpha=0.6)
for s in SITE_ORDER:
    st = SITE_STYLE[s]
    sub_ev = ev_level[(ev_level["site_id"] == s)].dropna(subset=["dSWVL3", "dNEE"])
    bx2.scatter(
        sub_ev["dSWVL3"], sub_ev["dNEE"],
        color=st["color"], marker=st["marker"], alpha=0.45, s=45, edgecolors="none"
    )
    sub_tw = tower_level[tower_level["site_id"] == s]
    bx2.scatter(
        sub_tw["dSWVL3"], sub_tw["dNEE"],
        color=st["color"], marker=st["marker"], s=140, edgecolors="black", linewidth=1.2,
        zorder=5
    )
    offsets = {"ID-PaD": (6, 6), "US-Vcm": (-44, 8), "NL-Vkp": (6, -11), "BE-Lon": (6, 4), "AU-How": (6, 5)}
    bx2.annotate(
        s, (sub_tw["dSWVL3"].values[0], sub_tw["dNEE"].values[0]),
        xytext=offsets[s], textcoords="offset points", fontsize=9, fontweight="bold"
    )
# Plot OLS line across the 5 tower means
x_grid = np.linspace(tower_level["dSWVL3"].min() - 0.01, tower_level["dSWVL3"].max() + 0.01, 50)
bx2.plot(
    x_grid, reg_t.intercept + reg_t.slope * x_grid,
    color="#222222", linestyle="-", linewidth=1.5,
    label=f"Tower-mean OLS (n = 5): r = {reg_t.rvalue:.2f}, p = {reg_t.pvalue:.2f}"
)
bx2.set_xlabel("Root-Zone Soil Moisture Anomaly, Δswvl3 (m³ m⁻³)\n[← drier than same-DOY normal]")
bx2.set_ylabel("NEE Anomaly, ΔNEE (g C m⁻² d⁻¹)")
bx2.set_title("B. NEE Anomaly vs. Root-Zone Soil Moisture Deficit")
bx2.legend(frameon=False, fontsize=8.5, loc="upper right")
bx2.set_ylim(-0.6, 6.1)
bx2.grid(linestyle=":", alpha=0.5)
fig2.tight_layout()
fig2_out = fig_dir / "fig2_q3_flux_response.png"
fig2.savefig(fig2_out, dpi=300)
plt.close(fig2)
print(f"\nSaved:\n - {tab_dir / 'table1_datasets_overview.csv'}\n - {fig1_out}\n - {fig2_out}")
