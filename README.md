# Environmental Monitoring and Data Analysis

Course material and student repository (**SanRoy-9**, Student 22) for the Master's course *Environmental Monitoring and Data Analysis* (1st semester, environmental science), Chair of Sensor-based Geoinformatics, University of Freiburg. Winter semester 2026/27.  
Lab website: <https://uni-freiburg.de/enr-geosense>

In this course you follow a set of five flux towers through the whole life of environmental data: you download their measurements, add satellite, climate and site data, clean and analyse the time series, model the fluxes, put everything into a shared database, and present what you found on a poster. Along the way you learn the tools of reproducible data science: Git and GitHub, R or Python, Quarto reports and the bwUniCluster.

## Contents

- [Quick start](#quick-start)
- [What is in this repository](#what-is-in-this-repository)
- [Block 5 task: compound dry-and-hot events](#block-5-task-compound-dry-and-hot-events)
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


## What is in this repository

```
datascience_env_monit/
├── README.md              this file
├── assignments/           one assignment sheet per block
├── scripts/               scripts used in the assignments (R and Python twins)
│   ├── cluster_hello.*        Block 2: first job on bwUniCluster
│   ├── get_my_towers.*        Block 4: download your five towers with the FLUXNET Shuttle
│   ├── read_flux.py           Block 4: helper to parse half-hourly FLUXNET archives
│   └── block5/                Block 5: ERA5-Land, WorldClim, Dheed, SoilGrids, PlantTraits,
│                              deadtrees.earth, iNaturalist, MODIS NDVI/EVI, merge (see its README)
├── jobs/                  Slurm job scripts for bwUniCluster
├── docs/                  templates and notes, e.g. STORAGE_TEMPLATE.md, STORAGE.md
├── reports/               Quarto notebooks and rendered HTML reports (Blocks 4 & 5)
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
| `outputs/` | Exported high-resolution figures (`outputs/figures/`) and CSV summary tables (`outputs/tables/`) | **yes** |
| `docs/STORAGE.md` | Where your data and results live, and when they expire | **yes** |

Run all scripts from the top folder of your project (the one that contains `data/` and `scripts/`).

## Block 5 task: compound dry-and-hot events

- **Assigned tower set (Student 22):** `ID-PaD` (Palangkaraya Drained Forest, Indonesia, `EBF`, 2001–2017), `US-Vcm` (Valles Caldera Mixed Conifer, USA, `ENF`, 2007–2025), `NL-Vkp` (Veenkampen, Netherlands, `GRA`, 2014–2025), `BE-Lon` (Lonzee, Belgium, `CRO`, 2004–2024), and `AU-How` (Howard Springs, Australia, `WSA`, 2002–2025).
- **Research question:** How do compound dry-and-hot (Dheed) extreme events alter daily net ecosystem $\text{CO}_2$ exchange ($\text{NEE}$) and gross primary productivity ($\text{GPP}$) across five contrasting FLUXNET towers, and does the magnitude of carbon sink loss scale with ERA5-Land root-zone soil moisture deficits (`swvl3`)?
- **Complementary datasets & workflow (`scripts/block5/`):**
  - **FLUXNET (`ONEFlux v1.3_r1`):** Daily `FLUXMET_DD` fluxes (`NEE_VUT_REF`, `GPP_NT_VUT_REF`, `RECO_NT_VUT_REF`, filtered at `NEE_VUT_REF_QC >= 0.50`) downloaded via `scripts/get_my_towers.py --student 22`.
  - **ERA5-Land Hourly Time-Series (`reanalysis-era5-land-timeseries`, $0.1^\circ$):** Downloaded via `scripts/block5/01_era5land.py --student 22` (`YEARS_BACK = 25` covering `2001–2025`; `volumetric_soil_water_level_1..3` for topsoil `swvl1` 0–7 cm and root-zone `swvl3` 28–100 cm) and aggregated to daily means.
  - **Dheed Database (`LabelCube` Zarr & `EventStats`, $0.25^\circ$, `1950–2023`):** Exact tower grid-cell event flags extracted via `scripts/block5/03_dheed.py --student 22`.
  - **Merge & analysis:** Daily tables merged via `scripts/block5/09_merge.py` (`33,969` tower-days), anomalies computed relative to same-DOY ($\pm 15\text{ day}$) non-event baselines across `2001–2023` in `scripts/block5/10_prepare_q3.py`, and event/tower statistics & OLS regressions run in `scripts/block5/11_analyze_q3.py`.
- **Key findings:** Across `2001–2023`, **22 unique Dheed events** (`122` total event days; `19` events / `86` days with $\text{QC} \ge 0.50$) weakened the net carbon sink across all five towers by a cross-tower mean of **$\Delta\text{NEE} = +1.22 \pm 1.27\text{ g C m}^{-2}\text{ d}^{-1}$** ($n = 5$ towers; one-sample $t = 2.15$, $p = 0.098$) and suppressed photosynthesis by **$\Delta\text{GPP} = -1.77\text{ g C m}^{-2}\text{ d}^{-1}$** ($n = 4$ towers with partitioned GPP). Cross-tower OLS sensitivity of $\Delta\text{NEE}$ to root-zone soil moisture anomaly ($\Delta\text{swvl3}$) is $-14.82\text{ g C m}^{-2}\text{ d}^{-1}\text{ per m}^3\text{ m}^{-3}$ ($r = -0.32$, $p = 0.603$, $n = 5$ towers), reflecting biome-specific traits and scale mismatch between tower footprints and reanalysis grids.
- **Deliverables:** [`reports/block5_question.ipynb`](reports/block5_question.ipynb), [`reports/block5_question.html`](reports/block5_question.html), [`outputs/figures/fig1_datasets_overview.png`](outputs/figures/fig1_datasets_overview.png), [`outputs/figures/fig2_q3_flux_response.png`](outputs/figures/fig2_q3_flux_response.png), and [`outputs/tables/table1_datasets_overview.csv`](outputs/tables/table1_datasets_overview.csv).

## Getting new material every week: `upstream`

Your fork is a copy of the course repository *from the day you forked it*. New material (assignment sheets, scripts) does **not** appear in your fork by itself, and `git pull` alone only talks to your fork (`origin`). You bring new material from the course repository (`upstream`):

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
