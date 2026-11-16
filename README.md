# Environmental Monitoring Data Science

Coursework repository for **Environmental Monitoring Data Science** (Sanglap Roy, Student 22). This repository contains reproducible workflows for high-performance computing exercises (Block 2) and half-hourly eddy-covariance data analysis across five global FLUXNET towers (Block 4).

---

## Repository Structure

| Path | Description |
| --- | --- |
| `assignments/` | Assignment instructions (`block-2-git-github-cluster.md`, `block-4-flux-data-summary.md`). |
| `data/` | **Local only (ignored in `.gitignore`)** — holds downloaded FLUXNET `.zip` archives (`data/raw/`), Shuttle metadata snapshots (`data/snapshots/`), and the isolated Shuttle environment (`data/.shuttle-env/`). |
| `docs/` | Cluster storage documentation (`STORAGE.md`). |
| `flux4student/` | Interactive FLUXNET Site Explorer web app from the course repository. |
| `jobs/` | Slurm cluster job submission scripts (`hello_py.sh`, `hello_R.sh`). |
| `reports/` | Block 4 analysis notebook (`fluxnet_data_summary.ipynb`) and rendered HTML report (`fluxnet_data_summary.html`). |
| `results/` | Cluster job output logs (`hello_py_8207322.out`). |
| `scripts/` | Reusable Python and R scripts (`cluster_hello.py`, `get_my_towers.py`, `read_flux.py`, and R equivalents). |

---

## Block 4: FLUXNET Data Summary Report

### Overview
The Block 4 report analyzes half-hourly FLUXNET observations (`_FLUXMET_HH_`, ONEFlux `v1.3_r1`) across five contrasting ecosystems (Student Set 22):

- **`AU-How`** — Howard Springs, Australia (`WSA`, Tropical Woody Savanna)
- **`BE-Lon`** — Lonzée, Belgium (`CRO`, Temperate Cropland)
- **`ID-PaD`** — Palangkaraya Drained Forest, Indonesia (`EBF`, Drained Tropical Peatland)
- **`NL-Vkp`** — Veenkampen, Netherlands (`GRA`, Temperate Grassland)
- **`US-Vcm`** — Valles Caldera Mixed Conifer, USA (`ENF`, Subalpine Mixed Conifer)

Raw archives remain untouched in `data/raw/` and are read directly from `.zip` files via `read_hh()` in `scripts/read_flux.py`, which parses `-9999` as `NaN` and converts `TIMESTAMP_START` strings into `datetime64` timestamps in **local standard time**. The notebook `reports/fluxnet_data_summary.ipynb` produces sections **C1–C6** (site overview and map, NEE measurement coverage heatmap, summary statistics, daily carbon-flux time series validated against `FLUXMET_DD`, hemisphere-aware seasonal diurnal cycles, energy-balance closure, and ecosystem synthesis) along with full **Data and Citation** attributions.

### Prerequisites
- **Python 3.12+** (Python 3.9+ required for the FLUXNET Shuttle)
- Install analysis and rendering dependencies:
  ```bash
  pip install pandas numpy matplotlib jupyter nbconvert
  ```

### Reproduce from a Fresh Clone
1. **Clone the repository and enter the project folder:**
   ```bash
   git clone https://github.com/SanRoy-9/datascience_env_monit.git
   cd datascience_env_monit
   ```
2. **Download the five FLUXNET tower archives** into `data/raw/` and record the Shuttle snapshot in `data/snapshots/` (this also creates an isolated environment in `data/.shuttle-env/` if needed):
   ```bash
   python scripts/get_my_towers.py --sites AU-How BE-Lon ID-PaD NL-Vkp US-Vcm
   ```
   *(Alternatively, if `tower_sets_block4.csv` is placed locally in the project root, run `python scripts/get_my_towers.py --student 22`.)*
3. **Execute the notebook and render the HTML report** (`reports/fluxnet_data_summary.html`):
   ```bash
   jupyter nbconvert --to notebook --execute --inplace --ExecutePreprocessor.timeout=300 reports/fluxnet_data_summary.ipynb
   jupyter nbconvert --to html reports/fluxnet_data_summary.ipynb
   ```

---

## Block 2: Cluster Hello

### Overview
`scripts/cluster_hello.py` bootstraps a synthetic Gross Primary Productivity (GPP) time series and estimates a 95% confidence interval using Monte Carlo resampling. It was used to test remote workflows and Slurm job submission on the bwUniCluster (`jobs/hello_py.sh`, `jobs/hello_R.sh`, with storage notes in `docs/STORAGE.md`).

### Run Locally
```bash
python scripts/cluster_hello.py 200
```
*(Pass the number of bootstrap replicates as the positional argument; output logs from cluster runs are saved in `results/`.)*

---

## Interactive Site Explorer (`flux4student/`)

The `flux4student/` directory contains the course FLUXNET Site Explorer. To browse it locally (serving over HTTP is required so JSON data files load properly):
```bash
cd flux4student
python -m http.server 8000
```
Then open `http://localhost:8000` in your browser.

---

## Author & Data Policy

- **Author:** Sanglap Roy
- **Data Licence:** FLUXNET data products are shared under the [CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/) licence. Full site citations, regional network acknowledgements, and methodological references are included in `reports/fluxnet_data_summary.html` and `data/raw/CITATIONS.txt`.
