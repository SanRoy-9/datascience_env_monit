from pathlib import Path
import numpy as np
import pandas as pd
in_path = Path("data/processed/site_daily.csv")
out_path = Path("data/processed/site_daily_q3.csv")
df = pd.read_csv(in_path, parse_dates=["date"])
df["year"] = df["date"].dt.year
df["doy"] = df["date"].dt.dayofyear
# 1. Dheed dataset ends 2023-12-31; mark 2024-2025 event status as missing (NA)
df["dheed_valid"] = np.where(df["year"] <= 2023, df["dheed_event"].astype(float), np.nan)
# Audit QC availability on the 122 Dheed event days before filtering
ev = df[df["dheed_valid"] == 1]
print("Dheed event days by site (total vs QC >= 0.50 vs QC >= 0.75):")
audit = ev.groupby("site_id").apply(
    lambda g: pd.Series({
        "total_event_days": len(g),
        "nee_non_na": g["NEE_VUT_REF"].notna().sum(),
        "qc_ge_0.50": (g["NEE_VUT_REF_QC"] >= 0.50).sum(),
        "qc_ge_0.75": (g["NEE_VUT_REF_QC"] >= 0.75).sum(),
    }),
    include_groups=False,
)
print(audit.to_string())
# 2. Apply Part C quality filter (keep measured/high-confidence days: QC >= 0.50)
QC_MIN = 0.50
flux_cols = ["NEE_VUT_REF", "GPP_NT_VUT_REF", "RECO_NT_VUT_REF", "LE_F_MDS"]
low_qc = df["NEE_VUT_REF_QC"].isna() | (df["NEE_VUT_REF_QC"] < QC_MIN)
df.loc[low_qc, flux_cols] = np.nan
# 3. Compute same-DOY (+/-15 day window) non-event baseline (2001-2023) per site
clim_vars = [
    "NEE_VUT_REF", "GPP_NT_VUT_REF", "RECO_NT_VUT_REF",
    "TA_F", "VPD_F", "era5l_swvl1", "era5l_swvl2", "era5l_swvl3",
]
base = df[df["dheed_valid"] == 0]
for col in clim_vars:
    anom_col = f"{col}_anom"
    df[anom_col] = np.nan
    for site, g_site in df.groupby("site_id"):
        b_site = base[base["site_id"] == site]
        doy_means = {}
        for d in range(1, 367):
            diff = np.abs(b_site["doy"] - d)
            diff = np.minimum(diff, 365 - diff)
            doy_means[d] = b_site.loc[diff <= 15, col].mean()
        df.loc[g_site.index, anom_col] = g_site[col] - g_site["doy"].map(doy_means)
df.to_csv(out_path, index=False)
print(f"\nSaved {out_path} ({len(df)} rows x {df.shape[1]} columns, QC >= {QC_MIN})")
