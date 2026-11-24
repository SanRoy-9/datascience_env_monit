# Environmental Monitoring and Data Analysis

In this you follow a set of five flux towers through the whole life of environmental data: you download their measurements, add satellite, climate and site data, clean and analyse the time series, model the fluxes, put everything into a shared database, and present what you found on a poster. Along the way you learn the tools of reproducible data science: Git and GitHub, R or Python, Quarto reports and the bwUniCluster.

## Contents

- [Quick start](#quick-start)
- [Course schedule](#course-schedule)
- [Completed blocks & deliverables](#completed-blocks--deliverables)
  - [Block 2: Git, GitHub & Remote Computing on bwUniCluster](#block-2-git-github--remote-computing-on-bwunicluster)
  - [Block 4: FLUXNET Half-Hourly Data Acquisition & Summary](#block-4-fluxnet-half-hourly-data-acquisition--summary)
  - [Block 5: Complementary Datasets & Compound Dry-and-Hot Event Analysis](#block-5-complementary-datasets--compound-dry-and-hot-event-analysis)
- [What is in this repository](#what-is-in-this-repository)
- [Getting new material every week: `upstream`](#getting-new-material-every-week-upstream)
- [Your data](#your-data)
- [Software you need](#software-you-need)
- [Online tools](#online-tools)
- [Help](#help)
- [Data citation and licence](#data-citation-and-licence)

## Quick start

1. **Fork** this repository on GitHub (button at the top right). The fork is your own copy.
2. **Clone your fork** to your laptop:
   ```bash
   git clone [https://github.com/SanRoy-9/datascience_env_monit.git](https://github.com/SanRoy-9/datascience_env_monit.git)
   cd datascience_env_monit
   ```
3. **Connect it to the course repository** once, so you can get new material later:
   ```bash
   git remote add upstream [https://github.com/negin-katal/datascience_env_monit.git](https://github.com/negin-katal/datascience_env_monit.git)
   git remote -v
   ```
   You should see `origin` (your fork) and `upstream` (the course repository).
4. Every week: **sync**, then follow the assignment sheet in `assignments/`. Commit small, push to your fork, hand in on ILIAS.

You never push to `upstream`. You work in your fork (`origin`), so your changes never touch the course material.


## Completed blocks & deliverables

### Block 2: Git, GitHub & Remote Computing on bwUniCluster

- **What was done:** Configured this repository as a forked Git workflow (`origin` → `SanRoy-9`, `upstream` → `negin-katal`) with `.gitignore` rules excluding raw/large datasets. Set up key-based SSH access to the Karlsruhe Institute of Technology `bwUniCluster` (`uc3.scc.kit.edu`), submitted and monitored Slurm batch compute jobs, and documented high-performance workspace directories and expiration dates.
- **Outputs:**
  - Cluster execution & Slurm scripts: `scripts/cluster_hello.py` and `jobs/`
  - Workspace storage documentation: [`docs/STORAGE.md`](docs/STORAGE.md)
- **Key outcomes:** Verified end-to-end version control syncing between `upstream` and `origin`, and confirmed non-interactive batch job scheduling and workspace storage management on `bwUniCluster`.

---

### Block 4: FLUXNET Half-Hourly Data Acquisition & Summary

- **What was done:** Downloaded ONEFlux `v1.3_r1` eddy-covariance archives (`_FLUXMET_HH_` and `_FLUXMET_DD_`) via the FLUXNET Shuttle (`scripts/get_my_towers.py --student 22`, snapshot `fluxnet_shuttle_snapshot_20261116T075027.csv`) for Student 22's five towers:
  - `AU-How` — Howard Springs, Australia (`WSA`, woody savanna, 2002–2025)
  - `BE-Lon` — Lonzee, Belgium (`CRO`, cropland, 2004–2024)
  - `ID-PaD` — Palangkaraya Drained Forest, Indonesia (`EBF`, evergreen broadleaf forest, 2001–2017)
  - `NL-Vkp` — Veenkampen, Netherlands (`GRA`, grassland, 2014–2025)
  - `US-Vcm` — Valles Caldera Mixed Conifer, USA (`ENF`, evergreen needleleaf forest, 2007–2025)
  Parsed half-hourly series with `scripts/read_flux.py` (`-9999` → `NaN`, local standard timestamps), evaluated `NEE_VUT_REF_QC` data coverage, aggregated half-hourly carbon fluxes to daily units ($\text{g C m}^{-2}\text{ d}^{-1}$) validated against `FLUXMET_DD`, compared hemisphere-aware seasonal diurnal cycles of $\text{NEE}$ and latent heat flux ($\text{LE}$), and assessed surface energy-balance closure at `AU-How`.
- **Outputs:**
  - **Report & Notebook:** [`reports/W04_sr651_tower_data.html`](reports/W04_sr651_tower_data.html) and [`reports/block4_summary.ipynb`](reports/block4_summary.ipynb)
  - **Figures (`outputs/figures/`):**
    - [`c1_site_locations_map.png`](outputs/figures/c1_site_locations_map.png) — Global map of the five flux towers
    - [`c2_nee_data_coverage.png`](outputs/figures/c2_nee_data_coverage.png) — Annual share of measured half-hourly $\text{NEE}$ (`QC == 0`)
    - [`c4_daily_carbon_flux_timeseries.png`](outputs/figures/c4_daily_carbon_flux_timeseries.png) — Daily $\text{GPP}$, $\text{RECO}$, and $\text{NEE}$ time series
    - [`c5_seasonal_diurnal_cycles.png`](outputs/figures/c5_seasonal_diurnal_cycles.png) — Hemisphere-adjusted seasonal diurnal cycles of $\text{NEE}$ and $\text{LE}$
    - [`c6_au_how_energy_balance_closure.png`](outputs/figures/c6_au_how_energy_balance_closure.png) — Measured half-hourly energy-balance closure at `AU-How`
  - **Tables (`outputs/tables/`):** [`c1_site_overview.csv`](outputs/tables/c1_site_overview.csv), [`c2_nee_coverage_by_year.csv`](outputs/tables/c2_nee_coverage_by_year.csv), [`c3_summary_stats_all_sites.csv`](outputs/tables/c3_summary_stats_all_sites.csv) (plus per-site `c3_summary_stats_<SITE>.csv`), and [`c4_us_vcm_fluxmet_dd_validation.csv`](outputs/tables/c4_us_vcm_fluxmet_dd_validation.csv)
- **Key findings:**
  - **Net carbon balance:** Tropical savanna `AU-How` exhibits the strongest annual net uptake (`−730.1 g C m⁻² yr⁻¹`), followed by cropland `BE-Lon` (`−347.1`), peatland `ID-PaD` (`−236.8`), subalpine conifer `US-Vcm` (`−96.9`), and wet grassland `NL-Vkp` (`−47.3`, nearly carbon-neutral despite high $\text{GPP} = 1,820.5\text{ g C m}^{-2}\text{ yr}^{-1}$).
  - **Seasonality & data gaps:** `BE-Lon` shows the widest seasonal $\text{NEE}$ amplitude (`6.24 µmol CO₂ m⁻² s⁻¹`), while `ID-PaD` has the lowest measured $\text{NEE}$ coverage (`19.4%`) and lacks nighttime-partitioned `GPP_NT_VUT_REF` and `RECO_NT_VUT_REF` (`100%` `-9999` in `v1.3_r1`).
  - **Energy closure:** At `AU-How`, measured turbulent fluxes (`H + LE`) against available energy (`NETRAD − G`) yield an OLS slope of `0.819` ($R^2 = 0.887$, $n = 254,495$).

---

### Block 5: Complementary Datasets & Compound Dry-and-Hot Event Analysis

- **What was done:** Tested whether compound dry-and-hot (Dheed) extreme events weaken ecosystem carbon uptake across the five towers and whether carbon sink loss scales with root-zone soil moisture deficits (`swvl3`). Merged daily FLUXNET records (`FLUXMET_DD`, filtered to `NEE_VUT_REF_QC >= 0.50`) with:
  1. **ERA5-Land hourly time series** (`0.1°`, `2001–2025`, downloaded via [`scripts/block5/01_era5land.py`](scripts/block5/01_era5land.py) with `YEARS_BACK = 25` and `volumetric_soil_water_level_1..3` aggregated to daily means), and
  2. **Dheed compound extreme database** (`0.25°`, `1950–2023`, exact tower grid-cell labels extracted from Zarr `LabelCube` via [`scripts/block5/03_dheed.py`](scripts/block5/03_dheed.py)).
  Merged datasets in [`scripts/block5/09_merge.py`](scripts/block5/09_merge.py) (`33,969` tower-days), computed same-DOY ($\pm 15\text{ day}$) non-event anomalies across `2001–2023` in [`scripts/block5/10_prepare_q3.py`](scripts/block5/10_prepare_q3.py), and performed event- and tower-level hypothesis tests and OLS regressions in [`scripts/block5/11_analyze_q3.py`](scripts/block5/11_analyze_q3.py).
- **Outputs:**
  - **Report & Notebook:** [`reports/block5_question.html`](reports/block5_question.html) and [`reports/block5_question.ipynb`](reports/block5_question.ipynb)
  - **Figures (`outputs/figures/`):**
    - [`fig1_datasets_overview.png`](outputs/figures/fig1_datasets_overview.png) — ERA5-Land topsoil (`swvl1`) and root-zone (`swvl3`) soil moisture during normal vs. Dheed days and event timeline (`2001–2023`)
    - [`fig2_q3_flux_response.png`](outputs/figures/fig2_q3_flux_response.png) — Event- and tower-level $\Delta\text{NEE}$ vs. $\Delta\text{GPP}$ and cross-tower OLS regression against root-zone soil moisture anomaly ($\Delta\text{swvl3}$)
  - **Table (`outputs/tables/`):** [`table1_datasets_overview.csv`](outputs/tables/table1_datasets_overview.csv)
- **Key findings:**
  - **Soil moisture drawdown:** Across `2001–2023`, **22 unique Dheed events** (`122` total event days; `19` events and `86` days with $\text{QC} \ge 0.50$) reduced mean topsoil moisture (`swvl1`, 0–7 cm) by $0.11\text{ to }0.24\text{ m}^3\text{ m}^{-3}$ and root-zone moisture (`swvl3`, 28–100 cm) by $0.04\text{ to }0.14\text{ m}^3\text{ m}^{-3}$ at every tower.
  - **Carbon sink weakening:** Every tower shifted toward positive $\Delta\text{NEE}$ anomalies during Dheed events, yielding a cross-tower mean of **$\Delta\text{NEE} = +1.22 \pm 1.27\text{ g C m}^{-2}\text{ d}^{-1}$** ($n = 5$ towers; one-sample $t = 2.15$, $p = 0.098$) and mean photosynthetic suppression of **$\Delta\text{GPP} = -1.77\text{ g C m}^{-2}\text{ d}^{-1}$** ($n = 4$ towers with partitioned GPP).
  - **Soil moisture sensitivity:** Cross-tower OLS regression of $\Delta\text{NEE}$ on $\Delta\text{swvl3}$ yielded a slope of $-14.82\text{ g C m}^{-2}\text{ d}^{-1}\text{ per m}^3\text{ m}^{-3}$ ($r = -0.32$, $p = 0.603$, $n = 5$ towers), demonstrating that biome traits (such as groundwater access at peatland `ID-PaD` vs. rainfed cropping at `BE-Lon`) and scale mismatch between tower footprints (~$100\text{ m}$–$1\text{ km}$) and reanalysis grids ($9$–$28\text{ km}$) strongly mediate drought sensitivity.


Each sheet has a time plan, *Check:* boxes after every step, a hand-in checklist and a troubleshooting table.

| Block | Assignment | Due | Status & Hand-In Deliverables |
| --- | --- | --- | --- |
| 2 | [Git, GitHub and your first cluster job](assignments/block-2-git-github-cluster.md) | before Block 3 | Completed (`scripts/cluster_hello.py`, `jobs/`, [`docs/STORAGE.md`](docs/STORAGE.md)) |
| 4 | [Download your towers and write a data summary](assignments/block-4-flux-data-summary.md) | before Block 5 | Completed ([`reports/W04_sr651_tower_data.html`](reports/W04_sr651_tower_data.html), [`reports/block4_summary.ipynb`](reports/block4_summary.ipynb)) |
| 5 | [Test one question with your towers and two more datasets](assignments/block-5-complementary-data.md) | before Block 6 | Completed ([`reports/block5_question.html`](reports/block5_question.html), [`reports/block5_question.ipynb`](reports/block5_question.ipynb)) |

New sheets are added here as the updated.


## What is in this repository

```
datascience_env_monit/
├── README.md              this file
├── assignments/           one assignment sheet per block
├── scripts/               scripts used in the assignments (R and Python twins)
│   ├── cluster_hello.*        Block 2: first job on bwUniCluster
│   ├── get_my_towers.*        Block 4: download your five towers with the FLUXNET Shuttle
│   ├── read_flux.py           Block 4: helper to parse half-hourly FLUXNET archives
│   └── block5/                Block 5: ERA5-Land, Dheed, merge & Q3 analysis scripts
├── jobs/                  Slurm job scripts for bwUniCluster
├── docs/                  templates and notes, e.g. STORAGE_TEMPLATE.md, STORAGE.md
├── reports/               Jupyter notebooks and rendered HTML reports (Blocks 4 & 5)
├── outputs/               exported figures (PNG) and summary tables (CSV)
├── ssh-connection/        SSH guide for bwUniCluster (also online, see below)
├── flux4student/          FLUXNET site explorer and weekly data of all course towers (also online)
└── LICENSE
```

**Folders maintained in this fork:**

| Folder / File | What goes in | In Git? |
| --- | --- | --- |
| `data/raw/` | Original downloads, untouched (FLUXNET zips, snapshot) | **no** |
| `data/external/` | Block 5 datasets, one subfolder per dataset (`era5land/`, `dheed/`) | **no** |
| `data/processed/` | Merged and quality-filtered tables built from raw/external data | **no** |
| `reports/` | Jupyter notebooks and rendered HTML reports (`block4_summary.ipynb`, `W04_sr651_tower_data.html`, `block5_question.ipynb`, `block5_question.html`) | **yes** |
| `outputs/` | Exported figures (`outputs/figures/`) and CSV summary tables (`outputs/tables/`) | **yes** |
| `docs/STORAGE.md` | Where your data and results live, and when they expire | **yes** |


## Getting new material every week: `upstream`

Tis fork is a copy of the course repository *from the day you forked it*. New material (assignment sheets, scripts) does **not** appear in your fork by itself, and `git pull` alone only talks to your fork (`origin`). You bring new material from the course repository (`upstream`):

```
negin-katal/datascience_env_monit  (upstream)  ──pull──▶  your laptop  ──push──▶  SanRoy-9/datascience_env_monit  (origin)
```

**Once:** add `upstream` (step 3 of the [quick start](#quick-start)). `git remote add` says `remote upstream already exists`? Then you have done it already.

**Every week, before you start:**

```bash
git status                            # must say: nothing to commit, working tree clean
git pull --no-rebase upstream main    # bring in the new course material
git push                              # send it on to your fork on GitHub
```

- Commit (or `git stash`) your own changes first.
- Always name the branch (`main`) and keep `--no-rebase`: your fork has your own commits, so Git must merge.
- If Git opens an editor for the merge message, keep the text, save and close (in vim: `:wq` and Enter).

**If Git reports a conflict in `README.md`:** you customized the README in your fork, and the course README changes too. Keep your own:

```bash
git checkout --ours README.md
git add README.md
git commit -m "Merge course updates, keep my README"
git push
```

For a conflict in any other file: open it, decide which lines to keep, delete the `<<<<<<<`, `=======` and `>>>>>>>` lines, then `git add` the file and commit. Lost? `git merge --abort` takes you back to before the pull.

**On github.com** you can also click **Sync fork → Update branch** on your fork's page, then run `git pull` on your laptop. If GitHub offers **Discard commits**, do not click it: that throws away your own work. Use the command line instead.

## Your data

- **Data never go into Git.** `data/` is listed in `.gitignore` (Block 4, Part A2). Git is for code and reports; data come from their original source, which your scripts and reports document.
- **Course files** that are not in this repository, such as `tower_sets_block4.csv` (your five towers), are on ILIAS in the folder *DATA*.
- **On bwUniCluster**, keep data and results in your workspace (`envmon`), not in your home folder, and note when it expires in `docs/STORAGE.md`. Workspaces are deleted after they expire.
- **Shared course data.** After Block 5 the course collects everyone's data in a shared cloud folder for the database blocks (11–12). Instructions follow on ILIAS.
- **Cite every dataset you use.** Each script states its citation in the header; the assignment sheets say what to put in your report.

## Software you need

| What | Why | Notes |
| --- | --- | --- |
| Git and a GitHub account | Version control, your fork | Set `git config --global user.name` and `user.email`. On Windows use Git Bash. |
| **R + Positron** *or* **Python + VS Code** | Analysis | Choose one route and keep it; every script exists in both languages. Setup: Block 1 material on ILIAS. |
| Quarto | Reports that render to HTML | Included in Positron. VS Code: install from <https://quarto.org> and the Quarto extension. |
| Python 3.9 or newer | The FLUXNET Shuttle (Block 4) is a Python tool | Needed on the R route too; `get_my_towers.R` sets it up for you. |
| bwUniCluster account | Remote computing, big files | Register before Block 2. Only reachable from the university network: use the VPN from home. |
| Copernicus CDS account | ERA5-Land in Block 5 | Free; accept the dataset licence on the dataset page. |

R and Python packages are listed at the top of each script and in [`scripts/block5/README.md`](scripts/block5/README.md).

## Online tools

- **flux4student explorer:** map, data availability and weekly time series of all course towers: <https://negin-katal.github.io/datascience_env_monit/flux4student/>
- **SSH connection guide for bwUniCluster:** <https://negin-katal.github.io/datascience_env_monit/ssh-connection/>
- **Climate data viewer:** <https://negin-katal.github.io/datascience_env_monit/climate-data-viewer/>

## Help

- **Stuck for more than 10 minutes?** Post the exact command and the last lines of the error on ILIAS, or raise your hand in class. Somebody else probably has the same problem.
- Every assignment sheet ends with a **troubleshooting table**; check it first.
- When you ask for help, say: what you ran, what you expected, what happened (copy the error text, not a photo), and whether you use R or Python, Windows, macOS or Linux.

## Data citation and licence

Course material: see [LICENSE](LICENSE).

- **FLUXNET2015 / ONEFlux (`v1.3_r1`):** The FLUXNET data in `flux4student/` and `data/raw/` are CC-BY-4.0 with citation requirements per site; see [`flux4student/README.md`](flux4student/README.md) and the site citations in `reports/`. When using flux data, cite each site's data product, Pastorello et al. (2020), *Scientific Data* 7, 225, <https://doi.org/10.1038/s41597-020-0534-3>, and include the FLUXNET acknowledgement.
- **ERA5-Land (`reanalysis-era5-land-timeseries`):** Muñoz-Sabater et al. (2021), *Earth System Science Data*, 13, 4349–4383, <https://doi.org/10.5194/essd-13-4349-2021>. Contains modified Copernicus Climate Change Service information (2026).
- **Dheed (`LabelCube` & `EventStats`):** Weynants et al. (2025), *Earth System Science Data*, 17, 6621, <https://doi.org/10.5194/essd-17-6621-2025>; Zenodo dataset: <https://doi.org/10.5281/zenodo.14884254>.
