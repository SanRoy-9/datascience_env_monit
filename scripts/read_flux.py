import zipfile
from pathlib import Path
import pandas as pd

KEEP_COLS = [
    "TIMESTAMP_START", "TIMESTAMP_END",
    "TA_F", "SW_IN_F", "VPD_F", "P_F",
    "NETRAD", "G_F_MDS", "H_F_MDS", "H_F_MDS_QC", "LE_F_MDS", "LE_F_MDS_QC",
    "NEE_VUT_REF", "NEE_VUT_REF_QC", "GPP_NT_VUT_REF", "RECO_NT_VUT_REF",
]


def read_hh(zip_file: str | Path, cols: list[str] = KEEP_COLS) -> pd.DataFrame:
    """Read the FLUXMET_HH CSV from a FLUXNET zip archive into a tidy DataFrame."""
    zip_path = Path(zip_file)
    with zipfile.ZipFile(zip_path) as z:
        matches = [n for n in z.namelist() if "FLUXMET_HH" in n]
        if not matches:
            raise FileNotFoundError(f"No FLUXMET_HH file found in {zip_path.name}")
        hh_name = matches[0]
        with z.open(hh_name) as f:
            df = pd.read_csv(
                f,
                na_values=[-9999, "-9999"],
                usecols=lambda c: c in cols,
                dtype={"TIMESTAMP_START": str, "TIMESTAMP_END": str},
            )

    df["site"] = Path(hh_name).name.split("_")[1]
    df["time"] = pd.to_datetime(df["TIMESTAMP_START"], format="%Y%m%d%H%M")
    return df


if __name__ == "__main__":
    zips = sorted(Path("data/raw").glob("*.zip"))

    # list files inside all 5 zips
    print("--- B1: Zip inventory ---")
    for zp in zips:
        with zipfile.ZipFile(zp) as z:
            hh = [n for n in z.namelist() if "FLUXMET_HH" in n]
            print(f"  {zp.name} -> {len(z.namelist())} files | HH: {hh}")

    with zipfile.ZipFile(zips[0]) as z:
        print(f"\nFiles inside {zips[0].name}:")
        for name in z.namelist():
            print(" ", name)

    # detailed checks on the first site
    one = read_hh(zips[0])
    print(f"\n--- B2 checks on {one['site'].iloc[0]} ---")
    print("Rows:", len(one), "| Duplicate timestamps:", one["time"].duplicated().sum())
    print("Range:", one["time"].min(), "->", one["time"].max())
    print("Rows per year:\n", one["time"].dt.year.value_counts().sort_index().to_string())
    print("\nTA_F summary:\n", one["TA_F"].describe().to_string())
    print("Measured NEE share (all rows):", (one["NEE_VUT_REF_QC"] == 0).mean())
    print("Measured NEE share (non-NA):", (one["NEE_VUT_REF_QC"].dropna() == 0).mean())

    # load all 5 towers into one table
    all_hh = pd.concat([read_hh(z) for z in zips], ignore_index=True)
    print("\n--- B3: All 5 towers combined ---")
    summary = all_hh.groupby("site").agg(
        rows=("time", "size"),
        dups=("time", lambda s: s.duplicated().sum()),
        start=("time", "min"),
        end=("time", "max"),
        ta_min=("TA_F", "min"),
        ta_mean=("TA_F", "mean"),
        ta_max=("TA_F", "max"),
    )
    print(summary.to_string())
